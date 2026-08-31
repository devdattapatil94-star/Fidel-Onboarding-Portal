# ========================================================
# --- SECTION 2: QUALIFICATIONS, LANGUAGES & RATES ---
# ========================================================
st.markdown("#### 🎓 Section 2: Qualifications, Languages & Rates")
native = st.text_input("Native Language *", placeholder="e.g., Japanese")
exp = st.slider("Years of Translation Experience", 0, 40, 2)

# --- SOURCE & TARGET LANGUAGES (Dropdowns with Tickmark Selections) ---
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
cat_options = [
    "MateCat", "MemoQ", "Memsource", "Phrase", 
    "SDL Trados 2019", "SDL Trados 2021", "SDL Trados 2022", 
    "SmartCAT", "WordFast"
]
selected_cat_tools = st.multiselect(
    "Proficient in which of the following CAT Tools:", 
    cat_options,
    placeholder="Select CAT tools..."
)
 
# --- DOMAIN EXPERTISE ---
domain_options = [
    "Banking", "Banking & Finance", "Dentistry", "E-learning", "Economics", 
    "Education", "Electrical", "Electronics", "Electronics Appliances", 
    "Employment Handbooks", "Finance", "General", "Health", "Health & Safety", 
    "Help Documents", "Information Technology", "Insurance", 
    "Law Patents, Trademarks, Copyrights", "Legal", "Logistics", 
    "Manufacturing", "Marketing", "Medical", "Medical Diseases", 
    "Patents", "Pharmaceuticals", "Retail", "Telecommunication", "Transport"
]
selected_domains = st.multiselect(
    "Domain Expertise:", 
    domain_options,
    placeholder="Select domain expertise..."
)
 
# --- SERVICES PROVIDED ---
services_options = [
    "Back Translation (Chars)", "Back Translation (Words)", "Closed Captioning", 
    "Data Annotation", "Data Collection", "Editing", 
    "Machine Translation and Full Post-Editing", "Machine Translation and Light Post-Editing", 
    "Post-Editing", "Proofreading", "Review", "Revision", 
    "Subtitling", "Transcreation", "Transcription", "Translation", "Voice-Over"
]
selected_services = st.multiselect(
    "Services you provide *:", 
    services_options,
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
