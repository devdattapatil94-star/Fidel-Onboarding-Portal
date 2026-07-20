import streamlit as st
import os
import io
import zipfile
import pandas as pd
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & INTAKE SETTINGS
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

TARGET_EMAIL = "vendor-mgmt@fideltech.com"

# Helper function to read local template files securely
def get_file_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f: 
                return f.read()
        except: 
            return b""
    return b""

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

st.markdown("Please complete the official empanelment profile form below, complete the translation test task, and upload your paperwork.")
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
 
st.markdown("#### 📥 Section 4: Download Standard Templates")
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

# ==========================================
# 📝 SECTION 5: TRANSLATION EVALUATION TEST
# ==========================================
st.markdown("#### 📝 Section 5: Mandatory Translation Evaluation Test")
st.write("Select your translation track below, download the respective assignment file, and upload your completed translation.")

test_track = st.selectbox("Select Translation Test Track *", [
    "-- Choose Track --", 
    "English to Indian Languages", 
    "English to Japanese", 
    "Japanese to English"
])

test_file_data = b""
target_filename = ""

if test_track == "English to Indian Languages":
    target_filename = "Test_English_to_Indian.docx"
elif test_track == "English to Japanese":
    target_filename = "Test_English_to_Japanese.docx"
elif test_track == "Japanese to English":
    target_filename = "Test_Japanese_to_English.docx"

if target_filename:
    test_file_data = get_file_data(target_filename)
    if len(test_file_data) > 0:
        st.download_button(
            label=f"📥 Download {test_track} Test File",
            data=test_file_data,
            file_name=target_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="secondary"
        )
    else:
        st.warning(f"⚠️ {target_filename} not found in the repository root path.")

file_test_attempt = st.file_uploader("Upload Your Completed Translation Test File *", type=['txt', 'doc', 'docx', 'pdf'])

# ==========================================
# 📤 Section 6: Compliance Documentation Submission
# ==========================================
st.markdown("#### 📤 Section 6: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3) *", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines *", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent *", type=['pdf'])
 
# ==========================================
# 🏅 Section 7: Additional Credentials & Certifications
# ==========================================
st.markdown("#### 🏅 Section 7: Additional Credentials & Certifications")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates *", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter *", type=['pdf', 'doc', 'docx'])
 
st.markdown("---")
 
# ==========================================
# 4. SUBMISSION VALIDATION ENGINE
# ==========================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit Onboarding Registration", type="primary"):
    # Clean check logic handling text values directly
    v_first_name = bool(f_name and f_name.strip())
    v_last_name = bool(l_name and l_name.strip())
    v_email_id = bool(v_email and v_email.strip())
    v_contact = bool(v_phone_local and v_phone_local.strip())
    v_city = bool(addr_city and addr_city.strip())
    v_country = bool(addr_country and addr_country.strip())
    v_native = bool(native and native.strip())
    v_work_lang = bool(lang_pairs and lang_pairs.strip())
    v_services = len(selected_services) > 0
    
    # Check logic handling file drop criteria
    v_track = test_track != "-- Choose Track --"
    v_test_file = file_test_attempt is not None
    v_compliance = (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    
    # Section 7 specific criteria (Educational and Reference files are required, Translation Cert is optional)
    v_section7 = (file_edu is not None) and (file_ref is not None)

    # Trigger complete strict validation execution pass
    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_work_lang and v_services and v_track and 
        v_test_file and v_compliance and v_section7):
        st.session_state.submitted = True
        st.rerun()
    else:
        st.error("❌ Submission Failed. Please make sure all mandatory fields (*) are complete and all files are uploaded.")

# ==========================================
# 5. CONCORDANCE AND ZIP COMPOSER PAD (.XLSX)
# ==========================================
if st.session_state.submitted:
    full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
    clean_name = full_vendor_name.replace(' ', '_')
    
    # Horizontal column formatting strategy matching matrix layout perfectly
    vendor_data = {
        "Registration Date": [datetime.now().strftime("%Y-%m-%d %H:%M")],
        "First Name": [f_name.strip()],
        "Last Name": [l_name.strip()],
        "Email ID": [v_email.strip()],
        "Contact Number": [v_phone],
        "Availability Status": [avail],
        "Street Address": [f"{addr_street} {addr_street2}".strip()],
        "City": [addr_city.strip()],
        "State": [addr_state.strip()],
        "Zip Code": [addr_zip.strip()],
        "Country": [addr_country.strip()],
        "Native Language": [native.strip()],
        "Experience (Years)": [exp],
        "Language Combinations": [lang_pairs.strip()],
        "CAT Tools": [', '.join(selected_cat_tools) if selected_cat_tools else "None"],
        "Domain Expertise": [', '.join(selected_domains) if selected_domains else "None"],
        "Services Provided": [', '.join(selected_services)],
        "Bank Name": [b_name.strip()],
        "Account Holder": [b_holder.strip()],
        "Bank Code": [b_code.strip()],
        "Account Number": [b_acc.strip()],
        "IFSC Code": [b_ifsc.strip()],
        "Swift Code": [b_swift.strip()],
        "PAN Card": [b_tax.strip()],
        "GST Number": [b_gst.strip()],
        "PayPal ID": [pay_paypal.strip()],
        "Payoneer ID": [pay_payoneer.strip()],
        "ProZ Link": [pay_proz.strip()],
        "Translation Test Track": [test_track],
        "Test File Name": [file_test_attempt.name]
    }
    
    df_individual = pd.DataFrame(vendor_data)
    
    # Compress matrix out to in-memory byte buffer streams
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df_individual.to_excel(writer, index=False, sheet_name="Vendor Onboarding Matrix")
    excel_data = excel_buffer.getvalue()
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f"{clean_name}_Registration_Details.xlsx", excel_data)
        
        uploaded_files = [
            (file_nda, "Signed_NDA"), 
            (file_po, "Signed_PO"), 
            (file_consent, "Signed_Data_Consent"),
            (file_test_attempt, "Completed_Translation_Test"),
            (file_edu, "Educational_Certificates"), 
            (file_ref, "Reference_Letter"), 
            (file_cert, "Translation_Certificate")
        ]
        
        for file_obj, filename_prefix in uploaded_files:
            if file_obj is not None:
                ext = os.path.splitext(file_obj.name)[1]
                zip_file.writestr(f"{filename_prefix}{ext}", file_obj.getvalue())
                
    zip_buffer.seek(0)
    
    st.info("ℹ️ Your registration data files have been verified and bundled successfully.")
    st.markdown("---")
    st.markdown("### 📧 Final Step: Dispatch Packages to Vendor Management")
    st.write("Follow these two quick steps to send your documentation straight to our team:")
    
    act_col1, act_col2 = st.columns(2)
    
    with act_col1:
        st.markdown("**Step 1:** Download the complete package.")
        st.download_button(
            label="📥 Download Onboarding Package (.zip)",
            data=zip_buffer.getvalue(),
            file_name=f"{clean_name}_Onboarding_Package.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        
    with act_col2:
        st.markdown("**Step 2:** Open email client dashboard.")
        email_subject = f"Onboarding Registration Submission - {full_vendor_name}"
        email_body = f"Hello VM Team,\n\nPlease find attached my unified resource onboarding folder package containing my registration details Excel sheet and signed compliance documentation.\n\nBest Regards,\n{full_vendor_name}"
        mailto_link = f"mailto:{TARGET_EMAIL}?subject={email_subject.replace(' ', '%20')}&body={email_body.replace(' ', '%20').replace('\n', '%0A')}"
        
        st.markdown(
            f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;">'
            f'<button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; font-size:16px; '
            f'border-radius:4px; cursor:pointer; width:100%; height:45px; margin-top:2px;">📨 Open Corporate Mail Client</button></a>', 
            unsafe_allow_html=True
        )
        
    st.info("💡 **Tip:** After you click Step 1 to download the file, hit Step 2. Your email app will instantly open up pre-addressed, and you can just drag the zip file from your download bar directly into that message window!")
