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
    l_name = st.text_input("Last Name *", placeholder="Enter your last name")
    
    st.markdown("<label style='font-size: 14px;'>Contact Number *</label>", unsafe_allow_html=True)
    c_code_col, phone_num_col = st.columns([1, 2])
    with c_code_col:
        all_country_codes = [
            "+91 (India)", "+1 (USA/Canada)", "+44 (UK)", "+81 (Japan)", "+49 (Germany)", "+33 (France)", 
            "+61 (Australia)", "+86 (China)", "+7 (Russia)", "+39 (Italy)", "+34 (Spain)", "+971 (UAE)", 
            "+65 (Singapore)", "+55 (Brazil)", "+27 (South Africa)", "+82 (South Korea)", "+41 (Switzerland)", 
            "+31 (Netherlands)", "+93 (Afghanistan)", "+355 (Albania)", "+213 (Algeria)", "+1-684 (American Samoa)", 
            "+376 (Andorra)", "+244 (Angola)", "+1-264 (Anguilla)", "+672 (Antarctica)", "+1-268 (Antigua & Barbuda)", 
            "+54 (Argentina)", "+374 (Armenia)", "+297 (Aruba)", "+43 (Austria)", "+994 (Azerbaijan)", 
            "+1-242 (Bahamas)", "+973 (Bahrain)", "+880 (Bangladesh)", "+1-246 (Barbados)", "+375 (Belarus)", 
            "+32 (Belgium)", "+501 (Belize)", "+229 (Benin)", "+1-441 (Bermuda)", "+975 (Bhutan)", 
            "+591 (Bolivia)", "+387 (Bosnia & Herzegovina)", "+267 (Botswana)", "+55 (Brazil)", 
            "+1-284 (British Virgin Islands)", "+673 (Brunei)", "+359 (Bulgaria)", "+226 (Burkina Faso)", 
            "+257 (Burundi)", "+855 (Cambodia)", "+237 (Cameroon)", "+238 (Cape Verde)", "+1-345 (Cayman Islands)", 
            "+236 (Central African Republic)", "+235 (Chad)", "+56 (Chile)", "+57 (Colombia)", "+269 (Comoros)", 
            "+242 (Congo - Brazzaville)", "+243 (Congo - Kinshasa)", "+682 (Cook Islands)", "+506 (Costa Rica)", 
            "+385 (Croatia)", "+53 (Cuba)", "+599 (Curaçao)", "+357 (Cyprus)", "+420 (Czechia)", 
            "+45 (Denmark)", "+253 (Djibouti)", "+1-767 (Dominica)", "+1-809 (Dominican Republic)", 
            "+593 (Ecuador)", "+20 (Egypt)", "+503 (El Salvador)", "+240 (Equatorial Guinea)", "+291 (Eritrea)", 
            "+372 (Estonia)", "+268 (Eswatini)", "+251 (Ethiopia)", "+500 (Falkland Islands)", "+298 (Faroe Islands)", 
            "+679 (Fiji)", "+358 (Finland)", "+594 (French Guiana)", "+689 (French Polynesia)", "+241 (Gabon)", 
            "+220 (Gambia)", "+995 (Georgia)", "+233 (Ghana)", "+350 (Gibraltar)", "+30 (Greece)", 
            "+299 (Greenland)", "+1-473 (Grenada)", "+590 (Guadeloupe)", "+1-671 (Guam)", "+502 (Guatemala)", 
            "+224 (Guinea)", "+245 (Guinea-Bissau)", "+592 (Guyana)", "+509 (Haiti)", "+504 (Honduras)", 
            "+852 (Hong Kong)", "+36 (Hungary)", "+354 (Iceland)", "+62 (Indonesia)", "+98 (Iran)", 
            "+964 (Iraq)", "+353 (Ireland)", "+972 (Israel)", "+1-876 (Jamaica)", "+962 (Jordan)", 
            "+7 (Kazakhstan)", "+254 (Kenya)", "+686 (Kiribati)", "+965 (Kuwait)", "+996 (Kyrgyzstan)", 
            "+856 (Laos)", "+371 (Latvia)", "+961 (Lebanon)", "+266 (Lesotho)", "+231 (Liberia)", 
            "+218 (Libya)", "+423 (Liechtenstein)", "+370 (Lithuania)", "+352 (Luxembourg)", "+853 (Macao)", 
            "+389 (North Macedonia)", "+261 (Madagascar)", "+265 (Malawi)", "+60 (Malaysia)", "+960 (Maldives)", 
            "+223 (Mali)", "+356 (Malta)", "+692 (Marshall Islands)", "+596 (Martinique)", "+222 (Mauritania)", 
            "+230 (Mauritius)", "+262 (Mayotte)", "+52 (Mexico)", "+691 (Micronesia)", "+373 (Moldova)", 
            "+377 (Monaco)", "+976 (Mongolia)", "+382 (Montenegro)", "+1-664 (Montserrat)", "+212 (Morocco)", 
            "+258 (Mozambique)", "+95 (Myanmar)", "+264 (Namibia)", "+674 (Nauru)", "+977 (Nepal)", 
            "+31 (Netherlands)", "+687 (New Caledonia)", "+64 (New Zealand)", "+505 (Nicaragua)", "+227 (Niger)", 
            "+234 (Nigeria)", "+683 (Niue)", "+672 (Norfolk Island)", "+850 (North Korea)", "+1-670 (Northern Mariana Islands)", 
            "+47 (Norway)", "+968 (Oman)", "+92 (Pakistan)", "+680 (Palau)", "+970 (Palestine)", 
            "+507 (Panama)", "+675 (Papua New Guinea)", "+595 (Paraguay)", "+51 (Peru)", "+63 (Philippines)", 
            "+1-787 (Puerto Rico)", "+974 (Qatar)", "+262 (Réunion)", "+40 (Romania)", "+7 (Russia)", 
            "+250 (Rwanda)", "+590 (Saint Barthélemy)", "+290 (Saint Helena)", "+1-869 (Saint Kitts & Nevis)", 
            "+1-758 (Saint Lucia)", "+590 (Saint Martin)", "+508 (Saint Pierre & Miquelon)", "+1-784 (Saint Vincent & Grenadines)", 
            "+685 (Samoa)", "+378 (San Marino)", "+239 (São Tomé & Príncipe)", "+966 (Saudi Arabia)", 
            "+221 (Senegal)", "+381 (Serbia)", "+248 (Seychelles)", "+232 (Sierra Leone)", "+421 (Slovakia)", 
            "+386 (Slovenia)", "+677 (Solomon Islands)", "+252 (Somalia)", "+94 (Sri Lanka)", "+249 (Sudan)", 
            "+597 (Suriname)", "+46 (Sweden)", "+963 (Syria)", "+886 (Taiwan)", "+992 (Tajikistan)", 
            "+255 (Tanzania)", "+66 (Thailand)", "+228 (Togo)", "+690 (Tokelau)", "+676 (Tonga)", 
            "+1-868 (Trinidad & Tobago)", "+216 (Tunisia)", "+90 (Turkey)", "+993 (Turkmenistan)", 
            "+1-649 (Turks & Caicos Islands)", "+688 (Tuvalu)", "+1-340 (U.S. Virgin Islands)", "+256 (Uganda)", 
            "+380 (Ukraine)", "+598 (Uruguay)", "+998 (Uzbekistan)", "+678 (Vanuatu)", "+39 (Vatican City)", 
            "+58 (Venezuela)", "+84 (Vietnam)", "+681 (Wallis & Futuna)", "+967 (Yemen)", "+260 (Zambia)", 
            "+263 (Zimbabwe)"
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
st.markdown("#### 🎓 Section 2: Qualifications & Languages")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)
lang_pairs = st.text_input("Working Language Combinations *", placeholder="e.g., English-Japanese, German-English")

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
selected_services = st.multiselect("Services you provide *:", services_options)

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

# PASTE YOUR APPS SCRIPT DEPLOYMENT URL HERE
GOOGLE_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbw5fkVPzjHG1tXIbOjTUyzLs5OMr7aYK58K1cF6J1tPXDwRRh4luvv81NdZHB9_azWO/exec"

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
    v_compliance = (file_nda is not None) and (file_po is not None) and (file_consent is not None)
    v_edu_docs = file_edu is not None
    v_ref_doc = file_ref is not None
    
    if (v_first_name and v_last_name and v_email_id and v_contact and v_city and 
        v_country and v_native and v_work_lang and v_services and v_compliance and 
        v_edu_docs and v_ref_doc):
        
        with st.spinner("Creating secure linguist folder context and processing uploads..."):
            try:
                payload_files = []
                
                def package_file(uploaded_file, custom_name):
                    if uploaded_file is not None:
                        b64_data = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                        payload_files.append({
                            "name": f"{custom_name}_{uploaded_file.name}",
                            "mimeType": uploaded_file.type,
                            "bytes": b64_data
                        })
                
                package_file(file_nda, "Signed_NDA")
                package_file(file_po, "Signed_PO")
                package_file(file_consent, "Signed_Data_Consent")
                package_file(file_edu, "Educational_Certificates")
                package_file(file_ref, "Reference_Letter")
                if file_cert:
                    package_file(file_cert, "Translation_Certificate")
                
                profile_report = f"FIDEL SOFTECH RESOURCE PROFILE DATA\n"                                  f"==================================\n"                                  f"Name: {f_name.strip()} {l_name.strip()}\n"                                  f"Email: {v_email.strip()} | Phone: {v_phone}\n"                                  f"Address: {addr_street}, {addr_city}, {addr_state}, {addr_country}\n"                                  f"Native Language: {native.strip()} | Pairs: {lang_pairs.strip()}\n"                                  f"Services: {', '.join(selected_services)}\n"                                  f"CAT Tools: {', '.join(selected_cat_tools)}\n\n"                                  f"FINANCIAL DATA:\n"                                  f"- Bank: {b_name} | Acc Holder: {b_holder}\n"                                  f"- Code/Number: {b_code} / {b_acc}\n"                                  f"- IFSC/Swift: {b_ifsc} / {b_swift}\n"                                  f"- PAN Card: {b_tax} | GST: {b_gst}\n"                                  f"- Alternates: PayPal: {pay_paypal} | Payoneer: {pay_payoneer} | ProZ: {pay_proz}"
                
                json_data = {
                    "folder_name": f"{f_name.strip()} {l_name.strip()}",
                    "profile_text": profile_report,
                    "files": payload_files
                }
                
                response = requests.post(GOOGLE_WEBHOOK_URL, json=json_data)
                
                if response.status_code == 200:
                    st.balloons()
                    st.success("🎉 Empanelment Complete! Your dedicated directory folder has been created inside the shared Google Drive container.")
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
        if not v_compliance: missing_fields.append("Compliance Documentation Submission")
        if not v_edu_docs: missing_fields.append("Educational Qualification Certificates")
        if not v_ref_doc: missing_fields.append("Reference or Recommendation Letter")
        
        st.error(f"❌ Submission Failed. Missing: {', '.join(missing_fields)}")
