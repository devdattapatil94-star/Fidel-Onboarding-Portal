import streamlit as st
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ==========================================
# 1. PAGE CONFIGURATION & SMTP MAIL SETTINGS
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

# SMTP Server Configurations (Update these with your corporate mail server details)
SMTP_SERVER = "smtp.fideltech.com"  # e.g., smtp.gmail.com, mail.fideltech.com, etc.
SMTP_PORT = 587                    # Standard TLS port
SENDER_EMAIL = "system-onboarding@fideltech.com"
SENDER_PASSWORD = "YOUR_SYSTEM_EMAIL_PASSWORD_HERE"

TARGET_EMAIL = "vendor-mgmt@fideltech.com"

# ==========================================
# 2. SMTP MAIL DISPATCH HELPER
# ==========================================
def send_onboarding_email_smtp(vendor_name, profile_text, file_attachments):
    """Dispatches an email containing the text summary and binary attachments using standard secure SMTP."""
    # Create the root message container
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = TARGET_EMAIL
    msg['Subject'] = f"🚀 New Resource Onboarding Submission: {vendor_name}"
    
    # Define HTML email body cover note
    body_content = f"""
    <h3>Fidel Softech Resource Empanelment Alert</h3>
    <p>A new linguist profile record has been submitted by <strong>{vendor_name}</strong>.</p>
    <p>Please find the profile summary text file and all signed compliance documentation attachments appended to this email.</p>
    <br>
    <hr>
    <small>Automated System Message - Operational Management Portal</small>
    """
    msg.attach(MIMEText(body_content, 'html'))
    
    # 1. Attach the generated Profile Details text file layout sheet
    profile_part = MIMEBase('text', 'plain')
    profile_part.set_payload(profile_text.encode('utf-8'))
    encoders.encode_base64(profile_part)
    profile_part.add_header('Content-Disposition', f"attachment; filename={vendor_name.replace(' ', '_')}_Profile_Details.txt")
    msg.attach(profile_part)
    
    # 2. Attach all uploaded compliance documents sequentially
    for file_name, file_bytes in file_attachments:
        attachment_part = MIMEBase('application', 'octet-stream')
        attachment_part.set_payload(file_bytes)
        encoders.encode_base64(attachment_part)
        attachment_part.add_header('Content-Disposition', f"attachment; filename={file_name}")
        msg.attach(attachment_part)
        
    # Connect to the secure server instance loop and send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade connection encryption mapping to TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, TARGET_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Mail Server Connection Failure: {e}")
        return False

# ==========================================
# 3. HEADER LAYOUT (LOGO & TITLE SIDE-BY-SIDE)
# ==========================================
logo_path = "FIDEL.NSE.png"
col_logo, col_title = st.columns([0.6, 4.4], vertical_alignment="center")
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=85)
    else:
        st.warning("⚠️ Place FIDEL.NSE.png in your repo")
with col_title:
    st.markdown("<h1 style='margin: 0; padding: 0; font-size: 2.25rem; white-space: nowrap;'>Fidel Softech Resource Onboarding</h1>", unsafe_allow_html=True)

st.markdown("Please complete the official empanelment profile form below and upload your signed compliance agreements.")
st.markdown("---")

st.subheader("📄 Resource Empanelment Profile")

# ==========================================
# 4. FORM SECTIONS
# ==========================================
st.markdown("#### 👤 Section 1: Personal Information")
col1, col2 = st.columns(2)
with col1:
    f_name = st.text_input("First Name *", placeholder="Enter your first name")
    v_email = st.text_input("Email ID *", placeholder="example@email.com")
with col2:
    l_name = st.text_input("Last Name *", placeholder="Enter your last name")
    
    st.markdown("<label style='font-size: 14px;'>Contact Number *</label>", unsafe_allow_html=True)
    c_code_col, phone_num_col = st.columns([1, 2])
    with c_code_col:
        all_country_codes = ["+91 (India)", "+1 (USA/Canada)", "+44 (UK)", "+81 (Japan)", "+49 (Germany)", "+33 (France)", "+61 (Australia)"]
        selected_code = st.selectbox("Code", all_country_codes, label_visibility="collapsed")
    with phone_num_col:
        v_phone_local = st.text_input("Phone Number", placeholder="XXXXX-XXXXX", label_visibility="collapsed")
    
    v_phone = f"{selected_code.split(' ')[0]} {v_phone_local.strip()}" if v_phone_local.strip() else ""
    
avail = st.selectbox("Availability Status", ["Full-time", "Part-time"])
 
st.markdown("##### 🏠 Address Information")
col_addr1, col_addr2 = st.columns(2)
with col_addr1:
    addr_street = st.text_input("Street")
    addr_zip = st.text_input("Zip Code")
    addr_state = st.text_input("State")
with col_addr2:
    addr_street2 = st.text_input("Street 2")
    addr_city = st.text_input("City *")
    addr_country = st.text_input("Country *")
 
st.markdown("#### 🎓 Section 2: Qualifications & Languages")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations *", placeholder="e.g., English-Japanese, German-English")
 
cat_options = ["Across", "Amazon (ATMS)", "Bureau Works (BWX)", "Crowdin", "MemoQ", "Phrase", "SDL Trados 2022", "XTM Cloud"]
selected_cat_tools = st.multiselect("Proficient in which of the following CAT Tools:", cat_options)
 
domain_options = ["Accounting", "Administrative", "Advertising", "Artificial Intelligence", "Banking & Finance", "Legal", "Medical"]
selected_domains = st.multiselect("Domain Expertise:", domain_options)
 
services_options = ["AI Voice-Over", "Editing", "Localization Testing", "Subtitling", "Translation"]
selected_services = st.multiselect("Services you provide *:", services_options)
 
st.markdown("#### 🏦 Section 3: Payment Details")
col_fin1, col_fin2 = st.columns(2)
with col_fin1:
    b_name = st.text_input("Bank Name")
    b_holder = st.text_input("Account Holder Name")
    b_code = st.text_input("Bank Code")
    b_acc = st.text_input("Account Number")
with col_fin2:
    b_ifsc = st.text_input("IFSC Code")
    b_swift = st.text_input("Swift Code")
    b_address = st.text_area("Bank Address", height=68)
    b_country = st.text_input("Bank Country")
 
col_tax1, col_tax2 = st.columns(2)
with col_tax1:
    b_tax = st.text_input("PAN Card")
with col_tax2:
    b_gst = st.text_input("GST Number")
 
st.markdown("##### 💳 Alternative Global Payment Systems")
col_alt1, col_alt2 = st.columns(2)
with col_alt1:
    pay_paypal = st.text_input("PayPal ID")
    pay_payoneer = st.text_input("Payoneer Code / ID")
with col_alt2:
    pay_proz = st.text_input("ProZ*Pay Link")
 
st.markdown("#### 📥 Section 4: Download Templates")
def get_file_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f: return f.read()
        except: return b""
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
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3) *", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines *", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent *", type=['pdf'])
 
st.markdown("#### 🏅 Section 6: Additional Credentials & Certifications")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates *", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter *", type=['pdf', 'doc', 'docx'])
 
st.markdown("---")
 
# ==========================================
# 5. SUBMISSION PIPELINE (SMTP SECURE EMAIL DISPATCH)
# ==========================================
if st.button("Submit Profile Record", type="primary"):
    v_first_name = len(f_name.strip()) > 0
    v_last_name = len(l_name.strip()) > 0
    v_email_id = len(v_email.strip()) > 0
    v_contact = len(v_phone.strip()) > 0
    v_city = len(addr_city.strip()) > 0
    v_country = len(addr_country.strip()) > 0
    v_native = len(native.strip()) > 0
    v_work_lang = len(lang_pairs.strip()) > 0
    v_services = len(selected_services) > 0
    v_compliance = (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    v_edu_docs = file_edu is not None
    v_ref_doc = file_ref is not None
    
    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_work_lang and v_services and v_compliance and 
        v_edu_docs and v_ref_doc):
        
        full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
        
        with st.spinner("Processing metadata profiles and executing secure email dispatch..."):
            
            # 1. Compile vendor resource dataset sheet text layout details
            profile_report = (
                f"FIDEL SOFTECH RESOURCE PROFILE DATA\n"
                f"==================================\n"
                f"Name: {full_vendor_name}\n"
                f"Email: {v_email.strip()} | Phone: {v_phone}\n"
                f"Address: {addr_street}, {addr_city}, {addr_state}, {addr_country}\n"
                f"Native Language: {native.strip()} | Pairs: {lang_pairs.strip()}\n"
                f"Services: {', '.join(selected_services)}\n"
                f"CAT Tools: {', '.join(selected_cat_tools)}\n\n"
                f"FINANCIAL DATA:\n"
                f"Bank: {b_name} | Acc Holder: {b_holder}\n"
                f"Code/Number: {b_code} / {b_acc}\n"
                f"IFSC/Swift: {b_ifsc} / {b_swift}\n"
                f"PAN Card: {b_tax} | GST: {b_gst}\n"
                f"Alternates: PayPal: {pay_paypal} | Payoneer: {pay_payoneer} | ProZ: {pay_proz}"
            )
            
            # 2. Package all uploaded compliance file data buffers
            raw_attachments = []
            files_to_package = [
                (file_nda, "Signed_NDA"), (file_po, "Signed_PO"), (file_consent, "Signed_Data_Consent"),
                (file_edu, "Educational_Certificates"), (file_ref, "Reference_Letter"), (file_cert, "Translation_Certificate")
            ]
            
            for file_obj, prefix in files_to_package:
                if file_obj is not None:
                    raw_attachments.append((f"{prefix}_{file_obj.name}", file_obj.getvalue()))
            
            # 3. Dispatch the complete email via internal server configurations
            success = send_onboarding_email_smtp(full_vendor_name, profile_report, raw_attachments)
            
            if success:
                st.success(f"🎉 Onboarding Complete! Your profile and signed files have been sent to {TARGET_EMAIL} successfully.")
            else:
                st.error("❌ Notification Delivery Failed. Please review SMTP configurations or network controls.")
    else:
        st.error("❌ Submission Failed. Please make sure all mandatory inputs (*) are filled and files uploaded.")
