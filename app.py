import streamlit as st
import google.generativeai as genai
import time
import sqlite3
import bcrypt
import os
from google.oauth2 import id_token
from google.auth.transport import requests
import json

# --- CONFIG ---
st.set_page_config(page_title="Agentic 2026", layout="wide")

# Google OAuth Client ID (apna client ID yahan daal)
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE,
            password_hash TEXT,
            auth_provider TEXT DEFAULT 'local',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #000; color: #f8fafc; }
    .stButton>button {
        background-color: #deff9a !important;
        color: #000 !important;
        border-radius: 50px !important;
        font-weight: bold;
        border: none;
        padding: 10px 25px;
        margin: 5px 0;
    }
    .stButton>button:hover {
        background-color: #c8e97a !important;
        transform: scale(1.02);
    }
    .google-btn {
        background-color: #4285f4 !important;
        color: white !important;
    }
    .stTextInput>div>div>input { 
        background-color: #111 !important; 
        color: #deff9a !important; 
        border: 1px solid #333 !important;
        border-radius: 10px;
    }
    .stSidebar { background-color: #0a0a0a !important; border-right: 1px solid #333; }
    h1, h2, h3 { color: #deff9a !important; }
    .card { 
        background-color: #111; 
        padding: 20px; 
        border-radius: 20px; 
        border: 1px solid #222; 
        margin-bottom: 20px; 
    }
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 40px 20px;
    }
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 20px 0;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #333;
    }
    .divider span {
        padding: 0 15px;
        color: #666;
    }
    .tab-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'login'

# --- SECURITY FUNCTIONS ---
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password kam se kam 8 characters ka hona chahiye"
    if not any(c.isupper() for c in password):
        return False, "Ek uppercase letter zaroor hona chahiye"
    if not any(c.islower() for c in password):
        return False, "Ek lowercase letter zaroor hona chahiye"
    if not any(c.isdigit() for c in password):
        return False, "Ek number zaroor hona chahiye"
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Ek special character zaroor hona chahiye (!@#$%^&*)"
    return True, "Strong password!"

def create_user(username: str, email: str, password: str, auth_provider: str = 'local') -> tuple[bool, str]:
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password) if password else None
        cursor.execute(
            'INSERT INTO users (username, email, password_hash, auth_provider) VALUES (?, ?, ?, ?)',
            (username, email, password_hash, auth_provider)
        )
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return False, "Username already exists"
        elif 'email' in str(e):
            return False, "Email already registered"
        return False, "Registration failed"

def authenticate_user(username: str, password: str) -> tuple[bool, str]:
    cursor = conn.cursor()
    cursor.execute('SELECT username, password_hash, auth_provider FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    
    if not result:
        return False, "User not found"
    
    if result[2] == 'google':
        return False, "Is account ke liye Google Sign-In use karo"
    
    if verify_password(password, result[1]):
        return True, result[0]
    return False, "Galat password"

def authenticate_google_user(email: str, name: str) -> tuple[bool, str]:
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    
    if result:
        return True, result[0]
    
    # New Google user - create account
    username = email.split('@')[0]
    base_username = username
    counter = 1
    while True:
        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if not cursor.fetchone():
            break
        username = f"{base_username}{counter}"
        counter += 1
    
    success, msg = create_user(username, email, None, 'google')
    if success:
        return True, username
    return False, msg

# --- GOOGLE OAUTH COMPONENT ---
def google_sign_in_button():
    google_oauth_html = f"""
    <div id="g_id_onload"
         data-client_id="{GOOGLE_CLIENT_ID}"
         data-callback="handleCredentialResponse"
         data-auto_prompt="false">
    </div>
    <div class="g_id_signin"
         data-type="standard"
         data-size="large"
         data-theme="filled_blue"
         data-text="sign_in_with"
         data-shape="pill"
         data-logo_alignment="left"
         data-width="300">
    </div>
    <script src="[accounts.google.com](https://accounts.google.com/gsi/client)" async defer></script>
    <script>
    function handleCredentialResponse(response) {{
        const data = {{credential: response.credential}};
        window.parent.postMessage({{type: 'google_auth', data: data}}, '*');
    }}
    </script>
    """
    st.components.v1.html(google_oauth_html, height=50)

# --- AUTH UI ---
def auth_page():
    st.markdown("<h1 style='text-align: center;'>AGENTIC<span style='color:#deff9a;'>2026</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Career Platform</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Tab selection
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
        
        with tab1:
            st.subheader("Welcome Back!")
            
            # Google Sign-In
            st.markdown("#### Sign in with Google")
            if st.button("🔵 Continue with Google", key="google_login", use_container_width=True):
                st.info("Google OAuth ke liye apna GOOGLE_CLIENT_ID environment variable set karo. Instructions neeche hain.")
            
            st.markdown("<div class='divider'><span>OR</span></div>", unsafe_allow_html=True)
            
            # Traditional Login
            st.markdown("#### Sign in with Username")
            login_user = st.text_input("Username", key="login_username", placeholder="Enter username")
            login_pass = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
            
            if st.button("🚀 Login", key="login_btn", use_container_width=True):
                if login_user and login_pass:
                    success, result = authenticate_user(login_user, login_pass)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user = result
                        st.success("Login successful!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Username aur password dono daalo")
        
        with tab2:
            st.subheader("Create New Account")
            
            # Google Sign-Up
            st.markdown("#### Sign up with Google")
            if st.button("🔵 Continue with Google", key="google_signup", use_container_width=True):
                st.info("Google OAuth ke liye setup instructions neeche dekho.")
            
            st.markdown("<div class='divider'><span>OR</span></div>", unsafe_allow_html=True)
            
            # Traditional Sign-Up
            st.markdown("#### Create with Email")
            new_username = st.text_input("Choose Username", key="signup_username", placeholder="minimum 3 characters")
            new_email = st.text_input("Email Address", key="signup_email", placeholder="your@email.com")
            new_password = st.text_input("Create Password", type="password", key="signup_password", placeholder="Strong password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password", placeholder="Re-enter password")
            
            # Password strength indicator
            if new_password:
                is_strong, msg = validate_password_strength(new_password)
                if is_strong:
                    st.success(f"✅ {msg}")
                else:
                    st.warning(f"⚠️ {msg}")
            
            if st.button("✨ Create Account", key="signup_btn", use_container_width=True):
                # Validation
                if len(new_username) < 3:
                    st.error("Username kam se kam 3 characters ka hona chahiye")
                elif '@' not in new_email or '.' not in new_email:
                    st.error("Valid email daalo")
                elif new_password != confirm_password:
                    st.error("Passwords match nahi kar rahe")
                else:
                    is_strong, msg = validate_password_strength(new_password)
                    if not is_strong:
                        st.error(msg)
                    else:
                        success, result = create_user(new_username, new_email, new_password)
                        if success:
                            st.success("🎉 Account created! Ab login kar sakte ho.")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(result)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Google OAuth Setup Instructions
        with st.expander("🔧 Google OAuth Setup Guide"):
            st.markdown("""
            **Google Sign-In enable karne ke liye:**
            
            1. [Google Cloud Console](https://console.cloud.google.com/) par jao
            2. Naya project banao ya existing select karo
            3. APIs & Services → Credentials par jao
            4. Create Credentials → OAuth 2.0 Client ID
            5. Application type: Web application
            6. Authorized JavaScript origins mein apni app URL daalo
            7. Client ID copy karo
            8. Environment variable set karo:
            ```
            GOOGLE_CLIENT_ID=your_client_id_here
            ```
            """)

# --- MAIN DASHBOARD ---
if not st.session_state.logged_in:
    auth_page()
else:
    # Sidebar Navigation
    st.sidebar.title("🤖 Agentic 2026")
    st.sidebar.markdown(f"👤 **{st.session_state.user}**")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "🎯 Job Hunter", "📝 Skill Lab", "📧 Comms Hub", "⚙️ Settings"])
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()

    if menu == "🏠 Dashboard":
        st.title(f"Welcome back, {st.session_state.user}!")
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("<div class='card'><h3>Jobs Applied</h3><h1>12</h1></div>", unsafe_allow_html=True)
        with col2: 
            st.markdown("<div class='card'><h3>Tests Taken</h3><h1>05</h1></div>", unsafe_allow_html=True)
        with col3: 
            st.markdown("<div class='card'><h3>AI Accuracy</h3><h1>94%</h1></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>🚀 Proactive Insight</h3><p>Dost, LinkedIn par 3 naye 'AI Evaluation' jobs post huye hain jo aapke profile se match karte hain. Kya main apply kar doon?</p></div>", unsafe_allow_html=True)

    elif menu == "🎯 Job Hunter":
        st.title("🎯 Job Center")
        role = st.text_input("Enter Role (e.g., AI Evaluator)", "AI Evaluation Specialist")
        loc = st.text_input("Location", "Remote")
        if st.button("🔍 Search Real-time"):
            with st.spinner("Scraping 2026 Market..."):
                time.sleep(2)
                st.success("Found 15 matching roles!")
                st.markdown(f"[🔗 View LinkedIn Jobs](https://www.linkedin.com/jobs/search/?keywords={role.replace(' ','%20')})")
                st.markdown(f"[🔗 View Indeed Jobs](https://in.indeed.com/jobs?q={role.replace(' ','+')})")

    elif menu == "📝 Skill Lab":
        st.title("📝 AI Skill Lab")
        st.info("Task: AI says 'Chai mein rice daalo'. Evaluate this.")
        eval_input = st.text_area("Your Analysis:")
        if st.button("📊 Submit for Grading"):
            if "rice" in eval_input.lower() or "chawal" in eval_input.lower() or "hallucination" in eval_input.lower():
                st.balloons()
                st.success("Perfect! Aapne 'Hallucination' pakad liya.")
            else:
                st.warning("Thoda aur dhyaan se dekho bhai.")

    elif menu == "📧 Comms Hub":
        st.title("📧 Communication Lab")
        intent = st.text_input("Aapka message kya hai?", "Boss ko chutti ki application")
        if st.button("✍️ Generate Draft"):
            st.code("Subject: Leave Application\n\nDear Boss, I need leave for 2 days due to personal reasons. Regards.")
    
    elif menu == "⚙️ Settings":
        st.title("⚙️ Account Settings")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Change Password")
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_new = st.text_input("Confirm New Password", type="password")
        
        if st.button("🔄 Update Password"):
            if new_pass != confirm_new:
                st.error("New passwords match nahi kar rahe")
            else:
                is_strong, msg = validate_password_strength(new_pass)
                if not is_strong:
                    st.error(msg)
                else:
                    cursor = conn.cursor()
                    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (st.session_state.user,))
                    result = cursor.fetchone()
                    if result and verify_password(current_pass, result[0]):
                        new_hash = hash_password(new_pass)
                        cursor.execute('UPDATE users SET password_hash = ? WHERE username = ?', 
                                      (new_hash, st.session_state.user))
                        conn.commit()
                        st.success("Password updated successfully!")
                    else:
                        st.error("Current password galat hai")
        st.markdown("</div>", unsafe_allow_html=True)
