import streamlit as st
import google.generativeai as genai
import pandas as pd
import PyPDF2
import io
import time
from PIL import Image

# --- 1. UI THEME & AGENTIC STYLING ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; font-family: 'Courier New', monospace; }
    .card { background: #111; padding: 25px; border-radius: 20px; border: 1px solid #deff9a; margin-bottom: 20px; }
    .stButton>button { background: #deff9a !important; color: #000 !important; font-weight: bold; border-radius: 50px; width: 100%; }
    .stTextInput>div>div>input { background-color: #111 !important; color: #deff9a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION & AUTH ---
if 'auth' not in st.session_state: st.session_state.auth = False

# Sidebar for API Configuration (Universal usage)
st.sidebar.title("🔐 Agent Config")
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password", help="Get your key from Google AI Studio")

if user_key:
    genai.configure(api_key=user_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.sidebar.success("AI Brain Connected 🟢")
else:
    st.sidebar.warning("API Key Required for AI Ops")

# --- 3. LOGIN GATE ---
if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: SECURE ACCESS")
    with st.columns([1,2,1])[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize System"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 4. UNIVERSAL COMMAND CENTER (THE MAIN APP) ---
else:
    st.title("🌐 UNIVERSAL AGENTIC DASHBOARD")
    st.caption("Supports: Excel (.xlsx, .csv) | PDF | Images (Resume/Docs)")

    if not user_key:
        st.error("👈 Bhai, pehle sidebar mein apni API Key dalo!")
        st.stop()

    file = st.file_uploader("Upload Document for Intelligence Analysis", type=['pdf', 'xlsx', 'csv', 'png', 'jpg', 'jpeg'])

    if file:
        file_ext = file.name.split('.')[-1].lower()
        extracted_text = ""
        
        with st.status("Agent Processing File...") as status:
            try:
                # --- EXCEL / CSV HANDLER ---
                if file_ext in ['xlsx', 'csv', 'xls']:
                    st.write("📊 Reading Data Table...")
                    df = pd.read_excel(file) if file_ext != 'csv' else pd.read_csv(file)
                    st.dataframe(df.head(10)) # Show preview
                    extracted_text = f"Analyze this data summary: {df.describe().to_string()} and top rows: {df.head(5).to_string()}"
                
                # --- PDF HANDLER (Text + Vision) ---
                elif file_ext == 'pdf':
                    st.write("📄 Scanning PDF Layers...")
                    file_bytes = file.read()
                    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                    extracted_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                    
                    if not extracted_text.strip():
                        st.write("🔍 OCR Active: Reading Scanned PDF...")
                        res = model.generate_content(["Scan this document text:", {"mime_type": "application/pdf", "data": file_bytes}])
                        extracted_text = res.text
                
                # --- IMAGE HANDLER ---
                elif file_ext in ['png', 'jpg', 'jpeg']:
                    st.write("🖼️ Visual Processing Active...")
                    img = Image.open(file)
                    res = model.generate_content(["Deeply analyze this image/document and explain everything in it:", img])
                    extracted_text = res.text
                
                status.update(label="Scanning Complete!", state="complete")
            except Exception as e:
                st.error(f"Error reading file: {e}")
                st.stop()

        # --- AI INTELLIGENCE OUTPUT ---
        if extracted_text:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🧠 Agentic Intelligence Report")
            
            # Smart Prompt based on file type
            if file_ext in ['xlsx', 'csv']:
                prompt = f"Tu ek Data Analyst Agent hai. Is data ko analyze kar aur 3 trends aur 2 business advice de Hinglish mein: {extracted_text}"
            else:
                prompt = f"Tu ek Universal Expert Agent hai. Is document/image ko analyze kar aur 5 bullet points mein summary aur 10 interview questions de (Hinglish): {extracted_text[:3000]}"
            
            with st.spinner("AI Brain Thinking..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

            # --- EXTRA TOOLS ---
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚀 Draft Professional Email"):
                    res = model.generate_content(f"Write a professional email based on this info: {extracted_text[:1000]}")
                    st.code(res.text)
            with c2:
                if st.button("🎤 Start Mock Interview"):
                    st.info("Agent: 'Bataiye, aapne is document mein jo skills mention ki hain, unka real-world use case kya hai?'")

st.sidebar.markdown("---")
if st.sidebar.button("System Logout"):
    st.session_state.auth = False
    st.rerun()
