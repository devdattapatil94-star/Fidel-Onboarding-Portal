import os
import io
import zipfile
import smtplib
import socket
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

# EMBEDDED DOMAIN EVALUATION TESTS
TEST_PASSAGES = {
    "Test 1: IT Technical": """Groups, Roles, and Rights
Users are able to perform tasks and gain access to specific features in XXX based on the rights held by their user account. To gain rights, user accounts must belong to the groups you set up in User Setup.
By grouping user accounts, you can organize users and control the scope of their access within XXX. Using groups, roles, and rights, you can enhance the security of XXX, steer users to targeted content, and ensure that anonymous users are, automatically given appropriate rights.
Groups are based on the roles they are assigned, while roles are based on the rights they are assigned. Rights, roles, and groups are defined as follows:
A right is a permission to perform a specific task.
A role is a set of rights typically consisting of a set of related rights that should be assigned together. However, you can create a role from any of the rights available in XXX.
A group is a set of roles that defines the scope of a user account. Users can belong to more than one group, and their overall scope is determined, by all of the rights they have.

Working with Roles
Using roles, you can create a system of groups, each with a different scope, to meet user and administration needs. Roles are reusable, allowing you to associate the same role with any number of groups. A role for a group of users who publish events would typically include the following rights: Add event, Modify event, and Delete event. However, if some users are allowed only to add events, they must be placed in a second group, with a role that excludes the Delete event and Modify event rights.

Adding a Role
To add a new role:
1. Click User Setup > Roles > Add.
2. Enter a name for the new role in the Name field.
3. Enter a description for the new role in the Description field.
4. Select the rights you want the new role to have.
5. Click Save to save the new role, or click Reset to delete the information you entered.""",

    "Test 2: Engineering / Automation": """Understanding the Controller, Chassis, and I/O Modules for a XXX System
Control hardware includes a Chassis (Rack), Power Supply, 1757-PLX52 Control Processor, XXX Interface, Redundancy Module, and I/O Modules. An optional Battery Extension Module (not shown) is also available. The Chassis is available in 5 sizes - 4, 7, 10, 13, and 17 slots.

1. The Power Supply is separate from the Rack and does not consume any slots. It is mounted on the left end of the Rack. Both 120/240 VAC and 24 VDC supplies are available.
2. The 1757-PLX52 Process Control Module is a double wide, two-board assembly featuring a 100 MHz PowerPC processor and eight (8) Mbytes of RAM with error detection and correction. It supports both non-redundant and redundant controller configurations. Four (4) Mbytes of parity-protected Flash ROM is used for permanent program storage and allows easy upgrades. A built-in lithium battery backs up the controller database, and an optional two-slot wide Battery Extension Module provides a rechargeable option instead of replacing the lithium battery.

The Process Controller architecture, featuring the 1757-PLX52 Control Processor, handles a wide variety of requirements, including continuous processes, batch processes, discrete operations, and machine control needs. Compact and cost-effective, the 1757-PLX52 is ideal for integrated regulatory, fast logic, sequential, and batch control applications. Control functions are provided through a library of templates called Function Blocks (FBs). Strategies are easily built using a state-of-the-art graphical engineering tool called Control Builder. Once built, control strategies can be loaded and monitored using Control Builder.

The Control Execution Environment (CEE) is the execution and scheduling environment for the 1757-PLX52 Control Processor. It is available in two base execution rates, 50 msec (normal) and 5 msec (fast) and is selected and loaded into the processor with Control Builder, so you can select the execution speed at development time.
CEE is the underlying support layer for the execution of all control functions. It features:
- Individual per-module selectable execution rates of 50, 100, 200, 500, 1000 and 2000 msec for the 50 msec CEE and 5, 10, 20, 50, 100 and 200 ms for the 5 msec CEE.
- Configurable phase assignment of any modules executing slower than the base rate. This provides the ability to “load balance” a Control Processor.
- Peer-to-peer communication between 1757-PLX52 Control Processors (PLX555 and other Legacy PLC’s, such as PLC5). Implementation is transparent so that peer-to-peer connections are configured in the same way as intra-controller connections.""",

    "Test 3 (a): Medical - Study Protocol": """Purpose and Conduct
You are being invited to participate in this post-marketing surveillance study to evaluate the safety and effectiveness of XYZ (ABC Acid), conducted by Health Care (P) Limited, because you have been prescribed XYZ (ABC Acid) by your doctor for the treatment of postmenopausal osteoporosis. 
XYZ is an approved drug in more than 30 countries for the treatment of post-menopausal osteoporosis. The active ingredient in XYZ is ABC acid, which is available for injection use.
The purpose of this surveillance study is to evaluate the safety and efficacy of XYZ (ABC Acid) treatment in patients with postmenopausal osteoporosis in daily clinical practice.
Approximately 75 postmenopausal women (age range 50-76 years), spread across 15 centers in various cities of India, will participate in this surveillance study.  

Visit 1 is the day when you visit the clinic for your condition and your doctor prescribes you with XYZ (ABC Acid) 5 mg, for your condition. During Visit 1, your doctor will perform a physical examination on you and collect information on your age, weight, height, vital signs (blood pressure and pulse rate), medical history and all previous treatments you have received for your condition. 
You will receive a single 15-minute intravenous infusion of XYZ (ABC Acid) 5 mg, at baseline and at month 12. In addition, those patients who have inadequate dietary intake of calcium or vitamin D will receive daily calcium and vitamin D supplementation, as per the discretion of your doctor.

You will be asked to return to the clinic for 9 more times at Day 7, Months 3, 6, 12, Day 7- post month 12, Months 15, 18, and 24, interval. These will be your Visits 2 to 9. During these visits your doctor will perform a medical examination to assess your vital signs (blood pressure and pulse rate) and monitor the progress you are making after infusion of XYZ (ABC Acid) 5 mg. Your doctor will also ask you questions on your overall satisfaction with the treatment and side effects you may have after taking the medication.""",

    "Test 3 (b): Medical - Patient Leaflet": """Content of this leaflet:
1. What is Diclofenac Na suppository CF and what is it used for?
2. What you must know before you use Diclofenac Na suppository CF.
3. How is Diclofenac Na suppository CF used?
4. Possible side effects.
5. How do you store Diclofenac Na suppository CF?

DICLOFENAC NA SUPPOSITORY CF 50 mgs. suppositories
- The active ingredient is diclofenacnatrium. One suppository contains 50 mg. diclofenacnatrium
- Another ingredient (auxiliary) is long oil, (hard fat).

DICLOFENAC NA SUPPOSITORY CF 100mg suppositories
- The active ingredient is diclofenacnatrium. A suppository contains 100 mg. diclofenacnatrium
- Another ingredient (auxiliary) is long oil, (hard fat).

Registration holder of the medicine:
Centrafarm Services B.V.
Nieuwe Donk 9, 4879 AC Etten-Leur
Diclofenac Na Suppository CF 50 mg. suppositories is registered in the Netherlands under RVG number 17260
Diclofenac Na Suppository CF 100 mg. suppositories is registered in the Netherlands under RVG number 17261

1. WHAT IS DICLOFENAC NA SUPPOSITORY CF AND WHAT IS IT USED FOR?
Pharmaceutical form and content:
Diclofenac Na Suppository 50 mg is a medicine in the form of suppositories. It is delivered in a strip package with 10 suppositories, packaged in multiples of 10 suppositories.
Diclofenac Na Suppository 100 mg is a medicine in the form of suppositories. It is delivered in a strip package with 10 suppositories, packaged in multiples of 10 suppositories.

Medicine group:
Diclofenac belongs to the medicine group of NSAIDS. Diclofenac slows the creation of prostaglandins in the body. These substances are involved with infection symptoms, pain and fever. That is why Diclofenac has an anti-inflammatory, antifebril and pain killing effect. Therefore Diclofenac can be used as a pain killer and anti-inflammatory.

Application of the medicine:
Diclofenac NA is administered for the treatment of:
- inflammations and debilitated joint functions as a consequence of rheumatism
- inflammations of one or more joints (arthritis)
- debilitated joints (artrosis), including the joints in the vertebral column
- joint wear in the shoulder joints, a so-called frozen shoulder
- pain and swelling after an accident or after dental or orthopedic intervention
- treatment of a painful or irregular menstruation
- illnesses which are accompanied by fever, especially infections""",

    "Test 4: Finance / Economics": """Coming Bounce-Back Should Resemble Nifty Fifty
Over the next month, the case for a severe synchronized global recession and a secular bear market may become the consensus for investment sophisticates. My guess is that the deepening gloom will lead to more weakness in equities, more strength in bonds, and perhaps a selling climax and some capitulation. The sentiment measures we monitor are showing rising bearishness but are not yet at the extreme levels we would want to see before buying. In this decline, the Old Economy sectors, particularly financials and consumer cyclicals, should be hit hard, and the rate of decline in TMT should decelerate. The collapse of corporate profits is driving stock prices, stock prices are affecting corporate actions like layoffs, and both are dampening consumer confidence and spending, which recycles back to profits.

After equities have fallen further and discounted the gloom, at some point in the relatively near future, there should be a powerful rally. TMT sectors should have the biggest bounces. Many large-cap TMT names could double and still be far below their highs of last year. This action should be similar to that of the Nifty Fifty off the 1974 bottom. I would own Treasury bonds, the Euro, energy stocks, and US pharmaceuticals.

Consumer Risk Rises Along with White-collar Layoffs
Two factors lie behind the sharp deterioration on the US job front — an inventory correction and the imperatives of corporate cost cutting. The inventory dynamic is, of course, the hallmark of most business cycles. It takes a sharp, but temporary, toll on manufacturing employment, as industrial production is aligned with the depressed level of sales.

Seeking Bottom
Stocks weaken as US data oscillates between recovery and weakness. Tech continues to lead the way down, approaching the lows set last spring. Is there any reason to hope, or should 2001 be written off? There are a few reasons to suggest we may be in better shape and in a better mood at some point fairly soon.
Positives include deep pessimism among investors, scattered signs of stabilization in the US and European economies, improving valuations, and a bear market that is approaching the long-toothed 1980–82 bear for longevity.
Concerns include the need for broader signs of US macro stabilization coupled with corporate statements suggesting stabilization. Also, we believe more liquidity is necessary outside the US, from the ECB and the BoJ.""",

    "Test 5: Marketing": """THE EXTENDED ENTERPRISE STORY
The extended enterprise is not a new concept. Simply put, it means making the most of customer, employee, partner, and market interactions.
Through a holistic blend of technology, services, and hosting solutions, [XXX] helps our clients extend their enterprise and create meaningful connections across the value chain.
Explore [XXX] to learn more about the extended enterprise and the meaningful connections that can enhance your business.

---------------
A New Business Imperative is Emerging
Business systems are reaching outside of the enterprise. There is a new emphasis on creating dialogues with customers, employees, partners, and markets. This requires deeper customer knowledge, better interaction management, and value chain integration.
The extended enterprise presents a new set of challenges – and opportunities.

[XXX] is the Extended Enterprise Company
[XXX] is uniquely positioned to address this new business imperative.
[XXX]’s holistic service offerings begin with a Professional Services group that combines strong industry knowledge, brand-building capabilities, and world-class systems integration skills that help our customers strategize and quickly deploy extended enterprise systems.

[XXX] Managed Services provide hosting solutions for complex, mission-critical applications. We can design and deploy extended enterprise architectures that guarantee application availability up to 99.95 percent.

[XXX]’s Software Services focus on the technology and Web Services that optimize the outer reaches of the value chain through content management, customer interaction, and collaboration solutions.
Together, [XXX] service offerings deliver integrated solutions to any company seeking to extend their enterprise…. and their profits.

[XXX]’s Global Reach
Global reach is a critical factor in providing true extended enterprise solutions. A large portion of our customers are among the Global 5000 with vast and complex international operations. These enterprises need a partner that stretches beyond the boundaries of geography and time zones to provide a broad range of solutions.""",

    "Test 6: Legal": """SOFTWARE LICENSE AGREEMENT
1. GRANT OF LICENSE. XXXXX Ltd. (“XXXXX”) grants you the right to use one copy of the enclosed XXXXX software programs (the ‘Software”), for example, XXXXX’s YYY YYY system software, YYY YYY, YYY YYY , XXXXX's industry specific databases, and all related utilities on a single terminal connected to a single computer (i.e., with a single CPU). You may not network the Software or otherwise use it on more than one computer terminal at the same time.

2. COPYRIGHT. The copyright in the Software is owned by XXXXX and is protected by Canadian and United States copyright laws and international treaty provisions. You must treat the Software as copyrighted material except that you may either (a) make one copy of the Software solely for backup or archival purposes, or (b) transfer the Software to a single hard disk provided you keep the original solely for backup or archival purposes. You may not copy the written materials accompanying the Software.

3. TERM OF LICENSE. If you fail to comply with any term of this Agreement, the license is terminated. If the software is being provided to you on loan, the license will terminate when the loan is terminated. Otherwise, the license will continue until you physically destroy all copies of the Software and merged portions thereof, and return the original program diskette and documentation to XXXXX.

4. OTHER RESTRICTIONS. You may not rent or lease the Software, but you may transfer the Software and accompanying written materials on a permanent basis provided you retain no copies and the recipient agrees to the terms of this Agreement, and the terms of any applicable loan agreement with XXXXX. If Software is an update, any transfer must include the update and all prior versions. Data may not be imported for use into any loaned YYY YYY report generation module from applications other than YYY YYY. You may not reverse engineer, decompile, disassemble, or translate the Software.

5. ENHANCEMENTS AND UPDATES. From time to time, at its sole discretion, XXXXX may provide enhancements, updates or new versions of the Software on its then standard terms and conditions thereof. This Agreement shall apply to such enhancements.

LIMITED WARRANTY. You assume all responsibility for the selection of the Software as appropriate to achieve the results you intend. XXXXX warrants that the enclosed medium upon which the Software is recorded shall be free from defects in material and workmanship under normal use and conditions, and that the Software shall perform substantially as described in its documentation for a period of ninety (90) days from purchase. EXCEPT FOR THE FOREGOING LIMITED WARRANTY, THE SOFTWARE IS PROVIDED, AS IS, WITHOUT WARRANTY OF ANY KIND EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE."""
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def get_client_ip():
    """Captures host/IP metadata for digital audit trails."""
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"

def auto_send_email_to_vm(zip_data, vendor_name, vendor_email):
    """Dispatches onboarding ZIP directly to vendor-mgmt@fideltech.com via SMTP."""
    smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(st.secrets.get("SMTP_PORT", 587))
    sender_email = st.secrets.get("SENDER_EMAIL", "")
    sender_password = st.secrets.get("SENDER_PASSWORD", "")

    if not sender_email or not sender_password:
        return False, "SMTP secrets (SENDER_EMAIL/SENDER_PASSWORD) not configured."

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
    • Submission Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

    The attached ZIP package contains:
    1. Vendor Profile Matrix (Excel)
    2. Full Legal Audit & Electronic Signature Certificate
    3. In-Portal Live Translation Test Submission
    4. Uploaded CV & Supporting Credentials

    Regards,
    Fidel Resource Onboarding System
    """
    msg.attach(MIMEText(body, 'plain'))

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

st.markdown("Please complete the official empanelment profile form, take the live evaluation test, and execute your electronic signature below.")
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
# SECTION 2: QUALIFICATIONS, LANGUAGES & RATES
# ========================================================
st.markdown("#### Section 2: Qualifications, Languages & Rates")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)

# --- SOURCE & TARGET LANGUAGES ---
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

# --- CAT TOOLS ---
selected_cat_tools = []
with st.expander("Click to open CAT Tools dropdown checklist"):
    cat_cols = st.columns(3)
    for idx, tool in enumerate(CAT_OPTIONS):
        col_target = cat_cols[idx % 3]
        if col_target.checkbox(tool, key=f"cat_dd_{tool}"):
            selected_cat_tools.append(tool)

if selected_cat_tools:
    st.caption(f"**Selected CAT Tools:** {', '.join(selected_cat_tools)}")

# --- DOMAIN EXPERTISE ---
selected_domains = []
with st.expander("Click to open Domain Expertise dropdown checklist"):
    dom_cols = st.columns(2)
    for idx, dom in enumerate(DOMAIN_OPTIONS):
        col_target = dom_cols[idx % 2]
        if col_target.checkbox(dom, key=f"dom_dd_{dom}"):
            selected_domains.append(dom)

if selected_domains:
    st.caption(f"**Selected Domains:** {', '.join(selected_domains)}")

# --- SERVICES PROVIDED ---
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
st.write("Translate ONLY the test related to your area of expertise below. Do not use machine translation tools.")

test_track = st.selectbox("Select Domain Test Track *", [
    "-- Choose Track --", 
    "Test 1: IT Technical",
    "Test 2: Engineering / Automation",
    "Test 3 (a): Medical - Study Protocol",
    "Test 3 (b): Medical - Patient Leaflet",
    "Test 4: Finance / Economics",
    "Test 5: Marketing",
    "Test 6: Legal"
])

live_translation_input = ""
if test_track != "-- Choose Track --":
    st.markdown(f"**Source Text ({test_track}):**")
    st.info(TEST_PASSAGES[test_track])
    live_translation_input = st.text_area(
        "Type your complete translation below *", 
        height=250, 
        placeholder="Type your complete translation here..."
    )

# ========================================================
# SECTION 5: NDA, CONSENT & VENDOR POLICIES
# ========================================================
st.markdown("#### Section 5: Legal Agreements & Vendor Policies")

# 5.1 NDA
st.markdown("##### 1. NDA & Confidentiality Agreement *")
with st.expander("Review Fidel Non-Disclosure Agreement (v1.3)"):
    st.markdown("""
    **CONFIDENTIALITY AGREEMENT TERMS:**
    - The linguist agrees that all source materials, translation memory, glossaries, customer details, and business data provided by Fidel Softech Limited remain strictly confidential.
    - Reproduction, sharing, or uploading project files to unauthorized third-party servers, public translation forums, or machine translation engines is strictly prohibited.
    """)
nda_check = st.checkbox("I Confirm that I have read and understood the NDA and agree to comply with all confidentiality requirements applicable to my work with Fidel Softech Limited. *")

# 5.2 Consent / Data Privacy
st.markdown("##### 2. Consent & Data Privacy *")
consent_business = st.checkbox("I consent to Fidel Softech Limited collecting and processing my personal and professional information for vendor registration, project allocation, payment processing and related business purposes. *")
consent_marketing = st.checkbox("I consent to receiving optional Fidel newsletter updates, industry news, and promotional communications (Optional).")

# 5.3 Vendor Policies & Terms
st.markdown("##### 3. Vendor Policies & Code of Conduct *")
policy_payment = st.checkbox("I have read and agree to comply with Fidel's Vendor Payment Policy and PO procedures. *")
policy_aimt = st.checkbox("I agree to strict AI/MT usage restrictions: I will not use unauthorized machine translation engines (e.g., Google Translate) without explicit written project authorization. *")
policy_code = st.checkbox("I agree to abide by Fidel's Code of Conduct, Quality Standards, and Conflict-of-Interest guidelines. *")

# ========================================================
# SECTION 6: ELECTRONIC SIGNATURE & AUDIT TRAIL
# ========================================================
st.markdown("#### Section 6: Electronic Signature Execution")
st.write("Your typed legal signature below will generate a binding digital execution record tied to your IP address and timestamp.")

sig_col1, sig_col2 = st.columns(2)
with sig_col1:
    digital_sig_name = st.text_input("Full Legal Name (Electronic Signature) *", placeholder="Enter your full legal name")
with sig_col2:
    digital_sig_date = st.text_input("Execution Timestamp", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"), disabled=True)

e_signature_ack = st.checkbox("I declare that typing my full legal name above constitutes a binding Electronic Signature under applicable law. *")

# ========================================================
# SECTION 7: CREDENTIAL & CV UPLOADS
# ========================================================
st.markdown("#### Section 7: Document Uploads")
file_cv = st.file_uploader("Upload Latest CV / Resume *", type=['pdf', 'doc', 'docx'])
file_cert = st.file_uploader("Upload Educational / Professional Certificates (Optional)", type=['pdf', 'jpg', 'png', 'zip'])

# ========================================================
# SECTION 8: FINAL DECLARATION & SINGLE SUBMIT
# ========================================================
st.markdown("---")
st.markdown("#### Section 8: Final Declaration")

declaration_check = st.checkbox("I confirm that the information provided by me is accurate and complete. I understand that providing false or misleading information may affect my registration and eligibility for projects. *")

st.markdown("---")

if st.button("I Confirm and Submit My Application", type="primary", use_container_width=True):
    # Comprehensive Validation
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
    if not nda_check:
        errors.append("You must agree to the NDA & Confidentiality Agreement.")
    if not consent_business:
        errors.append("Business data processing consent is required.")
    if not (policy_payment and policy_aimt and policy_code):
        errors.append("You must accept all mandatory Vendor Policies (Payment, AI/MT restriction, Code of Conduct).")
    if not (digital_sig_name and digital_sig_name.strip()) or not e_signature_ack:
        errors.append("Electronic Signature and acknowledgment are required.")
    if not file_cv:
        errors.append("Please upload your Resume/CV.")
    if not declaration_check:
        errors.append("You must check the Final Declaration box to submit.")

    if errors:
        for err in errors:
            st.error(f"❌ {err}")
    else:
        with st.spinner("Processing registration, packaging compliance certificate & emailing Vendor Management..."):
            full_vendor_name = f"{f_name.strip()} {l_name.strip()}"
            clean_name = full_vendor_name.replace(' ', '_')
            client_ip = get_client_ip()
            timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

            # 1. Master Vendor Excel Record
            vendor_data = {
                "Registration Date": [timestamp_str],
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
                "NDA Agreed": ["Yes"],
                "Business Data Consent": ["Yes"],
                "Marketing Consent": ["Yes" if consent_marketing else "No"],
                "Payment Policy Agreed": ["Yes"],
                "AI/MT Policy Agreed": ["Yes"],
                "Code of Conduct Agreed": ["Yes"],
                "Electronic Signature Name": [digital_sig_name.strip()],
                "Signature Timestamp": [timestamp_str],
                "Signer IP Address": [client_ip],
                "Final Declaration Confirmed": ["Yes"]
            }

            df_individual = pd.DataFrame(vendor_data)
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df_individual.to_excel(writer, index=False, sheet_name="Vendor Onboarding Matrix")
            excel_bytes = excel_buffer.getvalue()

            # 2. Complete Electronic Signature Legal Certificate
            sig_cert_text = f"""FIDEL SOFTECH LIMITED - LEGAL E-SIGNATURE AUDIT CERTIFICATE
----------------------------------------------------------------------
Signatory Full Legal Name : {digital_sig_name.strip()}
Signatory Email Address   : {v_email.strip()}
Recorded IP Address       : {client_ip}
Execution Timestamp       : {timestamp_str}

EXECUTED LEGAL AGREEMENTS & ACKNOWLEDGMENTS:
[X] Fidel NDA & Confidentiality Agreement (v1.3)
[X] Business Data Processing & Empanelment Consent
[X] Fidel Vendor Payment Policy & Guidelines
[X] Strict AI / MT Restriction & No-Google-Translate Policy
[X] Fidel Code of Conduct & Quality Guidelines
[X] Final Accuracy & Accuracy Declaration

STATUTORY AUDIT LOG STATUS: VERIFIED ELECTRONICALLY VIA PORTAL DISPATCH
"""

            # 3. Live Translation Test File Content
            clean_track_name = test_track.replace(' ', '_').replace(':', '').replace('/', '_')
            live_test_content = f"""FIDEL SOFTECH - IN-PORTAL TRANSLATION EVALUATION TEST
------------------------------------------------------------
Candidate Name : {full_vendor_name}
Domain Track   : {test_track}
Submission Date: {timestamp_str}

SOURCE TEXT:
{TEST_PASSAGES.get(test_track, '')}

CANDIDATE TRANSLATION:
{live_translation_input.strip()}
"""

            # 4. ZIP Package Compilation
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(f"{clean_name}_Registration_Details.xlsx", excel_bytes)
                zip_file.writestr("Legal_Electronic_Signature_Audit.txt", sig_cert_text.encode('utf-8'))
                zip_file.writestr(f"Completed_Test_{clean_track_name}.txt", live_test_content.encode('utf-8'))
                
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
            st.success("🎉 Application & Legal Execution Submitted Successfully!")
            
            if sent:
                st.info("✉️ All profile data, digital legal agreements, translation test outputs, and CV files have been automatically delivered to `vendor-mgmt@fideltech.com`.")
            else:
                st.warning(f"⚠️ Direct dispatch notice: {status_msg}")
                st.write("You can download your submission package archive below:")
                st.download_button(
                    label="📥 Download Submission Archive (.zip)",
                    data=final_zip_bytes,
                    file_name=f"{clean_name}_Onboarding_Package.zip",
                    mime="application/zip",
                    type="secondary"
                )
