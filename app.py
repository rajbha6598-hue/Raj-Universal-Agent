import streamlit as st
import google.generativeai as genai
import PyPDF2
import io
import os

# 1. API Config (Streamlit Cloud ke Secrets se uthayega)
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error("🚨 API Key nahi mili! Settings > Secrets mein GEMINI_API_KEY daalein.")
    st.stop()

# 2. Sundar Neon UI Setup
st.set_page_config(page_title="Raj-AI Sentinel", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #deff9a; }
    .card { 
        background: #111; 
        padding: 20px; 
        border-radius: 15px; 
        border: 1px solid #333; 
        margin-bottom: 20px;
        color: #fff;
    }
    .stButton>button { 
        background: #deff9a !important; 
        color: #000 !important; 
        font-weight: bold; 
        width: 100%; 
        border-radius: 50px; 
        border: none;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Main Dashboard Content
st.title("🤝 Raj-AI: Universal Job Agent")
st.write("Dost, apna Resume upload karo, AI baaki kaam kar dega.")

# Sidebar status (Jaise Colab mein tha)
st.sidebar.success("🟢 System OK: Gemini 2.5 Active")
st.sidebar.info("Aapka AI Agent taiyar hai.")

file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])

if file:
    # PDF Reading logic (Fixed Indentation)
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        
        if text.strip() == "":
            st.error("❌ Is PDF se text nahi nikal pa raha. Shayad ye scan ki hui photo hai?")
        else:
            st.success("✅ Resume successfully load ho gaya!")
            
            if st.button("Analyze & Find Jobs"):
                with st.spinner("AI dimaag laga raha hai..."):
                    # Colab wala powerful prompt
                    prompt = f"""
                    Tu ek Senior HR Manager hai. Is resume ko analyze kar:
                    {text[:3000]}
                    
                    Mujhe Hinglish mein bata:
                    1. Is bande ki TOP 3 SKILLS kya hain?
                    2. 2 matching Job Roles aur unhe dhoondhne ke direct search links.
                    3. Resume ko behtar banane ke liye 1 pro tip.
                    """
                    response = model.generate_content(prompt)
                    st.markdown(f"<div class='card'>{response.text}</div>", unsafe_allow_html=True)
                    st.balloons()
                    
    except Exception as e:
        st.error(f"⚠️ Error reading PDF: {e}")

st.divider()
st.caption("🤖 Sentinel Status: All systems secure & encrypted.")
