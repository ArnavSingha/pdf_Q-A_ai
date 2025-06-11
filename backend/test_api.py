import requests
import os
from pathlib import Path
import json

# API endpoints
BASE_URL = "http://localhost:8000"
UPLOAD_URL = f"{BASE_URL}/upload"

def test_pdf_upload_and_qa():
    try:
        # Test PDF path - you'll need to provide a PDF file
        test_pdf_path = "test.pdf"  # Replace with your PDF file path
        
        if not os.path.exists(test_pdf_path):
            print(f"❌ Test PDF file not found at: {test_pdf_path}")
            return

        # Upload PDF
        print("\n📤 Uploading PDF...")
        with open(test_pdf_path, "rb") as pdf_file:
            files = {"file": (os.path.basename(test_pdf_path), pdf_file, "application/pdf")}
            response = requests.post(UPLOAD_URL, files=files)
            
        if response.status_code == 200:
            pdf_data = response.json()
            print(f"✅ PDF uploaded successfully! Document ID: {pdf_data['id']}")
            
            # Test question answering
            doc_id = pdf_data['id']
            questions = [
                "What is the main topic of this document?",
                "What are the key points discussed?",
                "Can you summarize the content?"
            ]
            
            print("\n❓ Testing question answering...")
            for question in questions:
                print(f"\nQuestion: {question}")
                try:
                    response = requests.post(
                        f"{BASE_URL}/question/{doc_id}",
                        json={"question": question}
                    )
                    
                    if response.status_code == 200:
                        answer = response.text
                        print(f"Answer: {answer}")
                    else:
                        print(f"❌ Error asking question: {response.text}")
                        print(f"Status code: {response.status_code}")
                        if response.headers.get('content-type') == 'application/json':
                            print(f"Error details: {json.loads(response.text)}")
                except Exception as e:
                    print(f"❌ Exception while asking question: {str(e)}")
                    
        else:
            print(f"❌ Error uploading PDF: {response.text}")
            print(f"Status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_pdf_upload_and_qa() 