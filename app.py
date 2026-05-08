import streamlit as st
import google.generativeai as genai
import pandas as pd
import PyPDF2
import io
from PIL import Image

# --- 1. UI THEME ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; } .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; }</style>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False

# Sidebar
st.sidebar.title("🔐 Agent Config")
user_key = st.sidebar.text_input("Gemini API Key", type="password")
if user_key:
    genai.configure(api_key=user_key)
    model = genai.GenerativeModel('gemini-1.5-flash') # Hyper-fast model
    st.sidebar.success("Brain Connected 🟢")

# --- 2. LOGIN ---
if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Access System"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied!")
else:
    # --- 3. DASHBOARD ---
    st.title("🌐 UNIVERSAL COMMAND CENTER")
    file = st.file_uploader("Upload: PDF, Excel, or Image", type=['pdf', 'xlsx', 'csv', 'png', 'jpg'])

    if file and user_key:
        file_ext = file.name.split('.')[-1].lower()
        
        with st.status("🚀 Agentic Processing...") as status:
            file_bytes = file.read()
            
            # --- CASE A: EXCEL (Ultra Fast) ---
            if file_ext in ['xlsx', 'csv']:
                df = pd.read_excel(file) if file_ext != 'csv' else pd.read_csv(file)
                st.dataframe(df.head(5))
                prompt = f"Tu Data Analyst hai. Is data ke 3 trends bata Hinglish mein: {df.describe().to_string()}"
                response = model.generate_content(prompt)
                st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)

            # --- CASE B: PDF & IMAGE (Single-Shot Vision) ---
            else:
                # Prompt jo AI ko seedha report dene ko kahega
                analysis_prompt = "Tu ek Universal Expert Agent hai. Is resume/doc ko scan kar aur seedha ye report de (Hinglish): 1. ATS Score, 2. Top 3 Skills, 3. 10 Interview Questions. Short and crisp rakho."
                
                try:
                    if file_ext == 'pdf':
                        # Pehle text nikalne ki koshish (If not scanned, it's instant)
                        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                        
                        if text.strip():
                            st.write("📄 Text Mode: Processing instantly...")
                            response = model.generate_content([analysis_prompt, text])
                        else:
                            st.write("🔍 Vision Mode: Scanning Scanned PDF (Wait 10-15s)...")
                            response = model.generate_content([analysis_prompt, {"mime_type": "application/pdf", "data": file_bytes}])
                    else:
                        st.write("🖼️ Image Mode: Analyzing...")
                        img = Image.open(io.BytesIO(file_bytes))
                        response = model.generate_content([analysis_prompt, img])

                    status.update(label="Analysis Ready ✅", state="complete")
                    st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {e}")

st.caption("Raj-AI v16.0 | Single-Shot Logic | 2026")
