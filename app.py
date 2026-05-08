import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os

# API Config (Streamlit Cloud ke Secrets se uthayega)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Sundar Neon UI
st.set_page_config(page_title="Raj-AI Sentinel", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; }
    .card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 20px; }
    .stButton>button { background: #deff9a !important; color: #000 !important; font-weight: bold; width: 100%; border-radius: 50px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤝 Raj-AI: Universal Job Agent")
st.write("Dost, apna Resume upload karo, AI baki kaam kar dega.")

file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])

if file:
    # PDF Reading
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
    text = "".join([page.extract_text() for page in pdf_reader.pages])
    
    st.success("✅ Resume mil gaya!")
    
    if st.button("Analyze & Find Jobs"):
        with st.spinner("AI dimaag laga raha hai..."):
            prompt = f"Analyze this resume and give 2 job roles with search links in Hinglish: {text[:2500]}"
            response = model.generate_content(prompt)
            st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
