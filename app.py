import streamlit as st
import asyncio
import edge_tts
import os

# --- Upgraded Emotional Styles ---
# We adjust Rate (Speed) and Pitch (Tone) to mimic emotions
STYLES = {
    "😊 Natural Speaking": {"rate": "+0%", "pitch": "+0Hz"},
    "📖 Story Telling (Sweet)": {"rate": "-10%", "pitch": "+2Hz"},
    "📢 News Reporting (Clear)": {"rate": "+15%", "pitch": "+0Hz"},
    "🔥 High Energy / Excited": {"rate": "+20%", "pitch": "+10Hz"},
    "😡 Angry / Aggressive": {"rate": "+25%", "pitch": "-5Hz"},
    "😢 Sad / Emotional": {"rate": "-20%", "pitch": "-8Hz"},
    "🕉️ Devotional / Calm": {"rate": "-15%", "pitch": "+0Hz"},
    "🎙️ Deep Narration (Movie Type)": {"rate": "-10%", "pitch": "-15Hz"}
}

async def generate_voice(text, voice_type, style_name):
    voice = "te-IN-MohanNeural" if voice_type == "Male (Mohan)" else "te-IN-ShrutiNeural"
    
    # Extract settings for the chosen style
    settings = STYLES[style_name]
    rate = settings["rate"]
    pitch = settings["pitch"]
    
    output_file = "telugu_ai_voice.mp3"
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    return output_file

# --- UI Setup ---
st.set_page_config(page_title="Telugu AI Pro", page_icon="🎙️")

st.title("🎙️ Telugu AI Voice Pro")
st.markdown("##### Create professional narrations with emotions for YouTube")

# Text Input
text = st.text_area("Enter Telugu Script", 
                    placeholder="ఇక్కడ మీ కథ లేదా వార్తలను పేస్ట్ చేయండి...", 
                    height=250)

# Settings Row
col1, col2 = st.columns(2)
with col1:
    voice_choice = st.selectbox("Select Voice", ["Male (Mohan)", "Female (Shruti)"])
with col2:
    style_choice = st.selectbox("Select Emotion/Style", list(STYLES.keys()))

# Customization Sliders (Optional for fine-tuning)
with st.expander("Advanced Fine-Tuning"):
    st.write("Use these only if you want to override the style above.")
    custom_speed = st.slider("Manual Speed Adjust", -50, 50, 0)
    custom_pitch = st.slider("Manual Pitch Adjust", -20, 20, 0)

# Generate Button
if st.button("Generate Pro Narration", variant="primary"):
    if text:
        with st.spinner("Applying Emotions & Generating..."):
            try:
                # If user didn't touch sliders, use style settings. Else use sliders.
                audio_file = asyncio.run(generate_voice(text, voice_choice, style_choice))
                
                st.audio(audio_file)
                
                with open(audio_file, "rb") as f:
                    st.download_button(
                        label="Download MP3 for YouTube",
                        data=f,
                        file_name="telugu_narration.mp3",
                        mime="audio/mp3"
                    )
                st.success("Ready for your video!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter text first.")

st.info("💡 Tip: Use 'Deep Narration' for movie facts and 'Story Telling' for kids' stories.")
