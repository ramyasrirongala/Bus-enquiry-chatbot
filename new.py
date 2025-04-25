import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import traceback
import base64
from PIL import Image
import requests
from gtts import gTTS
import os
from src.helper import voice_input, llm_model_object, text_to_speech

# Background image URLs
BACKGROUND_IMAGES = {
    'Bus Services': 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?q=80&w=2069&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'Hospitals': 'https://plus.unsplash.com/premium_photo-1673988726931-127584121c34?q=80&w=1964&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'Police Services': 'https://images.unsplash.com/photo-1517913451214-e22ce660e086?q=80&w=1946&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    'Ask Anything': 'https://images.unsplash.com/photo-1517842645767-c639042777db?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
}

def set_background(image_url):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("{image_url}");
                    background-size: cover;
                    background-attachment: fixed;
                    background-position: center;
                }}
                .main {{
                    background-color: rgba(255,255,255,0.7);
                    padding: 2rem;
                    border-radius: 1rem;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
    except:
        pass

class TelanganaTransportChatbot:
    def __init__(self, gemini_api_key):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

        self.categories = {
            '🚍Bus Services': [
                '🛣️Bus routes',
                '⌛Bus Timings',
                '🎫Ticket Booking',
                '💰Fare Enquiry'
            ],
            '🏥Hospitals': [
                '🦺Emergency Services',
                '🩺Nearest Hospital',
                '📞Medical Helpline'
            ],
            '👮Police Services': [
                '📱Emergency Contacts',
                '🧑‍💻Complaint Registration',
                '🔐Safety Tips',
                '🚨Lost and Found'
            ]
        }

        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
        except Exception as e:
            st.error(f"Text-to-Speech error: {e}")

        self.recognizer = sr.Recognizer()

    def generate_chatbot_response(self, query, category):
        if not query:
            return "Please provide a valid query."

        main_category, subcategory = category.split(" - ")

        if main_category == '🚍Bus Services':
            if subcategory == '🛣️Bus routes':
                prompt = f"Provide ONLY the bus route between locations in: '{query}'. Format: Origin → Stop1 → Stop2 →stop3→ Stop4 →Stop5 → Stop6 → Stop7 → Stop8 → Stop9 → Destination. with only distances, no extra text."
            elif subcategory == '⌛Bus Timings':
                prompt = f"Provide ONLY bus timings between locations in: '{query}'. Format: First Bus: XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, XX:XX AM/PM, Last Bus: XX:XX AM/PM, Frequency: Every XX mins. Nothing else."
            elif subcategory == '🎫Ticket Booking':
                return "1. https://www.tsrtconline.in\n2. https://www.redbus.in"
            elif subcategory == '💰Fare Enquiry':
                prompt = f"Provide ONLY fare amounts for: '{query}'. Format: Standard: ₹XXX, Deluxe: ₹XXX. No explanations."

        elif main_category == '🏥Hospitals':
            prompt = f"Provide minimal hospital information for: '{query}'. Maximum 200 words with addresses and numbers. No introductions."

        elif main_category == 'Police Services':
            prompt = f"Provide minimal police information for: '{query}'. Maximum 200 words with contact and address. No extra details."

        try:
            if subcategory == 'Ticket Booking':
                return "1. https://www.tsrtconline.in\n2. https://www.redbus.in"

            response = self.model.generate_content(prompt)
            return ' '.join(response.text.strip().split()[:50])
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def speech_to_text(self):
        try:
            text = voice_input()
            if text:
                st.success(f"Recognized: {text}")
                return text.strip()
            else:
                st.warning("Could not understand audio")
                return ""
        except Exception as e:
            st.error(f"Voice input error: {str(e)}")
            return ""

def validate_query(query, selected_category):
    if not query:
        st.warning("Please enter a query")
        return False
    if selected_category == 'Bus Services' and 'to' not in query.lower():
        st.warning("For bus routes, use 'Origin to Destination' format")
        return False
    return True

def transport_page():
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY")
    chatbot = TelanganaTransportChatbot(GEMINI_API_KEY)

    st.title("🚏🕴️ Bus Enquiry Chatbot  🚌")
    selected_category = st.selectbox(
        "Select Service Category", 
        list(chatbot.categories.keys())
    )

    set_background(BACKGROUND_IMAGES.get(selected_category, BACKGROUND_IMAGES['Bus Services']))

    selected_subcategory = st.selectbox(
        "Select Specific Service", 
        chatbot.categories[selected_category]
    )

    user_query = st.text_input(f"Your query about {selected_subcategory}")

    if st.button("🎧Get Support😊"):
        if validate_query(user_query, selected_category):
            with st.spinner("Processing..."):
                response = chatbot.generate_chatbot_response(
                    user_query, 
                    f"{selected_category} - {selected_subcategory}"
                )
                st.markdown("### 🤖 Assistant Response")
                st.info(response)
        else:
            st.warning("Please enter a valid query")

    st.markdown("---")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("#### 🚌 Bus Services")
        st.write("- Route Maps")
        st.write("- Bus Timing")
        st.write("- Fares")
    with cols[1]:
        st.markdown("#### 🏥 Healthcare")
        st.write("- Emergency")
        st.write("- Hospital Info")
        st.write("- Helplines")
    with cols[2]:
        st.markdown("#### 🚔 Safety")
        st.write("- Police Contacts")
        st.write("- Complaints")
        st.write("- Safety Tips")

def ask_anything_page():
    st.title("💬 Ask Anything Chat")
    set_background(BACKGROUND_IMAGES['Ask Anything'])

    input_method = st.radio("How would you like to chat?", ["Text", "Voice"])

    user_input = ""
    if input_method == "Text":
        user_input = st.text_input("Type your message here...", key="text_input")
    else:
        if st.button("🎤 Speak your message"):
            user_input = voice_input()
            if user_input:
                st.text_input("Type your message here...", value=user_input, key="voice_input")

    if user_input:
        with st.spinner("Thinking of a response..."):
            response = llm_model_object(user_input)
            st.markdown("### 🤖 Response")
            st.success(response)

            text_to_speech(response)
            audio_file = open("speech.mp3", "rb")
            audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="Download Response",
                data=audio_bytes,
                file_name="response.mp3",
                mime="audio/mp3"
            )

def main():
    st.set_page_config(
        page_title="Bus enquiry chatbot",
        page_icon="🤖",
        layout="wide"
    )

    page = st.radio("", ["Transport Services", "Ask Anything Chat"], horizontal=True)

    if page == "Transport Services":
        transport_page()
    elif page == "Ask Anything Chat":
        ask_anything_page()

if __name__ == "__main__":
    main()
