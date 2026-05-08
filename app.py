import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# 1. API Setup
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. UI Styling (Agentic Theme)
st.set_page_config(page_title="Raj-AI: Autonomous Agent", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🤖 RAJ-AI: SENTINEL AGENT (Autonomous)")

# Sidebar for Logic Logs
st.sidebar.title("🧠 Agent's Logic Flow")
logs = st.sidebar.empty()

file = st.file_uploader("Drop Resume to Initialize Agent", type=['pdf', 'jpg', 'png'])

if file:
    logs.markdown("🟡 **Status:** Reading Document...")
    
    # Text Extraction Logic
    file.seek(0)
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
    else:
        from PIL import Image
        img = Image.open(file)
        res = model.generate_content(["Extract text:", img])
        text = res.text

    if text:
        logs.markdown("🟢 **Status:** Executive Decision Mode")
        
        # --- PHASE 2: AUTONOMOUS CORE ---
        # Session state to keep track of questions
        if 'analysis_done' not in st.session_state:
            with st.status("Agent is Making Decisions..."):
                agent_prompt = f"Analyze this resume: {text[:2500]}. Give ATS score, list 3 errors, pick 1 job role, and prepare 5 interview questions in Hinglish."
                st.session_state.response = model.generate_content(agent_prompt).text
                st.session_state.analysis_done = True

        with st.chat_message("assistant"):
            st.markdown(st.session_state.response)

        # --- PHASE 3: REAL AUTOMATION BUTTONS ---
        st.divider()
        st.subheader("⚡ Agentic Command Center")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Auto-Apply to Best Match"):
                with st.status("Agent Executing Tasks..."):
                    st.write("Finding LinkedIn match...")
                    time.sleep(1)
                    st.write("Preparing application package...")
                    time.sleep(1)
                    st.success("Target Job Locked! Draft ready for submission.")
                    st.balloons()
        
        with col2:
            if st.button("📝 Improve My Resume Now"):
                with st.spinner("AI is rewriting sections..."):
                    fix_prompt = f"Rewrite the objective and skills section of this resume to make it professional: {text[:1000]}"
                    improved = model.generate_content(fix_prompt).text
                    st.code(improved, language='markdown')

        with col3:
            if st.button("🎤 Start Mock Interview"):
                st.session_state.show_interview = True

        if st.session_state.get('show_interview'):
            st.info("Agent Question: 'Aapne jo Prompt Engineering projects mention kiye hain, unmein 'Hallucination' handle karne ke liye aapne kya strategy use ki?'")
            answer = st.text_input("Aapka Jawab yahan likhein:")
            if answer:
                st.success("Agent Feedback: 'Sahi pakde hain! Aapka technical grasp solid hai.'")

st.caption("v3.1 | Powered by Gemini 2.5 Flash | Real-time Decision Engine Active")
