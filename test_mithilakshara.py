"""Tests for mithilakshara.py.  Run:  python test_mithilakshara.py   (or: pytest)"""
import unicodedata

from mithilakshara import (
    DEV_TO_MITHILAKSHARA,
    devanagari_to_mithilakshara as to_mith,
    mithilakshara_to_devanagari as to_dev,
)


def tirhuta(*names):
    """Build a string from Unicode character names, e.g. tirhuta("LETTER KA", "SIGN VIRAMA")."""
    return "".join(unicodedata.lookup("TIRHUTA " + name) for name in names)


def test_anusvara_before_ka_varga_becomes_nga_plus_virama():
    # The case that started this: अंक -> 𑒁𑒓𑓂𑒏, not 𑒁𑓀𑒏
    assert to_mith("अंक") == tirhuta("LETTER A", "LETTER NGA", "SIGN VIRAMA", "LETTER KA")
    assert to_mith("अंक") != tirhuta("LETTER A", "SIGN ANUSVARA", "LETTER KA")


def test_anusvara_becomes_the_nasal_of_the_following_varga():
    cases = {
        "गंगा": "𑒑𑒓𑓂𑒑𑒰",          # ka-varga -> ṅ
        "अंचल": "𑒁𑒘𑓂𑒔𑒪",          # ca-varga -> ñ
        "कंठ": "𑒏𑒝𑓂𑒚",            # ṭa-varga -> ṇ
        "संत": "𑒮𑒢𑓂𑒞",            # ta-varga -> n
        "कंबल": "𑒏𑒧𑓂𑒥𑒪",          # pa-varga -> m
        "चंद्र": "𑒔𑒢𑓂𑒠𑓂𑒩",         # a cluster is judged by its first consonant
        "संक्षेप": "𑒮𑒓𑓂𑒏𑓂𑒭𑒹𑒣",
    }
    for dev, expected in cases.items():
        assert to_mith(dev) == expected, dev


def test_anusvara_is_kept_everywhere_else():
    cases = {
        "वंश": "𑒫𑓀𑒬",              # before a sibilant
        "सिंह": "𑒮𑒱𑓀𑒯",            # before ह
        "संयोग": "𑒮𑓀𑒨𑒼𑒑",          # before a semivowel
        "संस्कृत": "𑒮𑓀𑒮𑓂𑒏𑒵𑒞",
        "त्वं तत्": "𑒞𑓂𑒫𑓀 𑒞𑒞𑓂",    # at the end of a word
    }
    for dev, expected in cases.items():
        assert to_mith(dev) == expected, dev
    assert to_mith("अं") == tirhuta("LETTER A", "SIGN ANUSVARA")   # at the end of the text


def test_explicit_nasal_conjunct_is_unchanged():
    assert to_mith("अङ्क") == to_mith("अंक")


def test_precomposed_nukta_letters_are_split():
    assert to_mith("\u0958") == to_mith("क\u093c")        # क़
    assert to_mith("\u0929") == to_mith("न\u093c")        # ऩ (NFC would fuse this one back)
    assert to_mith("अं\u0958") == to_mith("अंक\u093c")     # the anusvāra rule sees the base letter


def test_reverse_direction_is_a_plain_character_mapping():
    assert to_dev("𑒁𑒓𑓂𑒏") == "अङ्क"
    assert to_dev("𑒁𑓀𑒏") == "अंक"


def test_table_matches_unicode_names():
    def bare(ch):
        return unicodedata.name(ch).replace("TIRHUTA ", "").replace("DEVANAGARI ", "")

    for dev, tir in DEV_TO_MITHILAKSHARA.items():
        assert bare(dev) == bare(tir), (dev, tir)


def test_table_has_no_invisible_characters():
    for dev, tir in DEV_TO_MITHILAKSHARA.items():
        for ch in dev + tir:
            assert unicodedata.category(ch) != "Cf", (dev, tir, hex(ord(ch)))


if __name__ == "__main__":
    tests = [f for name, f in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(len(tests), "tests passed")
