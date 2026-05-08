import streamlit as st
import google.generativeai as genai
import PyPDF2
import pandas as pd
from docx import Document
import io
from PIL import Image
# 1. API Config
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash') # Updated to 1.5 for better vision

# 2. UI Styling
st.set_page_config(page_title="Raj-AI Universal Agent", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; }</style>", unsafe_allow_html=True)

st.title("🌐 Raj-AI: Universal Job Agent")

file = st.file_uploader("Upload Resume", type=['pdf', 'jpg', 'png', 'docx', 'xlsx'])

if file:
    text = ""
    file_type = file.name.split('.')[-1].lower()
    
    with st.spinner("File process ho rahi hai..."):
        try:
            if file_type == 'pdf':
                # Pehle normal text nikalne ki koshish
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                
                # Agar text nahi mila (Scanned PDF), toh Gemini Vision use karenge
                if not text.strip():
                    st.warning("Ye scanned PDF lag rahi hai, AI vision use kar raha hoon...")
                    # Iske liye hum file ko image ki tarah direct Gemini ko bhej denge
                    file.seek(0)
                    response = model.generate_content(["Is resume PDF ko read karo aur text nikalo:", {"mime_type": "application/pdf", "data": file.read()}])
                    text = response.text

            elif file_type in ['jpg', 'png', 'jpeg']:
                img = Image.open(file)
                response = model.generate_content(["Is image resume ko analyze karo:", img])
                text = response.text

            # ... (Word aur Excel logic same rahega) ...

            if text.strip():
                st.success("✅ Content load ho gaya!")
                if st.button("Analyze Now"):
                    res = model.generate_content(f"Analyze this resume and give 2 jobs in Hinglish: {text[:4000]}")
                    st.info(res.text)
            else:
                st.error("Dost, ye file bilkul blank hai ya readable nahi hai.")
        except Exception as e:
            st.error(f"Error: {e}")
