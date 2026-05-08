import streamlit as st
import google.generativeai as genai
import pandas as pd
import PyPDF2
import io
import time
from PIL import Image

# --- 1. THEME & BRAIN CONFIG (2.5 FLASH) ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; } .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; }</style>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# Sidebar Key Handling
st.sidebar.title("🔐 Agent Config")
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if user_key:
    try:
        genai.configure(api_key=user_key)
        # UPDATED: Using the same model that worked in your Colab
        model = genai.GenerativeModel('gemini-2.5-flash')
        st.sidebar.success("Brain Connected (v2.5) 🟢")
    except:
        st.sidebar.error("Invalid API Key!")

# --- 2. LOGIN GATE ---
if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Access Dashboard"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied!")
else:
    # --- 3. UNIVERSAL DASHBOARD ---
    st.title("🌐 UNIVERSAL COMMAND CENTER")
    
    if not user_key:
        st.warning("👈 Bhai, Sidebar mein Nayi API Key dalo pehle!")
    else:
        file = st.file_uploader("Upload Document (PDF, Image, Excel)", type=['pdf', 'xlsx', 'csv', 'png', 'jpg'])

        if file:
            file_ext = file.name.split('.')[-1].lower()
            file_bytes = file.read()
            
            # --- AGENTIC PROCESSING ---
            with st.spinner("AI Brain is Scanning... (Scanned PDF may take 20s)"):
                try:
                    # Logic for Excel
                    if file_ext in ['xlsx', 'csv']:
                        df = pd.read_excel(file) if file_ext != 'csv' else pd.read_csv(file)
                        st.dataframe(df.head(5))
                        res = model.generate_content(f"Analyze this data trends: {df.describe().to_string()}")
                        st.markdown(f"<div class='card'>{res.text}</div>", unsafe_allow_html=True)

                    # Logic for PDF/Images (Single Call Optimization)
                    else:
                        analysis_prompt = "Tu ek Universal Career Agent hai. Is document ko deeply scan kar aur Hinglish mein bata: 1. ATS Score (0-100), 2. Top 3 Skills, 3. 10 Interview Questions. Short and clear answer do."
                        
                        if file_ext == 'pdf':
                            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                            
                            if text.strip():
                                response = model.generate_content([analysis_prompt, text])
                            else:
                                # OCR for Scanned PDF
                                response = model.generate_content([analysis_prompt, {"mime_type": "application/pdf", "data": file_bytes}])
                        else:
                            img = Image.open(io.BytesIO(file_bytes))
                            response = model.generate_content([analysis_prompt, img])

                        st.success("Scanning Complete! ✅")
                        st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

st.caption("Raj-AI v17.0 | 2.5-Flash Core | 2026")
