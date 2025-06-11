import os
import logging
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
from langchain.schema import Document
import fitz  # PyMuPDF

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the Hugging Face token from the environment
hf_token = os.getenv("HUGGING_FACE_HUB_TOKEN")
if not hf_token:
    logger.error("Hugging Face Hub token is not set")
    raise ValueError("Hugging Face Hub token is not set. Please set the HUGGING_FACE_HUB_TOKEN environment variable.")

try:
    # Load the model and tokenizer without the deprecated parameter
    logger.info("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-cased-distilled-squad", token=hf_token)
    model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad", token=hf_token)

    # Initialize the Hugging Face QA pipeline with the loaded model and tokenizer
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    logger.info("Model and tokenizer loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

def get_upload_directory():
    """Get the absolute path to the uploads directory."""
    # Get the absolute path to the backend directory
    current_file = os.path.abspath(__file__)
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    upload_dir = os.path.join(backend_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    logger.info(f"Upload directory: {upload_dir}")
    return upload_dir

def extract_text_from_pdf(file_path):
    """Extract text from PDF file using PyMuPDF."""
    try:
        logger.info(f"Extracting text from PDF: {file_path}")
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def get_answer_from_pdf(pdf_doc, question):
    try:
        # Get the upload directory
        upload_dir = get_upload_directory()
        file_path = os.path.join(upload_dir, pdf_doc.filename)
        
        logger.info(f"Processing question for PDF: {pdf_doc.filename}")
        logger.info(f"Question: {question}")
        logger.info(f"Looking for PDF at: {file_path}")
        
        if not os.path.exists(file_path):
            error_msg = f"PDF file not found: {file_path}"
            logger.error(error_msg)
            raise Exception(error_msg)
            
        pdf_text = extract_text_from_pdf(file_path)
        
        if not pdf_text.strip():
            error_msg = "No text could be extracted from the PDF"
            logger.error(error_msg)
            raise Exception(error_msg)

        # Prepare the input for the QA pipeline
        input_data = {
            "context": pdf_text,
            "question": question
        }

        # Run the QA pipeline with the text and the question
        logger.info("Running QA pipeline...")
        answer = qa_pipeline(input_data)
        logger.info(f"Answer generated: {answer['answer']}")
        return answer['answer']
    except Exception as e:
        logger.error(f"Error in get_answer_from_pdf: {str(e)}")
        raise Exception(f"Error processing question: {str(e)}")

