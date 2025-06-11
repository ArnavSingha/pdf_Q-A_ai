from app.database import engine, Base
from app.models import PDFDocument
import os

def init_db():
    # Create the database directory if it doesn't exist
    db_dir = os.path.dirname("sql_app.db")
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("✅ Tables created:")
    for table in Base.metadata.tables:
        print(f"   - {table}")

if __name__ == "__main__":
    init_db() 