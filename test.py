import os
from dotenv import load_dotenv
from groq import Groq
import textwrap

load_dotenv(".env")

client = Groq(api_key=os.getenv("GR_TOKEN"))

def generate_mcqs(text: str,num: int,level:str="Medium") -> str:   #difficulty is medium by default
    # Properly indented prompt using textwrap.dedent
    if num<1:
        num=1
    elif num>20:
        num=20

    prompt = textwrap.dedent(f"""
You are a teacher.

From the following text, generate {num} multiple-choice questions.
Difficulty level: {level}

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question text",
    "options": ["A) option", "B) option", "C) option", "D) option"],
    "answer": "X" the  option
  }}
]

Rules:
- Do NOT add any explanation
- Do NOT add extra text
- Output must be valid JSON only
- Each question must have exactly 4 options
- Answer must be A, B, C, or D show the answer with its containing option

Text:
{text}
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

    
    return completion.choices[0].message.content