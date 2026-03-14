
import streamlit as st
from test import generate_mcqs

st.title("LAST MINUTE")
st.subheader("Generate exam-ready MCQs instantly using Artificial Intelligence..")

notes=st.text_area("Paste your notes")
num=st.slider("Number of MCQs (1-20)",min_value=1,max_value=20,value=5)

if st.button("Generate MCQs"):
   if notes.strip()=="":
      st.warning("Please Paste some text!!")
   else:
      with st.spinner("Generatig MCQs"):
         mcq =generate_mcqs(notes,num)
         st.success("Here are your MCQs")
         st.text(mcq)

    