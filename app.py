import streamlit as st
import uuid
from datetime import datetime
import json

st.set_page_config(page_title="SmartAlloc Vendor Onboarding", page_icon="🌐", layout="centered")

# --- Title Header ---
st.title("🌐 SmartAlloc Vendor Onboarding Portal")
st.markdown("---")

# --- Tabs for PM vs Linguist ---
tab1, tab2 = st.tabs(["🔑 Internal PM Dashboard", "👤 External Linguist Portal"])

# Simulated session storage using streamlit session state
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

with tab1:
    st.subheader("Provision Onboarding Session Tokens")
    pm_name = st.text_input("Linguist Full Name", placeholder="e.g., Kenji Tanaka")
    pm_email = st.text_input("Linguist Contact Email", placeholder="e.g., kenji@example.com")
    pm_pair = st.text_input("Assigned Language Pair", value="English-Japanese")
    
    if st.button("Generate Onboarding Pipeline", type="primary"):
        if not pm_name or not pm_email:
            st.error("Name and Email are required.")
        else:
            token = str(uuid.uuid4())
            st.session_state.sessions[token] = {"name": pm_name, "email": pm_email, "pair": pm_pair}
            st.success(f"Session Active!")
            st.code(f"Token: {token}")
            st.info(f"Send your vendor this link structure: https://smartalloc.fideltech.com/register?token={token}")

with tab2:
    st.subheader("📄 Fidel Resource Empanelment Profile")
    token_in = st.text_input("Enter Access Session Token", placeholder="Paste the unique token here to unlock the form")
    
    if token_in:
        st.markdown("#### 👤 Section 1: Contact & Personal Profile")
        col1, col2 = st.columns(2)
        with col1:
            f_name = st.text_input("First Name")
            v_email = st.text_input("Email ID")
        with col2:
            l_name = st.text_input("Last Name")
            v_phone = st.text_input("Contact Number")
            
        avail = st.selectbox("Availability Status", ["Full-time", "Part-time"])
        
        st.markdown("#### 🎓 Section 2: Qualifications & Languages")
        native = st.text_input("Mother Tongue (Native Language)")
        exp = st.slider("Years of Translation Experience", 0, 40, 2)
        
        st.markdown("#### 🏦 Section 3: Bank Vault & Financials")
        col3, col4 = st.columns(2)
        with col3:
            b_name = st.text_input("Bank Name")
            b_ifsc = st.text_input("IFSC / SWIFT Code")
        with col4:
            b_acc = st.text_input("Account Number")
            b_tax = st.text_input("PAN Card Number")
            
        st.markdown("#### 📄 Section 4: Compliance Documentation Execution")
        st.markdown("Please download required corporate templates, execute signatures, and upload:")
        st.caption("📥 Download links: [Fidel NDA Template] | [PO Guidelines] | [Data Consent Form]")
        
        file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
        file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
        file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf', 'docx'])
        
        if st.button("Submit Profile Record", type="secondary"):
            if not f_name or not v_email or not native:
                st.error("Please fill in all mandatory profile fields.")
            else:
                submission_data = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "profile": {"name": f"{f_name} {l_name}", "email": v_email, "phone": v_phone, "status": avail},
                    "skills": {"experience": exp, "native_lang": native},
                    "bank": {"name": b_name, "account": b_acc, "ifsc": b_ifsc, "pan": b_tax},
                    "vault": {"NDA": file_nda is not None, "PO": file_po is not None, "Consent": file_consent is not None}
                }
                st.balloons()
                st.success("Empanelment submitted successfully!")
                st.json(submission_data)
