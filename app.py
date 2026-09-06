import streamlit as st
import asyncio
import edge_tts
import os

# --- Upgraded Emotional Styles ---
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

async def generate_voice(text, voice_type, style_name, c_speed, c_pitch):
    voice = "te-IN-MohanNeural" if voice_type == "Male (Mohan)" else "te-IN-ShrutiNeural"
    
    # If sliders are 0, use preset style. If sliders are moved, use sliders.
    if c_speed == 0 and c_pitch == 0:
        rate = STYLES[style_name]["rate"]
        pitch = STYLES[style_name]["pitch"]
    else:
        rate = f"{'+' if c_speed >= 0 else ''}{c_speed}%"
        pitch = f"{'+' if c_pitch >= 0 else ''}{c_pitch}Hz"
    
    output_file = "telugu_ai_voice.mp3"
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    return output_file

# --- UI Setup ---
st.set_page_config(page_title="Telugu AI Pro", page_icon="🎙️")

st.title("🎙️ Telugu AI Voice Pro")
st.markdown("##### Create professional narrations for YouTube")

text = st.text_area("Enter Telugu Script", 
                    placeholder="ఇక్కడ వ్రాయండి...", 
                    height=250)

col1, col2 = st.columns(2)
with col1:
    voice_choice = st.selectbox("Select Voice", ["Male (Mohan)", "Female (Shruti)"])
with col2:
    style_choice = st.selectbox("Select Emotion/Style", list(STYLES.keys()))

with st.expander("Advanced Fine-Tuning"):
    st.write("Use sliders to override the Style settings.")
    custom_speed = st.slider("Manual Speed Adjust (%)", -50, 50, 0)
    custom_pitch = st.slider("Manual Pitch Adjust (Hz)", -20, 20, 0)

# FIXED: Changed variant="primary" to type="primary"
if st.button("Generate Pro Narration", type="primary"):
    if text:
        with st.spinner("Generating..."):
            try:
                audio_file = asyncio.run(generate_voice(text, voice_choice, style_choice, custom_speed, custom_pitch))
                st.audio(audio_file)
                with open(audio_file, "rb") as f:
                    st.download_button(
                        label="Download MP3",
                        data=f,
                        file_name="telugu_narration.mp3",
                        mime="audio/mp3"
                    )
                st.success("Audio Created Successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text first.")
