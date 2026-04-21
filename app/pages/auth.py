"""app/pages/auth.py — Login & Registration pages."""
import re, time
import streamlit as st
from database.models import login_user, register_student
from config.settings import APP_TITLE, INSTITUTION


def _valid_email(email):
    return bool(re.match(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$', email.strip()))


def render_login():
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown(f"""
        <div style="text-align:center;padding:2rem 0 1.25rem;">
          <div style="font-size:3rem;">🎓</div>
          <h1 style="font-size:1.55rem;font-weight:700;margin:.4rem 0 .2rem;">{APP_TITLE}</h1>
          <p style="font-size:.85rem;margin:0;opacity:.6;">{INSTITUTION}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Sign In")
        with st.form("login_form"):
            user_id  = st.text_input("User ID", placeholder="e.g. STU2024001 / GM001 / ADMIN001")
            password = st.text_input("Password", type="password", placeholder="Your password")
            btn      = st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary")

        if btn:
            if not user_id.strip() or not password.strip():
                st.error("Please enter both User ID and Password.")
            else:
                with st.spinner("Authenticating..."):
                    user = login_user(user_id.strip(), password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("❌ Invalid User ID or Password.")

        st.divider()
        st.caption("New student?")
        if st.button("📝 Register as Student", use_container_width=True):
            st.session_state["page"] = "register"
            st.rerun()


def render_register():
    DEPARTMENTS = ["Computer Science","Information Technology","Electronics",
                   "Mechanical","Civil","Electrical","MBA","BBA",
                   "Commerce","Arts","Science","Other"]

    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem 0 1rem;">
          <div style="font-size:2.5rem;">📝</div>
          <h1 style="font-size:1.4rem;font-weight:700;margin:.4rem 0 .2rem;">Student Registration</h1>
          <p style="font-size:.85rem;margin:0;opacity:.6;">Create your account to raise complaints</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("reg_form"):
            c1, c2 = st.columns(2)
            with c1:
                name    = st.text_input("Full Name *", placeholder="e.g. Priya Patel")
                user_id = st.text_input("Student ID *", placeholder="e.g. STU2024001")
            with c2:
                email = st.text_input("Email Address *", placeholder="name@domain.com",
                                      help="Must be a valid email — e.g. priya@college.edu")
                dept  = st.selectbox("Department *", DEPARTMENTS)
            c3, c4 = st.columns(2)
            with c3: pwd  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
            with c4: cpwd = st.text_input("Confirm Password *", type="password")
            btn = st.form_submit_button("🚀 Create Account", use_container_width=True, type="primary")

        if btn:
            errors = []
            if not name.strip():          errors.append("Full name is required.")
            if not user_id.strip():       errors.append("Student ID is required.")
            if not email.strip():         errors.append("Email is required.")
            elif not _valid_email(email): errors.append("❌ Invalid email — please use format: name@domain.com")
            if len(pwd) < 6:              errors.append("Password must be at least 6 characters.")
            if pwd != cpwd:               errors.append("Passwords do not match.")

            if errors:
                for e in errors: st.error(e)
            else:
                with st.spinner("Creating account..."):
                    ok, msg = register_student(user_id.strip().upper(), name.strip(),
                                               email.strip().lower(), pwd, dept)
                if ok:
                    st.success("✅ Account created! Redirecting to login...")
                    st.balloons(); time.sleep(1.5)
                    st.session_state["page"] = "login"; st.rerun()
                else:
                    st.error(f"❌ {msg}")

        st.divider()
        if st.button("← Back to Sign In", use_container_width=True):
            st.session_state["page"] = "login"; st.rerun()
