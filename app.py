import streamlit as st
from utils.file_handler import save_uploaded_file
from chain.resume_chain import resume_chain
from chain.question_chain import run_interview
from chain.evaluation_chain import evaluate_results

st.set_page_config(page_title="Interview Preparation Application",layout="wide")
st.title("Interview Preparation Chatbot Application")

# Initialize session state
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "resume_context" not in st.session_state:
    st.session_state.resume_context = ""
if "file_path" not in st.session_state:
    st.session_state.file_path = None

#upload resume
upload_resume = st.file_uploader("Upload Resume in PDF Format",type="pdf")

if upload_resume:
    with st.spinner("Processing Resume....."):
        file_path = save_uploaded_file(upload_resume)
        st.session_state.file_path = file_path
        st.success("Resume Uploaded Succesfully")
else:
    st.info("📄 Please upload your resume in PDF format to start the interview")


#ChatUI
user_input = st.chat_input("Type Answer or Start Interview")
if user_input:
    st.chat_message("user").write(user_input)
    
    if user_input.lower() == "start interview":
        # Check if resume is uploaded
        if st.session_state.file_path is None:
            st.error("❌ Please upload your resume first before starting the interview!")
        else:
            st.session_state.resume_context = resume_chain(pdf_path=st.session_state.file_path, query=user_input)
            response = run_interview(user_input=user_input, context=st.session_state.resume_context)
            st.chat_message("assistant").write(response)
            st.session_state.last_question = response
            st.session_state.interview_started = True
    else:
        if st.session_state.interview_started and st.session_state.last_question:
            # Evaluate the answer
            evaluation_result = evaluate_results(answer=user_input, question=st.session_state.last_question)
            score = evaluation_result.get('score', 5)
            with st.expander("Evaluation Feedback", expanded=True):
                st.write(f"Score: {score}/10")
                st.write("Strengths:", evaluation_result.get('strengths', 'N/A'))
                st.write("weaknesses:", evaluation_result.get('weaknesses', 'N/A'))
                st.write("Improved Answer:", evaluation_result.get('improved_answer', 'N/A'))
            
            # Generate next question
            st.write("---")
            next_question = run_interview(user_input=user_input, context=st.session_state.resume_context)
            st.chat_message("assistant").write(next_question)
            st.session_state.last_question = next_question
    
    

