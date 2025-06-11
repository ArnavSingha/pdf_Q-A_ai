from app.database import SessionLocal
from app.models import PDFDocument
import os

def fix_database():
    db = SessionLocal()
    try:
        # Get the upload directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        upload_dir = os.path.join(current_dir, "uploads")
        
        # Get list of actual PDF files
        actual_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
        print(f"Found PDF files in uploads directory: {actual_files}")
        
        # Get all database entries
        db_entries = db.query(PDFDocument).all()
        print(f"Found database entries: {[entry.filename for entry in db_entries]}")
        
        # Delete entries that don't have corresponding files
        for entry in db_entries:
            if entry.filename not in actual_files:
                print(f"Deleting database entry for non-existent file: {entry.filename}")
                db.delete(entry)
        
        # Create entries for files that don't have database entries
        for filename in actual_files:
            if not db.query(PDFDocument).filter(PDFDocument.filename == filename).first():
                print(f"Creating database entry for file: {filename}")
                new_entry = PDFDocument(filename=filename)
                db.add(new_entry)
        
        db.commit()
        print("Database fixed successfully!")
        
    except Exception as e:
        print(f"Error fixing database: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_database() 