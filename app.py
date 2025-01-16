import sys
import os
import streamlit as st
import logging
from docx import Document

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pdf_processor import PDFProcessor
from vector_store import VectorStore
from transformers import pipeline

RESPONSE_TEMPLATE_DYNAMIC = """
{answer}
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_dynamic_response(user_question, vector_store, conversation, all_text_chunks=None):
    if "summarize the document" in user_question.lower():
        if not all_text_chunks:
            return "No document content available to summarize. Please upload and process a document first."

        try:
            full_text = " ".join(
                [chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in all_text_chunks]
            )
            if not full_text.strip():
                return "Error: No valid content found in the document to summarize."

            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            summary = summarizer(
                full_text[:4096],
                max_length=00,
                min_length=30,
                do_sample=False
            )

            if not summary or not summary[0]['summary_text'].strip():
                sentences = full_text.split('. ')
                fallback_summary = '. '.join(sentences[:10]) + '.'
                return RESPONSE_TEMPLATE_DYNAMIC.format(answer=fallback_summary)

            return RESPONSE_TEMPLATE_DYNAMIC.format(answer=summary[0]['summary_text'])
        except Exception as e:
            logging.error(f"Error during summarization: {str(e)}")
            return f"An error occurred during summarization: {str(e)}"

    retriever = vector_store.as_retriever(search_kwargs={"k": 50})
    try:
        relevant_chunks = retriever.get_relevant_documents(user_question)
        if not relevant_chunks:
            return "No relevant information found in the uploaded document to answer this question."

        retrieved_context = " ".join(
            [chunk.page_content if hasattr(chunk, 'page_content') else str(chunk) for chunk in relevant_chunks]
        )
        response = conversation(question=user_question, context=retrieved_context)
        return RESPONSE_TEMPLATE_DYNAMIC.format(answer=response['answer'])
    except Exception as e:
        logging.error(f"Error processing user question: {str(e)}")
        return f"An error occurred: {str(e)}"

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def process_files(uploaded_files):
    pdf_processor = PDFProcessor()
    all_text = ""
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.size == 0:
                logging.warning(f"The file {uploaded_file.name} is empty or corrupted.")
                st.warning(f"The file {uploaded_file.name} is empty or corrupted. Please upload a valid file.")
                continue

            if uploaded_file.type == "application/pdf":
                extracted_text = pdf_processor.extract_text(uploaded_file)
                logging.debug(f"Extracted text from {uploaded_file.name}: {extracted_text[:500]}")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                extracted_text = extract_text_from_docx(uploaded_file)
                logging.debug(f"Extracted text from {uploaded_file.name}: {extracted_text[:500]}")
            else:
                st.warning(f"Unsupported file type: {uploaded_file.type}. Please upload a PDF or Word document.")
                continue

            if not extracted_text:
                logging.warning(f"No text extracted from {uploaded_file.name}. The file may be scanned or contain no text.")
                st.warning(f"No text extracted from {uploaded_file.name}. Please upload a file with selectable text.")
                continue

            all_text += extracted_text
        except Exception as e:
            logging.error(f"Error processing {uploaded_file.name}: {str(e)}")
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            continue

    if not all_text.strip():
        raise ValueError("No text extracted from any of the uploaded files. Please ensure they contain selectable text.")

    try:
        chunks = pdf_processor.split_text(all_text, chunk_size=5000, overlap=500)
        logging.debug(f"Number of chunks: {len(chunks)}")
        return chunks
    except Exception as e:
        logging.error(f"Error splitting text into chunks: {str(e)}")
        raise ValueError(f"Error splitting text into chunks: {str(e)}")

def init_session_state():
    st.session_state.setdefault("conversation", None)
    st.session_state.setdefault("vector_store", None)
    st.session_state.setdefault("uploaded_files", None)
    st.session_state.setdefault("files_processed", False)
    st.session_state.setdefault("chat_history", [])
    st.session_state.setdefault("all_text_chunks", None)
    st.session_state.setdefault("user_question", "")

def create_or_load_vector_store(chunks):
    vector_store_manager = VectorStore()
    return vector_store_manager.create_vector_store(chunks)

def create_conversation_chain():
    try:
        qa_pipeline = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            tokenizer="deepset/roberta-base-squad2",
            truncation=True,
            padding="max_length"
        )
        return qa_pipeline
    except Exception as e:
        raise RuntimeError(f"Failed to initialize the question-answering pipeline: {str(e)}")

def display_chat_history():
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            overflow-y: auto;
            max-height: 80vh;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if "chat_history" in st.session_state and st.session_state.chat_history:
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            st.markdown("### Chat History")
        with col2:
            if st.button("🔄", key="refresh_chat_history"):
                st.session_state.chat_history = []
                st.rerun()

        for idx, chat in enumerate(st.session_state.chat_history.copy()):
            col1, col2 = st.sidebar.columns([1, 4])
            with col1:
                if st.button("🗑️", key=f"delete_{idx}"):
                    del st.session_state.chat_history[idx]
                    st.rerun()
            with col2:
                st.write(f"**Question:** {chat['question']}")
                st.write(f"**Answer:** {chat['answer']}")
                st.write("---")
    else:
        st.sidebar.write("No chat history yet.")

def main():
    init_session_state()
    st.markdown("<h1 class='main-title'>&#128218; Document Chat Assistant</h1>", unsafe_allow_html=True)
    display_chat_history()

    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload your documents", type=['pdf', 'docx'], accept_multiple_files=True)
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        st.success(f"Uploaded {len(uploaded_files)} files.")
    if st.session_state.uploaded_files and not st.session_state.files_processed:
        try:
            all_text_chunks = process_files(st.session_state.uploaded_files)
            if all_text_chunks:
                vector_store = create_or_load_vector_store(all_text_chunks)
                st.session_state.vector_store = vector_store
                st.session_state.conversation = create_conversation_chain()
                st.session_state.files_processed = True
                st.session_state.all_text_chunks = all_text_chunks
                st.success("Documents processed and ready for questions.")
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")
            logging.error(f"Error processing documents: {str(e)}")

    user_question = st.text_input(
        "Enter your question:",
        value=st.session_state.get("user_question", "")
    )

    if st.button("Submit Question"):
        if not user_question:
            st.error("Please enter a valid question.")
            return
        try:
            if "conversation" not in st.session_state or not st.session_state.conversation:
                st.error("Conversation chain is not initialized. Please upload and process documents first.")
                return
            dynamic_response = generate_dynamic_response(
                user_question,
                st.session_state.vector_store,
                st.session_state.conversation,
                st.session_state.all_text_chunks
            )
            existing_chat = next((chat for chat in st.session_state["chat_history"] if chat['question'].lower() == user_question.lower()), None)
            if existing_chat:
                st.write(f"**Question:** {existing_chat['question']}")
                st.write(f"**Answer:** {existing_chat['answer']}")
                st.info("This question was already asked. The answer is retrieved from the chat history.")
            else:
                st.session_state["chat_history"].append({"question": user_question, "answer": dynamic_response})
                st.write(f"**Question:** {user_question}")
                st.write(f"**Answer:** {dynamic_response}")
                st.session_state.user_question = ""
                st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()