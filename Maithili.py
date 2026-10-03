import html

import streamlit as st

from mithilakshara import (
    DEV_TO_MITHILAKSHARA,
    devanagari_to_mithilakshara,
    mithilakshara_to_devanagari,
)

st.set_page_config(page_title="Devanagari–Mithilakshara Transliteration", layout="wide")

# --- Interface text ---------------------------------------------------------------
# English and Maithili (Devanagari) are written out below.  The Mithilakshara
# interface is produced from the Maithili text by the converter that does the
# transliteration itself, so the two cannot drift apart.
LANGUAGES = {
    "English": {
        "title": "Devanagari–Mithilakshara Transliteration",
        "intro": "This application converts Maithili text between the Devanagari and Mithilakshara scripts.",
        "language_label": "Interface language",
        "direction_label": "Direction of transliteration",
        "direction_format": "{src} to {dst}",
        "script_options": ["Devanagari", "Mithilakshara"],
        "input_header": "Input",
        "output_header": "Output",
        "placeholder": "Enter text in {script}.",
        "button": "Transliterate",
        "swap": "Swap",
        "clear": "Clear",
        "empty_output": "The transliterated text will appear here.",
        "script_mismatch": "No {script} text was found in the input. Please check the selected direction.",
        "notes_title": "Conversion notes",
        "notes": [
            "Conversion is performed character by character. Letters, vowel signs and digits of one script are replaced by their equivalents in the other; all other characters, including Latin letters and punctuation, are left unchanged.",
            "Devanagari to Mithilakshara: an anusvāra immediately before a stop consonant is written as the nasal of that consonant's varga followed by a virāma. The anusvāra is retained before य, र, ल, व, श, ष, स and ह, and at the end of a word.",
            "Mithilakshara to Devanagari: anusvāra and nasal conjuncts are kept exactly as written; nasal conjuncts are not converted back to anusvāra.",
            "Mithilakshara is encoded in the Unicode block Tirhuta. If its characters appear as empty boxes, install a font that supports it, such as Noto Sans Tirhuta.",
        ],
        "examples_title": "Examples",
        "source_code": "Source code",
    },
    "Maithili (Devanagari)": {
        "title": "देवनागरी–मिथिलाक्षर लिप्यंतरण",
        "intro": "एहि एपसँ अहाँ मैथिली पाठ कए देवनागरी आ मिथिलाक्षर दुनू लिपिक बीच मे पाठ केँ लिप्यंतरण कऽ सकैत छी।",
        "language_label": "भाषा",
        "direction_label": "लिप्यंतरणक दिशा",
        "direction_format": "{src} सँ {dst} मे",
        "script_options": ["देवनागरी", "मिथिलाक्षर"],
        "input_header": "मूल पाठ",
        "output_header": "लिप्यंतरित पाठ",
        "placeholder": "{script} मे पाठ लिखू।",
        "button": "लिप्यंतरण करू",
        "swap": "अदला-बदली",
        "clear": "साफ करू",
        "empty_output": "लिप्यंतरित पाठ अतय प्रदर्शित होएत।",
        "script_mismatch": "मूल पाठ मे {script} पाठ नहि भेटल। कृपया चयनित दिशा जाँच करू।",
        "notes_title": "लिप्यंतरण संबंधी टिप्पणी",
        "notes": [
            "रूपांतरण अक्षर-दर-अक्षर होइत अछि। देवनागरी आ मिथिलाक्षरक वर्ण, मात्रा आ अंक बदलल जाइत अछि; लैटिन अक्षर आ विरामचिह्न सहित आन सभ वर्ण यथावत रहैत अछि।",
            "देवनागरी सँ मिथिलाक्षर मे: स्पर्श व्यंजनसँ ठीक पहिने अनुस्वार रहला पर ओकरा ओहि व्यंजनक वर्गक पंचमाक्षर आ हलन्त सँ लिखल जाइत अछि। य, र, ल, व, श, ष, स, ह सँ पहिने आ शब्दक अन्त मे अनुस्वार यथावत रहैत अछि।",
            "मिथिलाक्षर सँ देवनागरी मे: अनुस्वार आ अनुनासिक संयुक्ताक्षर जेना लिखल अछि तहिना रहैत अछि; संयुक्ताक्षर केँ फेर अनुस्वार मे नहि बदलल जाइत अछि।",
            "मिथिलाक्षर यूनिकोडक Tirhuta खंड मे एनकोड कएल गेल अछि। जँ वर्ण खाली डिब्बा जकाँ देखाय, तँ Noto Sans Tirhuta सन कोनो समर्थित फोंट स्थापित करू।",
        ],
        "examples_title": "उदाहरण",
        "source_code": "स्रोत कोड",
    },
}

# Names of the interface languages, each written in its own script.
LANGUAGE_NAMES = {
    "English": "English",
    "Maithili (Devanagari)": "मैथिली (देवनागरी)",
    "Maithili (Mithilakshara)": devanagari_to_mithilakshara("मैथिली (मिथिलाक्षर)"),
}


def _to_mithilakshara(value):
    if isinstance(value, str):
        return devanagari_to_mithilakshara(value)
    return [_to_mithilakshara(item) for item in value]


LANGUAGES["Maithili (Mithilakshara)"] = {
    key: _to_mithilakshara(value) for key, value in LANGUAGES["Maithili (Devanagari)"].items()
}

# --- Conversion directions --------------------------------------------------------
# "source" and "target" index into a language's script_options (Devanagari, Mithilakshara).
DIRECTIONS = {
    "dev_to_mith": {"source": 0, "target": 1, "convert": devanagari_to_mithilakshara},
    "mith_to_dev": {"source": 1, "target": 0, "convert": mithilakshara_to_devanagari},
}
SCRIPT_BLOCKS = (range(0x0900, 0x0980), range(0x11480, 0x114E0))  # Devanagari, Tirhuta
SHARED_PUNCTUATION = "।॥"


def contains_script(text, script_index):
    block = SCRIPT_BLOCKS[script_index]
    return any(ord(ch) in block and ch not in SHARED_PUNCTUATION for ch in text)


def swap_scripts():
    """Reverse the direction and carry the current output over as the new input."""
    direction = st.session_state.direction
    st.session_state.source_text = DIRECTIONS[direction]["convert"](st.session_state.source_text)
    st.session_state.direction = "mith_to_dev" if direction == "dev_to_mith" else "dev_to_mith"


def clear_text():
    st.session_state.source_text = ""


# --- Appearance ---------------------------------------------------------------------
# Noto Sans Devanagari and Noto Sans Tirhuta are loaded from Google Fonts so that both
# scripts display on any device; Streamlit's own font stays first for Latin text.
STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;600&family=Noto+Sans+Tirhuta&display=swap');
.block-container, [data-testid="stMainBlockContainer"] { max-width: 1080px; padding-top: 2.5rem; padding-bottom: 3rem; }
.stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp li, .stApp label, .stApp td, .stApp th,
.stApp summary, .stApp textarea, .stApp input, .stApp button, .stApp pre, .stApp code,
.stApp [data-baseweb="select"] div, [data-baseweb="popover"] li, [role="listbox"], [role="option"] {
    font-family: "Source Sans", "Source Sans Pro", "Noto Sans Devanagari", "Noto Sans Tirhuta", sans-serif;
}
.stApp h1 { font-size: 2rem; font-weight: 600; line-height: 1.5; padding: 0 0 0.25rem 0; }
.stApp textarea { font-size: 1.2rem; line-height: 1.8; }
.stApp [data-testid="stCode"] pre, .stApp [data-testid="stCode"] pre * { white-space: pre-wrap !important; word-break: break-word; }
.stApp [data-testid="stCode"] pre { min-height: 220px; box-sizing: border-box; }
.stApp [data-testid="stCode"] code { font-size: 1.2rem; line-height: 1.9; }
.panel-head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 0.5rem; }
.panel-head .name { font-weight: 600; font-size: 1.05rem; }
.panel-head .script { opacity: 0.65; font-size: 0.95rem; }
.empty-output { opacity: 0.6; min-height: 220px; padding-top: 0.5rem; }
</style>
"""
st.markdown(STYLE, unsafe_allow_html=True)

# --- Session state ---------------------------------------------------------------------
st.session_state.setdefault("ui_language", "English")
st.session_state.setdefault("direction", "dev_to_mith")
st.session_state.setdefault("source_text", "")

lang = LANGUAGES[st.session_state.ui_language]
names = lang["script_options"]


def direction_label(key):
    option = DIRECTIONS[key]
    return lang["direction_format"].format(src=names[option["source"]], dst=names[option["target"]])


def panel_head(heading, script):
    return (
        '<div class="panel-head">'
        f'<span class="name">{html.escape(heading)}</span>'
        f'<span class="script">{html.escape(script)}</span>'
        "</div>"
    )


# --- Header ---------------------------------------------------------------------------------
title_col, language_col = st.columns([3, 1], gap="large")
with title_col:
    st.title(lang["title"])
    st.write(lang["intro"])
with language_col:
    st.selectbox(
        lang["language_label"],
        list(LANGUAGES),
        key="ui_language",
        format_func=LANGUAGE_NAMES.get,
    )

# --- Direction ---------------------------------------------------------------------------------
# The radio is given the translated labels themselves and the selection is kept in
# st.session_state.direction.  (A radio with a key and a translated format_func returns a
# stale label after the next rerun once the interface language has been changed.)
direction_keys = list(DIRECTIONS)
direction_labels = [direction_label(key) for key in direction_keys]
st.caption(lang["direction_label"])
direction_col, swap_col, _ = st.columns([5, 2, 3])
with direction_col:
    chosen = st.radio(
        lang["direction_label"],
        direction_labels,
        index=direction_keys.index(st.session_state.direction),
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.direction = direction_keys[direction_labels.index(chosen)]
with swap_col:
    st.button(lang["swap"], on_click=swap_scripts)

direction = DIRECTIONS[st.session_state.direction]
source_name, target_name = names[direction["source"]], names[direction["target"]]

# --- Input and output ----------------------------------------------------------------------------
text = st.session_state.source_text
result = direction["convert"](text)

input_col, output_col = st.columns(2, gap="large")

with input_col:
    with st.container(border=True):
        st.markdown(panel_head(lang["input_header"], source_name), unsafe_allow_html=True)
        st.text_area(
            lang["input_header"],
            key="source_text",
            height=220,
            placeholder=lang["placeholder"].format(script=source_name),
            label_visibility="collapsed",
        )
    run_col, clear_col, _ = st.columns([3, 2, 4])
    with run_col:
        st.button(lang["button"], type="primary")
    with clear_col:
        st.button(lang["clear"], on_click=clear_text)
    if (
        text.strip()
        and not contains_script(text, direction["source"])
        and contains_script(text, direction["target"])
    ):
        st.warning(lang["script_mismatch"].format(script=source_name))

with output_col:
    with st.container(border=True):
        st.markdown(panel_head(lang["output_header"], target_name), unsafe_allow_html=True)
        if result.strip():
            st.code(result, language=None)  # the code block has a built-in copy control
        else:
            st.markdown(f'<div class="empty-output">{html.escape(lang["empty_output"])}</div>', unsafe_allow_html=True)

# --- Notes -------------------------------------------------------------------------------------------
def raw(text):
    """Character-for-character mapping, without the anusvāra rule."""
    return "".join(DEV_TO_MITHILAKSHARA.get(ch, ch) for ch in text)


examples = [
    ("अंक", devanagari_to_mithilakshara("अंक")),
    (raw("अङ्क"), mithilakshara_to_devanagari(raw("अङ्क"))),
    (raw("अंक"), mithilakshara_to_devanagari(raw("अंक"))),
]
example_table = f"| {lang['input_header']} | {lang['output_header']} |\n|---|---|\n" + "\n".join(
    f"| {before} | {after} |" for before, after in examples
)

with st.expander(lang["notes_title"]):
    st.markdown("\n".join(f"- {note}" for note in lang["notes"]))
    st.markdown(f"**{lang['examples_title']}**")
    st.markdown(example_table)

st.caption(f"[{lang['source_code']}](https://github.com/vijollobo/Maithili_transliterator)")
