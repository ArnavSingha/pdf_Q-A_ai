from fastapi import APIRouter, Depends, HTTPException
from app import models, schemas, deps
from sqlalchemy.orm import Session
from app.utils import nlp_processing
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

## Method to handle User's question
@router.post("/{doc_id}", response_model=str)
async def ask_question(doc_id: int, request: schemas.QuestionRequest, db: Session = Depends(deps.get_db)):
    try:
        logger.info(f"Received question request for document ID: {doc_id}")
        logger.info(f"Question: {request.question}")
        
        pdf_doc = db.query(models.PDFDocument).filter(models.PDFDocument.id == doc_id).first()
        if not pdf_doc:
            logger.error(f"PDF document not found with ID: {doc_id}")
            raise HTTPException(status_code=404, detail="PDF document not found")
        
        logger.info(f"Found PDF document: {pdf_doc.filename}")
        answer = nlp_processing.get_answer_from_pdf(pdf_doc, request.question)
        logger.info(f"Generated answer: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))