
import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent / "src"))

from app.services.indexing_service import index_pdf_file

def main():
    try:
        pdf_path = Path("data/uploads/Sample-Accounting-Income-Statement-PDF-File.pdf")
        if not pdf_path.exists():
            print(f"Error: PDF file not found at {pdf_path}")
            sys.exit(1)
            
        print(f"Indexing PDF: {pdf_path}")
        num_chunks = index_pdf_file(pdf_path)
        print(f"Successfully indexed {num_chunks} chunks.")
        
    except Exception as e:
        print(f"Error during ingestion: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
