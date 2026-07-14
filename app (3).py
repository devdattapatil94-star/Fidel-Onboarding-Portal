import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="Fidel Vendor Onboarding", page_icon="🌐", layout="centered")

st.title("🌐 Fidel Resource Onboarding Portal")
st.markdown("Please complete the official empanelment profile form below and upload your signed compliance agreements.")
st.markdown("---")

st.subheader("📄 Resource Empanelment Profile")

st.markdown("#### 👤 Section 1: Contact & Personal Profile")
col1, col2 = st.columns(2)
with col1:
    f_name = st.text_input("First Name *", placeholder="Enter your first name")
    v_email = st.text_input("Email ID *", placeholder="example@email.com")
with col2:
    l_name = st.text_input("Last Name", placeholder="Enter your last name")
    v_phone = st.text_input("Contact Number", placeholder="+91-XXXXX-XXXXX")
    
avail = st.selectbox("Availability Status", ["Full-time", "Part-time"])

st.markdown("#### 🎓 Section 2: Qualifications & Languages")
native = st.text_input("Mother Tongue (Native Language) *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations", placeholder="e.g., English-Japanese, German-English")

st.markdown("#### 🏦 Section 3: Bank Vault & Financials")
col3, col4 = st.columns(2)
with col3:
    b_name = st.text_input("Bank Name")
    b_ifsc = st.text_input("IFSC / SWIFT Code")
with col4:
    b_acc = st.text_input("Account Number")
    b_tax = st.text_input("PAN Card Number")
    
st.markdown("#### 📥 Section 4: Download Official Templates")

def get_file_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f:
                return f.read()
        except:
            return b""
    return b""

nda_data = get_file_data("Fidel_NDA_Ver 1.3.pdf")
po_data = get_file_data("Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf")
consent_data = get_file_data("Fidel Consent Form.pdf")

d_col1, d_col2, d_col3 = st.columns(3)
with d_col1:
    st.download_button("📥 Download NDA Template", data=nda_data, file_name="Fidel_NDA_Ver 1.3.pdf", mime="application/pdf", disabled=(len(nda_data) == 0))
with d_col2:
    st.download_button("📥 Download PO Terms", data=po_data, file_name="Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf", mime="application/pdf", disabled=(len(po_data) == 0))
with d_col3:
    st.download_button("📥 Download Consent Form", data=consent_data, file_name="Fidel Consent Form.pdf", mime="application/pdf", disabled=(len(consent_data) == 0))

if len(nda_data) == 0 or len(po_data) == 0 or len(consent_data) == 0:
    st.info("💡 Tip: Upload your blank template PDFs to GitHub to fully activate the download buttons above.")

st.markdown("#### 📤 Section 5: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf'])

st.markdown("---")
if st.button("Submit Profile Record", type="primary"):
    # Cleaned, precise check for empty string text values
    if f_name.strip() == "" or v_email.strip() == "" or native.strip() == "":
        st.error("❌ Please fill out all mandatory profile fields marked with an asterisk (*).")
    else:
        st.balloons()
        st.success("🎉 Profile submitted successfully!")
        
        # Display the captured structured package summary
        submission_summary = {
            "First Name": f_name,
            "Last Name": l_name,
            "Email": v_email,
            "Mother Tongue": native,
            "Language Pairs": lang_pairs
        }
        st.json(submission_summary)
