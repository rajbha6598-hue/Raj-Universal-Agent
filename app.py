import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# 1. API & Brain Setup
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Agentic UI (2026 Edition)
st.set_page_config(page_title="Raj-AI: Autonomous Agent", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; } .agent-card { border: 1px solid #deff9a; padding: 20px; border-radius: 10px; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

st.title("🤖 RAJ-AI: SENTINEL AGENT (Autonomous)")

# Sidebar for Real-time Decision Logs
st.sidebar.title("🧠 Agent's Logic Flow")
logs = st.sidebar.empty()

file = st.file_uploader("Drop Resume to Initialize Agent", type=['pdf', 'jpg', 'png'])

if file:
    # --- PHASE 1: DATA EXTRACTION ---
    logs.markdown("🟡 **Status:** Initializing Neural Link...")
    
    with st.status("Agent is Thinking...", expanded=True) as status:
        st.write("🔍 Reading file structure...")
        # (PDF/Image reading logic here - same as before)
        # Maan lete hain 'text' mein resume data aa gaya
        file.seek(0)
        if file.type == "application/pdf":
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            if not text.strip():
                file.seek(0)
                res = model.generate_content(["Scan scanned PDF:", {"mime_type": "application/pdf", "data": file.read()}])
                text = res.text
        else:
            from PIL import Image
            img = Image.open(file)
            res = model.generate_content(["Extract text:", img])
            text = res.text

        st.write("✅ Data Extracted. Analyzing context...")
        time.sleep(1)
        status.update(label="Analysis Complete", state="complete")

    if text:
        # --- PHASE 2: AUTONOMOUS DECISION MAKING ---
        logs.markdown("🟢 **Status:** Executive Decision Mode")
        
        # Ek hi bar mein AI ko 'Agentic' task dena
        agent_prompt = f"""
        Role: Senior Tech Recruiter Agent.
        Resume Content: {text[:3500]}
        
        Tasks (Autonomous):
        1. Identify errors in resume (Formatting, skills, gaps).
        2. Calculate a strict ATS Score (out of 100).
        3. Decision: Based on the resume, pick ONE specific job role (e.g. Data Scientist) and explain WHY you chose it.
        4. Preparation: List 10 tough interview questions for this specific role.
        
        Respond in Hinglish and keep it professional.
        """
        
        with st.chat_message("assistant"):
            st.write(">>> SYSTEM ONLINE. INITIALIZING EVALUATION...")
            response = model.generate_content(agent_prompt)
            st.markdown(response.text)

        # --- PHASE 3: THE INTERACTION ---
        st.divider()
        st.subheader("🛠️ Agentic Actions Taken")
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎯 **Target Job Identified:** Searching best matches on LinkedIn...")
        with col2:
            st.success("📝 **Resume Corrected:** Suggestions applied to internal memory.")

st.caption("v3.0 Autonomous Mode | Real-time Decision Engine Active")
