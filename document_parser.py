import pypdf
import fitz  # PyMuPDF
from docx import Document
import os

class DocumentParser:
    """Parse various document formats to extract text"""
    
    @staticmethod
    def parse_pdf(file_path):
        """Extract text from PDF using PyPDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"PyPDF failed, trying PyMuPDF: {e}")
            # Fallback to PyMuPDF
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text() + "\n"
            doc.close()
        return text
    
    @staticmethod
    def parse_docx(file_path):
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    @staticmethod
    def parse_txt(file_path):
        """Read plain text file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    @staticmethod
    def parse_file(file_path):
        """Auto-detect and parse file based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return DocumentParser.parse_pdf(file_path)
        elif ext == '.docx':
            return DocumentParser.parse_docx(file_path)
        elif ext == '.txt':
            return DocumentParser.parse_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")