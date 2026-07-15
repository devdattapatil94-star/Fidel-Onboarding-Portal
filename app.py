import streamlit as st
import os
import io
import zipfile

# ==========================================
# 1. PAGE CONFIGURATION & INTAKE SETTINGS
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

TARGET_EMAIL = "vendor-mgmt@fideltech.com"

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
# 4. SUBMISSION VALIDATION ENGINE
# ==========================================
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if st.button("Submit Onboarding Registration", type="primary"):
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
        st.session_state.submitted = True
    else:
        st.error("❌ Submission Failed. Please make sure all mandatory fields (*) are complete and all files are uploaded.")

# ==========================================
# 5. CONCORDANCE AND MAIL COMPOSER PAD
# ==========================================
if st.session_state.submitted:
    full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
    clean_name = full_vendor_name.replace(' ', '_')
    
    # Render the configuration data straight into Word-compliant HTML syntax
    # Uses 11pt Calibri where labels are bolded, but user values are standard weight text.
    word_html_doc = f"""<html xmlns:o='urn:schemas-microsoft-com:office:office' xmlns:w='urn:schemas-microsoft-com:office:word' xmlns='http://www.w3.org/TR/REC-html40'>
    <head>
        <title>Fidel Onboarding Data</title>
        <style>
            body {{
                font-family: 'Calibri', sans-serif;
                font-size: 11pt;
                line-height: 1.25;
            }}
            .section-title {{
                font-size: 13pt;
                font-weight: bold;
                border-bottom: 1px solid #000000;
                margin-top: 15pt;
                margin-bottom: 5pt;
            }}
            p {{
                margin: 0 0 4pt 0;
            }}
        </style>
    </head>
    <body>
        <h2>FIDEL SOFTECH RESOURCE PROFILE DATA</h2>
        <hr/>
        
        <div class="section-title">PERSONAL INFORMATION</div>
        <p><b>Name:</b> {full_vendor_name}</p>
        <p><b>Email ID:</b> {v_email.strip()}</p>
        <p><b>Contact Number:</b> {v_phone}</p>
        <p><b>Availability Status:</b> {avail}</p>
        <p><b>Street Address:</b> {addr_street} {addr_street2}</p>
        <p><b>City:</b> {addr_city}</p>
        <p><b>State:</b> {addr_state}</p>
        <p><b>Zip Code:</b> {addr_zip}</p>
        <p><b>Country:</b> {addr_country}</p>
        
        <div class="section-title">QUALIFICATIONS & LANGUAGES</div>
        <p><b>Native Language:</b> {native.strip()}</p>
        <p><b>Years of Experience:</b> {exp}</p>
        <p><b>Working Language Combinations:</b> {lang_pairs.strip()}</p>
        <p><b>CAT Tools Proficiency:</b> {', '.join(selected_cat_tools) if selected_cat_tools else 'None Specified'}</p>
        <p><b>Domain Expertise:</b> {', '.join(selected_domains) if selected_domains else 'None Specified'}</p>
        <p><b>Services Provided:</b> {', '.join(selected_services)}</p>
        
        <div class="section-title">FINANCIAL & BANK DETAILS</div>
        <p><b>Bank Name:</b> {b_name}</p>
        <p><b>Account Holder Name:</b> {b_holder}</p>
        <p><b>Bank Code:</b> {b_code}</p>
        <p><b>Account Number:</b> {b_acc}</p>
        <p><b>IFSC Code:</b> {b_ifsc}</p>
        <p><b>Swift Code:</b> {b_swift}</p>
        <p><b>Bank Address:</b> {b_address}</p>
        <p><b>Bank Country:</b> {b_country}</p>
        <p><b>PAN Card:</b> {b_tax}</p>
        <p><b>GST Number:</b> {b_gst}</p>
        
        <div class="section-title">ALTERNATIVE GLOBAL PAYMENT SYSTEMS</div>
        <p><b>PayPal ID:</b> {pay_paypal}</p>
        <p><b>Payoneer Code / ID:</b> {pay_payoneer}</p>
        <p><b>ProZ*Pay Link:</b> {pay_proz}</p>
    </body>
    </html>"""
    
    # Process memory buffer streams to compress document files dynamically
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Save explicitly as a native .doc Word element file 
        zip_file.writestr(f"{clean_name}_Registration_Details.doc", word_html_doc.encode('utf-8'))
        
        uploaded_files = [
            (file_nda, "Signed_NDA"), 
            (file_po, "Signed_PO"), 
            (file_consent, "Signed_Data_Consent"),
            (file_edu, "Educational_Certificates"), 
            (file_ref, "Reference_Letter"), 
            (file_cert, "Translation_Certificate")
        ]
        
        for file_obj, filename_prefix in uploaded_files:
            if file_obj is not None:
                ext = os.path.splitext(file_obj.name)[1]
                zip_file.writestr(f"{filename_prefix}{ext}", file_obj.getvalue())
                
    zip_buffer.seek(0)
    
    # Standard warning and informational instructions layout
    st.info("ℹ️ Your registration data files have been verified and bundled successfully.")
    st.markdown("---")
    st.markdown("### 📧 Final Step: Dispatch Packages to Vendor Management")
    st.write("Follow these two quick steps to send your documentation straight to our team:")
    
    # Set up actionable step metrics button columns side-by-side
    act_col1, act_col2 = st.columns(2)
    
    with act_col1:
        st.markdown("**Step 1:** Download the complete package.")
        st.download_button(
            label="📥 Download Onboarding Documents (.zip)",
            data=zip_buffer.getvalue(),
            file_name=f"{clean_name}_Onboarding_Documents.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )
        
    with act_col2:
        st.markdown("**Step 2:** Open email client dashboard.")
        email_subject = f"Onboarding Registration Submission - {full_vendor_name}"
        email_body = f"Hello VM Team,\n\nPlease find attached my unified resource onboarding folder package containing my registration details Word file and signed compliance documentation.\n\nBest Regards,\n{full_vendor_name}"
        mailto_link = f"mailto:{TARGET_EMAIL}?subject={email_subject.replace(' ', '%20')}&body={email_body.replace(' ', '%20').replace('\n', '%0A')}"
        
        st.markdown(
            f'<a href="{mailto_link}" target="_blank" style="text-decoration:none;">'
            f'<button style="background-color:#4CAF50; color:white; border:none; padding:10px 20px; font-size:16px; '
            f'border-radius:4px; cursor:pointer; width:100%; height:45px; margin-top:2px;">📨 Open Corporate Mail Client</button></a>', 
            unsafe_allow_html=True
        )
        
    st.info("💡 **Tip:** After you click Step 1 to download the file, hit Step 2. Your email app will instantly open up pre-addressed, and you can just drag the zip file from your download bar directly into that message window!")
