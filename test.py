import os
from dotenv import load_dotenv
from groq import Groq
import textwrap

load_dotenv(".env")

client = Groq(api_key=os.getenv("GR_TOKEN"))

def generate_mcqs(text: str,num: int) -> str:
    # Properly indented prompt using textwrap.dedent
    if num<1:
        num=1
    elif num>20:
        num=20


    prompt = textwrap.dedent(f"""\
        You are a teacher.

        From the following text, generate {num} multiple-choice questions.

        Text:
        {text}

        Format:
        """)
    for i in range(1,num+1):
        prompt+=textwrap.dedent(f"""
        Q1. question here
        A) option
        B) option
        C) option
        D) option
        Answer: X

        Q2. ...and so on
        Q3. ...and so on
    """)

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful teacher who creates clear, well-formatted MCQ questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    # Return the content of the API response
    return completion.choices[0].message.content