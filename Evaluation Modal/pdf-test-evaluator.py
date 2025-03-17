# main.py
"""
AI-Driven PDF Test Evaluation System
Main application file that ties together all components
"""
import os
import logging
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from typing import Dict, List, Optional
import uvicorn
from pydantic import BaseModel

from modules.pdf_processor import PDFProcessor
from modules.document_understanding import DocumentUnderstandingEngine
from modules.question_classifier import QuestionClassifier
from modules.answer_evaluator import AnswerEvaluationEngine
from modules.scoring import ScoringEngine
from modules.report_generator import ReportGenerator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Test Evaluation System")

# Response models
class EvaluationStatus(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None

class QuestionScore(BaseModel):
    question_id: str
    question_text: str
    question_type: str
    max_score: float
    awarded_score: float
    confidence: float
    feedback: Optional[str] = None

class TestEvaluationResult(BaseModel):
    job_id: str
    test_id: str
    total_score: float
    max_possible_score: float
    percentage: float
    question_scores: List[QuestionScore]
    evaluation_summary: str
    processing_time: float

# In-memory job tracking (replace with database in production)
evaluation_jobs = {}

@app.post("/evaluate-test/", response_model=EvaluationStatus)
async def evaluate_test(
    background_tasks: BackgroundTasks,
    test_file: UploadFile = File(...),
    answer_key_file: Optional[UploadFile] = File(None),
    config: Optional[Dict] = None
):
    """
    Upload a test PDF for evaluation.
    Optionally provide an answer key file and configuration parameters.
    """
    # Generate a unique job ID
    import uuid
    job_id = str(uuid.uuid4())
    
    # Save uploaded files
    test_path = f"uploads/{job_id}/test.pdf"
    answer_key_path = None
    
    os.makedirs(f"uploads/{job_id}", exist_ok=True)
    
    # Save test file
    with open(test_path, "wb") as f:
        f.write(await test_file.read())
    
    # Save answer key if provided
    if answer_key_file:
        answer_key_path = f"uploads/{job_id}/answer_key.pdf"
        with open(answer_key_path, "wb") as f:
            f.write(await answer_key_file.read())
    
    # Update job status
    evaluation_jobs[job_id] = {"status": "queued", "result": None}
    
    # Add evaluation task to background processing
    background_tasks.add_task(
        process_test_evaluation,
        job_id,
        test_path,
        answer_key_path,
        config
    )
    
    return EvaluationStatus(job_id=job_id, status="queued", message="Test evaluation has been queued")

@app.get("/evaluation-status/{job_id}", response_model=EvaluationStatus)
async def get_evaluation_status(job_id: str):
    """Get the status of a test evaluation job"""
    if job_id not in evaluation_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = evaluation_jobs[job_id]
    return EvaluationStatus(
        job_id=job_id,
        status=job["status"],
        message=job.get("message", None)
    )

@app.get("/evaluation-result/{job_id}", response_model=TestEvaluationResult)
async def get_evaluation_result(job_id: str):
    """Get the result of a completed test evaluation"""
    if job_id not in evaluation_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = evaluation_jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail=f"Evaluation is not complete. Current status: {job['status']}")
    
    return job["result"]

async def process_test_evaluation(
    job_id: str,
    test_path: str,
    answer_key_path: Optional[str],
    config: Optional[Dict]
):
    """
    Process the test evaluation in the background
    """
    try:
        import time
        start_time = time.time()
        
        # Update job status
        evaluation_jobs[job_id] = {"status": "processing", "message": "PDF processing started"}
        
        # Initialize components
        pdf_processor = PDFProcessor()
        doc_engine = DocumentUnderstandingEngine()
        question_classifier = QuestionClassifier()
        answer_evaluator = AnswerEvaluationEngine()
        scoring_engine = ScoringEngine()
        report_generator = ReportGenerator()
        
        # Process PDF
        logger.info(f"Processing PDF for job {job_id}")
        pdf_content = pdf_processor.process(test_path)
        
        # Process answer key if provided
        answer_key = None
        if answer_key_path:
            answer_key = pdf_processor.process(answer_key_path)
        
        # Update status
        evaluation_jobs[job_id]["status"] = "analyzing"
        evaluation_jobs[job_id]["message"] = "Document analysis in progress"
        
        # Understand document structure
        document_structure = doc_engine.analyze(pdf_content)
        
        # Classify questions
        questions = question_classifier.classify(document_structure)
        
        # Update status
        evaluation_jobs[job_id]["status"] = "evaluating"
        evaluation_jobs[job_id]["message"] = "Answer evaluation in progress"
        
        # Evaluate answers
        evaluation_results = answer_evaluator.evaluate(questions, answer_key)
        
        # Calculate scores
        scoring_results = scoring_engine.calculate_scores(evaluation_results)
        
        # Generate report
        report = report_generator.generate(scoring_results)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare result
        result = TestEvaluationResult(
            job_id=job_id,
            test_id=f"TEST-{job_id[:8]}",
            total_score=scoring_results["total_score"],
            max_possible_score=scoring_results["max_possible_score"],
            percentage=scoring_results["percentage"],
            question_scores=[
                QuestionScore(
                    question_id=q["id"],
                    question_text=q["text"][:100] + "..." if len(q["text"]) > 100 else q["text"],
                    question_type=q["type"],
                    max_score=q["max_score"],
                    awarded_score=q["awarded_score"],
                    confidence=q["confidence"],
                    feedback=q.get("feedback", None)
                )
                for q in scoring_results["questions"]
            ],
            evaluation_summary=report["summary"],
            processing_time=processing_time
        )
        
        # Update job status
        evaluation_jobs[job_id] = {
            "status": "completed",
            "message": "Evaluation completed successfully",
            "result": result
        }
        
        logger.info(f"Completed evaluation for job {job_id} in {processing_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
        evaluation_jobs[job_id] = {
            "status": "failed",
            "message": f"Evaluation failed: {str(e)}"
        }

if __name__ == "__main__":
    # Create upload directory
    os.makedirs("uploads", exist_ok=True)
    
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)
