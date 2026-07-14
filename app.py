import streamlit as st
from datetime import datetime
import os
import requests

st.set_page_config(page_title="Fidel Vendor Onboarding", page_icon="🌐", layout="centered")

# --- Target Inbox for Onboarding Notifications ---
NOTIFICATION_EMAIL = "vendor-mgmt@fideltech.com" 

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

st.markdown("#### 📤 Section 5: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf'])

st.markdown("---")

if st.button("Submit Profile Record", type="primary"):
    has_first_name = len(f_name.strip()) > 0
    has_email = len(v_email.strip()) > 0
    has_native_lang = len(native.strip()) > 0
    
    if has_first_name and has_email and has_native_lang:
        
        email_payload = {
            "Subject": f"🚨 New Vendor Registration: {f_name} {l_name}",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "First Name": f_name.strip(),
            "Last Name": l_name.strip(),
            "Email": v_email.strip(),
            "Phone": v_phone.strip(),
            "Availability": avail,
            "Native Language": native.strip(),
            "Language Pairs": lang_pairs.strip(),
            "Bank Name": b_name.strip(),
            "Account Number": b_acc.strip(),
            "IFSC Code": b_ifsc.strip(),
            "PAN Card": b_tax.strip(),
            "Uploaded NDA": "Yes" if file_nda else "No",
            "Uploaded PO": "Yes" if file_po else "No",
            "Uploaded Consent": "Yes" if file_consent else "No"
        }
        
        try:
            formsubmit_url = f"https://formsubmit.co/ajax/{NOTIFICATION_EMAIL}"
            response = requests.post(formsubmit_url, data=email_payload)
            
            if response.status_code == 200:
                st.balloons()
                st.success("🎉 Onboarding profile submitted successfully! An alert has been sent to the PM team.")
                st.json(email_payload)
            else:
                st.error("⚠️ Profile processed, but notification dispatch failed. Please check the API status.")
        except Exception as e:
            st.error(f"❌ Connection error during email dispatch: {e}")
            
    else:
        missing_fields = []
        if not has_first_name: missing_fields.append("First Name")
        if not has_email: missing_fields.append("Email ID")
        if not has_native_lang: missing_fields.append("Mother Tongue")
        st.error(f"❌ Submission Failed. Please fill out the required fields: {', '.join(missing_fields)}")
