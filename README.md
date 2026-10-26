# AI Study Companion — Cloud-ready edition

This deployment build was adapted from your uploaded ZIP. It retains Learning Mode, five-question Quiz Mode, scoring, `st.audio_input`, and audio playback. It replaces the original OpenAI calls with Gemini and server-compatible speech services.

## Deploy (Streamlit Community Cloud)

1. Upload **the contents of this folder** to a GitHub repository. Do not upload `.env` or `.streamlit/secrets.toml`.
2. Visit https://share.streamlit.io and choose **Create app** using the repository's `main` branch and `app.py` as the entrypoint.
3. Under **Advanced settings → Secrets**, paste the TOML line below with your *own* key:

   ```toml
   GEMINI_API_KEY = "YOUR_REAL_GEMINI_API_KEY"
   ```

4. Deploy. Streamlit reads dependencies from `requirements.txt`.

## Local run (Windows PowerShell)

```powershell
cd "C:\Users\Pc\Desktop\AI_Study_Assistant_Cloud_Ready"
C:\Users\Pc\.venv\Scripts\python.exe -m pip install -r requirements.txt
C:\Users\Pc\.venv\Scripts\python.exe -m streamlit run app.py
```

For local use copy `.env.example` to `.env` and put your key there. Never commit `.env`.

## Notes and limits

- Default Gemini model: `gemini-3.5-flash-lite`. Availability depends on API account/region; override using `GEMINI_MODEL` environment variable if needed.
- Free tiers have rate and usage restrictions; Google may change their availability.
- Speech recognition uses Google's internet-based web recognizer, not an offline/private speech engine. gTTS similarly requires internet.
- `st.audio_input` captures microphone audio in the visitor's browser. MP3 replies are played via `st.audio`.
- Quizzes and scores are kept in the browser session; no account system or durable database.
- Live Gemini API calls, hosted deployment, and user microphone permissions cannot be tested without your environment and key. Python syntax is checked.
