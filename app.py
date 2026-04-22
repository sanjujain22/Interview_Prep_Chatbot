import streamlit as st
from utils.file_handler import save_uploaded_file
from chain.resume_chain import resume_chain
from chain.question_chain import run_interview

st.title("Interview Preparation Application")


#upload resume
upload_resume = st.file_uploader("Upload Resume",type="pdf")

if upload_resume is not None:
    path = save_uploaded_file(upload_resume)
    st.success("Resume Uploaded")


#ChatUI
user_input = st.chat_input("Type Answer or Start Interview")
if user_input is not None:
    if user_input.lower() == "start interview":
        response = resume_chain.run(path)
    else:
        response=run_interview(user_input)
