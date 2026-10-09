from google import genai
import os

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts
    )

    return [embedding.values for embedding in response.embeddings]