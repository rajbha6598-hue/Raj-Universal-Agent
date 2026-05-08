import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
from PIL import Image

# 1. API Setup
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("🚨 API Key missing! Check Secrets.")
    st.stop()

# 2. UI Style (Neon Green)
st.set_page_config(page_title="Agentic Master 2026", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; font-family: monospace; }</style>", unsafe_allow_html=True)

st.title("🤖 RAJ-AI: SENTINEL (Colab Combined)")

file = st.file_uploader("Upload Resume (PDF/Image)", type=['pdf', 'jpg', 'png'])

if file:
    text = ""
    with st.spinner("AI is reading your document..."):
        try:
            if file.type == "application/pdf":
                # Normal Text Extraction
                pdf_data = file.read()
                reader = PyPDF2.PdfReader(io.BytesIO(pdf_data))
                text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                
                # AGENTIC FIX: Agar text blank hai (Scanned PDF), toh Vision use karo
                if not text.strip():
                    st.warning("⚠️ Scanned PDF detected. AI Vision is scanning...")
                    # Direct PDF bytes to Gemini
                    response = model.generate_content([
                        "Is resume PDF ko dhyan se padho aur iska poora text extract karo:",
                        {"mime_type": "application/pdf", "data": pdf_data}
                    ])
                    text = response.text
            else:
                # Image processing
                img = Image.open(file)
                res = model.generate_content(["Is resume image ko analyze karo aur text nikalo:", img])
                text = res.text

            if text.strip():
                st.sidebar.success("Agent Active 🟢")
                
                # --- PHASE 2: AUTOMATIC DECISIONS ---
                st.markdown("### 🧠 Agentic Intelligence Report")
                # Powerful prompt like your Colab
                prompt = f"""
                Tu ek Autonomous Career Agent hai. Is resume data ko analyze kar: {text[:3500]}
                Hinglish mein ye 4 kaam kar:
                1. Resume ki 2 galtiyan aur unhe theek karne ka tarika.
                2. Strict ATS Score (out of 100).
                3. Best Job Role jo is bande ko suit kare.
                4. Is role ke liye 10 tough interview questions.
                """
                response = model.generate_content(prompt)
                st.info(response.text)
                
                # --- AUTOMATION TOOLS ---
                st.divider()
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🚀 Search Jobs & Apply"):
                        st.write("Finding matches on LinkedIn & Naukri...")
                        links = model.generate_content(f"Give LinkedIn job search links for: {text[:500]}")
                        st.markdown(links.text)
                with c2:
                    if st.button("📧 Draft Application Email"):
                        email = model.generate_content(f"Write a professional email for this resume.")
                        st.code(email.text)
            else:
                st.error("Dost, ye file read nahi ho pa rahi. Dusri try karo.")

        except Exception as e:
            st.error(f"System Error: {e}")

st.caption("Agentic v8.0 | Full Automation Core Integrated")
