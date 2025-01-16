import PyPDF2
import pdf2image
import pytesseract
from PIL import Image
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class PDFProcessor:
    def __init__(self):
        self.poppler_path = r"C:\poppler\poppler-21.03.0\Library\bin"
        logging.debug(f"Poppler path set to: {self.poppler_path}")

    def extract_text(self, pdf_file):
        text = ""
        try:
            if not self._is_valid_pdf(pdf_file):
                raise ValueError("The uploaded file is not a valid PDF or is corrupted.")
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                extracted = page.extract_text()
                if extracted:
                    text += extracted
                else:
                    images = pdf2image.convert_from_bytes(pdf_file.read(), poppler_path=self.poppler_path)
                    for img in images:
                        img_text = pytesseract.image_to_string(img)
                        text += img_text
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF.")
        except Exception as e:
            logging.error(f"Error reading PDF: {e}")
            raise ValueError("The PDF file is corrupted or cannot be read.")
        return text

    def _is_valid_pdf(self, pdf_file):
        try:
            pdf_file.seek(0)
            header = pdf_file.read(4)
            if header != b'%PDF':
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating PDF file: {e}")
            return False

    def split_text(self, text, chunk_size=1500, overlap=200):
        words = text.split()
        chunks = []
        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = ' '.join(words[start:end])
            chunks.append(chunk)
            start += chunk_size - overlap
        return chunks