import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="Fidel Vendor Onboarding", page_icon="🌐", layout="centered")

# --- Title Header ---
st.title("🌐 Fidel Resource Onboarding Portal")
st.markdown("Please download the required corporate templates below, complete signatures with date, and re-upload your executed copies along with your profile details.")
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
    
st.markdown("#### 📥 Section 4: Download Official Templates")
st.markdown("Click the buttons below to download the blank frameworks to your desktop for signing:")

# Helper function to safely load file bytes for download buttons
def get_file_bytes(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            return f.read()
    return b""

nda_bytes = get_file_bytes("Fidel_NDA_Ver 1.3.pdf")
po_bytes = get_file_bytes("Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf")
consent_bytes = get_file_bytes("Fidel Consent Form.pdf")  # Updated file lookup name

d_col1, d_col2, d_col3 = st.columns(3)
with d_col1:
    st.download_button(
        label="📥 Download NDA Template",
        data=nda_bytes,
        file_name="Fidel_NDA_Ver 1.3.pdf",
        mime="application/pdf",
        disabled=len(nda_bytes) == 0
    )
with d_col2:
    st.download_button(
        label="📥 Download PO Terms",
        data=po_bytes,
        file_name="Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf",
        mime="application/pdf",
        disabled=len(po_bytes) == 0
    )
with d_col3:
    st.download_button(
        label="📥 Download Consent Form",
        data=consent_bytes,
        file_name="Fidel Consent Form.pdf",  # Updated downloaded file extension
        mime="application/pdf",              # Updated target MIME type for PDF delivery
        disabled=len(consent_bytes) == 0
    )

if len(consent_bytes) == 0:
    st.warning("⚠️ Note to Developer: Ensure the Consent Form filename on GitHub matches 'Fidel Consent Form.pdf' exactly.")

st.markdown("#### 📤 Section 5: Compliance Documentation Submission")
st.markdown("Upload your signed and dated copies here:")

file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf'])  # Constrained upload filter to PDF

st.markdown("---")
if st.button("Submit Profile Record", type="primary"):
    if not f_name or not v_email or not native:
        st.error("❌ Please fill out all mandatory profile fields marked with an asterisk (*).")
    else:
        submission_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "profile": {"name": f"{f_name} {l_name}", "email": v_email, "phone": v_phone, "status": avail},
            "skills": {"experience": exp, "native_lang": native, "pairs": lang_pairs},
            "bank": {"name": b_name, "account": b_acc, "ifsc": b_ifsc, "pan": b_tax},
            "vault": {"NDA_Attached": file_nda is not None, "PO_Guidelines_Attached": file_po is not None, "Consent_Form_Attached": file_consent is not None}
        }
        st.balloons()
        st.success("🎉 Onboarding profile and signed agreements submitted successfully!")
        st.json(submission_data)
