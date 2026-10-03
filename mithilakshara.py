"""Devanagari <-> Mithilākṣara (Tirhuta) transliteration for Maithili.

One shared module: the character table and the anusvāra rule live here, and
Maithili.py (Streamlit app), Devanagari_to_Mithilakshara.py and
Mithilakshara_to_Devanagari.py all import from it.

Mithilākṣara is encoded in the Unicode block Tirhuta (U+11480-U+114DF).  Text is
converted character by character, with one context-dependent step: the anusvāra
rule below.  Conjuncts, reph, khaṇḍa-ta and the like are left to the font.
"""
import re
import unicodedata

# --- Character table: Devanagari -> Mithilākṣara ---------------------------
DEV_TO_MITHILAKSHARA = {
    # independent vowels
    'अ': '𑒁',
    'आ': '𑒂',
    'इ': '𑒃',
    'ई': '𑒄',
    'उ': '𑒅',
    'ऊ': '𑒆',
    'ऋ': '𑒇',
    'ॠ': '𑒈',
    'ऌ': '𑒉',
    'ॡ': '𑒊',
    'ए': '𑒋',
    'ऐ': '𑒌',
    'ओ': '𑒍',
    'औ': '𑒎',
    # vowel signs
    'ा': '𑒰',
    'ि': '𑒱',
    'ी': '𑒲',
    'ु': '𑒳',
    'ू': '𑒴',
    'ृ': '𑒵',
    'ॄ': '𑒶',
    'ॢ': '𑒷',
    'ॣ': '𑒸',
    'े': '𑒹',
    'ै': '𑒻',
    'ो': '𑒼',
    'ौ': '𑒾',
    'ॆ': '𑒺',
    'ॊ': '𑒽',
    # signs: anusvāra, candrabindu, visarga, virāma, nukta, avagraha, Om
    'ं': '𑓀',
    'ँ': '𑒿',
    'ः': '𑓁',
    '्': '𑓂',
    '़': '𑓃',
    'ऽ': '𑓄',
    'ॐ': '𑓇',
    # consonants
    'क': '𑒏',
    'ख': '𑒐',
    'ग': '𑒑',
    'घ': '𑒒',
    'ङ': '𑒓',
    'च': '𑒔',
    'छ': '𑒕',
    'ज': '𑒖',
    'झ': '𑒗',
    'ञ': '𑒘',
    'ट': '𑒙',
    'ठ': '𑒚',
    'ड': '𑒛',
    'ढ': '𑒜',
    'ण': '𑒝',
    'त': '𑒞',
    'थ': '𑒟',
    'द': '𑒠',
    'ध': '𑒡',
    'न': '𑒢',
    'प': '𑒣',
    'फ': '𑒤',
    'ब': '𑒥',
    'भ': '𑒦',
    'म': '𑒧',
    'य': '𑒨',
    'र': '𑒩',
    'ल': '𑒪',
    'व': '𑒫',
    'श': '𑒬',
    'ष': '𑒭',
    'स': '𑒮',
    'ह': '𑒯',
    # Devanagari digits
    '०': '𑓐',
    '१': '𑓑',
    '२': '𑓒',
    '३': '𑓓',
    '४': '𑓔',
    '५': '𑓕',
    '६': '𑓖',
    '७': '𑓗',
    '८': '𑓘',
    '९': '𑓙',
    # ASCII digits
    '0': '𑓐',
    '1': '𑓑',
    '2': '𑓒',
    '3': '𑓓',
    '4': '𑓔',
    '5': '𑓕',
    '6': '𑓖',
    '7': '𑓗',
    '8': '𑓘',
    '9': '𑓙',
}

# Reverse table.  Digits appear twice above (Devanagari and ASCII); the later,
# ASCII entries win, so Mithilākṣara digits come back as 0-9.
MITHILAKSHARA_TO_DEV = {v: k for k, v in DEV_TO_MITHILAKSHARA.items()}

# --- Anusvāra rule -----------------------------------------------------------
# An anusvāra directly before a stop is written as the nasal of that stop's varga
# plus virāma, as in Sanskrit and traditional Bangla spelling:
#     अंक -> अङ्क        (𑒁𑒓𑓂𑒏: in Tirhuta ṅka is a single conjunct)
# Everywhere else -- before य र ल व श ष स ह, before a vowel, space or punctuation,
# or at the end of the text -- the anusvāra is kept (𑓀).
# A cluster is judged by its first consonant: संक्षेप -> सङ्क्षेप, मंत्र -> मन्त्र.
ANUSVARA = "\u0902"
VIRAMA = "\u094D"

VARGAS = (
    ("कखगघङ", "ङ"),  # ka-varga
    ("चछजझञ", "ञ"),  # ca-varga
    ("टठडढण", "ण"),  # ṭa-varga
    ("तथदधन", "न"),  # ta-varga
    ("पफबभम", "म"),  # pa-varga
)
_NASAL_FOR = {stop: nasal for stops, nasal in VARGAS for stop in stops}
_ANUSVARA_BEFORE_STOP = re.compile(ANUSVARA + "(?=([" + "".join(_NASAL_FOR) + "]))")

# Precomposed nukta letters (क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़, and ऩ ऱ ऴ) are split into base
# letter + nukta, so the table and the rule above only ever see base letters.
# (Not NFC: NFC would fuse न + ़ back into ऩ, which the table does not have.)
_SPLIT_NUKTA = str.maketrans({
    chr(cp): unicodedata.normalize("NFD", chr(cp))
    for cp in range(0x0900, 0x0980)
    if unicodedata.normalize("NFD", chr(cp))[1:] == "\u093C"
})


def devanagari_to_mithilakshara(text):
    """Convert Devanagari text to Mithilākṣara (Tirhuta)."""
    text = text.translate(_SPLIT_NUKTA)
    text = _ANUSVARA_BEFORE_STOP.sub(lambda m: _NASAL_FOR[m.group(1)] + VIRAMA, text)
    return "".join(DEV_TO_MITHILAKSHARA.get(ch, ch) for ch in text)


def mithilakshara_to_devanagari(text):
    """Convert Mithilākṣara (Tirhuta) text to Devanagari.

    The anusvāra rule is one-way: अंक goes out as 𑒁𑒓𑓂𑒏 and comes back as अङ्क.
    """
    return "".join(MITHILAKSHARA_TO_DEV.get(ch, ch) for ch in text)
