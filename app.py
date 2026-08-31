import io
import os
import smtplib
import zipfile
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import streamlit as st

# ========================================================
# --- PAGE CONFIGURATION & STYLING ---
# ========================================================
st.set_page_config(
    page_title="Fidel Resource Onboarding Portal",
    page_icon="🌐",
    layout="wide"
)

# Fidel Corporate Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #003366;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555555;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #003366;
        color: white;
        font-weight: 600;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #002244;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================================
# --- MASTER DATA POOLS ---
# ========================================================
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

# ========================================================
# --- HELPER FUNCTIONS (ZIP & EMAIL) ---
# ========================================================
def create_vendor_zip(vendor_data, uploaded_files):
    """Generates an Excel matrix and packages it with uploaded documents into a ZIP in memory."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # 1. Excel Generation
        df = pd.DataFrame([vendor_data])
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Vendor Profile')
        zip_file.writestr("Vendor_Profile.xlsx", excel_buffer.getvalue())
        
        # 2. Attach Files
        for file_name, file_obj in uploaded_files.items():
            if file_obj is not None:
                zip_file.writestr(f"Documents/{file_name}_{file_obj.name}", file_obj.getvalue())
                
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def send_dispatch_email(zip_data, vendor_name, vendor_email):
    """Dispatches the vendor package to vendor-mgmt@fideltech.com."""
    # Secrets management via Streamlit Cloud secrets or environment variables
    smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(st.secrets.get("SMTP_PORT", 587))
    sender_email = st.secrets.get("SENDER_EMAIL", "")
    sender_password = st.secrets.get("SENDER_PASSWORD", "")
    recipient_email = "vendor-mgmt@fideltech.com"

    if not sender_email or not sender_password:
        return False, "SMTP Credentials missing in Streamlit secrets."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"New Vendor Onboarding Submission: {vendor_name}"

    body = f"""
    Dear Vendor Management Team,

    A new vendor application has been submitted via the Fidel Onboarding Portal.

    Vendor Details:
    - Name: {vendor_name}
    - Contact Email: {vendor_email}

    The complete registration profile and uploaded compliance files are attached in the ZIP archive.

    Regards,
    Fidel Resource Onboarding Portal
    """
    msg.attach(MIMEText(body, 'plain'))

    # Attach ZIP File
    zip_filename = f"{vendor_name.replace(' ', '_')}_Onboarding_Package.zip"
    part = MIMEApplication(zip_data, Name=zip_filename)
    part['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True, "Success"
    except Exception as e:
        return False, str(e)


# ========================================================
# --- MAIN APPLICATION UI ---
# ========================================================
st.markdown("<div class='main-header'>Fidel Softech — Linguist Onboarding Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Digital Empanelment Hub for Translators, Reviewers & Localization Partners</div>", unsafe_allow_html=True)

with st.form("fidel_onboarding_form", clear_on_submit=False):
    
    # ----------------------------------------------------
    # SECTION 1: PERSONAL & CONTACT INFORMATION
    # ----------------------------------------------------
    st.markdown("#### 👤 Section 1: Personal & Contact Information")
    col_fn, col_ln = st.columns(2)
    with col_fn:
        first_name = st.text_input("First Name *", placeholder="First Name")
    with col_ln:
        last_name = st.text_input("Last Name *", placeholder="Last Name")
        
    col_email, col_phone, col_country = st.columns(3)
    with col_email:
        email = st.text_input("Email Address *", placeholder="name@domain.com")
    with col_phone:
        phone = st.text_input("Phone Number *", placeholder="+91 98765 43210")
    with col_country:
        country = st.text_input("Country of Residence *", placeholder="India")

    st.divider()

    # ----------------------------------------------------
    # SECTION 2: QUALIFICATIONS, LANGUAGES & RATES
    # ----------------------------------------------------
    st.markdown("#### 🎓 Section 2: Qualifications, Languages & Rates")
    
    col_nat, col_exp = st.columns([1, 1])
    with col_nat:
        native = st.text_input("Native Language *", placeholder="e.g., Japanese")
    with col_exp:
        exp = st.slider("Years of Translation Experience", 0, 40, 2)

    # --- SOURCE & TARGET LANGUAGES ---
    selected_source_langs = st.multiselect(
        "Source Language(s) * (Click to open dropdown & select with tickmarks):", 
        LANGUAGES_POOL,
        placeholder="Choose source language(s)..."
    )

    selected_target_langs = st.multiselect(
        "Target Language(s) * (Click to open dropdown & select with tickmarks):", 
        LANGUAGES_POOL,
        placeholder="Choose target language(s)..."
    )
     
    # --- CAT TOOLS ---
    selected_cat_tools = st.multiselect(
        "Proficient in which of the following CAT Tools:", 
        CAT_OPTIONS,
        placeholder="Select CAT tools..."
    )
     
    # --- DOMAIN EXPERTISE ---
    selected_domains = st.multiselect(
        "Domain Expertise:", 
        DOMAIN_OPTIONS,
        placeholder="Select domain expertise..."
    )
     
    # --- SERVICES PROVIDED ---
    selected_services = st.multiselect(
        "Services you provide *:", 
        SERVICES_OPTIONS,
        placeholder="Select services..."
    )

    # --- MANDATORY SERVICE RATES & PRICING ---
    st.markdown("##### 💰 Mandatory Service Rates & Pricing *")
    rate_curr_col, rate_trans_col, rate_edit_col = st.columns(3)
    with rate_curr_col:
        rate_currency = st.selectbox("Preferred Currency *", ["USD ($)", "JPY (¥)", "INR (₹)", "EUR (€)", "GBP (£)"])
    with rate_trans_col:
        rate_per_word = st.number_input("Translation Rate (per word) *", min_value=0.000, step=0.001, format="%.3f")
    with rate_edit_col:
        rate_per_hour = st.number_input("Editing/Review Rate (per hour) *", min_value=0.00, step=0.50, format="%.2f")

    st.divider()

    # ----------------------------------------------------
    # SECTION 3: COMPLIANCE & DOCUMENT UPLOADS
    # ----------------------------------------------------
    st.markdown("#### 📄 Section 3: Compliance & Document Uploads")
    
    col_cv, col_cert = st.columns(2)
    with col_cv:
        cv_file = st.file_uploader("Upload Updated CV/Resume (PDF/DOCX) *", type=["pdf", "docx"])
    with col_cert:
        cert_file = st.file_uploader("Certifications / Diplomas (Optional)", type=["pdf", "docx", "zip"])

    nda_agreed = st.checkbox("I agree to Fidel Softech's Non-Disclosure Agreement (NDA) & Privacy Policy. *")

    st.divider()

    # Submit Button
    submitted = st.form_submit_button("Submit Registration to Fidel VM Team")

# ========================================================
# --- PROCESSING & SUBMISSION HANDLER ---
# ========================================================
if submitted:
    # 1. Validation Logic
    errors = []
    if not first_name.strip() or not last_name.strip():
        errors.append("Please provide both First and Last Name.")
    if not email.strip() or "@" not in email:
        errors.append("A valid Email Address is required.")
    if not native.strip():
        errors.append("Native Language is required.")
    if not selected_source_langs:
        errors.append("Select at least one Source Language.")
    if not selected_target_langs:
        errors.append("Select at least one Target Language.")
    if not selected_services:
        errors.append("Select at least one Service.")
    if rate_per_word <= 0 and rate_per_hour <= 0:
        errors.append("Please specify at least one valid service rate.")
    if not cv_file:
        errors.append("Resume/CV upload is mandatory.")
    if not nda_agreed:
        errors.append("You must agree to the NDA & Terms to proceed.")

    # 2. Execution Block
    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
    else:
        with st.spinner("Processing application and packaging files..."):
            # Compile Form Payload
            vendor_matrix = {
                "First Name": first_name,
                "Last Name": last_name,
                "Email": email,
                "Phone": phone,
                "Country": country,
                "Native Language": native,
                "Years of Experience": exp,
                "Source Languages": ", ".join(selected_source_langs),
                "Target Languages": ", ".join(selected_target_langs),
                "CAT Tools": ", ".join(selected_cat_tools),
                "Domains": ", ".join(selected_domains),
                "Services": ", ".join(selected_services),
                "Currency": rate_currency,
                "Translation Rate (Word)": rate_per_word,
                "Editing Rate (Hour)": rate_per_hour,
                "NDA Agreed": nda_agreed
            }

            uploaded_docs = {
                "Resume": cv_file,
                "Certifications": cert_file
            }

            # Generate ZIP package
            zip_bytes = create_vendor_zip(vendor_matrix, uploaded_docs)

            # Try to route email directly
            email_sent, email_msg = send_dispatch_email(zip_bytes, f"{first_name} {last_name}", email)

            st.balloons()
            st.success("🎉 Application Submitted Successfully!")
            
            if email_sent:
                st.info("✉️ Your profile & documents have been routed directly to `vendor-mgmt@fideltech.com`.")
            else:
                st.warning("⚠️ Direct email dispatch skipped (SMTP config pending). You can download your packaged application ZIP below to submit manually.")
                
            # Direct ZIP Download Option
            st.download_button(
                label="📥 Download Onboarding Package (.ZIP)",
                data=zip_bytes,
                file_name=f"{first_name}_{last_name}_Fidel_Onboarding.zip",
                mime="application/zip"
            )

            # Profile Summary Preview
            with st.expander("🔍 View Processed Registration Matrix", expanded=False):
                st.json(vendor_matrix)
