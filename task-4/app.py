import streamlit as st
import os
from gemini_service import GeminiService
from pdf_summarizer import summarize_pdf_text
from quiz_generator import generate_quiz

st.set_page_config(page_title="Gemini-Powered App", layout="wide")

st.title("📚 Gemini-Powered Document Assistant")
st.write("Summarize documents and generate quizzes using Google Gemini API.")

# --- API Key Configuration ---
st.sidebar.header("Configuration")
gemini_api_key = st.sidebar.text_input(
    "Enter your Gemini API Key", 
    type="password", 
    help="You can get your API key from https://ai.google.dev/genai/docs/get-started#get_your_api_key"
)

# Initialize GeminiService
gemini_service = None
if gemini_api_key:
    try:
        gemini_service = GeminiService(api_key=gemini_api_key)
        st.sidebar.success("Gemini Service Initialized!")
    except ValueError as e:
        st.sidebar.error(f"Error initializing Gemini Service: {e}")
    except Exception as e:
        st.sidebar.error(f"An unexpected error occurred: {e}")
else:
    st.sidebar.warning("Please enter your Gemini API Key to proceed.")

st.markdown("---")

# --- PDF Summarizer Section ---
st.header("📝 Document Summarizer")
st.write("Paste your document text below to get a concise summary.")

summary_text_input = st.text_area("Document Text for Summarization", height=300, key="summary_input")

if st.button("Generate Summary", disabled=not gemini_service):
    if summary_text_input:
        with st.spinner("Generating summary..."):
            try:
                summary = summarize_pdf_text(gemini_service, summary_text_input)
                st.subheader("Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"Error during summarization: {e}")
    else:
        st.warning("Please enter some text to summarize.")

st.markdown("---")

# --- Quiz Generator Section ---
st.header("🧠 Quiz Generator")
st.write("Paste your document text below to generate multiple-choice quiz questions.")

quiz_text_input = st.text_area("Document Text for Quiz Generation", height=300, key="quiz_input")
num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=3)

if st.button("Generate Quiz", disabled=not gemini_service):
    if quiz_text_input:
        with st.spinner(f"Generating {num_questions} quiz questions..."):
            try:
                quiz = generate_quiz(gemini_service, quiz_text_input, num_questions)
                if quiz:
                    st.subheader("Generated Quiz:")
                    for i, q in enumerate(quiz):
                        st.markdown(f"**{i+1}. {q.get('question', 'No question found')}**")
                        options = q.get('options', [])
                        for opt_idx, option in enumerate(options):
                            st.write(f"  {chr(65 + opt_idx)}. {option}")
                        st.success(f"  **Correct Answer:** {q.get('answer', 'N/A')}")
                        st.markdown("---")
                else:
                    st.warning("Could not generate quiz. Please try again with different text or fewer questions.")
            except Exception as e:
                st.error(f"Error during quiz generation: {e}")
    else:
        st.warning("Please enter some text to generate a quiz.")

