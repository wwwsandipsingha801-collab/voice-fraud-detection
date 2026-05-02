import streamlit as st
import requests
import sounddevice as sd
import soundfile as sf
import tempfile
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Voice Fraud Detection", layout="centered")

API_URL = "http://127.0.0.1:8000/analyze"

# ------------------ CSS ------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #000000, #2b0000);
    color: white;
}

h1 {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #ffffff;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ff1a1a, #990000);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #ff3333, #660000);
}

/* Hide footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1>Voice Fraud Detection System</h1>", unsafe_allow_html=True)
st.markdown("### Detect real vs fake voice instantly")

# ------------------ MODE SELECT ------------------
mode = st.radio("Choose Mode", ["Upload Mode", "Live Detection Mode"])

# =================================================
# 🔹 UPLOAD MODE
# =================================================
if mode == "Upload Mode":

    uploaded = st.file_uploader("Upload .wav audio", type=["wav"])

    if uploaded:
        st.audio(uploaded, format="audio/wav")

        if st.button("🔍 Analyze Voice"):

            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress.progress(i + 1)

            try:
                res = requests.post(API_URL, files={"file": uploaded})
                result = res.json()

                # ✅ UPDATED LOGIC
                if result["result"] == "Real Voice":
                    st.success("✅ Real Voice Detected")
                    st.balloons()

                elif result["result"] == "Fake Voice":
                    st.error("🚨 Fake Voice Detected")
                    st.warning("⚠️ Possible Fraud Attempt!")

                else:
                    st.warning("⚠️ Suspicious Voice Detected")

            except:
                st.error("❌ Backend server not running!")

# =================================================
# 🔹 LIVE DETECTION MODE
# =================================================
elif mode == "Live Detection Mode":

    duration = st.slider("Recording Duration (seconds)", 2, 10, 3)

    if st.button("🎤 Start Live Detection"):

        st.info("🎙️ Recording... Speak now")

        fs = 22050
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(temp_file.name, recording, fs)

        st.audio(temp_file.name)

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        try:
            res = requests.post(API_URL, files={"file": open(temp_file.name, "rb")})
            result = res.json()

            # ✅ UPDATED LOGIC
            if result["result"] == "Real Voice":
                st.success("✅ Real Voice Detected (Live)")
                st.balloons()

            elif result["result"] == "Fake Voice":
                st.error("🚨 Fake Voice Detected (Live)")
                st.warning("⚠️ Possible Fraud Attempt!")

            else:
                st.warning("⚠️ Suspicious Voice Detected (Live)")

        except:
            st.error("❌ Backend server not running!")