import streamlit as st
import os
from document_parser import DocumentParser
from testcase_generator import TestCaseGenerator
import tempfile

# Page Configuration
st.set_page_config(page_title="AI Test Case Generator", page_icon="🤖", layout="wide")

# Initialize Session State for the Generator
if 'generator' not in st.session_state:
    st.session_state.generator = TestCaseGenerator(model_name="llama3.2:3b")
    st.session_state.parser = DocumentParser()

# UI Header
st.title("🤖 Local AI Test Case Generator")
st.markdown("---")

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Select Model", ["llama3.2:3b", "llama3.1:8b"], index=0)
    if st.button("Update Model"):
        st.session_state.generator = TestCaseGenerator(model_name=model_choice)
        st.success(f"Switched to {model_choice}")

# Main Layout: Two Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input Requirements")
    input_method = st.radio("Choose Input Method:", ["Upload File", "Paste Text", "Custom Prompt"])

    requirements_text = ""

    if input_method == "Upload File":
        uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
        if uploaded_file:
            # Save uploaded file temporarily to parse it
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name
            
            with st.spinner("Extracting text..."):
                requirements_text = st.session_state.parser.parse_file(tmp_path)
            os.remove(tmp_path) # Clean up
            st.success("File parsed successfully!")

    elif input_method == "Paste Text":
        requirements_text = st.text_area("Paste your requirements here:", height=300)

    else:
        requirements_text = st.text_input("Enter your custom prompt:")

    generate_btn = st.button("🚀 Generate Test Cases")

with col2:
    st.subheader("📊 Generated Test Cases")
    if generate_btn and requirements_text:
        with st.spinner("AI is thinking..."):
            try:
                if input_method == "Custom Prompt":
                    result = st.session_state.generator.generate_from_prompt(requirements_text)
                else:
                    result = st.session_state.generator.generate_test_cases(requirements_text)
                
                st.markdown(result)
                
                # Download Button
                st.download_button(
                    label="📥 Download as Text File",
                    data=result,
                    file_name="generated_test_cases.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("Input your requirements and click 'Generate' to see results here.")