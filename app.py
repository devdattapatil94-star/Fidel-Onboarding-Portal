import streamlit as st
from datetime import datetime
import os

# Set up the tab title and use the local logo for the browser icon if available
logo_path = "FIDEL.NSE.png"
st.set_page_config(
    page_title="Fidel Softech Resource Onboarding", 
    page_icon=logo_path if os.path.exists(logo_path) else "🌐", 
    layout="centered"
)

# Render the company logo and the updated portal title side-by-side
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
    l_name = st.text_input("Last Name", placeholder="Enter your last name")
    v_phone = st.text_input("Contact Number", placeholder="+91-XXXXX-XXXXX")
    
avail = st.selectbox("Availability Status", ["Full-time", "Part-time"])

st.markdown("##### 🏠 Address Information")
col_addr1, col_addr2 = st.columns(2)
with col_addr1:
    addr_street = st.text_input("Street")
    addr_zip = st.text_input("Zip Code")
    addr_state = st.text_input("State")
with col_addr2:
    addr_street2 = st.text_input("Street 2")
    addr_city = st.text_input("City")
    addr_country = st.text_input("Country")

# --- SECTION 2 ---
st.markdown("#### 🎓 Section 2: Qualifications & Languages")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations", placeholder="e.g., English-Japanese, German-English")

cat_options = [
    "Across", "Amazon Translation Management System (ATMS)", "Bureau Works (BWX)", "CafeTran Espresso", 
    "Captionhub", "Chopin", "Crowdin", "Déjà vu", "Erya", "Gentrans", "GlobalLink", "GlobalSight", 
    "Idiom WorldServer", "Keynote", "Lilt", "Lokalize", "MS-Excel", "MS-Word", "MateCat", "MateSub", 
    "MemoQ", "MetaTexis", "OmegaT", "OneForma", "Pairapharase", "Phrase", "Poedit", "Pootle", "Radar", 
    "SDL GroupShare 2020", "SDL Trados 2019", "SDL Trados 2021", "SDL Trados 2022", "SDL WorldServer", 
    "Similis", "SmartCAT", "Smartling", "Star Transit", "Trados Passolo", "Transifex", "TransitNXT", 
    "Virtaal", "Weglot", "Wordbee", "Wordfast", "Wordfast Anywhere", "XTM Cloud", "Xtrans"
]
selected_cat_tools = st.multiselect("Proficient in which of the following CAT Tools:", cat_options)

domain_options = [
    "Accounting", "Administrative", "Advertising", "Aerospace", "Agriculture", "Airconditioning", "Archeology", 
    "Architecture", "Art", "Artificial Intelligence", "Arts and Culture", "Astronomy", "Audio", "Audits", 
    "Automotive", "Aviation", "Ayurveda", "Banking", "Banking & Finance", "Beauty Product[s]", "Beverage products", 
    "Bigdata", "Biology", "Bookeeping", "Botany", "Brand Names", "Broadcasting", "Building & Construction", 
    "Business Communication", "Cable Management", "Casting", "Chemical Engineering & Technology", "Chemicals", 
    "Chemistry", "Civil Engineering", "Clothing", "Cloud Domain", "Commerce", "Commercial", "Computer Science", 
    "Computers", "Consulting", "Contracts", "Corporate Law", "Couriers", "Credit Management", "Crop Production", 
    "Culinary", "Customer Relationship Management", "Customs", "Cybersecurity", "Data Science", "Defense", 
    "Dentistry", "Desktop Publishing", "Dictionaries", "E-learning", "Ecology", "Economics", "Education", 
    "Electrical", "Electrical Engineering", "Electronic Data Processing", "Electronics", "Electronics Appliances", 
    "Employment Handbooks", "Employment Policies", "Energy", "Engineering", "Entertainment", "Environment", 
    "Environmental Performance of Buildings", "Ethics", "Finance", "Fishing", "Flexible Manufacturing Systems", 
    "Food", "Food Processing", "Food Standards", "Forestry", "Forms & Paperwork", "Fuels", "Gaming", "Gas", 
    "Geneology", "General", "Geology", "Geometry", "Geotechnics", "Government", "Government Procurement", 
    "Grammar", "HR", "Health", "Health & Safety", "Heavy Machinery", "Help Documents", "History", 
    "Human Resource Training", "Human Sciences", "Hydraulic Engineering", "Hydrology", "IFRS", "Idioms", 
    "Information Management", "Information Technology", "Insurance", "International Trade", "Internet Slang", 
    "Investment", "Joinery", "Judicial", "Law Patents, Trademarks, Copyrights", "Legal", "Leisure", "Letters", 
    "Lexicography", "Linguistics", "Literary", "Literature", "Logistics", "MSDS", "Machining", "Manufacturing", 
    "Marketing", "Masonry", "Materials", "Mathematics", "Mechanical", "Mechanical Engineering", "Mechatronics", 
    "Media", "Medical", "Medical Diseases", "Medical Technology", "Metallurgy", "Meteorology", "Military", 
    "Minerology", "Mining", "Miscellaneous", "Mobile UI", "Multimedia", "Music", "Mythology", "Natural Sciences", 
    "Nautical", "Nuclear", "Nuclear Physics", "Numismatics", "Nutrition", "Oil & Gas", "Optics", "Optoelectronics", 
    "Order Picking", "Packaging Industry", "Paper Industry", "Parliament", "Patents", "Petroleum and coal", 
    "Pharmaceuticals", "Philosophy", "Photography", "Physical Therapy", "Physics", "Politics", "Polymers", 
    "Popular Culture", "Precious Metals", "Printing & Paper Industry", "Process Engineering", "Procurement", 
    "Production", "Professional and Business Services", "Psychiatry", "Psychology", "Publishing Industry", 
    "Quality Assurance", "Radio Technology", "Railways", "Real Estate", "Religion", "Rental and Leasing", 
    "Repair and Maintenance", "Retail", "Robotics (Automation)", "Safety", "Sciences", "Securities", "Sewage", 
    "Social science", "Software", "Software OS", "Sports", "Survey", "Technology", "Telecommunication", 
    "Textile", "Trade", "Transport", "Travel and Tourism", "Utilities", "Warehouse and Storage", "Waste Management", 
    "Websites"
]
selected_domains = st.multiselect("Domain Expertise:", domain_options)

services_options = [
    "AI Voice-Over", "Alignment", "Audio Content Check", "Audio Data Collection", "Auto Delivery Customer", 
    "Back Translation (Chars)", "Back Translation (Words)", "Bug Fixing", "Client Feedback Implementation", 
    "Client Review", "Client Review Changes", "Client Review Validation", "Closed Captioning", "Computer Programming", 
    "Content Creation and Development", "Copy-Paste", "DTP Create D1", "DTP Final Files", "DTP Text Extract", 
    "DTP Vendor Create D1", "Data Annotation", "Data Collection", "Desktop Publishing", "Editing", 
    "Editing (By Segment)", "Engineering", "Evaluation", "External Linguistic Quality Assessment", "File Conversion", 
    "File Preparation", "Glossary Creation", "Image Caption", "Image Creation", "In Country Review", 
    "Internal Linguistic Quality Assessment", "Internal Vendor Testing", "Interpretation", "Language Engineering", 
    "Language Validation", "Linguistic Quality Assessment", "Linguistic Sign-off", "Localization Testing", 
    "Machine Translation", "Machine Translation and Full Post-Editing", "Machine Translation and Light Post-Editing", 
    "Minutes Translation", "OCR Creation", "OCR Editing", "PM - Final Files", "Post Layout Review", "Post-Editing", 
    "Proofreading", "Quality Assurance", "Quality Assurance PM", "Quote", "Quote - Machine Translation + Post-Editing", 
    "Rekey (PDF)", "Review", "Revision", "Score and Evaluation", "Style Guide Creation", "Subtitle Integration", 
    "Subtitling", "Training-Meeting", "Transcreation", "Transcription", "Translation", "Translation Analysis", 
    "Translation Editing and Proofreading", "Translation Memory Creation", "Translation Memory Update", 
    "Translation Sample Assessment", "Translation and DTP", "Translation and Editing", "Translation and Revision", 
    "Verification and Release", "Video Editing", "Video Integration", "Voice-Over", "Voice-Over-Integration", 
    "Web Development", "Website Testing", "XML-HTML Tagging"
]
selected_services = st.multiselect("Services you provide:", services_options)

# --- SECTION 3 (UPDATED) ---
st.markdown("#### 🏦 Section 3: Payment Details")

st.markdown("##### 🏢 Wire Transfer Details")
col_fin1, col_fin2 = st.columns(2)
with col_fin1:
    b_name = st.text_input("Bank Name")
    b_holder = st.text_input("Account Holder Name")
    b_code = st.text_input("Bank Code")
    b_acc = st.text_input("Account Number")
    b_iban = st.text_input("IBAN")
with col_fin2:
    b_swift = st.text_input("SWIFT - BIC")
    b_credref = st.text_input("Bank Assigned Creditor Reference")
    b_mandate = st.text_input("Mandate Reference Identifier")
    b_address = st.text_area("Bank Address (Bank)", height=68)
    b_country = st.text_input("Bank Country")

b_tax = st.text_input("PAN Card / Tax Registration Number")

st.markdown("##### 💳 Alternative Global Payment Systems")
col_alt1, col_alt2 = st.columns(2)
with col_alt1:
    pay_paypal = st.text_input("PayPal ID (Email Address)")
    pay_payoneer = st.text_input("Payoneer Code / ID")
with col_alt2:
    pay_proz = st.text_input("ProZ*Pay Link / ID")
    
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
    st.download_button("📥 Download NDA Template", data=nda_data, file_name="Fidel_NDA_Ver 1.3.pdf", mime="application/pdf", disabled=(len(nda_data) == 0))
with d_col2:
    st.download_button("📥 Download PO Terms", data=po_data, file_name="Fidel_PO-Invoice-Payment-Procedure_ver_1.3.pdf", mime="application/pdf", disabled=(len(po_data) == 0))
with d_col3:
    st.download_button("📥 Download Consent Form", data=consent_data, file_name="Fidel Consent Form.pdf", mime="application/pdf", disabled=(len(consent_data) == 0))

# --- SECTION 5 ---
st.markdown("#### 📤 Section 5: Compliance Documentation Submission")
file_nda = st.file_uploader("Upload Signed Fidel NDA (v1.3)", type=['pdf'])
file_po = st.file_uploader("Upload Signed Fidel PO Guidelines", type=['pdf'])
file_consent = st.file_uploader("Upload Signed Fidel Data Consent", type=['pdf'])

# --- SECTION 6 ---
st.markdown("#### 🏅 Section 6: Additional Credentials & Certifications")
file_cert = st.file_uploader("Upload Translation Certificate (if any)", type=['pdf', 'jpg', 'png'])
file_edu = st.file_uploader("Upload Educational Qualification Certificates", type=['pdf', 'jpg', 'png'])
file_ref = st.file_uploader("Upload Reference or Recommendation Letter", type=['pdf', 'doc', 'docx'])

st.markdown("---")

if st.button("Submit Profile Record", type="primary"):
    has_first_name = len(f_name.strip()) > 0
    has_email = len(v_email.strip()) > 0
    has_native_lang = len(native.strip()) > 0
    
    if has_first_name and has_email and has_native_lang:
        st.balloons()
        st.success("🎉 Onboarding Profile Submitted Successfully!")
        
        submission_summary = {
            "Vendor Name": f"{f_name.strip()} {l_name.strip()}",
            "Email Address": v_email.strip(),
            "Contact Phone": v_phone.strip(),
            "Address": f"{addr_street}, {addr_street2}, {addr_city}, {addr_state}, {addr_country} - {addr_zip}",
            "Availability": avail,
            "Native Language": native.strip(),
            "Language Pairs": lang_pairs.strip(),
            "Selected CAT Tools": selected_cat_tools,
            "Bank Details": f"{b_name} | Holder: {b_holder} | Code: {b_code} | Acc: {b_acc} | Address: {b_address}",
            "Alternative Financials": f"PayPal: {pay_paypal} | Payoneer: {pay_payoneer} | ProZ: {pay_proz}",
            "PAN Card": b_tax.strip()
        }
        st.json(submission_summary)
        
        body_text = f"🚨 NEW VENDOR REGISTRATION DATA%0A%0A"                     f"Full Name: {f_name.strip()} {l_name.strip()}%0A"                     f"Email ID: {v_email.strip()}%0A"                     f"Phone: {v_phone.strip()}%0A"                     f"Availability: {avail}%0A"                     f"Native Language: {native.strip()}%0A%0A"                     f"🏦 BANK WIRE VAULT:%0A"                     f"- Bank: {b_name}%0A"                     f"- Holder: {b_holder}%0A"                     f"- Code/Acc: {b_code} / {b_acc}%0A"                     f"- IBAN/SWIFT: {b_iban} / {b_swift}%0A"                     f"- Bank Address: {b_address.replace('%0A', ' ')}%0A%0A"                     f"💳 DIGITAL ECOSYSTEMS:%0A"                     f"- PayPal: {pay_paypal}%0A"                     f"- Payoneer: {pay_payoneer}%0A"                     f"- ProZ*Pay: {pay_proz}%0A%0A"                     f"📦 UPLOAD SUMMARY:%0A"                     f"- NDA: {'Yes' if file_nda else 'No'}, PO: {'Yes' if file_po else 'No'}%0A"                     f"- Certs/Ref: {'Yes' if file_cert else 'No'}/{'Yes' if file_edu else 'No'}/{'Yes' if file_ref else 'No'}"
        
        mailto_url = f"mailto:vendor-mgmt@fideltech.com?subject=New Onboarding Registration - {f_name.strip()} {l_name.strip()}&body={body_text}"
        
        st.markdown(
            f'<a href="{mailto_url}" target="_blank" style="display: inline-block; padding: 0.5rem 1rem; background-color: #ff4b4b; color: white; text-decoration: none; border-radius: 4px; font-weight: bold; margin-top: 10px;">✉️ Click to Route Profile directly to Vendor Management Inbox</a>', 
            unsafe_allow_html=True
        )
        
    else:
        missing_fields = []
        if not has_first_name: missing_fields.append("First Name")
        if not has_email: missing_fields.append("Email ID")
        if not has_native_lang: missing_fields.append("Native Language")
        st.error(f"❌ Submission Failed. Required: {', '.join(missing_fields)}")
