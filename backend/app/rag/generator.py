from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, chunks, history):
    context = ""

    for chunk in chunks:
        context += f"\nPage {chunk.page_number}:\n"
        context += chunk.text
        context += "\n"

    conversation = ""

    for message in history:
        conversation += f"{message.role}: {message.content}\n"

    prompt = f"""
You are an AI study assistant.

Answer the user's question using ONLY the provided study material.

Use the previous conversation to understand follow-up questions
and references such as "it", "its", "that" and "explain more".

Rules:
1. Use only the study material for factual answers.
2. Use conversation history to understand the user's intent.
3. Do not use outside knowledge.
4. Keep the answer clear and easy to understand.
5. Cite important statements using [Page X].
6. If the answer cannot be found in the study material, say:
"The information is not available in the provided study material."

Previous conversation:
{conversation}

Study material:
{context}

Current question:
{question}

Answer:
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def check_relevance(question: str, chunks):

    context = ""

    for chunk in chunks:
        context += f"\nPage {chunk.page_number}:\n"
        context += chunk.text
        context += "\n"

    prompt = f"""
You are checking whether study material can answer a question.

Study material:
{context}

Question:
{question}

Does the study material contain enough information to answer this question?

Reply with ONLY:
YES
or
NO
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()