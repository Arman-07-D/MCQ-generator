import streamlit as st
from test import generate_mcqs
import PyPDF2
import json

st.title("LAST MINUTE")
st.subheader("Generate exam-ready MCQs instantly using Artificial Intelligence..")

input_mode = st.radio("Select Input Mode", ["Text", "PDF"])

text = ""

if input_mode == "Text":
    text = st.text_area("Paste your notes")

elif input_mode == "PDF":
    uploaded_file = st.file_uploader("Upload a file", type="pdf")
    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        st.success("PDF loaded successfully")

num = st.slider("Number of MCQs (1-20)", min_value=1, max_value=20, value=5)
level = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])

if "mcqs" not in st.session_state:
    st.session_state.mcqs = []
if "simple_mcqs" not in st.session_state:
    st.session_state.simple_mcqs = []

col1, col2 = st.columns(2)

with col1:
    if st.button("Generate MCQs"):
        if not text.strip():
            st.warning("⚠️ Please provide text or upload a PDF")
        else:
            with st.spinner("Generating MCQs..."):
                st.session_state.mcqs = [] #clear quiz 
                response = generate_mcqs(text, num)
                try:
                    st.session_state.simple_mcqs = json.loads(response)
                except:
                    st.error("JSON parsing failed! Please try again.")

with col2:
    if st.button("🧠 Generate Instant Quiz"):
        if not text.strip():
            st.warning("⚠️ Please provide text or upload a PDF")
        else:
            with st.spinner("Generating Quiz..."):
                st.session_state.simple_mcqs = []  # clear simple MCQ display
                response = generate_mcqs(text, num) 
                try:
                    st.session_state.mcqs = json.loads(response)  
                except:
                    st.error("Failed to parse MCQs.")



# Show simple MCQs
if st.session_state.simple_mcqs:
    st.success(f"Here are your {num} MCQs")
    for i, mcq in enumerate(st.session_state.simple_mcqs):
        st.markdown(f"**Q{i+1}: {mcq['question']}**")
        for opt in mcq["options"]:
            st.write(opt)
        st.success(f"✅ Answer: {mcq['answer']}")
        st.divider()

# Show quiz
mcqs = st.session_state.mcqs

if mcqs:
    st.subheader("🧠 Quiz Ready")
    st.success(f"Here are your {len(mcqs)} questions")

    for i, mcq in enumerate(mcqs):
        options = ["--Select an option--"] + mcq["options"]
        st.radio(
            f"Q{i+1}: {mcq['question']}",
            options,
            key=f"quiz_{i}"
        )

# Submit button
if st.button("🚀 Submit Quiz"):
    if not mcqs:
        st.warning("⚠️ No quiz generated yet!")
    else:                          
        score = 0
        unanswered = 0

        for i, mcq in enumerate(mcqs):
            user_ans = st.session_state.get(f"quiz_{i}", "")
            if user_ans == "--Select an option--":
                unanswered += 1
                continue
            if user_ans == mcq["answer"]:
                score += 1

        st.markdown(f"🎯 Score: {score}/{len(mcqs)}")
        percentage = (score / len(mcqs)) * 100

        if percentage >= 80:
            st.success("🔥 Excellent! You're ready!")
        elif percentage >= 50:
            st.info("👍 Good, but can improve!")
        else:
            st.error("⚠️ You are not fully prepared yet.")

        if unanswered > 0:
            st.warning(f"⚠️ {unanswered} unanswered questions")
    