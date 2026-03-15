import os
from openai import OpenAI
from dotenv import load_dotenv
import re

load_dotenv()

client = OpenAI(
    base_url="https://api.sarvam.ai/v1",
    api_key=os.getenv("SARVAM_API_KEY"),
)

def generate_answer(query, context, category):
    system_prompt = """You are Annadata AI, an expert agricultural advisor 
for Indian farmers. You have deep knowledge of Indian crops, diseases, 
pest management, government schemes, soil health, and weather patterns.
Give practical, specific, actionable advice. Be concise but complete.
Always respond in English only."""

    user_message = f"""Use this context from ICAR documents:

{context}

Farmer's Question: {query}

Give detailed farming advice:"""

    response = client.chat.completions.create(
        model="sarvam-m",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=512,
    )

    answer = response.choices[0].message.content

    if "<think>" in answer:
        if "</think>" in answer:
            end = answer.find("</think>") + len("</think>")
            answer = answer[end:].strip()
        else:
            answer = answer.split("<think>")[-1].strip()

    clean_lines = []
    for line in answer.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = line.replace("**", "")
        line = line.replace("* ", "• ")
        line = line.replace("*", "")
        if line.startswith("#"):
            line = line.lstrip("#").strip()
        clean_lines.append(line)

    answer = "\n".join(clean_lines)
    return answer