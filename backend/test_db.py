from app.database import SessionLocal
from app.models import PDFDocument
from datetime import datetime, UTC

def test_database_connection():
    try:
        # Create a new database session
        db = SessionLocal()
        
        # Try to create a test record
        test_doc = PDFDocument(
            filename="test_document.pdf",
            upload_date=datetime.now(UTC)
        )
        
        # Add and commit the test record
        db.add(test_doc)
        db.commit()
        print("✅ Successfully created test record in database")
        
        # Try to read the record back
        saved_doc = db.query(PDFDocument).filter(PDFDocument.filename == "test_document.pdf").first()
        if saved_doc:
            print(f"✅ Successfully retrieved test record: {saved_doc.filename}")
        
        # Clean up test record
        db.delete(saved_doc)
        db.commit()
        print("✅ Successfully cleaned up test record")
        
        db.close()
        print("✅ Database connection test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error testing database connection: {str(e)}")
        raise e

if __name__ == "__main__":
    test_database_connection() 