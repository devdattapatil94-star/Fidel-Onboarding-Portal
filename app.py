import os
import io
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
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

# In-Portal Live Test Source Texts
TEST_PASSAGES = {
    "English to Indian Languages": (
        "Fidel Softech provides end-to-end localization, translation, and technology services to global enterprises. "
        "Maintaining terminology consistency, contextual accuracy, and strict adherence to domain guidelines is essential for all corporate deliverables."
    ),
    "English to Japanese": (
        "Our vendor management team evaluates external linguists based on domain expertise, CAT tool proficiency, and quality benchmark tests. "
        "Timely communication and strict compliance with project confidentiality requirements are mandatory."
    ),
    "Japanese to English": (
        "当社はローカライゼーションおよびITソリューションを提供するグローバル企業です。"
        "品質管理、情報セキュリティの順守、ならびに納期厳守を最優先事項として業務を遂行しています。"
    )
}

# ==========================================
# 2. HELPER FUNCTIONS (SMTP DISPATCH)
# ==========================================
def auto_send_email_to_vm(zip_data, vendor_name, vendor_email):
    """Silently dispatches the onboarding ZIP directly to vendor-mgmt@fideltech.com via SMTP."""
    smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(st.secrets.get("SMTP_PORT", 587))
    sender_email = st.secrets.get("SENDER_EMAIL", "")
    sender_password = st.secrets.get("SENDER_PASSWORD", "")

    if not sender_email or not sender_password:
        return False, "SMTP secret keys (SENDER_EMAIL/SENDER_PASSWORD) are not configured."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = TARGET_EMAIL
    msg['Subject'] = f"New Resource Onboarding Submission: {vendor_name}"

    body = f"""
    Hello Vendor Management Team,

    A new vendor registration profile has been completed via the Fidel Resource Onboarding Portal.

    Vendor Details:
    ------------------
    • Name: {vendor_name}
    • Email: {vendor_email}
    • Submission Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    The attached ZIP package contains:
    1. Plunet-ready Excel Vendor Matrix
    2. Digital Compliance & Signature Agreement
    3. In-Portal Live Translation Evaluation Test
    4. Uploaded CV & Supporting Credentials

    Regards,
    Fidel Resource Onboarding System
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach ZIP archive
    zip_filename = f"{vendor_name.replace(' ', '_')}_Onboarding_Package.zip"
    part = MIMEApplication(zip_data, Name=zip_filename)
    part['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, TARGET_EMAIL, msg.as_string())
        server.quit()
        return True, "Successfully dispatched to Vendor Management."
    except Exception as e:
        return False, str(e)


# ==========================================
# 3. HEADER LAYOUT
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

st.markdown("Please complete the official empanelment profile form, take the live evaluation test, and digitally sign your agreement below.")
st.markdown("---")

st.subheader("Resource Empanelment Profile")

# ==========================================
# 4. FORM SECTIONS
# ==========================================
st.markdown("#### Section 1: Personal Information")
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

st.markdown("##### Address Information")
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
st.markdown("#### Section 2: Qualifications, Languages & Rates")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)

# --- SOURCE & TARGET LANGUAGES (STANDARD MULTISELECT DROPDOWNS) ---
selected_source_langs = st.multiselect(
    "Source Language(s) *:", 
    LANGUAGES_POOL,
    placeholder="Choose source language(s)..."
)

selected_target_langs = st.multiselect(
    "Target Language(s) *:", 
    LANGUAGES_POOL,
    placeholder="Choose target language(s)..."
)

# --- CAT TOOLS (EXPANDABLE CHECKLIST DROPDOWN) ---
selected_cat_tools = []
with st.expander("Click to open CAT Tools dropdown checklist"):
    cat_cols = st.columns(3)
    for idx, tool in enumerate(CAT_OPTIONS):
        col_target = cat_cols[idx % 3]
        if col_target.checkbox(tool, key=f"cat_dd_{tool}"):
            selected_cat_tools.append(tool)

if selected_cat_tools:
    st.caption(f"**Selected CAT Tools:** {', '.join(selected_cat_tools)}")

# --- DOMAIN EXPERTISE (EXPANDABLE CHECKLIST DROPDOWN) ---
selected_domains = []
with st.expander("Click to open Domain Expertise dropdown checklist"):
    dom_cols = st.columns(2)
    for idx, dom in enumerate(DOMAIN_OPTIONS):
        col_target = dom_cols[idx % 2]
        if col_target.checkbox(dom, key=f"dom_dd_{dom}"):
            selected_domains.append(dom)

if selected_domains:
    st.caption(f"**Selected Domains:** {', '.join(selected_domains)}")

# --- SERVICES PROVIDED (EXPANDABLE CHECKLIST DROPDOWN) ---
selected_services = []
with st.expander("Click to open Services Provided dropdown checklist *"):
    srv_cols = st.columns(3)
    for idx, srv in enumerate(SERVICES_OPTIONS):
        col_target = srv_cols[idx % 3]
        if col_target.checkbox(srv, key=f"srv_dd_{srv}"):
            selected_services.append(srv)

if selected_services:
    st.caption(f"**Selected Services:** {', '.join(selected_services)}")

# --- MANDATORY SERVICE RATES & PRICING ---
st.markdown("##### Mandatory Service Rates & Pricing *")
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
st.markdown("#### Section 3: Payment Details")
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

st.markdown("##### Alternative Global Payment Systems")
col_alt1, col_alt2 = st.columns(2)
with col_alt1:
    pay_paypal = st.text_input("PayPal ID")
    pay_payoneer = st.text_input("Payoneer Code / ID")
with col_alt2:
    pay_proz = st.text_input("ProZ*Pay Link")

# ========================================================
# SECTION 4: IN-PORTAL LIVE TRANSLATION EVALUATION TEST
# ========================================================
st.markdown("#### Section 4: Mandatory Translation Evaluation Test")
st.write("Select your translation track below and complete the test directly in the text area.")

test_track = st.selectbox("Select Translation Test Track *", [
    "-- Choose Track --", 
    "English to Indian Languages", 
    "English to Japanese", 
    "Japanese to English"
])

live_translation_input = ""
if test_track != "-- Choose Track --":
    st.info(f"**Source Text ({test_track}):**\n\n{TEST_PASSAGES[test_track]}")
    live_translation_input = st.text_area(
        "Type your translated text here *", 
        height=180, 
        placeholder="Enter your translated text here..."
    )

# ========================================================
# SECTION 5: DIGITAL / E-SIGNATURE & COMPLIANCE
# ========================================================
st.markdown("#### Section 5: Legal Compliance & Digital Signature")

with st.expander("Review Fidel Terms, NDA (v1.3), PO Guidelines & Data Consent Policy"):
    st.markdown("""
    **Summary of Terms:**
    1. **Confidentiality:** All materials, source files, and project communications remain the strict property of Fidel Softech.
    2. **Quality Assurance:** Work delivered must comply with agreed glossaries, style guides, and translation standards.
    3. **Data Protection:** Personal information provided in this form is processed strictly for vendor management and empanelment auditing.
    """)

st.markdown("##### Digital Signature Execution *")
sig_col1, sig_col2 = st.columns(2)
with sig_col1:
    digital_sig_name = st.text_input("Full Legal Name (Digital Signature) *", placeholder="e.g., Jane Doe")
with sig_col2:
    digital_sig_date = st.text_input("Date of Execution", value=datetime.now().strftime("%Y-%m-%d"), disabled=True)

digital_nda_agreed = st.checkbox("I confirm that typing my full legal name above serves as a legally binding electronic signature under applicable digital transaction laws. *")

# ========================================================
# SECTION 6: CREDENTIAL & CV UPLOADS
# ========================================================
st.markdown("#### Section 6: Document Uploads")
file_cv = st.file_uploader("Upload Latest CV / Resume *", type=['pdf', 'doc', 'docx'])
file_cert = st.file_uploader("Upload Educational / Professional Certificates (Optional)", type=['pdf', 'jpg', 'png', 'zip'])

st.markdown("---")

# ========================================================
# 5. UNIFIED SINGLE "SUBMIT" BUTTON & PROCESSING
# ========================================================
if st.button("Submit Onboarding Registration", type="primary", use_container_width=True):
    # Field Validation
    errors = []
    if not (f_name and f_name.strip()):
        errors.append("First Name is required.")
    if not (l_name and l_name.strip()):
        errors.append("Last Name is required.")
    if not (v_email and v_email.strip()):
        errors.append("Email ID is required.")
    if not (v_phone_local and v_phone_local.strip()):
        errors.append("Phone Number is required.")
    if not (addr_city and addr_city.strip()) or not (addr_country and addr_country.strip()):
        errors.append("City and Country are required.")
    if not (native and native.strip()):
        errors.append("Native Language is required.")
    if not selected_source_langs:
        errors.append("Select at least one Source Language.")
    if not selected_target_langs:
        errors.append("Select at least one Target Language.")
    if not selected_services:
        errors.append("Select at least one Service.")
    if rate_per_word <= 0 and rate_per_hour <= 0:
        errors.append("Please specify at least one valid service rate (Word or Hour).")
    if test_track == "-- Choose Track --":
        errors.append("Please select a Translation Test Track.")
    if not (live_translation_input and live_translation_input.strip()):
        errors.append("Please complete your translation test in the text area.")
    if not (digital_sig_name and digital_sig_name.strip()) or not digital_nda_agreed:
        errors.append("Digital Signature and Agreement Checkbox are required.")
    if not file_cv:
        errors.append("Please upload your Resume/CV.")

    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    else:
        with st.spinner("Processing registration, generating compliance certificate, and packaging files..."):
            full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
            clean_name = full_vendor_name.replace(' ', '_')

            # 1. Master Vendor Excel Record Data
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
                "Source Languages": [', '.join(selected_source_langs)],
                "Target Languages": [', '.join(selected_target_langs)],
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
                "Test Track Selected": [test_track],
                "Digital Signature Name": [digital_sig_name.strip()],
                "Digital Signature Date": [digital_sig_date],
                "E-Signature Agreed": ["Yes"]
            }

            df_individual = pd.DataFrame(vendor_data)
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df_individual.to_excel(writer, index=False, sheet_name="Vendor Onboarding Matrix")
            excel_bytes = excel_buffer.getvalue()

            # 2. Digital Signature Certificate Document
            sig_cert_text = f"""FIDEL SOFTECH - DIGITAL COMPLIANCE EXECUTION CERTIFICATE
------------------------------------------------------------
Signatory Name: {digital_sig_name.strip()}
Signatory Email: {v_email.strip()}
Execution Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

Agreed Policies:
- Fidel Non-Disclosure Agreement (NDA v1.3)
- Fidel PO Terms & Conditions
- Fidel Data Consent & Privacy Policy

Status: ELECTRONICALLY SIGNED & VERIFIED IN-PORTAL
"""

            # 3. Live Translation Test File Content
            live_test_content = f"""FIDEL SOFTECH - IN-PORTAL TRANSLATION EVALUATION TEST
------------------------------------------------------------
Candidate: {full_vendor_name}
Track: {test_track}
Submission Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

SOURCE TEXT:
{TEST_PASSAGES.get(test_track, '')}

CANDIDATE TRANSLATION:
{live_translation_input.strip()}
"""

            # 4. ZIP Package Compilation
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                # Add Excel Profile Matrix
                zip_file.writestr(f"{clean_name}_Registration_Details.xlsx", excel_bytes)
                # Add Digital Signature Certificate
                zip_file.writestr("Digital_Signature_Certificate.txt", sig_cert_text.encode('utf-8'))
                # Add Completed Translation Test Output
                zip_file.writestr(f"Completed_Translation_Test_{test_track.replace(' ', '_')}.txt", live_test_content.encode('utf-8'))
                
                # Add Uploaded Files
                if file_cv:
                    ext = os.path.splitext(file_cv.name)[1]
                    zip_file.writestr(f"CV_Resume{ext}", file_cv.getvalue())
                if file_cert:
                    ext = os.path.splitext(file_cert.name)[1]
                    zip_file.writestr(f"Certificates{ext}", file_cert.getvalue())

            zip_buffer.seek(0)
            final_zip_bytes = zip_buffer.getvalue()

            # 5. Automated Silent Dispatch to vendor-mgmt@fideltech.com
            sent, status_msg = auto_send_email_to_vm(final_zip_bytes, full_vendor_name, v_email.strip())

            st.balloons()
            st.success("🎉 Application Submitted Successfully!")
            
            if sent:
                st.info("✉️ All details, digital signatures, translation test results, and documents have been automatically delivered to the Vendor Management team (`vendor-mgmt@fideltech.com`).")
            else:
                st.warning(f"⚠️ Direct dispatch notice: {status_msg}")
                st.write("You can also download a copy of your completed registration package below:")
                st.download_button(
                    label="📥 Download Submission Archive (.zip)",
                    data=final_zip_bytes,
                    file_name=f"{clean_name}_Onboarding_Package.zip",
                    mime="application/zip",
                    type="secondary"
                )
