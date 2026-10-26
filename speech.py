"""Server-compatible audio: Streamlit browser recorder -> Google web STT; gTTS MP3."""
from io import BytesIO
import speech_recognition as sr
from gtts import gTTS


def speech_to_text(wav_bytes: bytes) -> str:
    recognizer = sr.Recognizer()
    with sr.AudioFile(BytesIO(wav_bytes)) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="en-US").strip()
    except sr.UnknownValueError as exc:
        raise ValueError("Speech was not understood. Try recording again or type your answer.") from exc
    except sr.RequestError as exc:
        raise RuntimeError("Speech recognition service unavailable. Try typing instead.") from exc


def text_to_speech(text: str) -> bytes:
    out = BytesIO()
    gTTS(text=text[:3000], lang="en").write_to_fp(out)
    return out.getvalue()
