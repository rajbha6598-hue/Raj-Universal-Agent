import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time

# --- 1. CONFIG & STYLE ---
st.set_page_config(page_title="Universal Agent 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; } .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #deff9a; margin-bottom: 20px; }</style>", unsafe_allow_html=True)

# --- 2. API & AUTH ---
if 'auth' not in st.session_state: st.session_state.auth = False
user_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if not st.session_state.auth:
    st.title("🤖 RAJ-AI SENTINEL: LOGIN")
    with st.columns([1,2,1])[1]:
        u = st.text_input("Agent ID")
        p = st.text_input("Vault Key", type="password")
        if st.button("Initialize Link"):
            if u == "admin" and p == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied.")
else:
    # --- 3. DASHBOARD CORE ---
    st.title("🌐 UNIVERSAL COMMAND CENTER")
    
    if not user_key:
        st.warning("👈 Sidebar mein apni Gemini API Key dalo pehle!")
    else:
        genai.configure(api_key=user_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
        
        if file:
            # Step 1: Text Extraction
            with st.spinner("Agent scanning document..."):
                reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
            
            if text:
                st.success("Document Scanned Successfully!")
                
                # Step 2: AI Intelligence Analysis
                # Humne display ko simplify kiya hai taaki stuck na ho
                st.markdown("### 🧠 Agentic Intelligence Report")
                with st.chat_message("assistant"):
                    report_placeholder = st.empty()
                    report_placeholder.info("AI is thinking... (Please wait 5-10 seconds)")
                    
                    try:
                        # Full-Fledge Prompt like Colab
                        prompt = f"Analyze this resume: {text[:3000]}. Give ATS Score (0-100), 2 major mistakes, and 10 interview questions in Hinglish."
                        response = model.generate_content(prompt)
                        
                        # Displaying final report
                        report_placeholder.markdown(response.text)
                        
                        # Step 3: Action Buttons
                        st.divider()
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("🚀 Search Jobs"):
                                job_res = model.generate_content(f"Give LinkedIn links for: {text[:500]}")
                                st.write(job_res.text)
                        with c2:
                            if st.button("📧 Write Email"):
                                email_res = model.generate_content(f"Write a job email for this resume.")
                                st.code(email_res.text)
                                
                    except Exception as e:
                        report_placeholder.error(f"AI Connection Error: {e}")
            else:
                st.error("Bhai, is PDF mein text nahi mila. Scanned image hai kya?")

st.caption("Universal Agent v14.0 | BYOK | 2026 Edition")
