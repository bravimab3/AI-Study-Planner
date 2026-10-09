from google import genai
import os
import json


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_quiz(chunks, num_questions=5):

    context = ""

    for chunk in chunks:
        context += f"\nPage {chunk.page_number}:\n"
        context += chunk.text
        context += "\n"

    prompt = f"""
You are an AI study assistant.

Create {num_questions} multiple-choice questions using ONLY
the provided study material.

Study material:
{context}

Rules:
1. Questions must be based only on the study material.
2. Each question must have exactly 4 options.
3. Only one option should be correct.
4. Include an explanation for the correct answer.
5. Include the page number where the answer was found.
6. Do not use outside knowledge.
7. Return ONLY valid JSON.
8. Do not use markdown or code fences.

Return the JSON in exactly this format:

[
    {{
        "question": "Question text",
        "options": [
            "Option A",
            "Option B",
            "Option C",
            "Option D"
        ],
        "correct_answer": 0,
        "explanation": "Explanation of the correct answer",
        "source_page": 2
    }}
]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    print("RAW GEMINI RESPONSE:")
    print(repr(response.text))

    quiz = json.loads(response.text)

    return quiz