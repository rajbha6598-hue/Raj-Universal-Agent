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
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. UI Styling
st.set_page_config(page_title="Raj-AI Universal Agent", layout="wide")
st.markdown("<style>.stApp { background-color: #000; color: #deff9a; }</style>", unsafe_allow_html=True)

st.title("🌐 Raj-AI: Universal Job Agent")
st.sidebar.success("🟢 System OK: Universal Mode Active")

# File uploader for ALL types
file = st.file_uploader("Upload Resume (PDF, Image, Word, Excel)", type=['pdf', 'jpg', 'png', 'docx', 'xlsx'])

if file:
    text = ""
    file_type = file.name.split('.')[-1].lower()
    
    try:
        # --- PDF Logic ---
        if file_type == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        
        # --- IMAGE Logic (Gemini Vision) ---
        elif file_type in ['jpg', 'png', 'jpeg']:
            img = Image.open(file)
            st.image(img, caption="Uploaded Image", width=300)
            with st.spinner("AI photo padh raha hai..."):
                response = model.generate_content(["Is image se sara text nikal kar do:", img])
                text = response.text
        
        # --- WORD Logic ---
        elif file_type == 'docx':
            doc = Document(io.BytesIO(file.read()))
            text = "\n".join([para.text for para in doc.paragraphs])
            
        # --- EXCEL Logic ---
        elif file_type == 'xlsx':
            df = pd.read_excel(file)
            text = df.to_string()

        # Check if text was extracted
        if text.strip():
            st.success(f"✅ {file_type.upper()} file successfully load ho gayi!")
            
            if st.button("Analyze Everything"):
                with st.spinner("AI analysis kar raha hai..."):
                    prompt = f"Analyze this resume content and give 3 job roles in Hinglish: {text[:3000]}"
                    res = model.generate_content(prompt)
                    st.info(res.text)
        else:
            st.error("Dost, is file se text nahi mil raha. Please clear file upload karein.")
            
    except Exception as e:
        st.error(f"Galti ho gayi: {e}")

st.divider()
st.caption("🤖 Sentinel Status: Supporting all file formats.")
