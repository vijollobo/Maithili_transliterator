import streamlit as st

# --- Script Mappings ---
# Devanagari to Mithilakshara
DEV_TO_MITHILAKSHARA = {'अ': '𑒁', 'आ': '𑒂', 'इ': '𑒃', 'ई': '𑒄', 'उ': '𑒅', 'ऊ': '𑒆', 'ऋ': '𑒇', 'ॠ': '𑒈', 'ऌ': '𑒉', 'ॡ': '𑒊', 'ए': '𑒋', 'ऐ': '𑒌', 'ओ': '𑒍', 'औ': '𑒎', 'ा': '𑒰', 'ि': '𑒱', 'ी': '𑒲', 'ु': '𑒳', 'ू': '𑒴', 'ृ': '𑒵', 'ॄ': '𑒶', 'ॢ': '𑒷', 'ॣ': '𑒸', 'े': '𑒹', 'ै': '𑒻', 'ो': '𑒼', 'ौ': '𑒾', 'ॆ': '𑒺', 'ॊ': '𑒽', 'ं': '𑓀', 'ँ': '𑒿', 'ः': '𑓁', '्': '𑓂', '़': '𑓃', 'ऽ': '𑓄', 'ॐ': '𑓇', 'क': '𑒏', 'ख': '𑒐', 'ग': '𑒑', 'घ': '𑒒', 'ङ': '𑒓', 'च': '𑒔', 'छ': '𑒕', 'ज': '𑒖', 'झ': '𑒗', 'ञ': '𑒘', 'ट': '𑒙', 'ठ': '𑒚', 'ड': '𑒛', 'ढ': '𑒜', 'ण': '𑒝', 'त': '𑒞', 'थ': '𑒟', 'द': '𑒠', 'ध': '𑒡', 'न': '𑒢', 'प': '𑒣', 'फ': '𑒤', 'ब': '𑒥', 'भ': '𑒦', 'म': '𑒧', 'य': '𑒨', 'र': '𑒩', 'ल': '𑒪', 'व': '𑒫', 'श': '𑒬', 'ष': '𑒭', 'स': '𑒮', 'ह': '𑒯', '०': '𑓐', '१': '𑓑', '२': '𑓒', '३': '𑓓', '४': '𑓔', '५': '𑓕', '६': '𑓖', '७': '𑓗', '८': '𑓘', '९': '𑓙', '0': '𑓐', '1': '𑓑', '2': '𑓒', '3': '𑓓', '4': '𑓔', '5': '𑓕', '6': '𑓖', '7': '𑓗', '8': '𑓘', '9': '𑓙'}
# Mithilakshara to Devanagari
MITHILAKSHARA_TO_DEV = {v: k for k, v in DEV_TO_MITHILAKSHARA.items()}

# --- Transliteration Function ---
def transliterate(text, mapping):
    transliterated_text = ""
    for char in text:
        transliterated_text += mapping.get(char, char)
    return transliterated_text

# --- Language Dictionaries ---
LANGUAGES = {
    "English": {
        "title": "Devanagari ↔ Mithilakshara Transliteration",
        "intro": "This app allows you to convert Maithili text between Devanagari and Mithilakshara scripts.",
        "from": "From:",
        "to": "To:",
        "placeholder": "Enter text here:",
        "button": "Transliterate",
        "output_header": "Transliterated Text",
        "script_options": ["Devanagari", "Mithilakshara"],
        "lang_option": "English",
        'copy_button': "Copy Text"
    },
    "Maithili (Devanagari)": {
        "title": "देवनागरी ↔ मिथिलाक्षर लिप्यंतरण",
        "intro": "एहि एपसँ अहाँ मैथिली पाठ कए देवनागरी आ मिथिलाक्षर दुनू लिपिक बीच मे पाठ केँ लिप्यंतरण कऽ सकैत छी।",
        "from": "सँ:",
        "to": "लेल:",
        "placeholder": "अतय पाठ लिखू:",
        "button": "लिप्यंतरण करू",
        "output_header": "लिप्यंतरित पाठ",
        "script_options": ["देवनागरी", "मिथिलाक्षर"],
        "lang_option": "मैथिली (देवनागरी)",
        'copy_button':'पाठ के प्रतिलिपि करू'
    },
    "Maithili (Mithilakshara)": {
        "title": "𑒠𑒹𑒫𑒢𑒰𑒑𑒩𑒲 ↔ 𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩 𑒪𑒱𑒣𑓂𑒨𑒢𑓂𑒞𑒩𑒝",
        "intro": "𑒋𑒯𑒱 𑒋𑒣𑒮𑒿 𑒁𑒯𑒰𑒿 𑒧𑒻𑒟𑒱𑒪𑒲 𑒣𑒰𑒚 𑒏𑒋 𑒠𑒹𑒫𑒢𑒰𑒑𑒩𑒲 𑒂 𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩 𑒠𑒳𑒢𑒴 𑒪𑒱𑒣𑒱𑒏 𑒥𑒲𑒔 𑒧𑒹 𑒣𑒰𑒚 𑒏𑒹𑒿  𑒪𑒱𑒣𑓂𑒨𑒢𑓂𑒞𑒩𑒝 𑒏𑓄 𑒮𑒏𑒻𑒞 𑒕𑒲।",
        "from": "𑒮𑒿:",
        "to": "𑒪𑒹𑒪:",
        "placeholder": "𑒁‎𑒞𑒨 𑒣𑒰𑒚 𑒪𑒱𑒐𑒴:",
        "button": "𑒪𑒱𑒣𑓂𑒨𑒢𑓂𑒞𑒩𑒝 𑒏‎𑒩𑒴",
        "output_header": "𑒪𑒱𑒣𑓂𑒨𑒢𑓂𑒞𑒩𑒱𑒞 𑒣𑒰𑒚",
        "script_options": ["𑒠𑒹𑒫𑒢𑒰𑒑𑒩𑒲", "𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩"],
        "lang_option": "𑒧𑒻𑒟𑒱𑒪𑒲 (𑒧𑒱𑒟𑒱𑒪𑒰𑒏‎𑓂𑒭𑒩)",
        'copy_button':'𑒣𑒰𑒚 𑒏𑒹 𑒣𑓂𑒩𑒞𑒱𑒪𑒱𑒣𑒱 𑒏𑒩𑒴'
    }
}

# --- Streamlit UI ---

# Set page configuration
st.set_page_config(page_title="Transliteration", layout="wide")

# Language selection
st.sidebar.header("Select Language")
lang_choice = st.sidebar.selectbox(
    "Choose a language:",
    list(LANGUAGES.keys()),
    key='language_selector'
)
lang = LANGUAGES[lang_choice]

script_name_map = {
    "Devanagari": lang["script_options"][0],
    "Mithilakshara": lang["script_options"][1]
}

if st.session_state.language_selector != st.session_state.get('last_language', None):
    # This block executes when the language dropdown is changed
    st.session_state.from_script = script_name_map.get(st.session_state.get('from_script', 'Devanagari'), lang["script_options"][0])
    st.session_state.to_script = script_name_map.get(st.session_state.get('to_script', 'Mithilakshara'), lang["script_options"][1])
    st.session_state.last_language = st.session_state.language_selector
    st.rerun() # Force a rerun to apply the new script names
    
# Session state initialization for switching scripts
if 'from_script' not in st.session_state:
    st.session_state['from_script'] = lang["script_options"][0]
if 'to_script' not in st.session_state:
    st.session_state['to_script'] = lang["script_options"][1]

st.title(lang["title"])
st.markdown(lang["intro"])

col1, col2, col3 = st.columns([1, 0.2, 1])

with col1:
    from_script_dropdown = st.selectbox(
        lang["from"],
        lang["script_options"],
        index=lang["script_options"].index(st.session_state.from_script),
        key='from_script_select'
    )
    
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Spacer for alignment
    if st.button("🔄", help="Switch scripts"):
        temp = st.session_state.from_script
        st.session_state.from_script = st.session_state.to_script
        st.session_state.to_script = temp
        st.rerun()

with col3:
    to_script_dropdown = st.selectbox(
        lang["to"],
        lang["script_options"],
        index=lang["script_options"].index(st.session_state.to_script),
        key='to_script_select'
    )

# Sync dropdowns with session state
if st.session_state.from_script_select != st.session_state.from_script or \
   st.session_state.to_script_select != st.session_state.to_script:
    st.session_state.from_script = st.session_state.from_script_select
    st.session_state.to_script = st.session_state.to_script_select

# Text input and output
text_input = st.text_area(f"{lang['placeholder']}", height=150)

if st.button(lang["button"]):
    source_script_name = st.session_state.from_script
    target_script_name = st.session_state.to_script

    # Determine which mapping to use
    if (source_script_name in ["Devanagari", "देवनागरी", "𑒠𑒹𑒫𑒢𑒰𑒑𑒩𑒲"]) and (target_script_name in ["Mithilakshara", "मिथिलाक्षर", "𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩"]):
        mapping = DEV_TO_MITHILAKSHARA
    elif (source_script_name in ["Mithilakshara", "मिथिलाक्षर", "𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩"]) and (target_script_name in ["Devanagari", "देवनागरी", "𑒠𑒹𑒫𑒢𑒰𑒑𑒩𑒲"]):
        mapping = MITHILAKSHARA_TO_DEV
    else:
        mapping = {} # No change needed if same script

    transliterated_text = transliterate(text_input, mapping)
    
    st.subheader(lang["output_header"])
    st.text_area("", value=transliterated_text, height=150)
    
