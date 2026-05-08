import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# --- 1. AGENTIC UI THEME ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; font-family: monospace; }
    .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; margin-bottom: 20px; }
    .stButton>button { background: #deff9a !important; color: #000 !important; font-weight: bold; border-radius: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR: API KEY MANAGEMENT ---
st.sidebar.title("🔐 Agent Configuration")
user_key = st.sidebar.text_input("Enter your Gemini API Key", type="password", help="Get it free from Google AI Studio")

if not user_key:
    st.sidebar.warning("⚠️ System Offline: API Key Required")
    st.sidebar.markdown(f"[Get Free API Key here](https://aistudio.google.com/app/apikey)")
else:
    try:
        genai.configure(api_key=user_key)
        # Using the latest 2.5-flash from your Colab experiments
        model = genai.GenerativeModel('gemini-1.5-flash')
        st.sidebar.success("System Online 🟢")
    except:
        st.sidebar.error("Invalid API Key!")

# --- 3. AUTHENTICATION (Optional but kept for your admin control) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: UNIVERSAL ACCESS")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize Link"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
else:
    # --- 4. UNIVERSAL DASHBOARD ---
    st.title("🌐 UNIVERSAL COMMAND CENTER")
    
    if not user_key:
        st.error("Bhai, pehle Sidebar mein apni API Key dalo, tabhi Agent kaam karega!")
    else:
        file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
        
        if file:
            with st.status("Agentic Analysis in Progress...") as status:
                # Text Extraction Logic
                reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                
                if text:
                    status.update(label="Scanning Complete ✅", state="complete")
                    
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("🧐 AI Intelligence Report")
                    
                    # Colab Prompt Logic
                    prompt = f"Tu ek Autonomous Career Agent hai. Is resume ko analyze kar aur ATS score, 2 galtiyan, aur 10 interview questions de: {text[:3000]}"
                    try:
                        response = model.generate_content(prompt)
                        st.write(response.text)
                    except Exception as e:
                        st.error(f"AI Error: {e}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Automation Buttons
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🚀 Job Search"):
                            st.write(model.generate_content(f"LinkedIn links for: {text[:500]}").text)
                    with c2:
                        if st.button("📧 Email Draft"):
                            st.code(model.generate_content(f"Draft application email for this resume").text)

st.caption("Universal Agent v13.0 | BYOK Edition | 2026")
