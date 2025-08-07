from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
import os


# Remove dotenv usage and .env loading
# Set your OpenAI API key directly here (replace with your actual key)
OPENAI_API_KEY = "sk-IRZBxV_CDtKHN1pZYr8_sQ"  # <-- Replace with your actual API key

# Initialize OpenAI client with API key
client = OpenAI(
api_key=OPENAI_API_KEY,
base_url="https://agent.dev.hyperverge.org/v1"
)

app = FastAPI()

class AssessmentRequest(BaseModel):
    role: str
    skills: List[str]
    difficulty: str
    num_questions: int

def build_prompt(role: str, skills: List[str], difficulty: str, num_questions: int) -> str:
    skills_csv = ", ".join(skills)
    return f"""
You are an expert question-setter for skill-based hiring assessments.

Your task is to generate {num_questions} high-quality assessment questions for the role of a {role}.

The questions should assess the following skills: {skills_csv}.  
The difficulty level is: {difficulty}.

Each question must include:
- the question text
- 4 options (for MCQs), or direct answer (for SAQs)
- the correct answer
- a 1–2 sentence explanation of the answer

Use a mix of formats: majority MCQs, a few SAQs. Structure the output in clean JSON.

Example format:

{{
  "questions": [
    {{
      "type": "MCQ",
      "skill": "SQL",
      "question": "Which SQL clause is used to filter rows?",
      "options": ["GROUP BY", "ORDER BY", "WHERE", "HAVING"],
      "correct_answer": "WHERE",
      "explanation": "The WHERE clause is used to filter rows before grouping or aggregation."
    }},
    {{
      "type": "SAQ",
      "skill": "Metrics",
      "question": "Define a North Star Metric for an e-commerce business.",
      "answer": "Number of successful purchases per active user",
      "explanation": "North Star Metrics reflect long-term business value; purchases per user indicates user conversion."
    }}
  ]
}}
"""

@app.post("/generate-questions")
def generate_questions(data: AssessmentRequest):
    prompt = build_prompt(
        role=data.role,
        skills=data.skills,
        difficulty=data.difficulty,
        num_questions=data.num_questions
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assessment designer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )

        content = response.choices[0].message.content

        return {
            "success": True,
            "raw_output": content
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


