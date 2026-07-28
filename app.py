import streamlit as st
from datetime import datetime
import os
import requests
import base64

# Set up the tab title and use the local logo for the browser icon if available
logo_path = "FIDEL.NSE.png"
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon=logo_path if os.path.exists(logo_path) else "🌐",
    layout="centered"
)

# Render the company logo and the portal title
col_logo, col_title = st.columns([1, 4])
with col_logo:
    if os.path.exists(logo_path):
        st.image(logo_path, width=90)
    else:
        st.warning("⚠️ Place FIDEL.NSE.png in your GitHub repo")
with col_title:
    st.title("Fidel Softech Resource Onboarding")

st.markdown("Please complete the official empanelment profile form below and upload your signed compliance agreements.")
st.markdown("---")

st.subheader("📄 Resource Empanelment Profile")

# --- SECTION 1 ---
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
        all_country_codes = [
            "+91 (India)", "+1 (USA/Canada)", "+44 (UK)", "+81 (Japan)", "+49 (Germany)", "+33 (France)", 
            "+61 (Australia)", "+86 (China)", "+7 (Russia)", "+39 (Italy)", "+34 (Spain)", "+971 (UAE)", 
            "+65 (Singapore)", "+55 (Brazil)", "+27 (South Africa)", "+82 (South Korea)", "+41 (Switzerland)", 
            "+31 (Netherlands)"
        ]
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

# --- SECTION 2 ---
st.markdown("#### 🎓 Section 2: Qualifications, Languages & Rates")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations *", placeholder="e.g., English-Japanese, German-English")

# UPDATED CAT TOOLS LIST
cat_options = [
    "MateCat", 
    "MemoQ", 
    "Memsource", 
    "Phrase", 
    "SDL Trados 2019", 
    "SDL Trados 2021", 
    "SDL Trados 2022", 
    "SmartCAT", 
    "WordFast"
]
selected_cat_tools = st.multiselect("Proficient in which of the following CAT Tools:", cat_options)

domain_options = ["Accounting", "Administrative", "Advertising", "Artificial Intelligence", "Banking & Finance", "Legal", "Medical"]
selected_domains = st.multiselect("Domain Expertise:", domain_options)

services_options = ["AI Voice-Over", "Editing", "Localization Testing", "Subtitling", "Translation"]
selected_services = st.multiselect("Services you provide *:", services_options)

# MANDATORY RATE FIELD SECTION
st.markdown("##### 💰 Mandatory Service Rates & Pricing *")
rate_curr_col, rate_trans_col, rate_edit_col = st.columns(3)
with rate_curr_col:
    rate_currency = st.selectbox("Preferred Currency *", ["USD ($)", "JPY (¥)", "INR (₹)", "EUR (€)", "GBP (£)"])
with rate_trans_col:
    rate_per_word = st.number_input("Translation Rate (per word) *", min_value=0.000, step=0.001, format="%.3f")
with rate_edit_col:
    rate_per_hour = st.number_input("Editing/Review Rate (per hour) *", min_value=0.00, step=0.50, format="%.2f")

# --- SECTION 3 ---
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

# --- SECTION 4 ---
st.markdown("#### 📥 Section 4: Download Official Documents")
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
    st.download_button("📥 Download NDA Template", data=nda_data if nda_data else b"", file_name="Fidel_NDA_Ver 1.3.pdf", mime="application/pdf", disabled=(len(nda_data) == 0))
with d_col2:
    st.download_button("📥 Download PO Terms", data=po_data if po_data else b"", file_name="Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf", mime="application/pdf", disabled=(len(po_data) == 0))
with d_col3:
    st.download_button("📥 Download Consent Form", data=consent_data if consent_data else b"", file_name="Fidel Consent Form.pdf", mime="application/pdf", disabled=(len(consent_data) == 0))

# --- SECTION 5 ---
st.markdown("#### 📤 Section 5: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3) *", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines *", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent *", type=['pdf'])

# --- SECTION 6 ---
st.markdown("#### 🏅 Section 6: Additional Credentials & Certifications")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates *", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter *", type=['pdf', 'doc', 'docx'])

st.markdown("---")

GOOGLE_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyYs4qak8MwQDXnB2Cwaynr-qALR7IeUKOeAgddeedO1naOPn60F5xEZOhFo7OZyoGwmg/exec"

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
    v_rates = (rate_per_word > 0.0) or (rate_per_hour > 0.0)
    v_compliance = (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    v_edu_docs = file_edu is not None
    v_ref_doc = file_ref is not None
    
    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_work_lang and v_services and v_rates and 
        v_compliance and v_edu_docs and v_ref_doc):
        
        with st.spinner("Submitting..."):
            try:
                payload_files = []
                
                def package_file(uploaded_file, custom_name):
                    if uploaded_file is not None:
                        b64_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        mtype = uploaded_file.type if hasattr(uploaded_file, 'type') and uploaded_file.type else "application/pdf"
                        payload_files.append({
                            "name": f"{custom_name}_{uploaded_file.name}",
                            "mimeType": mtype,
                            "bytes": b64_data
                        })
                
                package_file(file_nda, "Signed_NDA")
                package_file(file_po, "Signed_PO")
                package_file(file_consent, "Signed_Data_Consent")
                package_file(file_edu, "Educational_Certificates")
                package_file(file_ref, "Reference_Letter")
                if file_cert:
                    package_file(file_cert, "Translation_Certificate")
                
                profile_report = f"FIDEL SOFTECH RESOURCE PROFILE DATA\n" \
                                 f"==================================\n" \
                                 f"**Name:** {f_name.strip()} {l_name.strip()}\n" \
                                 f"**Email:** {v_email.strip()} | **Phone:** {v_phone}\n" \
                                 f"**Address:** {addr_street}, {addr_city}, {addr_state}, {addr_country}\n" \
                                 f"**Native Language:** {native.strip()} | **Pairs:** {lang_pairs.strip()}\n" \
                                 f"**Services:** {', '.join(selected_services)}\n" \
                                 f"**CAT Tools:** {', '.join(selected_cat_tools)}\n" \
                                 f"**RATES:** {rate_currency} | Per Word: {rate_per_word:.3f} | Per Hour: {rate_per_hour:.2f}\n\n" \
                                 f"FINANCIAL DATA:\n" \
                                 f"**Bank:** {b_name} | **Acc Holder:** {b_holder}\n" \
                                 f"**Code/Number:** {b_code} / {b_acc}\n" \
                                 f"**IFSC/Swift:** {b_ifsc} / {b_swift}\n" \
                                 f"**PAN Card:** {b_tax} | **GST:** {b_gst}\n" \
                                 f"**Alternates:** PayPal: {pay_paypal} | Payoneer: {pay_payoneer} | ProZ: {pay_proz}"
                
                json_data = {
                    "folder_name": f"{f_name.strip()} {l_name.strip()}",
                    "profile_text": profile_report,
                    "files": payload_files
                }
                
                response = requests.post(GOOGLE_WEBHOOK_URL, json=json_data)
                
                if response.status_code == 200 and "error" not in response.text.lower():
                    st.success("Empanelment Complete!")
                else:
                    st.error(f"❌ Upload Bridge Warning: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Gateway Pipeline Error: {e}")
    else:
        missing_fields = []
        if not v_first_name: missing_fields.append("First Name")
        if not v_last_name: missing_fields.append("Last Name")
        if not v_email_id: missing_fields.append("Email ID")
        if not v_contact: missing_fields.append("Contact Number")
        if not v_city: missing_fields.append("City")
        if not v_country: missing_fields.append("Country")
        if not v_native: missing_fields.append("Native Language")
        if not v_work_lang: missing_fields.append("Working Language Combinations")
        if not v_services: missing_fields.append("Services you provide")
        if not v_rates: missing_fields.append("Mandatory Service Rates")
        if not v_compliance: missing_fields.append("Compliance Documentation Submission")
        if not v_edu_docs: missing_fields.append("Educational Qualification Certificates")
        if not v_ref_doc: missing_fields.append("Reference or Recommendation Letter")
        
        st.error(f"❌ Submission Failed. Missing: {', '.join(missing_fields)}")
