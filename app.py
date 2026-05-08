import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# 1. Google Auth Simulated Setup (For 2026 Speed)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 2. AI Agent Config
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🚨 Gemini API Key missing in Secrets!")

# 3. Acid Green UI
st.set_page_config(page_title="Agentic Master 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; } .card { background: #111; padding: 25px; border-radius: 20px; border: 1px solid #333; }</style>", unsafe_allow_html=True)

# --- LOGIN / SIGNUP PAGE ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>RAJ-AI<span> SENTINEL</span></h1>", unsafe_allow_html=True)
    
    with st.columns([1,2,1])[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔐 Entry Portal")
        
        # Asli Google Login Button ki feeling
        if st.button("🚀 Sign in with Google (Fast Access)"):
            with st.spinner("Authenticating with Google..."):
                time.sleep(1.5)
                st.session_state.logged_in = True
                st.session_state.user_email = "google_user@gmail.com"
                st.rerun()
        
        st.markdown("<p style='text-align:center;'>--- OR ---</p>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        
        if st.button("Login with Credentials"):
            if user == "admin" and pw == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Galti hai bhai!")
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN AGENTIC DASHBOARD (COLAB CORE) ---
else:
    st.sidebar.title("🤖 Agentic Brain")
    st.sidebar.success(f"User: {st.session_state.get('user_email', 'Admin')}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🌐 Universal Agent Dashboard")
    
    file = st.file_uploader("Upload Resume to Begin Automation", type=['pdf'])
    
    if file:
        with st.status("Agent performing Autonomous Task...", expanded=True):
            reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            st.write("✅ Resume Scan Complete")
        
        if text:
            # Colab's Intelligent Analysis
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🧐 AI Intelligence Report")
            analysis_prompt = f"Analyze this resume and give ATS score, 2 errors, and 10 interview questions in Hinglish: {text[:2500]}"
            res = model.generate_content(analysis_prompt)
            st.write(res.text)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Colab's Automation Tools
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🚀 Auto-Find Jobs"):
                    st.info(model.generate_content(f"Give LinkedIn links for: {text[:500]}").text)
            with c2:
                if st.button("🎤 Mock Interview Mode"):
                    st.warning("Agent: Q1 - Aapne jo achievements likhe hain, unka logic samjhao?")
