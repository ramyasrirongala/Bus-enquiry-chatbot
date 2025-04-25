
# Telangana Transport Voice-Enabled Chatbot 🚍🗣️

A bilingual, voice-enabled chatbot built using Streamlit and Gemini API to help users inquire about Telangana's transport services, healthcare facilities, and police services.

## 🚀 Features

- 🎙️ Voice and text input support
- 🚌 Real-time bus route, fare, and schedule info
- 🏥 Nearby hospital and emergency medical services
- 🚓 Police contact info and complaint registration
- 💬 "Ask Anything" AI assistant
- 🔊 Text-to-speech response playback
- 🌐 Gemini (Google) Generative AI integration

## 📁 Project Structure

```
.
├── .env                  # Contains API keys
├── requirements.txt      # Python dependencies
├── new.py                # Main multi-page Streamlit app
├── try.py                # Standalone empathetic voice bot
├── speech.mp3            # Sample/generated TTS output
├── 20140711.CSV.zip      # Sample dataset (not yet used)
├── notebook*.ipynb       # Related Jupyter notebook (not parsed here)
└── src/
    └── helper.py         # Custom voice input/output and AI logic (assumed)
```

## 🔧 Setup

1. **Clone the repository** and navigate into the directory.

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**

   Create a `.env` file (already provided) and add your Gemini API key:

   ```env
   GOOGLE_API_KEY="your-gemini-api-key"
   ```

4. **Run the app:**

   ```bash
   streamlit run new.py
   ```

   Or for the empathetic response bot:

   ```bash
   streamlit run try.py
   ```

## 🎯 Usage

- **Transport Services Page:** Choose a service category and sub-service, then type or speak your query.
- **Ask Anything Page:** Interact freely with an AI-powered chatbot using either voice or text.
- **Output:** You’ll get a response both on-screen and via synthesized voice.

## 📦 Dependencies

Key libraries used:

- `streamlit`
- `google-generativeai`
- `speechrecognition`, `pyttsx3`, `gtts`, `pyaudio`
- `PIL`, `requests`

See `requirements.txt` for the full list.

## 📌 Notes

- Ensure `pyaudio` and microphone permissions are properly set up for voice features.
- The chatbot uses Gemini 2.0 Flash model via Google's API.
- Backend logic like `voice_input()` and `llm_model_object()` is assumed to be in `src/helper.py`.
