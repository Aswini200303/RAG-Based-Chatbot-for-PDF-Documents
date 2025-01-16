# Document Chat Assistant

This project is a **Document Chat Assistant** that allows users to upload PDF and Word documents, process them, and ask context-aware questions. It uses advanced Natural Language Processing (NLP) models to generate summaries and retrieve answers from the uploaded content.

## Features

- Upload and process PDF and DOCX files.
- Extract text from uploaded documents.
- Summarize documents using a pre-trained Hugging Face model.
- Answer user queries based on document content.
- Save and load chat history.

## Technology Stack

- **Backend**: Python
- **Frontend**: Streamlit
- **NLP Models**: Hugging Face Transformers
- **Database**: SQLite
- **Dependencies**: FAISS, PyPDF2, Sentence-Transformers, PyMuPDF, Pytesseract

## Installation

### Prerequisites

Ensure you have the following installed:

- **Python**: Version 3.8 or later
- **Poppler**: Required for PDF processing ([Installation Guide](https://poppler.freedesktop.org/))
- **Tesseract-OCR**: Required for OCR ([Installation Guide](https://github.com/tesseract-ocr/tesseract))

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/arvetiaswini/document-chat-assistant.git
   cd document-chat-assistant
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure the `poppler_path` in `pdf_processor.py` (line 8) to point to your local Poppler installation.

4. Run the application:

   ```bash
   streamlit run app.py
   ```

## How to Use

1. Open the application in your browser (Streamlit will provide a URL).
2. Upload one or more PDF or DOCX files using the file uploader.
3. Ask questions about the document content or request a summary.
4. View the chat history to revisit previous answers.

## Project Structure

```
document-chat-assistant/
│
├── app.py                    # Main Streamlit application
├── embeddings_manager.py     # Manages text embeddings
├── llm.py                    # Custom LLM wrapper for Hugging Face
├── pdf_processor.py          # PDF processing and text extraction
├── vector_store.py           # Vector storage implementation with FAISS
├── requirements.txt          # Required dependencies
├── users.db                  # SQLite database for storing user data
└── README.md                 # Project documentation
```

## Requirements

- **Python**: Version 3.8 or later
- **Poppler**: Required for advanced PDF processing
- **Tesseract-OCR**: Required for OCR-based text extraction

## Dependencies

The following Python packages are required and listed in `requirements.txt`:

- Streamlit
- LangChain
- FAISS-CPU
- PyPDF2
- Transformers (>=4.30.0)
- Torch (>=2.0.0)
- Huggingface-Hub
- PyMuPDF
- Sentence-Transformers (>=2.2.0)
- LangChain-Community
- Pydantic (>=2.1)
- PDF2Image
- PyTesseract
- Pillow
