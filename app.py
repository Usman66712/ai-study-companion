import streamlit as st
from dotenv import load_dotenv
from ai_engine import explain_topic, generate_quiz
from quiz import calculate_score, option_from_speech
from speech import speech_to_text, text_to_speech

load_dotenv()

st.set_page_config(page_title="AI Study Companion", page_icon="🎓")
st.title("🎓 AI Study Companion")
st.caption("Learn with AI, speak your questions, and test your knowledge.")
st.caption("AI explanations use Gemini. Voice input uses Google web speech recognition; audio uses gTTS. These speech services require an internet connection.")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = []
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "answer_pick" not in st.session_state:
    st.session_state.answer_pick = 0

mode = st.sidebar.radio("Choose a mode", ["Learning Mode", "Quiz Mode"])


def show_audio(text):
    try:
        audio = text_to_speech(text)
        st.audio(audio, format="audio/mp3")
    except Exception:
        st.warning("Text is available, but voice playback failed.")


if mode == "Learning Mode":
    st.subheader("Learn a topic")
    typed = st.text_input("Type a question or topic", key="learning_text")
    recording = st.audio_input("Or record a question")
    if st.button("Explain", type="primary"):
        try:
            question = speech_to_text(recording.getvalue()) if recording else typed.strip()
            if not question:
                st.warning("Type a question or record your voice first.")
            else:
                st.write("**You asked:**", question)
                with st.spinner("The tutor is thinking..."):
                    explanation = explain_topic(question)
                st.write("**AI Tutor:**")
                st.write(explanation)
                show_audio(explanation)
        except Exception as error:
            st.error(f"Request failed: {type(error).__name__}: {error}")

else:
    st.subheader("Practice with a five-question quiz")
    topic = st.text_input("Enter your quiz topic", value=st.session_state.topic)
    if st.button("Generate Quiz", type="primary"):
        if not topic.strip():
            st.warning("Enter a topic first.")
        else:
            try:
                with st.spinner("Generating questions..."):
                    new_questions = generate_quiz(topic.strip())
                st.session_state.questions = new_questions
                st.session_state.answers = []
                st.session_state.topic = topic.strip()
                st.session_state.answer_pick = 0
                st.rerun()
            except Exception as error:
                st.error(f"Quiz generation failed: {type(error).__name__}: {error}")

    questions = st.session_state.questions
    answers = st.session_state.answers
    if questions and len(answers) < len(questions):
        position = len(answers)
        question = questions[position]
        st.progress(position / len(questions))
        st.markdown(f"**Question {position + 1} of {len(questions)}**")
        st.write(question.question)
        options = [f"{letter}. {label}" for letter, label in zip("ABCD", question.options)]
        selected = st.radio("Choose an answer", range(4), format_func=lambda i: options[i], key=f"choice_{position}")
        st.caption("Optional: Say 'A', 'B', 'C', or 'D' into the microphone.")
        recorded_answer = st.audio_input("Record an answer (optional)", key=f"voice_{position}")
        if st.button("Submit Answer", key=f"submit_{position}"):
            try:
                pick = selected
                if recorded_answer:
                    transcript = speech_to_text(recorded_answer.getvalue())
                    detected = option_from_speech(transcript)
                    if detected is None:
                        st.warning(f"I heard '{transcript}'. Say 'Option B', for example, or use the radio buttons.")
                        st.stop()
                    pick = detected
                    st.write("Recognized:", transcript)
                st.session_state.answers.append(pick)
                st.rerun()
            except Exception:
                st.error("Unable to transcribe that answer. Please select an option instead.")

    elif questions:
        correct, total = calculate_score(questions, answers)
        st.success(f"Quiz complete! Your score: {correct}/{total} ({correct/total:.0%})")
        for i, (question, answer) in enumerate(zip(questions, answers), 1):
            is_correct = answer == question.correct_index
            with st.expander(f"Q{i}: {'Correct' if is_correct else 'Incorrect'}"):
                st.write(question.question)
                st.write("Your answer:", question.options[answer])
                st.write("Correct answer:", question.options[question.correct_index])
                st.write("Explanation:", question.explanation)
        summary = f"You scored {correct} out of {total}. " + (
            "Excellent work!" if correct == total else "Review the explanations and try again."
        )
        if st.button("Listen to score"):
            show_audio(summary)
        if st.button("Try a new quiz"):
            st.session_state.questions = []
            st.session_state.answers = []
            st.rerun()
