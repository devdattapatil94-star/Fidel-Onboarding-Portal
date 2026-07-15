import streamlit as st
import os
from datetime import datetime
import pandas as pd

# ==========================================
# 1. PAGE CONFIGURATION & DIRECTORY MANAGEMENT
# ==========================================
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon="🌐",
    layout="centered"
)

# Dedicated directory folder to store isolated vendor spreadsheets
RECORD_DIR = "vendor_records"
if not os.path.exists(RECORD_DIR):
    try:
        os.makedirs(RECORD_DIR)
    except:
        pass

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
 
st.markdown("#### 🏅 Section 7: Additional Credentials & Certifications")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates *", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter *", type=['pdf', 'doc', 'docx'])
 
st.markdown("---")
 
# ==========================================
# 4. SUBMISSION & ISOLATED EXCEL AUTO-GENERATION
# ==========================================
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
    v_track = test_track != "-- Choose Track --"
    v_test_file = file_test_attempt is not None
    v_compliance = (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    v_edu_docs = file_edu is not None
    v_ref_doc = file_ref is not None

    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_work_lang and v_services and v_track and 
        v_test_file and v_compliance and v_edu_docs and v_ref_doc):
        
        full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
        clean_name = full_vendor_name.replace(' ', '_')
        
        # Build the structured row data dataset explicitly for this single linguist
        vendor_data = {
            "Field Matrix": [
                "Registration Date", "First Name", "Last Name", "Email ID", "Contact Number",
                "Availability Status", "Street Address", "City", "State", "Zip Code", "Country",
                "Native Language", "Experience (Years)", "Language Combinations", "CAT Tools",
                "Domain Expertise", "Services Provided", "Bank Name", "Account Holder",
                "Bank Code", "Account Number", "IFSC Code", "Swift Code", "PAN Card", "GST Number",
                "PayPal ID", "Payoneer ID", "ProZ Link", "Translation Test Track", "Test File Name"
            ],
            "Vendor Response Value": [
                datetime.now().strftime("%Y-%m-%d %H:%M"),
                f_name.strip(),
                l_name.strip(),
                v_email.strip(),
                v_phone,
                avail,
                f"{addr_street} {addr_street2}".strip(),
                addr_city.strip(),
                addr_state.strip(),
                addr_zip.strip(),
                addr_country.strip(),
                native.strip(),
                exp,
                lang_pairs.strip(),
                ', '.join(selected_cat_tools) if selected_cat_tools else "None",
                ', '.join(selected_domains) if selected_domains else "None",
                ', '.join(selected_services),
                b_name.strip(),
                b_holder.strip(),
                b_code.strip(),
                b_acc.strip(),
                b_ifsc.strip(),
                b_swift.strip(),
                b_tax.strip(),
                b_gst.strip(),
                pay_paypal.strip(),
                pay_payoneer.strip(),
                pay_proz.strip(),
                test_track,
                file_test_attempt.name
            ]
        }
        
        # Convert data profile structure to pandas matrix DataFrame
        df_individual = pd.DataFrame(vendor_data)
        
        # Save explicitly as their own isolated standalone file inside the vendor folder directory
        individual_filename = os.path.join(RECORD_DIR, f"{clean_name}_Onboarding_Details.csv")
        df_individual.to_csv(individual_filename, index=False)
        
        st.info("ℹ️ Your profile details have been compiled into an individual spreadsheet matrix entry successfully.")
        
        st.markdown("<div style='padding:15px; background-color:#e8f4fd; border-radius:5px; border-left:4px solid #2196f3;'>"
                    "<b>Onboarding Step Complete:</b> A dedicated registration tracking sheet has been generated for your profile record."
                    "</div>", unsafe_allow_html=True)
    else:
        st.error("❌ Submission Failed. Please ensure all mandatory fields (*) are complete.")
