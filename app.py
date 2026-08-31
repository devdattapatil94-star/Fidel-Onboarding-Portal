import streamlit as st

# ========================================================
# --- PAGE CONFIGURATION & STYLING ---
# ========================================================
st.set_page_config(
    page_title="Translator Onboarding Portal",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS for UI enhancements
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1rem;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================================
# --- MASTER DATA POOLS ---
# ========================================================
LANGUAGES_POOL = [
    "Arabic", "Bengali", "Chinese (Simplified)", "Chinese (Traditional)", 
    "Dutch", "English", "French", "German", "Hindi", "Italian", 
    "Japanese", "Korean", "Polish", "Portuguese", "Russian", 
    "Spanish", "Swedish", "Turkish", "Vietnamese"
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
# --- HEADER ---
# ========================================================
st.markdown("<div class='main-header'>🌐 Linguist Onboarding Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Please complete your profile details and rate card below to register with our network.</div>", unsafe_allow_html=True)

# ========================================================
# --- FORM START ---
# ========================================================
with st.form("onboarding_form", clear_on_submit=False):
    
    # ----------------------------------------------------
    # SECTION 1: PERSONAL & CONTACT INFORMATION
    # ----------------------------------------------------
    st.markdown("#### 👤 Section 1: Personal & Contact Information")
    col_fn, col_ln = st.columns(2)
    with col_fn:
        first_name = st.text_input("First Name *", placeholder="Jane")
    with col_ln:
        last_name = st.text_input("Last Name *", placeholder="Doe")
        
    col_email, col_phone = st.columns(2)
    with col_email:
        email = st.text_input("Email Address *", placeholder="jane.doe@example.com")
    with col_phone:
        phone = st.text_input("Phone Number", placeholder="+1 (555) 000-0000")
        
    cv_file = st.file_uploader("Upload Resume/CV (PDF or DOCX) *", type=["pdf", "docx"])
    
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
    # SECTION 3: TERMS & SUBMISSION
    # ----------------------------------------------------
    st.markdown("#### 📝 Section 3: Availability & Agreement")
    
    col_avail, col_cap = st.columns(2)
    with col_avail:
        availability = st.selectbox("Weekly Availability", ["Full-time (< 40 hrs/wk)", "Part-time (10-20 hrs/wk)", "Ad-hoc / On-demand"])
    with col_cap:
        daily_capacity = st.number_input("Daily Word Capacity", min_value=500, max_value=10000, value=2500, step=250)
        
    terms_agreed = st.checkbox("I confirm that the information provided above is accurate and complete. *")
    
    # Submit Button
    submitted = st.form_submit_button("Submit Application")

# ========================================================
# --- FORM PROCESSING & VALIDATION ---
# ========================================================
if submitted:
    # Validate required fields
    errors = []
    if not first_name.strip():
        errors.append("First Name is required.")
    if not last_name.strip():
        errors.append("Last Name is required.")
    if not email.strip() or "@" not in email:
        errors.append("A valid Email Address is required.")
    if not cv_file:
        errors.append("Please upload your Resume/CV.")
    if not native.strip():
        errors.append("Native Language is required.")
    if not selected_source_langs:
        errors.append("At least one Source Language must be selected.")
    if not selected_target_langs:
        errors.append("At least one Target Language must be selected.")
    if not selected_services:
        errors.append("At least one Service must be selected.")
    if rate_per_word <= 0 and rate_per_hour <= 0:
        errors.append("Please enter at least one valid rate (Translation or Editing).")
    if not terms_agreed:
        errors.append("You must agree to the confirmation check before submitting.")

    # Render Validation Result
    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
    else:
        st.balloons()
        st.success("🎉 Application Submitted Successfully!")
        
        # Payload Preview
        submission_payload = {
            "Applicant": f"{first_name} {last_name}",
            "Email": email,
            "Native Language": native,
            "Experience": f"{exp} years",
            "Source Languages": selected_source_langs,
            "Target Languages": selected_target_langs,
            "CAT Tools": selected_cat_tools,
            "Domains": selected_domains,
            "Services": selected_services,
            "Rates": {
                "Currency": rate_currency,
                "Per Word": rate_per_word,
                "Per Hour": rate_per_hour
            },
            "Availability": availability,
            "Daily Capacity": f"{daily_capacity} words"
        }
        
        with st.expander("📄 View Submitted Data Summary", expanded=True):
            st.json(submission_payload)
