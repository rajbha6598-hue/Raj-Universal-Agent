import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# --- 1. SUPER-AGENT CONFIG ---
st.set_page_config(page_title="Raj-AI Sentinel 2026", layout="wide")

# Theme
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: 'Courier New', monospace; } .card { background: #111; padding: 25px; border-radius: 20px; border: 1px solid #deff9a; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# Sidebar Config
st.sidebar.title("🧠 Agentic Brain")
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if user_key:
    try:
        genai.configure(api_key=user_key)
        # Using the High-Level model from your Colab
        model = genai.GenerativeModel('gemini-2.5-flash') 
        st.sidebar.success("Sentinel Core: Online 🟢")
    except:
        st.sidebar.error("Invalid Key!")

# --- 2. LOGIN GATEWAY ---
if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: SECURE ACCESS")
    with st.columns([1,2,1])[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize Link"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 3. FULL-FLEDGE AGENTIC DASHBOARD ---
else:
    st.title("🌐 UNIVERSAL AGENTIC COMMAND CENTER")
    
    if not user_key:
        st.warning("👈 Pehle Sidebar mein Nayi API Key dalo!")
    else:
        file = st.file_uploader("Upload Resume (PDF/JPG/PNG)", type=['pdf', 'jpg', 'png'])

        if file:
            file_bytes = file.read()
            text_content = ""
            
            # --- PHASE 1: FORENSIC EXTRACTION ---
            with st.status("🕵️ Agent is Scanning Document...") as status:
                if file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                    text_content = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                    
                    # Colab Logic: If PDF is scanned/image, use Vision
                    if not text_content.strip():
                        st.write("Vision Core Activated: Reading pixels...")
                        res = model.generate_content(["Extract every single detail from this resume:", {"mime_type": "application/pdf", "data": file_bytes}])
                        text_content = res.text
                else:
                    img = Image.open(io.BytesIO(file_bytes))
                    res = model.generate_content(["Analyze this resume image deeply:", img])
                    text_content = res.text
                
                status.update(label="Scanning Complete! ✅", state="complete")

            # --- PHASE 2: COLAB MODULES INTEGRATION ---
            if text_content:
                st.markdown("---")
                
                # Module 1: Resume Forensic (Colab Logic)
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.subheader("📊 Advanced Resume Forensic Report")
                forensic_prompt = f"""
                Analyze this resume as a Senior HR Expert: {text_content[:3000]}
                Provide:
                1. ATS Compatibility Score (0-100).
                2. Top 3 Strengths & 3 Critical Areas to improve.
                3. Best Matching Job Roles (at least 3).
                4. Professional Summary for LinkedIn.
                Hinglish mein detailed jawab do.
                """
                with st.spinner("AI is performing Deep Analysis..."):
                    report = model.generate_content(forensic_prompt)
                    st.markdown(report.text)
                st.markdown("</div>", unsafe_allow_html=True)

                # Module 2: Job Hunter & Interview Prep
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("🚀 Job Hunter")
                    if st.button("Find Best Matches"):
                        job_prompt = f"Based on this resume: {text_content[:500]}, give 5 direct LinkedIn and Indeed job search titles and links."
                        jobs = model.generate_content(job_prompt)
                        st.write(jobs.text)
                    st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("🎤 Interview Lab")
                    if st.button("Get 10 Expert Questions"):
                        q_prompt = f"Generate 10 tough interview questions for this person: {text_content[:1000]}"
                        questions = model.generate_content(q_prompt)
                        st.write(questions.text)
                    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Raj-AI Sentinel v18.0 | Colab-Ported Logic | 2026")
