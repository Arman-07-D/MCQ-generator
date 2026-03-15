import streamlit as st
from test import generate_mcqs
import PyPDF2

st.title("LAST MINUTE")
st.subheader("Generate exam-ready MCQs instantly using Artificial Intelligence..")
#for normal text
notes=st.text_area("Paste your notes")
#for PDFs
uploaded_file=st.file_uploader("Upload a file",type="pdf")
text=""
if uploaded_file is not None:
   pdf_reader=PyPDF2.PdfReader(uploaded_file)
   for page in pdf_reader.pages:
      text+=page.extract_text()
#number of question slider

num=st.slider("Number of MCQs (1-20)",min_value=1,max_value=20,value=5)
#Difficulty dropbox

level = st.selectbox("Select difficulty level", ["Easy", "Medium", "Hard"])
if level not in ["Easy", "Medium", "Hard"]:
    raise ValueError("Difficulty must be Easy, Medium, or Hard")

if st.button("Generate MCQs"):
   if notes.strip()==""and text=="":
      st.warning("Please Paste some text!! or upload a file!!")
   elif text!="":
      with st.spinner("Generatig MCQs"):
         mcq =generate_mcqs(text,num)
         st.success(f"Here are your {num} MCQs")
         st.text(mcq)
      

   else:
      with st.spinner("Generatig MCQs"):
         mcq =generate_mcqs(notes,num)
         st.success(f"Here are your {num} MCQs")
         st.text(mcq)

    