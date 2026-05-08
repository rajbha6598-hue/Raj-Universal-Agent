import streamlit as st
import google.generativeai as genai
import time
import PyPDF2
import io

# 1. API Setup
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🚨 API Key missing in Secrets!")

# 2. UI Styling
st.set_page_config(page_title="Agentic 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; }</style>", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN LOGIC ---
if not st.session_state.logged_in:
    st.title("🤖 RAJ-AI SENTINEL")
    with st.columns([1,2,1])[1]:
        st.subheader("🔐 Access Portal")
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Enter Dashboard"):
            if user == "admin" and pw == "2026": # Aapka password
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials!")
        
        st.markdown("---")
        if st.button("🚀 Continue with Google"):
            st.info("Simulating Google Auth...")
            time.sleep(1)
            st.session_state.logged_in = True
            st.rerun()

# --- AGENTIC DASHBOARD (COLAB POWER) ---
else:
    st.sidebar.success("System: Online 🟢")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🌐 Universal Agent Dashboard")
    file = st.file_uploader("Upload Resume", type=['pdf'])
    
    if file:
        with st.status("Agent Scanning..."):
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        
        if text:
            st.markdown("### 🧠 AI Intelligence Report")
            res = model.generate_content(f"Analyze this resume and give 10 interview questions: {text[:2000]}")
            st.write(res.text)
