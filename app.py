import streamlit as st
from datetime import datetime
import os
import requests
import base64

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Fidel Softech Onboarding", page_icon="🌐", layout="centered")

# ==========================================
# 2. CUSTOM BACKGROUND & WATERMARK CONFIGURATION
# ==========================================
bg_logo_path = "fidel_bg_logo.png"
if os.path.exists(bg_logo_path):
    with open(bg_logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    
    custom_style = f'''
    <style>
    .stApp, [data-testid="stHeader"], [data-testid="stSidebar"] {{
        background-color: #FFFFFF !important;
    }}
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1;
        background-image: url("data:image/png;base64,{encoded_logo}");
        background-repeat: no-repeat; background-position: center center; background-size: 40%;
        opacity: 0.05; pointer-events: none;
    }}
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p {{
        color: #1E293B !important;
    }}
    </style>
    '''
    st.markdown(custom_style, unsafe_allow_html=True)
else:
    st.markdown('''<style>.stApp {{ background-color: #FFFFFF !important; }} h1, h2, h3, h4, h5, h6, p, label {{ color: #1E293B !important; }}</style>''', unsafe_allow_html=True)

# ==========================================
# 3. HEADER BANNER SECTION
# ==========================================
banner_path = "fidel_banner.png"
if os.path.exists(banner_path):
    st.image(banner_path, use_column_width=True)

st.markdown("<h1 style='margin-top: 20px; margin-bottom: 5px; font-size: 2.3rem;'>Resource Onboarding Portal</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-size: 15px; margin-top: 5px;'>Please complete the official empanelment profile form below and upload your signed compliance agreements.</p>", unsafe_allow_html=True)
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
        all_country_codes = ["+91 (India)", "+1 (USA/Canada)", "+44 (UK)", "+81 (Japan)", "+49 (Germany)", "+33 (France)", "+61 (Australia)", "+971 (UAE)", "+65 (Singapore)"] # Truncated for clarity, add others as needed
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

# ==========================================
# 5. FILE UPLOADS & WEBHOOK LOGIC
# ==========================================
st.markdown("#### 📤 Section 4: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3) *", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines *", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent *", type=['pdf'])

st.markdown("#### 🏅 Section 5: Additional Credentials")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates *", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter *", type=['pdf', 'doc', 'docx'])

st.markdown("---")

GOOGLE_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyYs4qak8MwQDXnB2Cwaynr-qALR7IeUKOeAgddeedO1naOPn60F5xEZOhFo7OZyoGwmg/exec"

if st.button("Submit Profile Record", type="primary"):
    v_first_name = len(f_name.strip()) > 0
    v_last_name = len(l_name.strip()) > 0
    v_email_id = len(v_email.strip()) > 0
    
    if v_first_name and v_last_name and v_email_id:
        with st.spinner("Submitting your profile..."):
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
                if file_cert: package_file(file_cert, "Translation_Certificate")
                
                profile_report = f"FIDEL SOFTECH RESOURCE PROFILE DATA\n"                                  f"==================================\n"                                  f"**Name:** {f_name.strip()} {l_name.strip()}\n"                                  f"**Email:** {v_email.strip()} | **Phone:** {v_phone}\n"                                  f"**Native Language:** {native.strip()} | **Pairs:** {lang_pairs.strip()}\n"                                  f"**Bank:** {b_name} | **PAN Card:** {b_tax} | **GST:** {b_gst}"
                
                json_data = {
                    "folder_name": f"{f_name.strip()} {l_name.strip()}",
                    "profile_text": profile_report,
                    "files": payload_files
                }
                
                response = requests.post(GOOGLE_WEBHOOK_URL, json=json_data)
                
                if response.status_code == 200 and "error" not in response.text.lower():
                    st.success("🎉 Empanelment Complete! Welcome to Fidel Softech.")
                else:
                    st.error(f"❌ Upload Warning: {response.text}")
            except Exception as e:
                st.error(f"❌ Pipeline Error: {e}")
    else:
        st.error("❌ Submission Failed. Please complete all required fields (*).")

# ==========================================
# 6. FOOTER BANNER SECTION
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)

footer_path = "fidel_footer.png"
if os.path.exists(footer_path):
    st.image(footer_path, use_column_width=True)
