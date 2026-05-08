import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# 1. API Config
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🚨 API Key missing in Secrets!")

# 2. Acid Green UI
st.set_page_config(page_title="Raj-AI Sentinel 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; } .card { background: #111; padding: 25px; border-radius: 20px; border: 1px solid #333; }</style>", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>RAJ-AI<span> SENTINEL</span></h1>", unsafe_allow_html=True)
    with st.columns([1,2,1])[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔐 Entry Portal")
        if st.button("🚀 Continue with Google"):
            with st.spinner("Connecting to Google Account..."):
                time.sleep(1.5)
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("<p style='text-align:center;'>--- OR ---</p>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and pw == "2026":
                st.session_state.logged_in = True
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- AGENTIC DASHBOARD ---
else:
    st.title("🌐 Universal Agent Dashboard")
    file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    if file:
        with st.status("Agent Scanning..."):
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
        if text:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🧐 AI Intelligence Report")
            res = model.generate_content(f"Analyze this resume and give 10 interview questions in Hinglish: {text[:2000]}")
            st.write(res.text)
            st.markdown("</div>", unsafe_allow_html=True)
