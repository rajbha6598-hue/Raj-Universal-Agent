import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; } .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

# --- 2. API & AUTH ---
if 'auth' not in st.session_state: st.session_state.auth = False
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: LOGIN")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize Link"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
else:
    st.title("🌐 UNIVERSAL COMMAND CENTER")
    if not user_key:
        st.warning("👈 Sidebar mein Gemini API Key dalo!")
    else:
        genai.configure(api_key=user_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        file = st.file_uploader("Upload Resume (PDF/Image)", type=['pdf', 'jpg', 'png'])
        
        if file:
            text = ""
            with st.status("Agent Scanning Document (Deep Vision)..."):
                file_bytes = file.read()
                if file.type == "application/pdf":
                    # Pehle text nikalne ki koshish
                    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                    text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                    
                    # AGENTIC FIX: Agar text blank hai toh AI Vision use karo
                    if not text.strip():
                        st.write("🔍 Scanned PDF detected. Triggering AI Vision...")
                        res = model.generate_content(["Is resume ko scan karke pura text nikalo:", {"mime_type": "application/pdf", "data": file_bytes}])
                        text = res.text
                else:
                    # Agar image upload ki hai
                    img = Image.open(io.BytesIO(file_bytes))
                    res = model.generate_content(["Analyze this resume image:", img])
                    text = res.text
            
            if text:
                st.success("Document Scanned Successfully!")
                st.markdown("### 🧠 Agentic Intelligence Report")
                
                # --- PHASE 2: COLAB CORE LOGIC ---
                prompt = f"Analyze this resume: {text[:3000]}. Give ATS Score (0-100), 2 major mistakes, and 10 interview questions in Hinglish."
                try:
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    # Action Tools
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🚀 Search Jobs"):
                            jobs = model.generate_content(f"Give LinkedIn links for: {text[:500]}")
                            st.write(jobs.text)
                    with c2:
                        if st.button("📧 Write Email"):
                            email = model.generate_content(f"Write a job email for this profile.")
                            st.code(email.text)
                except Exception as e:
                    st.error(f"AI Error: {e}")

st.caption("Universal Agent v15.0 | Deep Vision Enabled | 2026 Edition")
