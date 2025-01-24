# PDF Chatbot

This project is a Streamlit-based chatbot application that allows users to upload PDF documents and ask questions about the content. It uses the Groq API for language model completions and PyPDF for extracting text from PDF files.

## Features

- **Upload PDFs**: Easily upload PDF files for text extraction.
- **Chat Interface**: Ask questions about the uploaded PDF content.
- **Groq Integration**: Utilizes the Groq API for generating responses based on the PDF content.
- **Chat History**: View previous questions and answers in the sidebar, with options to refresh or delete entries.
- **Custom Styling**: Aesthetic design with custom CSS for chat messages and the sidebar.

## Installation

1. **Clone the Repository**

    ```bash
    cd D:\Chatpdf
git clone https://github.com/Aswini200303/RAG-Based-Chatbot-for-PDF-Documents.git
cd RAG-Based-Chatbot-for-PDF-Documents
    ```

2. **Install Dependencies**

    Ensure you have Python installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**

    Create a `.env` file or export the Groq API key:

    ```bash
    export GROQ_API_KEY="your-groq-api-key"
    ```

## Usage

1. **Run the Application**

    ```bash
    streamlit run app.py
    ```

2. **Upload a PDF**

    Use the file uploader to select a PDF document.

3. **Ask Questions**

    Enter questions related to the uploaded PDF in the chat input box. The chatbot will provide relevant answers based on the document content.

4. **View Chat History**

    Check the sidebar for a history of questions and answers. You can refresh or delete individual entries as needed.

## Project Structure

```
.
├── app.py                # Main application file
├── README.md             # Project documentation
└── .env                  # Environment variables (not included in repo)
```

## Dependencies

- **Streamlit**: For building the web application interface.
- **PyPDF**: For extracting text from PDF files.
- **Transformers**: For natural language processing.
- **Groq API**: For AI completions based on PDF content.

## Customization

- **CSS Styling**: Modify the custom CSS in `app.py` for styling adjustments.
- **Groq Model**: Change the model and parameters in the `client.chat.completions.create` method to experiment with different outputs.

