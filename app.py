import os
import io
import zipfile
import pandas as pd
from datetime import datetime
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & INTAKE SETTINGS
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

TARGET_EMAIL = "vendor-mgmt@fideltech.com"

# Comprehensive Master Data Pools
LANGUAGES_POOL = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", 
    "Bengali", "Bulgarian", "Burmese", "Catalan", "Chinese (Simplified)", 
    "Chinese (Traditional)", "Croatian", "Czech", "Danish", "Dutch", 
    "English", "Estonian", "Finnish", "French", "Georgian", "German", 
    "Greek", "Gujarati", "Hebrew", "Hindi", "Hungarian", "Indonesian", 
    "Italian", "Japanese", "Kannada", "Kazakh", "Khmer", "Korean", 
    "Lao", "Latvian", "Lithuanian", "Malay", "Malayalam", "Marathi", 
    "Mongolian", "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", 
    "Punjabi", "Romanian", "Russian", "Serbian", "Sinhala", "Slovak", 
    "Slovenian", "Spanish", "Swahili", "Swedish", "Tagalog / Filipino", 
    "Tamil", "Telugu", "Thai", "Turkish", "Ukrainian", "Urdu", "Vietnamese"
]

CAT_OPTIONS = [
    "MateCat", "MemoQ", "Memsource", "Phrase", 
    "SDL Trados 2019", "SDL Trados 2021", "SDL Trados 2022", 
    "SmartCAT", "WordFast"
]

DOMAIN_OPTIONS = [
    "Banking", "Banking & Finance", "Dentistry", "E-learning", "Economics", 
    "Education", "Electrical", "Electronics", "Electronics Appliances", 
    "Employment Handbooks", "Finance", "General", "Health", "Health & Safety", 
    "Help Documents", "Information Technology", "Insurance", 
    "Law Patents, Trademarks, Copyrights", "Legal", "Logistics", 
    "Manufacturing", "Marketing", "Medical", "Medical Diseases", 
    "Patents", "Pharmaceuticals", "Retail", "Telecommunication", "Transport"
]

SERVICES_OPTIONS = [
    "Back Translation (Chars)", "Back Translation (Words)", "Closed Captioning", 
    "Data Annotation", "Data Collection", "Editing", 
    "Machine Translation and Full Post-Editing", "Machine Translation and Light Post-Editing", 
    "Post-Editing", "Proofreading", "Review", "Revision", 
    "Subtitling", "Transcreation", "Transcription", "Translation", "Voice-Over"
]

def get_file_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "rb") as f: 
                return f.read()
        except: 
            return b""
    return b""

# ==========================================
# 2. HEADER LAYOUT
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

# ========================================================
# --- SECTION 2: QUALIFICATIONS, LANGUAGES & RATES ---
# ========================================================
st.markdown("#### 🎓 Section 2: Qualifications, Languages & Rates")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)

# --- SOURCE LANGUAGES (CHECKLIST INSIDE DROPDOWN) ---
selected_source_langs = []
src_label = f"🌐 Source Language(s) * ({len(selected_source_langs)} selected)"
with st.expander("🌐 Click to open Source Language(s) dropdown checklist *"):
    src_cols = st.columns(3)
    for idx, lang in enumerate(LANGUAGES_POOL):
        col_target = src_cols[idx % 3]
        if col_target.checkbox(lang, key=f"src_dd_{lang}"):
            selected_source_langs.append(lang)
    other_src = st.text_input("Other Source Languages (if not listed):", key="src_other_txt", placeholder="e.g., Finnish, Hebrew")
    if other_src.strip():
        selected_source_langs.append(other_src.strip())

if selected_source_langs:
    st.caption(f"**Selected Source:** {', '.join(selected_source_langs)}")

# --- TARGET LANGUAGES (CHECKLIST INSIDE DROPDOWN) ---
selected_target_langs = []
with st.expander("🎯 Click to open Target Language(s) dropdown checklist *"):
    tgt_cols = st.columns(3)
    for idx, lang in enumerate(LANGUAGES_POOL):
        col_target = tgt_cols[idx % 3]
        if col_target.checkbox(lang, key=f"tgt_dd_{lang}"):
            selected_target_langs.append(lang)
    other_tgt = st.text_input("Other Target Languages (if not listed):", key="tgt_other_txt", placeholder="e.g., Danish, Thai")
    if other_tgt.strip():
        selected_target_langs.append(other_tgt.strip())

if selected_target_langs:
    st.caption(f"**Selected Target:** {', '.join(selected_target_langs)}")

# --- CAT TOOLS (CHECKLIST INSIDE DROPDOWN) ---
selected_cat_tools = []
with st.expander("🛠️ Click to open CAT Tools dropdown checklist"):
    cat_cols = st.columns(3)
    for idx, tool in enumerate(CAT_OPTIONS):
        col_target = cat_cols[idx % 3]
        if col_target.checkbox(tool, key=f"cat_dd_{tool}"):
            selected_cat_tools.append(tool)

if selected_cat_tools:
    st.caption(f"**Selected CAT Tools:** {', '.join(selected_cat_tools)}")

# --- DOMAIN EXPERTISE (CHECKLIST INSIDE DROPDOWN) ---
selected_domains = []
with st.expander("📚 Click to open Domain Expertise dropdown checklist"):
    dom_cols = st.columns(2)
    for idx, dom in enumerate(DOMAIN_OPTIONS):
        col_target = dom_cols[idx % 2]
        if col_target.checkbox(dom, key=f"dom_dd_{dom}"):
            selected_domains.append(dom)

if selected_domains:
    st.caption(f"**Selected Domains:** {', '.join(selected_domains)}")

# --- SERVICES PROVIDED (CHECKLIST INSIDE DROPDOWN) ---
selected_services = []
with st.expander("⚙️ Click to open Services Provided dropdown checklist *"):
    srv_cols = st.columns(3)
    for idx, srv in enumerate(SERVICES_OPTIONS):
        col_target = srv_cols[idx % 3]
        if col_target.checkbox(srv, key=f"srv_dd_{srv}"):
            selected_services.append(srv)

if selected_services:
    st.caption(f"**Selected Services:** {', '.join(selected_services)}")

# --- MANDATORY SERVICE RATES & PRICING ---
st.markdown("##### 💰 Mandatory Service Rates & Pricing *")
rate_curr_col, rate_trans_col, rate_edit_col = st.columns(3)
with rate_curr_col:
    rate_currency = st.selectbox("Preferred Currency *", ["USD ($)", "JPY (¥)", "INR (₹)", "EUR (€)", "GBP (£)"])
with rate_trans_col:
    rate_per_word = st.number_input("Translation Rate (per word) *", min_value=0.000, step=0.001, format="%.3f")
with rate_edit_col:
    rate_per_hour = st.number_input("Editing/Review Rate (per hour) *", min_value=0.00, step=0.50, format="%.2f")

# ==========================================
# SECTION 3: PAYMENT DETAILS
# ==========================================
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
    b_gst = st.text_input("GST Number (if applicable)")

st.markdown("##### 💳 Alternative Global Payment Systems")
col_alt1, col_alt2 = st.columns(2)
with col_alt1:
    pay_paypal = st.text_input("PayPal ID")
    pay_payoneer = st.text_input("Payoneer Code / ID")
with col_alt2:
    pay_proz = st.text_input("ProZ*Pay Link")

# ==========================================
# SECTION 4: DOWNLOAD TEMPLATES
# ==========================================
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
# SECTION 5: TRANSLATION EVALUATION TEST
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
# SECTION 6: COMPLIANCE DOCUMENTATION
# ==========================================
st.markdown("#### 📤 Section 6: Compliance Documentation Submission")
file_cv = st.file_uploader("Upload Latest CV / Resume *", type=['pdf', 'doc', 'docx'])
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3) *", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines *", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent *", type=['pdf'])

# ==========================================
# SECTION 7: ADDITIONAL CREDENTIALS
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
    v_first_name = bool(f_name and f_name.strip())
    v_last_name = bool(l_name and l_name.strip())
    v_email_id = bool(v_email and v_email.strip())
    v_contact = bool(v_phone_local and v_phone_local.strip())
    v_city = bool(addr_city and addr_city.strip())
    v_country = bool(addr_country and addr_country.strip())
    v_native = bool(native and native.strip())
    
    v_source_lang = len(selected_source_langs) > 0
    v_target_lang = len(selected_target_langs) > 0
    v_services = len(selected_services) > 0
    v_rates = (rate_per_word > 0.0) or (rate_per_hour > 0.0)
    
    v_track = test_track != "-- Choose Track --"
    v_test_file = file_test_attempt is not None
    
    v_compliance = (file_cv is not None) and (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    v_section7 = (file_edu is not None) and (file_ref is not None)

    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_source_lang and v_target_lang and v_services and v_rates and 
        v_track and v_test_file and v_compliance and v_section7):
        st.session_state.submitted = True
        st.rerun()
    else:
        st.error("❌ Submission Failed. Please check that all mandatory checkboxes and fields (*) are filled.")

# ==========================================
# 5. ZIP PACKAGE COMPOSITION (.XLSX + FILES)
# ==========================================
if st.session_state.submitted:
    full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
    clean_name = full_vendor_name.replace(' ', '_')
    
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
        "Source Language Selection": [', '.join(selected_source_langs)],
        "Target Language Selection": [', '.join(selected_target_langs)],
        "CAT Tools": [', '.join(selected_cat_tools) if selected_cat_tools else "None"],
        "Domain Expertise": [', '.join(selected_domains) if selected_domains else "None"],
        "Services Provided": [', '.join(selected_services)],
        "Preferred Currency": [rate_currency],
        "Translation Rate (Per Word)": [rate_per_word],
        "Editing Rate (Per Hour)": [rate_per_hour],
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
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df_individual.to_excel(writer, index=False, sheet_name="Vendor Onboarding Matrix")
    excel_data = excel_buffer.getvalue()
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(f"{clean_name}_Registration_Details.xlsx", excel_data)
        
        uploaded_files = [
            (file_cv, "CV_Resume"),
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
