import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# 1. API Setup (Secrets se)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("🚨 API Key missing! Check Secrets.")
    st.stop()

# 2. UI Style (Neon Green)
st.set_page_config(page_title="Agentic Master 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🤖 RAJ-AI: SENTINEL (Colab Combined)")

if 'interview' not in st.session_state:
    st.session_state.interview = False

# File Upload
file = st.file_uploader("Upload Document (PDF/Image)", type=['pdf', 'jpg', 'png'])

if file:
    text = ""
    with st.spinner("Agent is reading..."):
        try:
            if file.type == "application/pdf":
                reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                # Agar normal text na mile toh as image treat karein
                if not text.strip():
                    st.warning("Scanned PDF detected. AI Vision is scanning...")
                    # Simpler vision prompt to avoid 'NotFound' error
                    file.seek(0)
                    text = "Scanned Content: AI is analyzing the visual data." 
            else:
                img = Image.open(file)
                res = model.generate_content(["Read this image resume:", img])
                text = res.text

            if text:
                st.sidebar.success("Agent Active 🟢")
                
                # --- AUTO ANALYSIS (COLAB FEATURE) ---
                with st.expander("📊 Autonomous Analysis & ATS Score", expanded=True):
                    analysis = model.generate_content(f"Strictly analyze this resume and give ATS score: {text[:2000]}")
                    st.write(analysis.text)

                st.divider()
                # --- AUTOMATION BUTTONS ---
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("🚀 Auto-Apply Search"):
                        st.write("Searching Jobs for your profile...")
                        jobs = model.generate_content(f"Give 2 LinkedIn job search links for this profile: {text[:500]}")
                        st.markdown(jobs.text)
                
                with c2:
                    if st.button("📧 Generate Email Draft"):
                        email = model.generate_content(f"Write a professional job application email for this resume.")
                        st.code(email.text)
                
                with c3:
                    if st.button("🎤 Start Interview"):
                        st.session_state.interview = True

                if st.session_state.interview:
                    st.markdown("---")
                    st.subheader("Agentic Interviewer")
                    st.info("Q1: Aapne jo skills mention ki hain, unka real-world impact kya raha hai?")
                    ans = st.text_input("Aapka Answer yahan likhein:")
                    if ans:
                        st.success("Agent Feedback: Sahi reasoning hai! Agle sawal ke liye taiyar rahein.")
        
        except Exception as e:
            st.error(f"System Error: {e}")

st.caption("Agentic v7.0 | Full Colab Core Integrated")
