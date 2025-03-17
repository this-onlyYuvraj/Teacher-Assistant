# modules/answer_evaluator.py
"""
Answer Evaluation Engine
Evaluates student answers based on question type and answer key
"""
import re
import math
import logging
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from difflib import SequenceMatcher

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass  # Handle case where network is unavailable

logger = logging.getLogger(__name__)

class AnswerEvaluationEngine:
    def __init__(self, llm_service=None):
        logger.info("Initializing Answer Evaluation Engine")
        
        # Initialize language processing tools
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize text similarity tools
        self.vectorizer = TfidfVectorizer(
            tokenizer=self._preprocess_text,
            stop_words='english'
        )
        
        # Initialize LLM service for essay evaluation if provided
        self.llm_service = llm_service
    
    def evaluate(self, questions: List[Dict], answer_key: Optional[Dict] = None) -> List[Dict]:
        """
        Evaluate answers for all questions
        
        Args:
            questions: List of classified questions
            answer_key: Optional answer key information
            
        Returns:
            List of questions with evaluation results
        """
        logger.info(f"Evaluating {len(questions)} questions")
        
        # Extract answer key data if provided
        answers = {}
        if answer_key:
            answers = self._extract_answers_from_key(answer_key)
        
        # Process each question
        evaluated_questions = []
        
        for question in questions:
            question_id = question["id"]
            
            # Get the correct answer for this question
            correct_answer = answers.get(question_id)
            
            # If answer key wasn't provided, try to extract from question
            if not correct_answer:
                correct_answer = self._extract_answer_from_question(question)
            
            # If we still don't have an answer, mark for manual review
            if not correct_answer:
                question["evaluation"] = {
                    "status": "needs_review",
                    "message": "No answer key found",
                    "confidence": 0.0
                }
                evaluated_questions.append(question)
                continue
            
            # Store the correct answer
            question["answer_key"] = correct_answer
            
            # Evaluate based on question type
            if question["type"] == "multiple_choice":
                self._evaluate_multiple_choice(question, correct_answer)
            elif question["type"] == "true_false":
                self._evaluate_true_false(question, correct_answer)
            elif question["type"] == "short_answer":
                self._evaluate_short_answer(question, correct_answer)
            elif question["type"] == "essay":
                self._evaluate_essay(question, correct_answer)
            elif question["type"] == "fill_in_blank":
                self._evaluate_fill_in_blank(question, correct_answer)
            elif question["type"] == "matching":
                self._evaluate_matching(question, correct_answer)
            elif question["type"] == "mathematical":
                self._evaluate_mathematical(question, correct_answer)
            else:
                # Default to marking for review
                question["evaluation"] = {
                    "status": "needs_review",
                    "message": f"Unsupported question type: {question['type']}",
                    "confidence": 0.0
                }
            
            evaluated_questions.append(question)
        
        logger.info(f"Completed evaluation for {len(evaluated_questions)} questions")
        return evaluated_questions
    
    def _extract_answers_from_key(self, answer_key: Dict) -> Dict:
        """Extract answers from the provided answer key"""
        answers = {}
        
        # Process answer key based on format
        # This is a simplified implementation
        
        # Check for tables containing answers
        for table in answer_key.get("tables", []):
            for row in table.get("cells", []):
                for cell in row:
                    text = cell.get("text", "").strip()
                    
                    # Look for question ID and answer pattern
                    match = re.search(r'(question-\d+|q\d+)[\s:]+([A-Za-z0-9].*)', text, re.IGNORECASE)
                    if match:
                        q_id = match.group(1).lower()
                        answer = match.group(2).strip()
                        answers[q_id] = answer
        
        # Look for answers in text blocks
        for page in answer_key.get("pages", []):
            for block in page.get("text_blocks", []):
                text = block.get("text", "").strip()
                
                # Look for answer patterns
                lines = text.split('\n')
                for line in lines:
                    match = re.search(r'(question-\d+|q\d+|#\d+)[\s:]+([A-Za-z0-9].*)', line, re.IGNORECASE)
                    if match:
                        q_id = match.group(1).lower().replace('#', 'question-')
                        if not q_id.startswith('question-'):
                            q_id = 'question-' + q_id[1:]
                        answer = match.group(2).strip()
                        answers[q_id] = answer
        
        return answers
    
    def _extract_answer_from_question(self, question: Dict) -> Optional[Any]:
        """Try to extract the correct answer from the question data"""
        # Look for indicators of correct answers in multiple choice
        if question["type"] == "multiple_choice" and question.get("options"):
            for option in question["options"]:
                option_text = option["text"].lower()
                # Sometimes correct answers are marked in the PDF
                if '★' in option_text or '*' in option_text or 'correct' in option_text:
                    return option["id"]
        
        # For true/false, try to determine from question wording
        if question["type"] == "true_false":
            text = question["text"].lower()
            # If question has negation, it's more likely false
            if re.search(r'not|never|none|no', text):
                return "false"
            # Questions with "always", "all", etc. are often false
            if re.search(r'always|all|every|nobody', text):
                return "false"
            # Default to true (this is just a heuristic)
            return "true"
        
        # No answer found
        return None
    
    def _preprocess_text(self, text: str) -> List[str]:
        """Preprocess text for similarity comparison"""
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(word) 
            for word in tokens 
            if word not in self.stop_words and word.isalnum()
        ]
        
        return tokens
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # For short texts, use sequence matcher
        if len(text1) < 50 and len(text2) < 50:
            return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
        
        # For longer texts, use TF-IDF and cosine similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            # Fallback to sequence matcher if vectorizer fails
            return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def _evaluate_multiple_choice(self, question: Dict, correct_answer: Any):
        """Evaluate multiple choice question"""
        # Initialize evaluation
        evaluation = {
            "status": "evaluated",
            "correct_answer": correct_answer,
            "student_answer": None,  # Would be filled with actual student answer
            "is_correct": False,
            "score": 0.0,
            "max_score": question.get("points", 1.0),
            "confidence": 0.9  # High confidence for MCQ evaluation
        }
        
        # Simplified evaluation for demonstration
        # In a real implementation, this would compare the student's answer with the correct answer
        
        question["evaluation"] = evaluation
    
    def _evaluate_true_false(self, question: Dict, correct_answer: Any):
        """Evaluate true/false question"""
        # True/false is similar to multiple choice but simpler
        evaluation = {
            "status": "evaluated",
            "correct_answer": correct_answer.lower(),
            "student_answer": None,  # Would be filled with actual student answer
            "is_correct": False,
            "score": 0.0,
            "max_score": question.get("points", 1.0),
            "confidence": 0.95  # Very high confidence for T/F
        }
        
        question["evaluation"] = evaluation
    
    def _evaluate_short_answer(self, question: Dict, correct_answer: Any):
        """Evaluate short answer question"""
        # For short answers, we need text similarity comparison
        evaluation = {
            "status": "evaluated",
            "correct_answer": correct_answer,
            "student_answer": None,  # Would be filled with actual student answer
            "is_correct": False,
            "score": 0.0,
            "max_score": question.get("points", 2.0),
            "confidence": 0.7,  # Lower confidence for short answers
            "similarity_threshold": 0.8  # Threshold for considering answer correct
        }
        
        question["evaluation"] = evaluation
    
    def _evaluate_essay(self, question: Dict, correct_answer: Any):
        """Evaluate essay question"""
        # Essays generally require more complex evaluation with rubrics
        evaluation = {
            "status": "needs_review",  # Essays often need human review
            "rubric": correct_answer if isinstance(correct_answer, dict) else {"criteria": "General evaluation"},
            "student_answer": None,  # Would be filled with actual student answer
            "score": 0.0,
            "max_score": question.get("points", 5.0),
            "confidence": 0.5,  # Low confidence for automated essay scoring
            "feedback": "This essay requires manual review."
        }
        
        # If LLM service is available, attempt automated evaluation
        if self.llm_service:
            evaluation["status"] = "partially_evaluated"
            evaluation["message"] = "Essay evaluated with AI assistance, but human review recommended."
            evaluation["confidence"] = 0.6
        
        question["evaluation"] = evaluation
    
    def _evaluate_fill_in_blank(self, question: Dict, correct_answer: Any):
        """Evaluate fill-in-the-blank question"""
        # Parse correct answers - may be multiple for multiple blanks
        if isinstance(correct_answer, str) and ',' in correct_answer:
            correct_answers = [ans.strip() for ans in correct_answer.split(',')]
        else:
            correct_answers = [correct_answer]
        
        evaluation = {
            "status": "evaluated",
            "correct_answer": correct_answers,
            "student_answer": None,  # Would be filled with actual student answer
            "is_correct": False,
            "score": 0.0,
            "max_score": question.get("points", 1.0),
            "confidence": 0.85,
            "similarity_threshold": 0.9  # High threshold for fill-in-blank
        }
        
        question["evaluation"] = evaluation
    
    def _evaluate_matching(self, question: Dict, correct_answer: Any):
        """Evaluate matching question"""
        # Parse the correct matching pairs
        if isinstance(correct_answer, str):
            # Format might be "A-1, B-2, C-3"
            pairs = []
            for pair in correct_answer.split(','):
                if '-' in pair:
                    left, right = pair.split('-')
                    pairs.append((left.strip(), right.strip()))
            correct_answer = pairs
        
        evaluation = {
            "status": "evaluated",
            "correct_answer": correct_answer,
            "student_answer": None,  # Would be filled with actual student answer
            "is_correct": False,
            "score": 0.0,
            "max_score": question.get("points", len(correct_answer) if isinstance(correct_answer, list) else 2.0),
            "confidence": 0.9,
            "partial_credit": True  # Allow partial credit for partially correct matches
        }
        
        question["evaluation"] = evaluation
    
    def _evaluate_mathematical(self, question: Dict, correct_answer: Any):
        """Evaluate mathematical question"""
        # Mathematical questions need numerical comparison with tolerance
        try:
            # Try to convert to float if it's a number
            correct_value = float(correct_answer)
            has_units = False
        except:
            # Check if it has units
            match = re.search(r'([\d.]+)\s*([a-zA-Z]+)', correct_answer)
            if match:
                correct_value =