from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from app import crud, schemas, models, deps
from sqlalchemy.orm import Session
from app.utils.nlp_processing import get_upload_directory
import shutil
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/latest", response_model=schemas.PDFDocument)
async def get_latest_document(db: Session = Depends(deps.get_db)):
    """Get the most recently uploaded PDF document."""
    try:
        latest_doc = db.query(models.PDFDocument).order_by(models.PDFDocument.upload_date.desc()).first()
        if not latest_doc:
            raise HTTPException(status_code=404, detail="No PDF documents found")
        return latest_doc
    except Exception as e:
        logger.error(f"Error getting latest document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

## Method to handle Uploaded PDF
@router.post("/", response_model=schemas.PDFDocument)
async def upload_pdf(file: UploadFile = File(...), db: Session = Depends(deps.get_db)):
    try:
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Invalid file type")
            
        # Get upload directory
        upload_dir = get_upload_directory()
        file_path = os.path.join(upload_dir, file.filename)
        
        logger.info(f"Saving PDF to: {file_path}")
        
        # Save file to local storage
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"PDF saved successfully")

        # Create DB entry
        pdf_doc = models.PDFDocument(filename=file.filename)
        db.add(pdf_doc)
        db.commit()
        db.refresh(pdf_doc)
        
        logger.info(f"Created database entry with ID: {pdf_doc.id}")
        return pdf_doc
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

