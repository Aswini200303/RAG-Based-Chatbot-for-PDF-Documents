import streamlit as st
from pypdf import PdfReader
import os
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
# Download NLTK stopwords
nltk.download('stopwords')
# Set page configuration
st.set_page_config(page_title="PDF Chatbot", layout="wide")
# Inject custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #F2F2F2;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 10px;
    }
    .stChatMessage.user {
        background-color: #E1F5FE;
    }
    .stChatMessage.assistant {
        background-color: #E3E3E3;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("PDF Chatbot")
# Set Groq API key
os.environ["GROQ_API_KEY"] = "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"
# File upload widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    try:
        # Read PDF content using PyPDF
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    except Exception as e:
        st.error(f"An error occurred while reading the PDF: {e}")
    if pdf_text.strip():
        # Chat interface
        user_input = st.chat_input("Ask a question about the PDF")
        if user_input:
            # Prepare system message with the PDF content
            system_message = {
                "role": "system",
                "content": f"You are an assistant that answers questions based on the following PDF content:\n\n{pdf_text}"
            }
            # Initialize Groq client
            from groq import Groq
            client = Groq()
            try:
                # Send query to Groq
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[system_message, {"role": "user", "content": user_input}],
                    temperature=1,
                    max_completion_tokens=128,
                    top_p=1,
                    stream=False,
                    stop=None,
                )
                # Display the assistant's response
                response = completion.choices[0].message.content
                st.markdown(f"**Assistant:** {response}")
                # Update chat history
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"question": user_input, "answer": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")
# Display chat history in the sidebar
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
            if st.button(":arrows_counterclockwise:", key="refresh_chat_history"):
                st.session_state.chat_history = []
                st.rerun()
        for idx, chat in enumerate(st.session_state.chat_history.copy()):
            col1, col2 = st.sidebar.columns([1, 4])
            with col1:
                if st.button(":wastebasket:", key=f"delete_{idx}"):
                    del st.session_state.chat_history[idx]
                    st.rerun()
            with col2:
                st.write(f"**Question:** {chat['question']}")
                st.write(f"**Answer:** {chat['answer']}")
                st.write("---")
    else:
        st.sidebar.write("No chat history yet.")
# Call the chat history display function
display_chat_history()