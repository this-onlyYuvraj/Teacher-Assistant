def _analyze_questions(self, document_structure: Dict, pdf_content: Dict):
        """Analyze identified questions to determine their types and details"""
        for question in document_structure["questions"]:
            # Skip questions already classified
            if question["type"] != "unknown":
                document_structure["metadata"]["identified_question_types"].add(question["type"])
                continue
            
            # Analyze the question to determine its type
            question_type = self._classify_question_type(question, pdf_content)
            question["type"] = question_type
            
            # Add to metadata
            document_structure["metadata"]["identified_question_types"].add(question_type)
            
            # Extract additional information based on question type
            if question_type == "multiple_choice":
                pass  # Already handled in _extract_answer_options
            elif question_type == "true_false":
                self._process_true_false_question(question)
            elif question_type == "short_answer":
                self._process_short_answer_question(question, pdf_content)
            elif question_type == "essay":
                self._process_essay_question(question)
    
    def _classify_question_type(self, question: Dict, pdf_content: Dict) -> str:
        """Classify the type of a question based on its content and structure"""
        # Check if it's a multiple choice question (already has options)
        if question.get("options", []):
            return "multiple_choice"
        
        # Check if it's a true/false question
        if self._is_true_false_question(question):
            return "true_false"
        
        # Check if it's an essay question
        if self._is_essay_question(question):
            return "essay"
        
        # Check if it's a short answer question
        if self._is_short_answer_question(question, pdf_content):
            return "short_answer"
        
        # Default to "other" if we can't classify
        return "other"
    
    def _is_true_false_question(self, question: Dict) -> bool:
        """Determine if a question is a true/false question"""
        text = question["text"].lower()
        
        # Check for true/false keywords
        true_false_patterns = [
            r'true or false',
            r'mark (t|true) or (f|false)',
            r'(t|true)/(f|false)'
        ]
        
        for pattern in true_false_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def _is_essay_question(self, question: Dict) -> bool:
        """Determine if a question is an essay question"""
        text = question["text"].lower()
        
        # Check for essay question indicators
        essay_indicators = [
            r'discuss',
            r'explain in detail',
            r'analyze',
            r'compare and contrast',
            r'evaluate',
            r'describe',
            r'elaborate on'
        ]
        
        # Check for essay keywords
        for indicator in essay_indicators:
            if re.search(indicator, text):
                return True
        
        # Check if question is long (likely requires long answer)
        if len(text.split()) > 15:
            return True
        
        return False
    
    def _is_short_answer_question(self, question: Dict, pdf_content: Dict) -> bool:
        """Determine if a question is a short answer question"""
        # Check if there's a blank line or space after the question
        page_num = question["page"]
        bbox = question["bbox"]
        
        # Get the page content
        page = pdf_content["pages"][page_num]
        
        # Look for blank lines or underscores after the question
        for block in page["text_blocks"]:
            if block["bbox"][1] > bbox[3]:  # Block is below the question
                if "_" * 5 in block["text"] or "__" in block["text"]:
                    return True
        
        # Default to short answer if it's not multiple choice or essay
        return True
    
    def _process_true_false_question(self, question: Dict):
        """Process a true/false question to extract its structure"""
        # Add standard options
        question["options"] = [
            {"id": "true", "text": "True"},
            {"id": "false", "text": "False"}
        ]
    
    def _process_short_answer_question(self, question: Dict, pdf_content: Dict):
        """Process a short answer question to identify answer space"""
        # Identify the answer area if possible
        page_num = question["page"]
        bbox = question["bbox"]
        
        # Get the page content
        page = pdf_content["pages"][page_num]
        
        # Look for answer spaces (blank lines, underscores, boxes)
        answer_space = None
        for block in page["text_blocks"]:
            if block["bbox"][1] > bbox[3]:  # Block is below the question
                if "_" * 3 in block["text"] or "__" in block["text"]:
                    answer_space = block["bbox"]
                    break
        
        if answer_space:
            question["answer_space"] = answer_space
    
    def _process_essay_question(self, question: Dict):
        """Process an essay question to extract its structure"""
        # No specific processing needed for basic essay questions
        # In a more advanced system, this could extract word count requirements,
        # rubric information, etc.
        pass
