import streamlit as st
import google.generativeai as genai
import time

# --- CUSTOM CSS: ACID GREEN & DARK MODE ---
st.set_page_config(page_title="Agentic 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #f8fafc; }
    .stButton>button {
        background-color: #deff9a !important;
        color: #000 !important;
        border-radius: 50px !important;
        font-weight: bold;
        border: none;
    }
    .stTextInput>div>div>input { background-color: #111 !important; color: #deff9a !important; border: 1px solid #333 !important; }
    .stSidebar { background-color: #0a0a0a !important; border-right: 1px solid #333; }
    h1, h2, h3 { color: #deff9a !important; }
    .card { background-color: #111; padding: 20px; border-radius: 20px; border: 1px solid #222; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE & AUTH ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown("<h1 style='text-align: center;'>AGENTIC<span>2026</span></h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔐 Secure Entry")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if user == "admin" and password == "2026":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Galti hai dost! Sahi password daalo.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
if not st.session_state.logged_in:
    login()
else:
    # Sidebar Navigation
    st.sidebar.title("🤖 Agentic 2026")
    menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🎯 Job Hunter", "📝 Skill Lab", "📧 Comms Hub"])
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if menu == "🏠 Dashboard":
        st.title("Welcome back, User")
        col1, col2, col3 = st.columns(3)
        with col1: st.markdown("<div class='card'><h3>Jobs Applied</h3><h1>12</h1></div>", unsafe_allow_html=True)
        with col2: st.markdown("<div class='card'><h3>Tests Taken</h3><h1>05</h1></div>", unsafe_allow_html=True)
        with col3: st.markdown("<div class='card'><h3>AI Accuracy</h3><h1>94%</h1></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>🚀 Proactive Insight</h3><p>Dost, LinkedIn par 3 naye 'AI Evaluation' jobs post huye hain jo aapke profile se match karte hain. Kya main apply kar doon?</p></div>", unsafe_allow_html=True)

    elif menu == "🎯 Job Hunter":
        st.title("🎯 Job Center")
        role = st.text_input("Enter Role (e.g., AI Evaluator)", "AI Evaluation Specialist")
        loc = st.text_input("Location", "Remote")
        if st.button("Search Real-time"):
            with st.spinner("Scraping 2026 Market..."):
                time.sleep(2)
                st.success("Found 15 matching roles!")
                st.markdown(f"[🔗 View LinkedIn Jobs](https://www.linkedin.com/jobs/search/?keywords={role.replace(' ','%20')})")
                st.markdown(f"[🔗 View Indeed Jobs](https://in.indeed.com/jobs?q={role.replace(' ','+')})")

    elif menu == "📝 Skill Lab":
        st.title("📝 AI Skill Lab")
        st.info("Task: AI says 'Chai mein rice daalo'. Evaluate this.")
        eval_input = st.text_area("Your Analysis:")
        if st.button("Submit for Grading"):
            if "rice" in eval_input.lower() or "chawal" in eval_input.lower():
                st.balloons()
                st.success("Perfect! Aapne 'Hallucination' pakad liya.")
            else:
                st.warning("Thoda aur dhyaan se dekho bhai.")

    elif menu == "📧 Comms Hub":
        st.title("📧 Communication Lab")
        intent = st.text_input("Aapka message kya hai?", "Boss ko chutti ki application")
        if st.button("Generate Draft"):
            st.code("Subject: Leave Application\n\nDear Boss, I need leave for 2 days due to personal reasons. Regards.")

    
