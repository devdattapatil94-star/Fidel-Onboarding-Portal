import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="Fidel Vendor Onboarding", page_icon="🌐", layout="centered")

# --- Title Header ---
st.title("🌐 Fidel Resource Onboarding Portal")
st.markdown("Please complete the official empanelment profile form below and upload your signed compliance agreements.")
st.markdown("---")

# --- Form Interface ---
st.subheader("📄 Resource Empanelment Profile")

st.markdown("#### 👤 Section 1: Contact & Personal Profile")
col1, col2 = st.columns(2)
with col1:
    f_name = st.text_input("*First Name", placeholder="Enter your first name")
    v_email = st.text_input("*Email ID", placeholder="example@email.com")
with col2:
    l_name = st.text_input("*Last Name", placeholder="Enter your last name")
    v_phone = st.text_input("Contact Number", placeholder="+91-XXXXX-XXXXX")
    
avail = st.selectbox("Availability Status", ["Full-time", "Part-time"])

st.markdown("#### 🎓 Section 2: Qualifications & Languages")
native = st.text_input("*Mother Tongue (Native Language)", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations", placeholder="e.g., English-Japanese, German-English")

st.markdown("#### 🏦 Section 3: Bank Vault & Financials")
col3, col4 = st.columns(2)
with col3:
    b_name = st.text_input("Bank Name")
    b_ifsc = st.text_input("IFSC / SWIFT Code")
with col4:
    b_acc = st.text_input("Account Number")
    b_tax = st.text_input("PAN Card Number (For Indian Vendors)")
    
st.markdown("#### 📄 Section 4: Compliance Documentation Execution")
st.markdown("Please download each required template, execute signatures with date, and re-upload here:")
st.markdown("📥 **Download Frameworks:** [Fidel NDA Template] | [PO Guidelines] | [Data Consent Form]")

file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf', 'docx'])

st.markdown("---")
if st.button("Submit Profile Record", type="primary"):
    if not f_name or not v_email or not native:
        st.error("❌ Please fill out all mandatory profile fields marked with an asterisk (*).")
    else:
        submission_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": {
                "name": f"{f_name} {l_name}",
                "email": v_email,
                "phone": v_phone,
                "status": avail
            },
            "skills": {
                "experience": exp,
                "native_lang": native,
                "pairs": lang_pairs
            },
            "bank": {
                "name": b_name,
                "account": b_acc,
                "ifsc": b_ifsc,
                "pan": b_tax
            },
            "vault": {
                "NDA_Attached": file_nda is not None,
                "PO_Guidelines_Attached": file_po is not None,
                "Consent_Form_Attached": file_consent is not None
            }
        }
        st.balloons()
        st.success("🎉 Empanelment profile submitted successfully!")
        st.json(submission_data)
