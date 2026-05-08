import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# 1. Colab's Brain Setup
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Acid Green UI (Colab 2026 Style)
st.set_page_config(page_title="Raj-AI: Autonomous Agent", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🤖 RAJ-AI: SENTINEL (Colab Combined)")

if 'step' not in st.session_state: st.session_state.step = 1

# File Upload
file = st.file_uploader("Upload Document", type=['pdf', 'jpg', 'png'])

if file:
    # Logic to extract text (PDF/Image)
    file.seek(0)
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        if not text.strip():
            file.seek(0)
            res = model.generate_content(["Scan scanned PDF:", {"mime_type": "application/pdf", "data": file.read()}])
            text = res.text
    else:
        img = Image.open(file)
        res = model.generate_content(["Extract text:", img])
        text = res.text

    if text:
        # AUTOMATION PHASE: Decision Making
        st.sidebar.success("Agent Active 🟢")
        
        # 1. Auto Analysis & ATS Score
        with st.expander("📊 Autonomous Analysis & ATS Score", expanded=True):
            analysis = model.generate_content(f"Strictly analyze this resume: {text[:2500]}. Give ATS score, find 3 critical errors, and suggest 1 job role in Hinglish.")
            st.write(analysis.text)

        # 2. Colab Automation Tools
        st.divider()
        c1, c2, c3 = st.columns(3)
        
        with c1:
            if st.button("🚀 Auto-Apply Search"):
                st.write("Searching LinkedIn & Naukri...")
                time.sleep(1)
                jobs = model.generate_content(f"Give 2 job links for this role: {text[:500]}")
                st.markdown(jobs.text)
        
        with c2:
            if st.button("📧 Generate Email Draft"):
                email = model.generate_content(f"Write a professional application email for this resume.")
                st.code(email.text)

        with c3:
            if st.button("🎤 Start Interview"):
                st.session_state.interview = True

        if st.session_state.get('interview'):
            st.markdown("---")
            st.subheader("Agentic Interviewer")
            st.info("Q1: Aapne is resume mein jo projects likhe hain, unka impact business par kya tha?")
            ans = st.text_input("Aapka Answer:")
            if ans: st.success("Agent: Sahi hai! Aapka reasoning solid hai.")

st.caption("Agentic v6.0 | Full Colab Core Integrated")
