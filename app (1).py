import streamlit as st
from datetime import datetime
import os
import requests
import base64

# ==========================================
# 0. DYNAMIC PATH HELPER
# ==========================================
def find_image(filename):
    # Automatically checks both the absolute root and the content directory
    paths_to_check = [filename, f"/{filename}", f"/content/{filename}"]
    for p in paths_to_check:
        if os.path.exists(p):
            return p
    return None

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(page_title="Fidel Softech Onboarding", page_icon="🌐", layout="centered")

# ==========================================
# 2. CUSTOM BACKGROUND & WATERMARK CONFIGURATION
# ==========================================
bg_path = find_image("fidel_bg_logo.png")
if bg_path:
    with open(bg_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
    
    custom_style = f'''
    <style>
    /* Force main layout containers to true solid white */
    .stApp, [data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {{
        background-color: #FFFFFF !important;
    }}
    
    /* Force input text boxes to be light gray with solid dark text */
    input, textarea, select, div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: #F8FAFC !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        -webkit-text-fill-color: #1E293B !important;
    }}
    
    /* FIX INVISIBLE PLACEHOLDER TEXT: Force placeholder text to show up in dark gray */
    input::placeholder, textarea::placeholder, .stTextInput input::placeholder {{
        color: #94A3B8 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #94A3B8 !important;
    }}
    
    /* Centered watermark layout background layer */
    .stApp::before {{
        content: ""; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -1;
        background-image: url("data:image/png;base64,{encoded_logo}");
        background-repeat: no-repeat; background-position: center center; background-size: 35%;
        opacity: 0.08; pointer-events: none;
    }}
    
    /* Enforce dark legible text globally for all titles and labels */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] p, span, .stSelectbox label {{
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
banner_path = find_image("fidel_banner.png")
if banner_path:
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

footer_path = find_image("fidel_footer.png")
if footer_path:
    st.image(footer_path, use_column_width=True)
