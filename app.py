from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai 
import os
import PyPDF2 as pdf
import docx

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text  # Assuming `.text` is the correct way to access the generated text

def get_pdf_content(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

def get_word_content(uploaded_file):
    reader = docx.Document(uploaded_file)
    text = ""
    for para in reader.paragraphs:
        text += para.text
    return text

input_prompt1 = """
 You are an experienced HR manager,your task is to review the provided resume against the given job description. 
 Please share your professional evaluation on whether the resume aligns with the job description. 
 Highlight the strengths and weaknesses of the resume in relation to the specified job description.
 resume: {text}
 job description: {jd}
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any of the following roles 
software engineering or Data Analyst or Data Science or big data engineer or  Product Manager or HR or Business Analyst
and ATS functionality as well. Your task is to give the percentage of match if the resume matches to the job description with 
a high accuracy rate.First output the percentage match then followed by list of keywords that are missing.
Also, your need to evaluate the resume against the provided job description.further, provide recommendations for 
enhancing the candidate's skills and identify which areas require further development.
resume: {text}
job description: {jd}
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any of the following roles 
software engineering or Data Analyst or Data Science or big data engineer or  Product Manager or HR or Business Analyst
and ATS functionality as well. Your task is to list down the keywords that are missing while comparing job description 
with the uploaded resume.Also, provide recommendations for enhancing the candidate's skills that is there in the resume
and identify which areas require further development.
resume: {text}
job description: {jd}
"""
st.set_page_config(page_title="ATS App")
st.markdown("<h1 style='text-align: center;'>Application Tracking System</h1>", unsafe_allow_html=True)
st.header("Improve Resume using ATS Assistance ✒️")
jd = st.text_area("Copy & Paste The JD here")
uploaded_file = st.file_uploader("Upload Your Resume only in PDF or WORD Format", type=['pdf', 'docx'], help='Please upload the Pdf or Word')

if uploaded_file is not None:
    file_type = uploaded_file.type.split('/')[-1].upper()
    if file_type == "PDF":
        st.write(f"📄 {file_type} Uploaded Successfully")
    elif file_type == "VND.OPENXMLFORMATS-OFFICEDOCUMENT.WORDPROCESSINGML.DOCUMENT":
        st.write(f"📝 WORD Uploaded Successfully")

submit1 = st.button("Summarize About the Resume & Suggest to improvise skills")
submit2 = st.button("Percentage match")
submit3 = st.button("Important Keywords Missing?")

if uploaded_file is not None:
    file_type = uploaded_file.type
    if file_type == 'application/pdf':
        text = get_pdf_content(uploaded_file)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text = get_word_content(uploaded_file)

    if submit1:
        response = get_gemini_response(input_prompt1.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
    
    if submit2:
        response = get_gemini_response(input_prompt2.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
    
    if submit3:
        response = get_gemini_response(input_prompt3.format(text=text, jd=jd))
        st.subheader("The Response is")
        st.write(response)
else:
    st.write("Please upload a PDF or Word file to proceed.")
