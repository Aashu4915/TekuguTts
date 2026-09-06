import streamlit as st
import asyncio
import edge_tts
import os

# Define Styles
STYLES = {
    "Natural Speaking": {"rate": "+0%", "pitch": "+0Hz"},
    "Story Telling": {"rate": "-10%", "pitch": "+2Hz"},
    "News Reporting": {"rate": "+15%", "pitch": "+0Hz"},
    "Documentary": {"rate": "-5%", "pitch": "-3Hz"}
}

async def generate_voice(text, voice_type, style):
    voice = "te-IN-MohanNeural" if voice_type == "Male" else "te-IN-ShrutiNeural"
    rate = STYLES[style]["rate"]
    pitch = STYLES[style]["pitch"]
    output_file = "voice.mp3"
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    return output_file

st.title("🎙️ Telugu AI Voice")

text = st.text_area("Enter Telugu Text", placeholder="ఇక్కడ వ్రాయండి...", height=200)
col1, col2 = st.columns(2)
with col1:
    voice_choice = st.selectbox("Voice", ["Male", "Female"])
with col2:
    style_choice = st.selectbox("Style", list(STYLES.keys()))

if st.button("Generate Audio"):
    if text:
        with st.spinner("Generating..."):
            audio_file = asyncio.run(generate_voice(text, voice_choice, style_choice))
            st.audio(audio_file)
            with open(audio_file, "rb") as f:
                st.download_button("Download Audio", f, file_name="telugu_narration.mp3")
    else:
        st.warning("Please enter some text.")
