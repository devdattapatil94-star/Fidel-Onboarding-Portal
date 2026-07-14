import streamlit as st
from datetime import datetime
import os
import streamlit.components.v1 as components

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
        st.balloons()
        st.success("🎉 Onboarding Profile Submitted Successfully!")
        
        # Format the data cleanly to present to the coordinator
        submission_summary = {
            "Vendor Name": f"{f_name.strip()} {l_name.strip()}",
            "Email Address": v_email.strip(),
            "Contact Phone": v_phone.strip(),
            "Availability": avail,
            "Native Language": native.strip(),
            "Language Pairs": lang_pairs.strip(),
            "Bank Details": f"{b_name} | Acc: {b_acc} | IFSC: {b_ifsc}",
            "PAN Card": b_tax.strip(),
            "NDA Provided": "Yes" if file_nda else "No",
            "PO Signed": "Yes" if file_po else "No",
            "Consent Given": "Yes" if file_consent else "No"
        }
        st.json(submission_summary)
        
        # Build an automated mailto link that packages everything natively for your Outlook/Email Client
        body_text = f"🚨 NEW VENDOR REGISTRATION DATA%0A%0A"                     f"Full Name: {f_name.strip()} {l_name.strip()}%0A"                     f"Email ID: {v_email.strip()}%0A"                     f"Phone: {v_phone.strip()}%0A"                     f"Availability: {avail}%0A"                     f"Native Language: {native.strip()}%0A"                     f"Language Pairs: {lang_pairs.strip()}%0A"                     f"Bank: {b_name} | Acc: {b_acc} | IFSC: {b_ifsc}%0A"                     f"PAN Card Number: {b_tax.strip()}%0A"                     f"NDA Uploaded: {'Yes' if file_nda else 'No'}%0A"                     f"PO Terms Signed: {'Yes' if file_po else 'No'}%0A"                     f"Consent Form Uploaded: {'Yes' if file_consent else 'No'}"
        
        mailto_url = f"mailto:vendor-mgmt@fideltech.com?subject=New Onboarding Registration - {f_name.strip()} {l_name.strip()}&body={body_text}"
        
        st.markdown(f'<a href="{mailto_url}" target="_blank" style="display: inline-block; padding: 0.5rem 1rem; background-color: #ff4b4b; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 10px;">✉️ Click to Route Profile directly to Vendor Management Inbox</a>', unsafe_allow_html=True)
        
    else:
        missing_fields = []
        if not has_first_name: missing_fields.append("First Name")
        if not has_email: missing_fields.append("Email ID")
        if not has_native_lang: missing_fields.append("Mother Tongue")
        st.error(f"❌ Submission Failed. Required: {', '.join(missing_fields)}")
