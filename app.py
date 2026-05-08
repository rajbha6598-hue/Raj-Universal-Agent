import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import time
import pandas as pd
from PIL import Image

# 1. API Config
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Acid Green Neon UI
st.set_page_config(page_title="Agentic Master 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; }
    .card { background: #111; padding: 25px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; }
    .stButton>button { background: #deff9a !important; color: #000 !important; font-weight: bold; width: 100%; border-radius: 50px; height: 45px; }
    .stat-box { text-align: center; border: 1px solid #deff9a; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🤖 Agentic Pro")
st.sidebar.markdown("<div class='stat-box'><h3>Accuracy</h3><h1>94%</h1></div>", unsafe_allow_html=True)
st.sidebar.info("System Status: Online & Secure 🟢")

# MAIN DASHBOARD
st.title("🌐 Raj-AI: Universal Automation Agent")

file = st.file_uploader("Upload Resume (PDF/Image)", type=['pdf', 'jpg', 'png'])

if file:
    text = ""
    file_type = file.type
    
    with st.spinner("AI Brain reading your resume..."):
        try:
            if file_type == "application/pdf":
                # Normal PDF reading
                reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])
                
                # Agar text nahi mila (Scanned PDF), toh Gemini ko direct bhejenge
                if not text.strip():
                    st.warning("⚠️ Scanned PDF detected. Using AI Vision...")
                    file.seek(0)
                    # Gemini 1.5 direct PDF bhi scan kar leta hai
                    response = model.generate_content(["Is scanned PDF resume ko read karo aur text nikalo:", {"mime_type": "application/pdf", "data": file.read()}])
                    text = response.text
            else:
                # Agar Image hai (JPG/PNG)
                img = Image.open(file)
                res = model.generate_content(["Is image resume ko analyze karo aur text nikalo:", img])
                text = res.text

            if text.strip():
                st.success("✅ Content Extracted Successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("📝 Resume Intelligence")
                    if st.button("Start Analysis"):
                        analysis = model.generate_content(f"Analyze this resume: {text[:3000]}")
                        st.write(analysis.text)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("🎯 Job Automation")
                    if st.button("Search & Match Jobs"):
                        job_res = model.generate_content(f"Give 2 job roles and search links for: {text[:1000]}")
                        st.write(job_res.text)
                    st.markdown("</div>", unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Galti: {e}")

st.divider()
st.caption("🤖 Powered by Gemini 1.5 Flash | Built for Rajbha Malik")
