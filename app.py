import streamlit as st
import os

# ==========================================
# 1. PAGE CONFIGURATION & INTAKE SETTINGS
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

TARGET_EMAIL = "vendor_mgmt@fideltech.com"

# ==========================================
# 2. HEADER LAYOUT (LOGO & TITLE SIDE-BY-SIDE)
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
# 3. FORM SECTIONS
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
# 4. SUBMISSION DATA PACKAGE GENERATOR
# ==========================================
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
    
    # Compile text configuration summary content
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
    
    st.success("✅ Profile completed successfully! Click the button below to save your generated details summary.")
    
    # Expose a clean, localized download generation link anchor
    st.download_button(
        label="📥 Download Profile Details File",
        data=profile_report,
        file_name=f"{full_vendor_name.replace(' ', '_')}_Profile_Details.txt",
        mime="text/plain",
        type="primary"
    )
    
    st.info(f"📧 **Next Step:** Please email the downloaded text details sheet along with your signed compliance documents directly to **{TARGET_EMAIL}**.")
else:
    st.warning("⚠️ Complete all required fields marked with an asterisk (*) to unlock your Profile Generation download button.")
