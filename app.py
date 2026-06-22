from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from groq import Groq
from PyPDF2 import PdfReader

# Configure Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Groq response function
def get_groq_response(job_description, resume_text, prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"""
                Job Description:
                {job_description}

                Resume:
                {resume_text}
                """
            }
        ]
    )

    return response.choices[0].message.content


# Extract text from PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit App
st.set_page_config(page_title="Resume Analyzer")
st.header("PrepWiseAI - AI Powered Resume Analyzer")

input_text = st.text_area("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("About Resume")
submit3 = st.button("Percentage Match")


input_prompt1 = """
You are an experienced Technical Human Resource Manager.
Review the provided resume against the job description.
Share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight strengths and weaknesses.
"""

input_prompt3 = """
You are a skilled ATS scanner.
Evaluate the resume against the provided job description.

Give:
1. Percentage match
2. Missing keywords
3. Final thoughts
"""


if submit1:
    if uploaded_file is not None:
        resume_text = input_pdf_setup(uploaded_file)
        response = get_groq_response(input_text, resume_text, input_prompt1)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Please upload the resume")


if submit3:
    if uploaded_file is not None:
        resume_text = input_pdf_setup(uploaded_file)
        response = get_groq_response(input_text, resume_text, input_prompt3)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Please upload the resume")