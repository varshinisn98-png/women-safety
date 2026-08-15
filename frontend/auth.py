import streamlit as st
import requests

def login_signup_screen():
    """Renders login/signup tab layout in Streamlit querying FastAPI backend."""
    st.markdown('<h2 class="glow-title" style="text-align: center; margin-bottom: 30px;">Access Safety Portal</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Create Account"])
        
        with tab1:
            st.write("Enter your credentials to access personalized safety analytics and crowdsourced reporting.")
            login_username = st.text_input("Username", key="login_username_input").strip()
            login_password = st.text_input("Password", type="password", key="login_password_input")
            
            if st.button("Sign In", use_container_width=True):
                if not login_username or not login_password:
                    st.error("Please fill in all fields.")
                else:
                    try:
                        payload = {"username": login_username, "password": login_password}
                        resp = requests.post("http://localhost:8000/auth/login", json=payload, timeout=3)
                        if resp.status_code == 200:
                            user = resp.json()
                            st.session_state.logged_in = True
                            st.session_state.username = user["username"]
                            st.session_state.user_role = user["role"]
                            st.session_state.user_email = user["email"]
                            st.success(f"Welcome back, {user['username']} ({user['role']})!")
                            st.rerun()
                        else:
                            detail = resp.json().get("detail", "Invalid credentials.")
                            st.error(detail)
                    except Exception as e:
                        st.error("FastAPI Backend Server offline. Please make sure the service is running on port 8000.")
                        
        with tab2:
            st.write("Sign up as a Citizen, Officer, or Admin to submit safety reviews and generate scorecards.")
            reg_username = st.text_input("Choose Username", key="reg_username_input").strip()
            reg_email = st.text_input("Email Address", key="reg_email_input").strip()
            reg_password = st.text_input("Password", type="password", key="reg_password_input")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_input")
            reg_role = st.selectbox("I am registering as:", ["Citizen", "Law Enforcement"], key="reg_role_input")
            
            if st.button("Create Account", use_container_width=True):
                if not reg_username or not reg_email or not reg_password:
                    st.error("All fields are required.")
                elif reg_password != reg_confirm_password:
                    st.error("Passwords do not match.")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("Please enter a valid email address.")
                else:
                    try:
                        payload = {
                            "username": reg_username,
                            "password": reg_password,
                            "email": reg_email,
                            "role": reg_role
                        }
                        resp = requests.post("http://localhost:8000/auth/signup", json=payload, timeout=3)
                        if resp.status_code == 200:
                            st.success("Account created successfully! You can now log in from the Sign In tab.")
                        else:
                            detail = resp.json().get("detail", "Failed to sign up.")
                            st.error(detail)
                    except Exception as e:
                        st.error("FastAPI Backend Server offline. Please make sure the service is running on port 8000.")
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logs out the user and clears session state."""
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.user_role = None
    st.session_state.user_email = None
    st.rerun()
