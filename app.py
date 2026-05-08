import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Agentic 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #f8fafc; }
    .stButton>button { background-color: #deff9a !important; color: #000 !important; border-radius: 50px !important; font-weight: bold; width: 100%; }
    .google-btn>button { background-color: #ffffff !important; color: #000 !important; border: 1px solid #ddd !important; }
    .card { background-color: #111; padding: 20px; border-radius: 20px; border: 1px solid #222; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE FOR AUTH ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'auth_mode' not in st.session_state: st.session_state.auth_mode = "Login"

def login_signup_page():
    st.markdown("<h1 style='text-align: center; color:#deff9a;'>AGENTIC<span>2026</span></h1>", unsafe_allow_html=True)
    
    with st.columns([1,2,1])[1]:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "Login":
            st.subheader("🔐 Secure Entry")
            user = st.text_input("Email or Username")
            pw = st.text_input("Password", type="password")
            
            if st.button("Access Dashboard"):
                if user == "admin" and pw == "2026": # Temporary bypass
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials!")
            
            st.markdown("<p style='text-align:center;'>OR</p>", unsafe_allow_html=True)
            st.markdown("<div class='google-btn'>", unsafe_allow_html=True)
            if st.button("🚀 Continue with Google"):
                st.info("Google OAuth is being initialized... (Redirecting)")
                time.sleep(1)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("Naya Account Banana Hai? Create Account"):
                st.session_state.auth_mode = "Signup"
                st.rerun()

        else: # SIGNUP MODE
            st.subheader("📝 Create Sentinel Account")
            new_user = st.text_input("Choose Username")
            new_email = st.text_input("Email Address")
            new_pw = st.text_input("Create Password", type="password")
            
            if st.button("Register & Initialize Agent"):
                st.success("Account Created! Now login to proceed.")
                st.session_state.auth_mode = "Login"
                st.rerun()
            
            if st.button("Already have an account? Login"):
                st.session_state.auth_mode = "Login"
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN APP LOGIC ---
if not st.session_state.logged_in:
    login_signup_page()
else:
    # Aapka wahi Colab wala pura Agentic Dashboard yahan shuru hoga
    st.sidebar.title("🤖 Raj-AI Agent")
    # ... (Baaki code wahi rahega)
