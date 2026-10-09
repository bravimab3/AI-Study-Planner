from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import ChatSession, ChatMessage
from app.rag.retriever import retrieve_chunks
from app.rag.generator import generate_answer, check_relevance

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    document_id: int
    session_id: int


@router.post("/chat/sessions")
def create_chat_session(
    user_id: int,
    db: Session = Depends(get_db)
):
    session = ChatSession(user_id=user_id)

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "session_id": session.id
    }


@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):

    # Save user's question
    user_message = ChatMessage(
        session_id=request.session_id,
        role="user",
        content=request.question
    )

    db.add(user_message)
    db.commit()

    # Get conversation history
    history = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == request.session_id)
        .order_by(ChatMessage.created_at)
        .all()
    )

    # Print conversation history for testing
    for message in history:
        print(message.role, ":", message.content)

    # Retrieve relevant PDF chunks
    chunks = retrieve_chunks(
        request.question,
        db,
        request.document_id,
        top_k=5
    )

    # Check whether the question can be answered
    relevance = check_relevance(
        request.question,
        chunks
    )

    if relevance != "YES":

        answer = "The information is not available in the provided study material."

        # Save assistant's response
        assistant_message = ChatMessage(
            session_id=request.session_id,
            role="assistant",
            content=answer
        )

        db.add(assistant_message)
        db.commit()

        return {
            "answer": answer,
            "sources": []
        }

    # Generate answer
    answer = generate_answer(
    request.question,
    chunks,
    history
)

    # Save assistant's answer
    assistant_message = ChatMessage(
        session_id=request.session_id,
        role="assistant",
        content=answer
    )

    db.add(assistant_message)
    db.commit()

    # Prepare sources
    sources = []

    for chunk in chunks:
        sources.append({
            "document_id": chunk.document_id,
            "document": chunk.document.filename,
            "page": chunk.page_number,
            "chunk": chunk.chunk_index
        })

    return {
        "answer": answer,
        "sources": sources
    }