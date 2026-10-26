"""Gemini-based explanations and structured five-question quizzes."""
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent / ".env")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

class Question(BaseModel):
    question: str
    options: list[str]
    correct_index: int
    explanation: str

class Quiz(BaseModel):
    questions: list[Question]

def _client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        try:
            import streamlit as st
            key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
        except Exception:
            pass
    if not key or key.startswith("your_"):
        raise RuntimeError("Gemini API key missing. Add GEMINI_API_KEY to Streamlit Secrets (online) or .env (local).")
    return genai.Client(api_key=key)

def explain_topic(topic: str) -> str:
    response = _client().models.generate_content(
        model=MODEL,
        contents=f"Explain this student question or topic: {topic[:1000]}",
        config=types.GenerateContentConfig(
            system_instruction=("You are a clear, accurate university study tutor. Explain in simple English "
                                "with one practical example and 2-3 key points, within 180 words. "
                                "If unsure, say so."),
            temperature=0.5,
        ),
    )
    if not response.text:
        raise ValueError("The AI model returned no explanation.")
    return response.text

def generate_quiz(topic: str) -> list[Question]:
    response = _client().models.generate_content(
        model=MODEL,
        contents=("Create EXACTLY FIVE factual, beginner-friendly multiple-choice questions about: "
                  f"{topic[:500]}. Each needs FOUR options, one correct_index from 0 to 3, "
                  "and a short explanation. Make all choices plausible."),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Quiz,
            temperature=0.4,
        ),
    )
    if not response.text:
        raise ValueError("The AI model returned no quiz.")
    parsed = Quiz.model_validate_json(response.text)
    if len(parsed.questions) != 5:
        raise ValueError("The AI generated an incorrect number of questions. Please retry.")
    for question in parsed.questions:
        if len(question.options) != 4 or not 0 <= question.correct_index < 4:
            raise ValueError("The AI generated invalid answer options. Please retry.")
    return parsed.questions
