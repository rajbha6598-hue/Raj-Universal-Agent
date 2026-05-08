import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# 1. BRAIN CONFIGURATION (Colab Verified)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Using the exact same 2.5 Flash model from your Colab
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"🚨 API Key Connection Failed: {e}")
    st.stop()

# 2. AGENTIC UI THEME
st.set_page_config(page_title="Raj-AI: Full Sentinel", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; font-family: 'Courier New', monospace; }
    .stButton>button { background: #deff9a !important; color: #000 !important; font-weight: bold; border-radius: 10px; }
    .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION MANAGEMENT (Strict Auth)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: SECURE LOGIN")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize Link"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
else:
    # --- FULL-FLEDGE AGENT DASHBOARD ---
    st.sidebar.title("🧠 Agentic Logic Flow")
    logs = st.sidebar.empty()
    logs.info("System: Awaiting Document...")

    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("🌐 UNIVERSAL AGENTIC COMMAND CENTER")
    
    file = st.file_uploader("Upload Resume (PDF/Image)", type=['pdf', 'png', 'jpg'])

    if file:
        logs.warning("System: Deep Scanning...")
        text = ""
        
        # COLAB CORE: Forensic Extraction
        file_bytes = file.read()
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            # Vision Fallback for Scanned PDF (Colab v8 Logic)
            if not text.strip():
                st.warning("Vision Core Active: Scanning Scanned PDF...")
                res = model.generate_content(["Scan this document text:", {"mime_type": "application/pdf", "data": file_bytes}])
                text = res.text
        else:
            img = Image.open(io.BytesIO(file_bytes))
            res = model.generate_content(["Analyze this resume image:", img])
            text = res.text

        if text:
            logs.success("System: Data Parsed ✅")
            
            # --- PHASE 1: AUTONOMOUS ANALYSIS ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📊 Forensic Resume Report")
            analysis_prompt = f"""
            Analyze this resume forensicly: {text[:3000]}
            1. ATS Score (0-100).
            2. Top 3 Critical Errors & Fixes.
            3. Best Job Role (Decision).
            4. 10 Expert Interview Questions for this role.
            Respond in professional Hinglish.
            """
            with st.spinner("Agentic Reasoning in progress..."):
                response = model.generate_content(analysis_prompt)
                st.markdown(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- PHASE 2: COLAB AUTOMATION TOOLS ---
            st.divider()
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.subheader("🚀 Job Hunter")
                if st.button("Find Best Matches"):
                    with st.spinner("Scraping Portals..."):
                        jobs = model.generate_content(f"Give 3 LinkedIn/Indeed search links for: {text[:500]}")
                        st.write(jobs.text)
            
            with col2:
                st.subheader("📧 Comms Hub")
                if st.button("Generate Email Draft"):
                    email = model.generate_content(f"Write a professional application email for this profile.")
                    st.code(email.text)
            
            with col3:
                st.subheader("🎤 Interview Lab")
                if st.button("Start Mock Interview"):
                    st.info("Agent: 'Aapne jo CRM experience likha hai, use sales growth ke saath kaise link karenge?'")
                    ans = st.text_input("Aapka Jawab:")
                    if ans: st.success("Feedback: Solid Point! Par metrics bhi add karein.")

st.caption("Raj-AI v10.0 | Full-Fledge Agentic Core | 2026 Edition")
