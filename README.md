# Maithili Transliterator

<img height="100" alt="image" src="https://github.com/user-attachments/assets/3c55d1d9-134c-4251-a240-4494e57b1732" />

A tool for transliterating **Maithili** text between the **Devanagari** and **Mithilakshara** (Tirhuta) scripts, in both directions. It consists of a Streamlit web application, a small Python module that performs the conversion, two command-line scripts and a test suite.

**Live application:** <https://maithilitransliterator.streamlit.app/>

## Contents

- [Overview](#overview)
- [Quick start](#quick-start)
- [Repository layout](#repository-layout)
- [Installation](#installation)
- [Using the web application](#using-the-web-application)
- [Using the command-line scripts](#command-line-scripts)
- [Using the Python module](#python-module)
- [How the conversion works](#how-the-conversion-works)
   - [The pipeline](#pipeline)
   - [The character table](#character-table)
   - [Precomposed nukta letters](#nukta-letters)
   - [The anusvāra rule](#anusvara-rule)
   - [The reverse direction](#reverse-direction)
   - [Characters that are not converted](#unconverted-characters)
   - [Worked examples](#worked-examples)
- [The Streamlit application in detail](#application-in-detail)
   - [Layout and data flow](#app-layout)
   - [Interface languages](#interface-languages)
   - [State handling](#app-state)
   - [The direction control](#direction-control)
   - [The wrong-direction warning](#script-mismatch)
   - [Fonts and styling](#fonts-and-styling)
   - [Theme](#theme)
- [Tests](#tests)
- [Customisation](#customisation)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Limitations](#limitations)
- [Background: Maithili and Mithilakshara](#background)
   - [The Maithili language](#maithili-language)
   - [Scripts used for Maithili](#scripts-used-for-maithili)
   - [The Mithilakshara (Tirhuta) script](#tirhuta-script)
   - [Devanagari and Tirhuta compared](#devanagari-and-tirhuta)
   - [Nasal sounds and the anusvāra](#nasals-and-anusvara)
- [Appendix: the Maithili Lexicon spreadsheet](#lexicon-spreadsheet)
- [References](#references)

<a id="overview"></a>

## Overview

Maithili is an Indo-Aryan language of the Mithilā region of India and Nepal. It is written today mainly in Devanagari, but its historical and original script is Mithilakshara, which Unicode calls Tirhuta. This project converts text between the two.

The conversion is a script-to-script mapping. It replaces letters, vowel signs and digits with their counterparts in the other script and applies one orthographic rule, for the anusvāra (see [The anusvāra rule](#anusvara-rule)). It does not translate, correct spelling or analyse words.

**Features**

- Conversion in both directions between Devanagari and Mithilakshara (Unicode block Tirhuta, U+11480 to U+114DF).
- Traditional handling of the anusvāra when writing Mithilakshara: before a stop consonant it becomes the nasal of that consonant's varga followed by a virāma (अंक becomes 𑒁𑒓𑓂𑒏); elsewhere it is kept. Going back to Devanagari, anusvāra signs and nasal conjuncts are left exactly as they are.
- Support for precomposed nukta letters (क़, ख़, ग़, ज़, ड़, ढ़, फ़, य़ and ऩ, ऱ, ऴ).
- A web application with three interface languages (English, Maithili in Devanagari, Maithili in Mithilakshara), a direction selector, Swap and Clear buttons, a copy control on the output, a warning when the input is in the wrong script, built-in conversion notes with live examples, and light and dark themes.
- The Mithilakshara interface text is produced by the converter itself from the Maithili text, so the two versions cannot drift apart.
- Command-line scripts and an importable module with no third-party dependencies.
- A test suite that checks the character table against Unicode character names and locks down the anusvāra rule.

**At a glance**

| Item | Detail |
|---|---|
| Scripts | Devanagari and Mithilakshara (Tirhuta) |
| Web application | `Maithili.py`, built with Streamlit |
| Conversion module | `mithilakshara.py`, standard library only |
| Character table | 89 entries (79 distinct Mithilakshara characters) |
| Lexicon | [`Maithili Lexicon.xlsx`](https://github.com/vijollobo/Maithili_transliterator/blob/main/Maithili%20Lexicon.xlsx) (names, IAST, IPA), reproduced in full in the appendix |
| Tests | 8 tests, runnable with plain Python or pytest |
| Python | 3.10 or newer (required by current Streamlit releases) |
| Tested with | Streamlit 1.64.0 |

<a id="quick-start"></a>

## Quick start

```bash
git clone https://github.com/vijollobo/Maithili_transliterator.git
cd Maithili_transliterator
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# macOS and Linux:       source .venv/bin/activate
pip install streamlit
streamlit run Maithili.py
```

The application opens at <http://localhost:8501>. Full instructions, including Windows specifics, are in [Installation](#installation).

<a id="repository-layout"></a>

## Repository layout

| Path | Purpose |
|---|---|
| `Maithili.py` | The Streamlit web application. |
| `mithilakshara.py` | The conversion module: the character table, the anusvāra rule and the two conversion functions. Everything else depends on it. |
| `Devanagari_to_Mithilakshara.py` | Command-line script, Devanagari to Mithilakshara. |
| `Mithilakshara_to_Devanagari.py` | Command-line script, Mithilakshara to Devanagari. |
| `test_mithilakshara.py` | Test suite for the conversion module. |
| `.streamlit/config.toml` | Light and dark theme colours for the web application. |
| [`Maithili Lexicon.xlsx`](https://github.com/vijollobo/Maithili_transliterator/blob/main/Maithili%20Lexicon.xlsx) | The Maithili Lexicon: the character table with Unicode names, code points, IAST and IPA, and the nasal conjuncts. It is reproduced in full in [the appendix](#lexicon-spreadsheet); no program reads it. |
| `README.md` | This document. |

The dependencies are simple:

```
Maithili.py                      --\
Devanagari_to_Mithilakshara.py   ----> mithilakshara.py  (standard library only)
Mithilakshara_to_Devanagari.py   --/
test_mithilakshara.py            --/
```

Keep these files in one folder. The scripts import `mithilakshara` by name, and Streamlit and Python both put the script's own folder on the import path, so no installation step is needed.

<a id="installation"></a>

## Installation

### Requirements

- **Python 3.10 or newer.** Check with `python --version`.
- **Streamlit.** The application was developed and tested with Streamlit 1.64.0. Use a current release; see [Troubleshooting](#troubleshooting) if the input box is cleared or the interface language resets after you press the button, which was seen on an older installation and disappeared after upgrading.
- **Git** to clone the repository, or download the repository as a ZIP file from GitHub.
- An internet connection in the browser, so that the web fonts for Devanagari and Tirhuta can load from Google Fonts. Without it the application still works, but Mithilakshara text depends on a font installed on the device.

### Windows (PowerShell)

```powershell
git clone https://github.com/vijollobo/Maithili_transliterator.git
cd Maithili_transliterator
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install streamlit
```

If PowerShell refuses to run the activation script, allow scripts for the current window only and try again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

In Command Prompt, activate with `.venv\Scripts\activate.bat` instead.

### macOS and Linux

```bash
git clone https://github.com/vijollobo/Maithili_transliterator.git
cd Maithili_transliterator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install streamlit
```

### Check the installation

```bash
python test_mithilakshara.py
```

Expected output:

```
8 tests passed
```

### Run the web application

Run it from the repository folder, so that `.streamlit/config.toml` is picked up:

```bash
streamlit run Maithili.py
```

If the `streamlit` command is not found, use `python -m streamlit run Maithili.py`. To use another port, add `--server.port 8502`.

### Upgrade Streamlit

```bash
pip install --upgrade streamlit
```

### Optional: a requirements file

The repository does not contain a `requirements.txt`. If you deploy the application (see [Deployment](#deployment)), create one with this line:

```
streamlit>=1.64
```

<a id="using-the-web-application"></a>

## Using the web application

The page is laid out like this:

```
+------------------------------------------------------------------------------+
|  Title                                                   Interface language  |
|  One-line description                                   [ English        v]  |
|                                                                              |
|  Direction of transliteration                                                |
|  (o) Devanagari to Mithilakshara   ( ) Mithilakshara to Devanagari   [Swap]  |
|                                                                              |
|  +------------------------------+     +------------------------------+       |
|  | Input           Devanagari   |     | Output        Mithilakshara  |       |
|  |                              |     |                              |       |
|  | [ text box                 ] |     | [ result, with copy icon   ] |       |
|  |                              |     |                              |       |
|  +------------------------------+     +------------------------------+       |
|  [Transliterate] [Clear]                                                     |
|                                                                              |
|  > Conversion notes                                                          |
|  Source code                                                                 |
+------------------------------------------------------------------------------+
```

| Control | What it does |
|---|---|
| Interface language | Switches the whole page between English, Maithili in Devanagari and Maithili in Mithilakshara. The input text and the direction are kept. |
| Direction | Chooses Devanagari to Mithilakshara or Mithilakshara to Devanagari. The panel headings and the hint in the empty input box follow the choice. |
| Swap | Reverses the direction and carries the current output over into the input box, so a conversion can be checked by converting it back. |
| Input | The text to convert. Streamlit applies the text when you leave the box or press Ctrl+Enter (Cmd+Enter on macOS). |
| Transliterate | The explicit trigger. Pressing it moves the focus out of the input box, which applies the text, and refreshes the output. |
| Clear | Empties the input box. |
| Output | The converted text. A copy icon appears at the top right of the output block when you point at it. |
| Warning | Shown when the input contains only the other script, for example Devanagari text while the direction expects Mithilakshara. |
| Conversion notes | A collapsible panel with the conversion rules and three live examples that are produced by the converter. |

**A typical session**

1. Choose the interface language and the direction.
2. Type or paste text into the input box. Devanagari can be typed with any Devanagari input method; Mithilakshara text is usually pasted from another source.
3. Press **Transliterate**, or click outside the box, or press Ctrl+Enter.
4. Copy the result with the copy icon.
5. To check the result, press **Swap**: the output becomes the input and the direction reverses.

The output is recomputed from the current input and direction on every run of the page; nothing is saved, and the text exists only for the duration of the browser session.

<a id="command-line-scripts"></a>

## Using the command-line scripts

Each script reads one line of text, converts it and prints the result.

```
$ python Devanagari_to_Mithilakshara.py
Enter text in Devanagari Script : अंक
𑒁𑒓𑓂𑒏

$ python Mithilakshara_to_Devanagari.py
Enter text in Mithilakshara script : 𑒁𑒓𑓂𑒏
अङ्क
```

Notes:

- The scripts are three lines long: they import the matching function from `mithilakshara.py`, call `input()` and print the result.
- `input()` reads a single line. For longer or multi-line text, use the web application or the module (see [Using the Python module](#python-module)).
- Many terminals have no font for Tirhuta and show empty boxes even though the text is correct. If that happens, write the result to a UTF-8 file and open it in a browser or editor that has a Tirhuta font (see the snippet in [Using the Python module](#python-module)), or use the web application.

<a id="python-module"></a>

## Using the Python module

`mithilakshara.py` can be used on its own. It needs only the Python standard library.

```python
from mithilakshara import devanagari_to_mithilakshara, mithilakshara_to_devanagari

print(devanagari_to_mithilakshara("अंक"))
print(devanagari_to_mithilakshara("मैथिली भाषाक लिपि मिथिलाक्षर अछि।"))
print(mithilakshara_to_devanagari("𑒁𑒓𑓂𑒏"))
```

Output:

```
𑒁𑒓𑓂𑒏
𑒧𑒻𑒟𑒱𑒪𑒲 𑒦𑒰𑒭𑒰𑒏 𑒪𑒱𑒣𑒱 𑒧𑒱𑒟𑒱𑒪𑒰𑒏𑓂𑒭𑒩 𑒁𑒕𑒱।
अङ्क
```

**Public names**

| Name | Type | Description |
|---|---|---|
| `devanagari_to_mithilakshara(text)` | function | Converts a string from Devanagari to Mithilakshara, applying the anusvāra rule. Returns a string. |
| `mithilakshara_to_devanagari(text)` | function | Converts a string from Mithilakshara to Devanagari. Returns a string. |
| `DEV_TO_MITHILAKSHARA` | dict | The character table, 89 entries. |
| `MITHILAKSHARA_TO_DEV` | dict | The reverse table, 79 entries (built by inverting the table above). |
| `ANUSVARA`, `VIRAMA` | str | The Devanagari anusvāra (U+0902) and virāma (U+094D). |
| `VARGAS` | tuple | The five varga rows used by the anusvāra rule: the stops of each varga and its nasal. |

```python
import mithilakshara as m

print(len(m.DEV_TO_MITHILAKSHARA), len(m.MITHILAKSHARA_TO_DEV))
print(m.VARGAS[0])
print(m.ANUSVARA == "\u0902", m.VIRAMA == "\u094D")
```

```
89 79
('कखगघङ', 'ङ')
True True
```

Both functions take and return `str`. Characters they do not know are passed through unchanged.

**Converting a file**

```python
from pathlib import Path
from mithilakshara import devanagari_to_mithilakshara

text = Path("input.txt").read_text(encoding="utf-8")
Path("output.txt").write_text(devanagari_to_mithilakshara(text), encoding="utf-8")
```

With an `input.txt` that contains two lines, `अंक` and `गंगा`, the file `output.txt` will contain:

```
𑒁𑒓𑓂𑒏
𑒑𑒓𑓂𑒑𑒰
```

<a id="how-the-conversion-works"></a>

## How the conversion works

<a id="pipeline"></a>

### The pipeline

Converting Devanagari to Mithilakshara takes three steps, all in `devanagari_to_mithilakshara()`:

```
Devanagari text
      |
      v
1. Split precomposed nukta letters      (11 characters, str.translate)
      |
      v
2. Apply the anusvara rule              (one regular-expression substitution)
      |
      v
3. Look every character up in the table (characters not in the table pass through)
      |
      v
Mithilakshara text
```

The text stays in logical order, the order in which it is typed, and no characters are reordered. Conjunct formation, vowel-sign placement, reph and ligatures are the job of the font during rendering, not of the converter.

Converting back is a single step, a character-by-character lookup (see [The reverse direction](#reverse-direction)).

<a id="character-table"></a>

### The character table

Devanagari and Tirhuta are both Brahmic scripts with parallel structure, and almost every Devanagari character has a Tirhuta counterpart with the same Unicode name apart from the script prefix. For example, DEVANAGARI LETTER KA (U+0915) corresponds to TIRHUTA LETTER KA (U+1148F). The table in `mithilakshara.py` maps each Devanagari character to the Tirhuta character of the same name, and a test verifies this for every entry (see [Tests](#tests)).

| Group | Entries | Examples |
|---|---|---|
| Independent vowels | 14 | अ → 𑒁 आ → 𑒂 इ → 𑒃 |
| Vowel signs | 15 | ◌ा → ◌𑒰 ◌ि → ◌𑒱 ◌ी → ◌𑒲 |
| Signs | 7 | ◌ं → ◌𑓀 ◌ँ → ◌𑒿 ◌ः → ◌𑓁 |
| Consonants | 33 | क → 𑒏 ख → 𑒐 ग → 𑒑 |
| Devanagari digits | 10 | ० → 𑓐 १ → 𑓑 २ → 𑓒 |
| ASCII digits | 10 | 0 → 𑓐 1 → 𑓑 2 → 𑓒 |

The table has 89 entries but only 79 distinct Mithilakshara characters, because the Devanagari digits and the ASCII digits both map to the Tirhuta digits. The complete table, with code points, Unicode names, IAST and IPA, is in [Appendix: the Maithili Lexicon spreadsheet](#lexicon-spreadsheet).

<a id="nukta-letters"></a>

### Precomposed nukta letters

Unicode gives 11 Devanagari letters a precomposed form that is canonically equivalent to a base letter followed by the nukta sign (U+093C): क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़ (U+0958 to U+095F) and ऩ ऱ ऴ (U+0929, U+0931, U+0934). The table contains only base letters and the nukta, so the converter first expands these 11 characters:

| Precomposed | Code point | Expanded to |
|---|---|---|
| ऩ | U+0929 | U+0928 U+093C |
| ऱ | U+0931 | U+0930 U+093C |
| ऴ | U+0934 | U+0933 U+093C |
| क़ | U+0958 | U+0915 U+093C |
| ख़ | U+0959 | U+0916 U+093C |
| ग़ | U+095A | U+0917 U+093C |
| ज़ | U+095B | U+091C U+093C |
| ड़ | U+095C | U+0921 U+093C |
| ढ़ | U+095D | U+0922 U+093C |
| फ़ | U+095E | U+092B U+093C |
| य़ | U+095F | U+092F U+093C |

The converter does **not** use Unicode normalisation (NFC) for this, for two reasons. NFC would turn न + ़ back into the single character ऩ, which the table does not contain, and normalisation would also rewrite accents and other combining sequences in any non-Devanagari text that happens to be in the input. Expanding exactly these 11 characters has neither effect. As a side benefit, the anusvāra rule then always sees a base letter, so अं + क़ is handled like अं + क.

<a id="anusvara-rule"></a>

### The anusvāra rule

**The rule.** When converting to Mithilakshara, an anusvāra (ं) that is immediately followed by a stop consonant is replaced by the nasal consonant of that stop's varga plus a virāma. In every other position the anusvāra is kept and mapped to the Tirhuta anusvāra.

| Varga | Stops | Nasal + virāma | Example | After the rule | Output |
|---|---|---|---|---|---|
| ka-varga | क ख ग घ ङ | ङ् | गंगा | गङ्गा | 𑒑𑒓𑓂𑒑𑒰 |
| ca-varga | च छ ज झ ञ | ञ् | अंचल | अञ्चल | 𑒁𑒘𑓂𑒔𑒪 |
| ṭa-varga | ट ठ ड ढ ण | ण् | कंठ | कण्ठ | 𑒏𑒝𑓂𑒚 |
| ta-varga | त थ द ध न | न् | संत | सन्त | 𑒮𑒢𑓂𑒞 |
| pa-varga | प फ ब भ म | म् | कंबल | कम्बल | 𑒏𑒧𑓂𑒥𑒪 |

The five rows are the five classes of stops in their traditional order. Each class ends with its own nasal, and that is the letter used.

**Where the anusvāra stays**

| Input | Output | Why the anusvāra stays |
|---|---|---|
| सिंह | 𑒮𑒱𑓀𑒯 | the next letter is ह |
| वंश | 𑒫𑓀𑒬 | the next letter is a sibilant (श) |
| हंस | 𑒯𑓀𑒮 | the next letter is a sibilant (स) |
| संयोग | 𑒮𑓀𑒨𑒼𑒑 | the next letter is a semivowel (य) |
| संवाद | 𑒮𑓀𑒫𑒰𑒠 | the next letter is a semivowel (व) |
| संस्कृत | 𑒮𑓀𑒮𑓂𑒏𑒵𑒞 | the next letter is a sibilant (स); the cluster after it is not examined |
| त्वं तत् | 𑒞𑓂𑒫𑓀 𑒞𑒞𑓂 | the anusvāra ends a word (a space follows) |
| अं | 𑒁𑓀 | the anusvāra ends the text |
| हँस | 𑒯𑒿𑒮 | candrabindu (ँ) is a different sign and is never touched |

The semivowels (य र ल व), the sibilants (श ष स) and ह are not stops and have no homorganic nasal, so there is no nasal conjunct to write in these positions.

**Clusters and explicit nasals**

| Input | After the rule | Output | Why |
|---|---|---|---|
| संक्षेप | सङ्क्षेप | 𑒮𑒓𑓂𑒏𑓂𑒭𑒹𑒣 | a cluster is judged by its first consonant (क, ka-varga) |
| संज्ञा | सञ्ज्ञा | 𑒮𑒘𑓂𑒖𑓂𑒘𑒰 | first consonant ज (ca-varga) |
| मंत्र | मन्त्र | 𑒧𑒢𑓂𑒞𑓂𑒩 | first consonant त (ta-varga) |
| चंद्र | चन्द्र | 𑒔𑒢𑓂𑒠𑓂𑒩 | first consonant द (ta-varga) |
| संमान | सम्मान | 𑒮𑒧𑓂𑒧𑒰𑒢 | म is in the pa-varga, so the nasal is म् |
| अङ्क | अङ्क | 𑒁𑒓𑓂𑒏 | an explicit nasal is left alone, so the result equals that of अंक |

**Implementation.** The rule is one regular-expression substitution on the Devanagari text, before the table lookup:

```python
_ANUSVARA_BEFORE_STOP = re.compile(ANUSVARA + "(?=([" + "".join(_NASAL_FOR) + "]))")
text = _ANUSVARA_BEFORE_STOP.sub(lambda m: _NASAL_FOR[m.group(1)] + VIRAMA, text)
```

The compiled pattern is `ं(?=([कखगघङचछजझञटठडढणतथदधनपफबभम]))`. The part in `(?=...)` is a lookahead: it looks at the next character without consuming it, and captures it so that the replacement can choose the nasal. The match itself is only the anusvāra, because the lookahead consumes nothing; that one character is replaced by the nasal and a virāma, and the stop stays where it is. The rule works on Devanagari text, before the lookup, so the inserted nasal and virāma are converted by the table like any other characters. `_NASAL_FOR` is a dictionary from each of the 25 stops to its nasal, built from `VARGAS`.

**Why this rule.** In Sanskrit orthography a nasal before a stop takes the place of articulation of the stop, and Devanagari offers the anusvāra as a shorthand for it. Bengali–Assamese, a script family closely related to Tirhuta, traditionally writes the explicit nasal conjunct instead (for example অঙ্ক, গঙ্গা, সঙ্গীত). This project takes traditional Bangla orthography as its reference for Mithilakshara, so the shorthand is expanded. A Devanagari text that already has the explicit conjunct (अङ्क) and one that uses the shorthand (अंक) therefore give the same Mithilakshara output. More background is in [Nasal sounds and the anusvāra](#nasals-and-anusvara).

**What it looks like.** The two spellings are drawn differently by a Tirhuta font. In Noto Sans Tirhuta 2.003, the anusvāra spelling of अंक is drawn as 3 glyphs (the letter a, a separate anusvāra mark and the ka), while the conjunct spelling is drawn as 2 glyphs: the letter a and one ṅka ligature. Not every nasal conjunct has its own ligature in every font. In the tested release, 15 of the 25 combinations are single ligature glyphs:

ङ्क (𑒓𑓂𑒏), ङ्ख (𑒓𑓂𑒐), ङ्ग (𑒓𑓂𑒑), ङ्घ (𑒓𑓂𑒒), ञ्च (𑒘𑓂𑒔), ञ्छ (𑒘𑓂𑒕), ण्ट (𑒝𑓂𑒙), ण्ठ (𑒝𑓂𑒚), ण्ड (𑒝𑓂𑒛), ण्ढ (𑒝𑓂𑒜), ण्ण (𑒝𑓂𑒝), न्त (𑒢𑓂𑒞), न्द (𑒢𑓂𑒠), न्ध (𑒢𑓂𑒡), न्न (𑒢𑓂𑒢)

9 are drawn as two letters joined by a visible virāma:

ङ्ङ (𑒓𑓂𑒓), ञ्ज (𑒘𑓂𑒖), ञ्झ (𑒘𑓂𑒗), ञ्ञ (𑒘𑓂𑒘), न्थ (𑒢𑓂𑒟), म्प (𑒧𑓂𑒣), म्फ (𑒧𑓂𑒤), म्भ (𑒧𑓂𑒦), म्म (𑒧𑓂𑒧)

and 1 is drawn with half forms:

म्ब (𑒧𑓂𑒥)

This is a property of the font, not of the encoding. The text is the same in all cases.

<a id="reverse-direction"></a>

### The reverse direction

`mithilakshara_to_devanagari()` is a plain character lookup. The reverse table is built by inverting the main table:

```python
MITHILAKSHARA_TO_DEV = {v: k for k, v in DEV_TO_MITHILAKSHARA.items()}
```

Three consequences follow.

- **Anusvāra signs and nasal conjuncts are preserved exactly as written.** 𑒁𑒓𑓂𑒏 returns as अङ्क, and 𑒁𑓀𑒏 returns as अंक. Nasal conjuncts are never folded back into the anusvāra.
- **A round trip is not the identity.** अंक becomes 𑒁𑒓𑓂𑒏 and returns as अङ्क, which is the explicit spelling.
- **Digits come back as ASCII digits.** The table lists the digits twice, Devanagari first and ASCII second, and in the inverted dictionary the later entry wins. If you prefer Devanagari digits, see [Customisation](#customisation).

<a id="unconverted-characters"></a>

### Characters that are not converted

Any character that is not in the table passes through unchanged, in both directions. That covers Latin letters, spaces, ASCII punctuation, emoji and every script other than Devanagari and Tirhuta. It also covers 38 characters of the Devanagari block that have no entry in the table:

| Group | Characters | Notes |
|---|---|---|
| Danda and double danda | । ॥ | Shared by both scripts, so they are deliberately left as they are. |
| Vedic accent marks | ◌॑ ◌॒ ◌॓ ◌॔ | No counterpart in the table. |
| Letters and signs used for other languages and dialects | ◌ऀ ऄ ऍ ऎ ऑ ऒ ळ ◌ऺ ◌ऻ ◌ॅ ◌ॉ ◌ॎ ◌ॏ ◌ॕ ◌ॖ ◌ॗ ॰ ॱ ॲ ॳ ॴ ॵ ॶ ॷ ॸ ॹ ॺ ॻ ॼ ॽ ॾ ॿ | Candra vowels, short A, ळ, the extended letters U+0972 to U+097F and similar. Tirhuta has no corresponding characters, or the table does not cover them. |

In the other direction, the three Tirhuta characters the converter never produces (Anji U+11480, Gvang U+114C5 and the abbreviation sign U+114C6) also pass through when they appear in the input.

<a id="worked-examples"></a>

### Worked examples

Each table shows the text after every step, with its code points.

**अंक**

| Step | Text | Code points |
|---|---|---|
| Input | अंक | U+0905 U+0902 U+0915 |
| 1. Split precomposed nukta letters | अंक | U+0905 U+0902 U+0915 |
| 2. Anusvāra rule | अङ्क | U+0905 U+0919 U+094D U+0915 |
| 3. Table lookup (output) | 𑒁𑒓𑓂𑒏 | U+11481 U+11493 U+114C2 U+1148F |

**सिंह**

| Step | Text | Code points |
|---|---|---|
| Input | सिंह | U+0938 U+093F U+0902 U+0939 |
| 1. Split precomposed nukta letters | सिंह | U+0938 U+093F U+0902 U+0939 |
| 2. Anusvāra rule | सिंह | U+0938 U+093F U+0902 U+0939 |
| 3. Table lookup (output) | 𑒮𑒱𑓀𑒯 | U+114AE U+114B1 U+114C0 U+114AF |

**ज़िंदगी**

| Step | Text | Code points |
|---|---|---|
| Input | ज़िंदगी | U+095B U+093F U+0902 U+0926 U+0917 U+0940 |
| 1. Split precomposed nukta letters | ज़िंदगी | U+091C U+093C U+093F U+0902 U+0926 U+0917 U+0940 |
| 2. Anusvāra rule | ज़िन्दगी | U+091C U+093C U+093F U+0928 U+094D U+0926 U+0917 U+0940 |
| 3. Table lookup (output) | 𑒖𑓃𑒱𑒢𑓂𑒠𑒑𑒲 | U+11496 U+114C3 U+114B1 U+114A2 U+114C2 U+114A0 U+11491 U+114B2 |

In the first example the anusvāra (U+0902) is followed by क (U+0915), which is a ka-varga stop, so step 2 inserts ङ and a virāma. In the second the next letter is ह, so the anusvāra is kept all the way to the output (U+114C0). In the third the precomposed ज़ (U+095B) is first split into ज and a nukta, and the anusvāra before द then becomes न्.

<a id="application-in-detail"></a>

## The Streamlit application in detail

`Maithili.py` is a single script. Streamlit runs it from top to bottom on every interaction. This section describes how it is organised, and why some parts are written the way they are.

<a id="app-layout"></a>

### Layout and data flow

```
Maithili.py
 |
 |- imports the converters and the table from mithilakshara.py
 |- LANGUAGES            interface text for three languages
 |- DIRECTIONS           the two conversion directions
 |- STYLE                CSS and web-font import
 |
 |- header               title, description, interface-language selector
 |- direction            radio buttons and the Swap button
 |- input panel          text box, Transliterate and Clear buttons, warning
 |- output panel         converted text, or a hint when there is none
 |- conversion notes     rules and live examples in an expander
 |- footer               link to this repository
```

Data flows in one direction on each run:

```
session state      set by                       used for
ui_language  <--  interface-language selector  lang = LANGUAGES[ui_language]
direction    <--  direction radio (and Swap)   direction = DIRECTIONS[direction]
source_text  <--  text box (and Clear, Swap)   result = direction["convert"](source_text)
                                              -> shown with st.code(result)
```

<a id="interface-languages"></a>

### Interface languages

`LANGUAGES` maps three keys, `"English"`, `"Maithili (Devanagari)"` and `"Maithili (Mithilakshara)"`, to dictionaries of interface text. Only the first two are written out in the file. The third is generated from the Maithili text by the converter:

```python
LANGUAGES["Maithili (Mithilakshara)"] = {
    key: _to_mithilakshara(value) for key, value in LANGUAGES["Maithili (Devanagari)"].items()
}
```

This keeps the Mithilakshara interface identical in wording to the Devanagari one, and it applies the anusvāra rule to the interface itself: the Devanagari word लिप्यंतरण appears as लिप्यन्तरण in Mithilakshara. The names of the interface languages in the selector are kept in `LANGUAGE_NAMES`, each written in its own script, and the selector uses them through `format_func`.

Every language dictionary has the same keys:

| Key | Content |
|---|---|
| `title` | Page heading. |
| `intro` | One-sentence description under the heading. |
| `language_label` | Label of the interface-language selector. |
| `direction_label` | Caption and accessible label of the direction control. |
| `direction_format` | Template for the two direction labels; placeholders `{src}` and `{dst}`. |
| `script_options` | Names of the two scripts, in the order Devanagari, Mithilakshara. |
| `input_header` | Heading of the input panel (also the first header of the examples table). |
| `output_header` | Heading of the output panel (also the second header of the examples table). |
| `placeholder` | Hint shown in the empty input box; placeholder `{script}`. |
| `button` | Label of the primary button. |
| `swap` | Label of the Swap button. |
| `clear` | Label of the Clear button. |
| `empty_output` | Text shown in the output panel while there is nothing to show. |
| `script_mismatch` | Wrong-direction warning; placeholder `{script}`. |
| `notes_title` | Title of the Conversion notes panel. |
| `notes` | List of notes shown inside that panel. |
| `examples_title` | Heading above the examples table. |
| `source_code` | Text of the footer link to this repository. |

Text containing `{src}`, `{dst}` or `{script}` is completed with `str.format` when the page is built. Avoid ASCII digits in Maithili interface text: the converter would turn them into Tirhuta digits.

<a id="app-state"></a>

### State handling

Three values are kept in `st.session_state`:

| Key | Holds | Bound to |
|---|---|---|
| `ui_language` | The key of the chosen interface language. | The interface-language selector (`key="ui_language"`). |
| `direction` | `"dev_to_mith"` or `"mith_to_dev"`. | Set from the direction radio buttons and by Swap. |
| `source_text` | The text in the input box. | The text box (`key="source_text"`), and set by Clear and Swap. |

Defaults are set with `setdefault` at the top of the script. The output is never stored. It is recomputed from `source_text` and `direction` on every run, so it cannot become stale.

Two small callbacks change state before the page is redrawn: `swap_scripts()` converts the current text with the current direction, stores the result in `source_text` and flips `direction`; `clear_text()` empties `source_text`. Streamlit runs callbacks before the script body, which is why they can change the values of widgets that are drawn later in the same run.

<a id="direction-control"></a>

### The direction control

The direction radio looks simpler than it is. The obvious implementation gives the radio `key="direction"`, passes the two direction keys as options and translates them with `format_func`. During testing with Streamlit 1.64 that version failed in one sequence: with a stored selection, change the interface language, then trigger any other rerun, and the radio returned its translated label instead of its key, which crashed the lookup in `DIRECTIONS`. The application therefore passes the translated labels themselves as the options, restores the selection from `st.session_state.direction` through the `index` argument, and maps the chosen label back to the key:

```python
direction_keys = list(DIRECTIONS)
direction_labels = [direction_label(key) for key in direction_keys]
chosen = st.radio(
    lang["direction_label"],
    direction_labels,
    index=direction_keys.index(st.session_state.direction),
    horizontal=True,
    label_visibility="collapsed",
)
st.session_state.direction = direction_keys[direction_labels.index(chosen)]
```

Keep this shape if you modify the control. There is a comment in the source at that point.

<a id="script-mismatch"></a>

### The wrong-direction warning

When the input contains characters of the target script but none of the source script, the application shows a warning instead of silently returning text that looks unchanged. `contains_script()` checks code points against two ranges, Devanagari (U+0900 to U+097F) and Tirhuta (U+11480 to U+114DF). The danda and double danda are ignored because both scripts share them. Mixed text, digits-only text and Latin-only text do not trigger the warning.

<a id="fonts-and-styling"></a>

### Fonts and styling

The `STYLE` string is injected once with `st.markdown(..., unsafe_allow_html=True)`.

- **Web fonts.** An `@import` loads Noto Sans Devanagari and Noto Sans Tirhuta from Google Fonts. Streamlit's own font stays first in the stack, so Latin text keeps its normal look, and the browser falls back to the Noto fonts for Devanagari and Tirhuta characters.
- **Where the font stack is applied.** To headings, paragraphs, labels, list items, table cells, the expander summary, the text area, inputs, buttons, code blocks and the selector's drop-down list. It is deliberately not applied to every element, because a blanket rule would also override the icon font that Streamlit uses for its own controls.
- **Output block.** `st.code` provides the copy control. CSS makes its text wrap instead of scrolling sideways (the highlighter sets `white-space` on inner elements, hence the `!important`), gives it the same minimum height as the input box and enlarges the text.
- **Layout.** The page is `layout="wide"`, and the content is limited to 1080 pixels so that long lines stay readable.

The selectors rely on attributes such as `data-testid="stCode"` that belong to Streamlit's front end. They are stable between recent releases but are not a public interface, so check the output panel after a major Streamlit upgrade.

<a id="theme"></a>

### Theme

`.streamlit/config.toml` sets the accent colour:

```toml
[theme.light]
primaryColor = "#2B5C9E"

[theme.dark]
primaryColor = "#3B73B9"
```

The two sections are used instead of a single `[theme]` section because, in Streamlit 1.64, a `[theme]` section that sets only `primaryColor` replaces the automatic light and dark switching and keeps the application in the light theme. With separate sections the application follows the system setting. Streamlit reads this file from the folder in which `streamlit run` is started, so run the application from the repository folder.

<a id="tests"></a>

## Tests

`test_mithilakshara.py` checks the conversion module. Run it with plain Python:

```bash
python test_mithilakshara.py
```

or with pytest (`pip install pytest`, then `pytest`). Both need no other setup.

| Test | What it checks |
|---|---|
| `test_anusvara_before_ka_varga_becomes_nga_plus_virama` | अंक gives exactly the four characters A, NGA, VIRAMA, KA (built from Unicode names) and not the anusvāra form. |
| `test_anusvara_becomes_the_nasal_of_the_following_varga` | Seven words: one for each of the five vargas, plus चंद्र and संक्षेप, which show that a cluster is judged by its first consonant. |
| `test_anusvara_is_kept_everywhere_else` | Words with a sibilant, ह, a semivowel, a word-final anusvāra and an anusvāra at the end of the text. |
| `test_explicit_nasal_conjunct_is_unchanged` | अङ्क and अंक give the same output. |
| `test_precomposed_nukta_letters_are_split` | क़ and ऩ behave like their two-character forms, and the anusvāra rule sees the base letter. |
| `test_reverse_direction_is_a_plain_character_mapping` | The explicit conjunct and the anusvāra both come back unchanged. |
| `test_table_matches_unicode_names` | For all 89 entries, the Devanagari and Tirhuta characters have the same Unicode name apart from the script prefix. |
| `test_table_has_no_invisible_characters` | No entry contains a format character such as the left-to-right mark. |

The last two tests protect the table itself. The first catches a wrong or mistyped mapping, and the second catches invisible characters of the kind that earlier versions of the scripts contained (see [Appendix: the Maithili Lexicon spreadsheet](#lexicon-spreadsheet)).

<a id="customisation"></a>

## Customisation

**Keep the anusvāra before one varga.** Remove or comment out its row in `VARGAS` in `mithilakshara.py`. For example, with the pa-varga disabled:

```python
VARGAS = (
    ("कखगघङ", "ङ"),  # ka-varga
    ("चछजझञ", "ञ"),  # ca-varga
    ("टठडढण", "ण"),  # ṭa-varga
    ("तथदधन", "न"),  # ta-varga
    # ("पफबभम", "म"),  # pa-varga (disabled)
)
```

In a scratch copy of the module with that edit, कंबल then converts to 𑒏𑓀𑒥𑒪 (anusvāra kept) while अंक still converts to 𑒁𑒓𑓂𑒏. The tests that expect the pa-varga conversion would need to be adjusted.

**Return Devanagari digits.** After importing the module, update the reverse table:

```python
import mithilakshara as m

m.MITHILAKSHARA_TO_DEV.update({m.DEV_TO_MITHILAKSHARA[d]: d for d in "०१२३४५६७८९"})
print(m.mithilakshara_to_devanagari("𑓑𑓒𑓓"))
```

```
१२३
```

**Add an interface language.** Add a dictionary with all the keys listed in [Interface languages](#interface-languages) to `LANGUAGES` and a display name to `LANGUAGE_NAMES`. The selector picks it up automatically. Keep `script_options` in the order Devanagari, Mithilakshara.

**Change the Maithili wording.** Edit the strings under `"Maithili (Devanagari)"`. The Mithilakshara interface is regenerated from them.

**Change the accent colour.** Edit `primaryColor` in `.streamlit/config.toml`.

**Add characters to the table.** Add the pair to `DEV_TO_MITHILAKSHARA`. If the two characters do not share a Unicode name (for instance Gvang, which has no Devanagari counterpart), `test_table_matches_unicode_names` will fail by design, and the test then needs an explicit exception.

<a id="deployment"></a>

## Deployment

**Streamlit Community Cloud**

1. Push the whole repository to GitHub, including `mithilakshara.py` and `.streamlit/config.toml`.
2. Add a `requirements.txt` containing `streamlit>=1.64`.
3. In Community Cloud, create an app from the repository and choose `Maithili.py` as the main file.
4. After you change `requirements.txt` or the Python version, reboot the app from the Community Cloud dashboard so that the new environment is built.

**Your own server**

```bash
streamlit run Maithili.py --server.address 0.0.0.0 --server.port 8501
```

Run it from the repository folder. If the application sits behind a reverse proxy, the proxy must pass WebSocket connections through, because Streamlit uses them for every interaction.

**What the deployment needs from the visitor's browser.** Access to `fonts.googleapis.com` and `fonts.gstatic.com`, so that the Noto fonts can load. If those hosts are blocked, text in both scripts depends on the fonts installed on the device.

<a id="troubleshooting"></a>

## Troubleshooting

| Symptom | Cause and remedy |
|---|---|
| Mithilakshara text shows as empty boxes. | The device has no font for the Tirhuta block. In the web application, check that the browser can reach Google Fonts. Elsewhere, install Noto Sans Tirhuta (<https://github.com/notofonts/tirhuta>) or another font that covers U+11480 to U+114DF. |
| Dotted circles or gaps appear inside Mithilakshara words. | Either the font lacks shaping rules for the cluster, or the text contains an invisible character such as U+200E. Earlier versions of the scripts produced these marks. Use the current `mithilakshara.py`, which contains none, and check text from other sources with `unicodedata.category(ch) == 'Cf'`. |
| The input box is cleared and the interface language returns to English after pressing Transliterate. | This was seen with an older Streamlit installation and disappeared after upgrading. Run `pip install --upgrade streamlit` and restart the application (on Community Cloud, reboot it). |
| `ModuleNotFoundError: No module named 'mithilakshara'`. | `mithilakshara.py` is not in the same folder as the script. Keep all the files together. |
| `ModuleNotFoundError: No module named 'streamlit'`. | Streamlit is not installed in the active environment. Activate the virtual environment and run `pip install streamlit`. |
| `streamlit` is not recognised as a command. | Use `python -m streamlit run Maithili.py`, or activate the virtual environment first. |
| PowerShell cannot activate the virtual environment. | Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that window and try again. |
| The port is already in use. | Start the application on another port: `streamlit run Maithili.py --server.port 8502`. |
| A warning says that no Devanagari (or Mithilakshara) text was found. | The input is in the other script. Change the direction or press Swap. |
| The anusvāra was not converted. | The conversion applies only before stop consonants. Before य र ल व श ष स ह and at the end of a word it is kept on purpose (see [The anusvāra rule](#anusvara-rule)). |
| The result looks the same as the input. | Characters that are not in the table pass through. Check that the direction matches the script of the input. |

<a id="limitations"></a>

## Limitations

- **Script conversion only.** There is no translation, spelling correction or normalisation of Maithili orthography. Conventions such as the marks some authors use for a pronounced final schwa are carried over character by character and are not reinterpreted.
- **The anusvāra rule looks only at the next letter.** It cannot tell an anusvāra that is etymologically a nasal from one written as a shorthand, and it treats both alike before a stop. It never converts an anusvāra before a semivowel, sibilant or ह, or at the end of a word.
- **The reverse direction is not the inverse of the forward one.** Nasal conjuncts stay conjuncts, and Tirhuta digits return as ASCII digits.
- **38 characters of the Devanagari block are not in the table** and pass through unchanged (see [Characters that are not converted](#unconverted-characters)). ASCII digits are converted to Tirhuta digits, which can be unwelcome in numbers such as telephone numbers.
- **Rendering depends on the font.** The converter produces correct code points in logical order. Whether a cluster is drawn as a ligature, with a visible virāma or in half forms is decided by the font.
- **Only two scripts.** Kaithi, Newar and Roman (IAST or ISO 15919) input and output are not supported.
- **No Vedic accent handling.** Vedic accent marks are not in the table.

<a id="background"></a>

## Background: Maithili and Mithilakshara

This section collects background that is useful for understanding the tool and for checking its choices. The spellings Maithili, Mithilakshara, Devanagari and Tirhuta are used as in the code and the interface. Linguistic terms (anusvāra, virāma, varga) and Indian names are written in IAST.

<a id="maithili-language"></a>

### The Maithili language

Maithili (Maithilī, ISO 639-3 code `mai`) is an Eastern Indo-Aryan language that descends from Magadhi Prakrit through Apabhraṃśa. It is native to Mithilā: northern and eastern Bihar and the Santhal Pargana division of Jharkhand in India, and the eastern Terai of Nepal, in the Koshi and Madhesh Provinces. The name comes from Mithilā, the ancient kingdom of King Janaka; Maithilī is also a name of Janaka's daughter Sītā.

**Status.** Maithili was added to the Eighth Schedule of the Constitution of India in 2003 (92nd Amendment), which makes it one of the 22 scheduled languages. Jharkhand gave it the status of a second official language in 2018. In Nepal it is the second most widely spoken language and has official status in the Koshi and Madhesh Provinces.

**Speakers.** The Census of India 2011 recorded 13,583,464 people (1.12 per cent of the population) with Maithili as their mother tongue; some sources consider this an undercount, because census returns depend on how speakers report their mother tongue. Estimates of the total number of speakers differ widely between sources, from roughly 34 million to 75 million.

**Varieties.** Maithili has many dialects, and how its varieties are classified is debated. Bajjika, for example, is sometimes called Western Maithili and sometimes treated as a separate language. A script converter is unaffected by dialect, because it changes letters and not words.

**A short timeline**

| Period | Event |
|---|---|
| c. 700 to 1300 | The Caryāpada songs, in which several scholars see traces of proto-Maithili. |
| Early 14th century | Jyotirīśvara Ṭhākura writes the Varṇa Ratnākara, the earliest known Maithili prose text, in Mithilakshara. |
| 14th and 15th centuries | Vidyāpati composes more than a thousand songs in Maithili. |
| 1881 | George Grierson publishes the first grammar of Maithili and treats it as a distinct language. |
| Early 20th century | Devanagari spreads, Kaithi is in everyday use, and Tirhuta is mostly associated with Maithil Brahmins. |
| 1965 | The Sahitya Akademi recognises Maithili. |
| 2003 | Maithili is added to the Eighth Schedule of the Indian Constitution. |
| 2013 | The Mithilakshar Saksharta Abhiyan, a campaign for literacy in the script, begins. |
| 2014 | Tirhuta is added to the Unicode Standard in version 7.0. |
| 2018 | Maithili becomes a second official language of Jharkhand. |

<a id="scripts-used-for-maithili"></a>

### Scripts used for Maithili

| Script | Role |
|---|---|
| Mithilakshara (Tirhuta) | The historical and original script of Maithili, in use for many centuries. It is still used for ceremonial writing, signage, religious texts, genealogical records and letters, and has seen a revival of interest in the 21st century. |
| Kaithi | Widely used for everyday and administrative writing until the 20th century. |
| Newar | Used for Maithili in Nepal in the past. |
| Devanagari | The dominant script today, and the form in which Maithili is officially recognised and taught. |

Over the 20th century Devanagari gradually replaced the other scripts in print and education. That is why most Maithili text that exists in digital form is in Devanagari, and why a converter from Devanagari is the practical way to produce Mithilakshara text.

<a id="tirhuta-script"></a>

### The Mithilakshara (Tirhuta) script

**Names.** The script is called Mithilakshara (Mithilākṣara, "the letters of Mithilā"), Tirhuta (after Tirhut, the historical name of the region around Darbhanga and Muzaffarpur), Maithili script, or Vaidehi script. Its ISO 15924 code is `Tirh`.

**Structure.** Tirhuta is an abugida written from left to right. Each consonant letter carries an inherent vowel; vowel signs change it; the virāma suppresses it and is used to form conjunct consonants; independent vowel letters are used at the start of a syllable. It descends from Brāhmī through the Gupta, Siddhaṃ and Gauḍī scripts, and it belongs to the same family as Bengali–Assamese and Odia. It looks most like Bengali–Assamese.

**Distinctive features.**

- Separate dependent vowel signs for short e (𑒺) and short o (𑒽), with no independent letters for them.
- Its own decimal digits (𑓐 to 𑓙).
- The Gvang sign (𑓅), which marks nasalisation, and the Anji sign (𑒀), an auspicious sign written at the beginning of a text.
- Many conjunct ligatures, including nasal conjuncts such as 𑒓𑓂𑒏 (ṅka).

**In Unicode.** The block Tirhuta covers U+11480 to U+114DF and was added in Unicode 7.0 (June 2014). It lies in plane 1 (the Supplementary Multilingual Plane), outside the Basic Multilingual Plane. In UTF-8 each character takes four bytes, and in UTF-16 (as used by JavaScript and Java) each is a surrogate pair, which matters if you port the code. Python 3 strings treat each one as a single character.

| Category | Count | Code points | Notes |
|---|---|---|---|
| Anji (invocation sign) | 1 | U+11480 | An auspicious sign written at the beginning of a text; no Devanagari counterpart in the table. |
| Independent vowels | 14 | U+11481 to U+1148E | No independent letters for short e and short o. |
| Consonants | 33 | U+1148F to U+114AF | The same 33 consonants as Devanagari. |
| Vowel signs | 15 | U+114B0 to U+114BE | Includes separate signs for short e and short o. |
| Signs | 9 | U+114BF to U+114C7 | Candrabindu, anusvāra, visarga, virāma, nukta, avagraha, Gvang, abbreviation sign, Om. |
| Digits | 10 | U+114D0 to U+114D9 | Tirhuta has its own decimal digits. |

Total: 82 assigned characters in the block U+11480 to U+114DF.

**Fonts.** Showing Tirhuta needs a font that covers the block and has OpenType shaping rules for the script. Noto Sans Tirhuta (from the Noto project, under the SIL Open Font License, available on Google Fonts) is the font used by the web application. A system without a Tirhuta font shows empty boxes, which is why the application loads the font itself.

<a id="devanagari-and-tirhuta"></a>

### Devanagari and Tirhuta compared

| Category | Devanagari (in the table) | Tirhuta | Notes |
|---|---|---|---|
| Independent vowels | 14 | 14 | One for one. Devanagari ऎ and ऒ (short e and o) have no Tirhuta letters and pass through. |
| Vowel signs | 15 | 15 | One for one, including the short e and short o signs. |
| Consonants | 33 | 33 | One for one. ळ has no Tirhuta letter and passes through. |
| Signs | 7 | 9 | Candrabindu, anusvāra, visarga, virāma, nukta, avagraha and Om are mapped. Tirhuta also has Gvang and an abbreviation sign, which have no entry in the table. |
| Digits | 10 (plus 10 ASCII) | 10 | Both the Devanagari digits and the ASCII digits are converted. |
| Punctuation | danda, double danda | (shared) | Tirhuta text uses the same danda characters, so they are not converted. |
| Invocation | (none) | Anji | Not produced by the converter. |

Because the two scripts are so parallel, the whole conversion is a table lookup plus one rule for the anusvāra.

<a id="nasals-and-anusvara"></a>

### Nasal sounds and the anusvāra

**The sounds.** In Sanskrit and its descendants a nasal consonant before a stop is *homorganic*: it is made at the same place as the stop. Before velars (the ka-varga) it is ṅ, before palatals (ca-varga) ñ, before retroflexes (ṭa-varga) ṇ, before dentals (ta-varga) n and before labials (pa-varga) m. Before the semivowels, the sibilants and ह there is no corresponding nasal consonant, and the nasality is written with the anusvāra (ṃ).

**Devanagari.** Devanagari offers two ways to write the homorganic nasal: the explicit conjunct (अङ्क, सन्त, कम्बल) or the anusvāra as a shorthand (अंक, संत, कंबल). Both spellings occur in Maithili writing, so a converter has to expect both.

**Bengali–Assamese.** The traditional spelling writes the explicit conjunct (অঙ্ক, গঙ্গা, সঙ্গীত) and keeps ং for the other positions. Modern Bangla spelling writes ং in some compounds, such as সংগীত, while the traditional spelling সঙ্গীত remains in use.

**This project.** Mithilakshara is closely related to Bengali–Assamese and has the same kind of nasal conjunct ligatures, so the project takes traditional Bangla orthography as its model. Going to Mithilakshara, an anusvāra before a stop is written as the explicit conjunct, and it is kept elsewhere. Going to Devanagari, nothing is folded back into the anusvāra, so the result keeps whatever the Mithilakshara text had. If your own convention differs, [Customisation](#customisation) shows how to change the rule.

<a id="lexicon-spreadsheet"></a>

## Appendix: the Maithili Lexicon spreadsheet

The file [`Maithili Lexicon.xlsx`](https://github.com/vijollobo/Maithili_transliterator/blob/main/Maithili%20Lexicon.xlsx) ([download](https://github.com/vijollobo/Maithili_transliterator/raw/main/Maithili%20Lexicon.xlsx)) is the Maithili Lexicon: the reference table of Devanagari to Mithilakshara correspondences, with Unicode names, code points, IAST transliteration and IPA values. This appendix reproduces its contents, so the data can be read here without opening the workbook. The workbook documents the converter's table; no program reads it, and the authoritative table is the one in `mithilakshara.py`.

**Sheets**

| Sheet | Contents |
|---|---|
| `Lexicon` | One row for each of the 89 entries of the conversion table, below a header row, in the order of `mithilakshara.py`. Columns A and B hold the Devanagari and the Mithilakshara character; the other columns hold the category, IAST, IPA, the two code points, the two Unicode names, the Unicode general category and notes. |
| `Nasal conjuncts` | The 25 combinations of a varga's nasal, a virāma and a stop of that varga, which is what an anusvāra before a stop becomes: IAST, how Noto Sans Tirhuta 2.003 draws each one, and an example word where a common one exists. |
| `Notes` | Definitions of the columns, sources and conventions, summary counts that are calculated by formulas, and the changes made in this version. |

**Conventions**

- **IAST** is standard IAST, with two exceptions: short e and short o are written ĕ and ŏ, and the candrabindu is written m̐, as in ISO 15919, because IAST proper has no symbols for them. Consonant letters include the inherent a.
- **IPA** values are the conventional ones given for the Tirhuta letters in the Wikipedia article on the script, with one adjustment: अ is written /ə/ instead of /a/, to agree with the inherent vowel of the consonant letters. Consonants are given without that inherent vowel. Actual pronunciation varies by dialect and by context; for example, the inherent vowel is often not pronounced at the end of a word.
- **Unicode** names, code points and general categories come from Python's `unicodedata` module (Unicode 15.0.0).
- **Fonts.** Reading the Mithilakshara columns in Excel needs a font that covers the Tirhuta block, such as Noto Sans Tirhuta. Without one, Excel shows empty boxes.

**Changes in this version of the workbook**

- A header row and columns C to K were added, together with the `Nasal conjuncts` and `Notes` sheets.
- Invisible characters were removed. The previous version held a left-to-right mark (U+200E) in 3 cells of column B, a no-break space (U+00A0) in 20 cells of column B (rows 15 to 34), and a trailing space in cell B5. The same three entries carried the same marks in earlier versions of the scripts, where they broke conjunct formation.
- The Devanagari and ASCII digits, previously stored as the numbers 0 to 9, are now stored as text, as the characters the converter uses.
- The last row, which mapped a space to a space, was dropped, because the converter passes spaces through unchanged.
- Apart from that clean-up, columns A and B are unchanged. They equal the table in `mithilakshara.py`, entry by entry.

**The Lexicon sheet.** A dotted circle (◌) stands in for a combining sign that cannot be shown on its own. The bold rows are group headings that are not in the workbook. The Category, Unicode category and Notes columns, and the full Unicode names of the two scripts, are in the workbook only.

| No. | Devanagari | Mithilakshara | IAST | IPA | Code points (Devanagari → Tirhuta) | Unicode name (shared) |
|---|---|---|---|---|---|---|
|  | **Independent vowels** |  |  |  |  |  |
| 1 | अ | 𑒁 | a | /ə/ | U+0905 → U+11481 | LETTER A |
| 2 | आ | 𑒂 | ā | /aː/ | U+0906 → U+11482 | LETTER AA |
| 3 | इ | 𑒃 | i | /i/ | U+0907 → U+11483 | LETTER I |
| 4 | ई | 𑒄 | ī | /iː/ | U+0908 → U+11484 | LETTER II |
| 5 | उ | 𑒅 | u | /u/ | U+0909 → U+11485 | LETTER U |
| 6 | ऊ | 𑒆 | ū | /uː/ | U+090A → U+11486 | LETTER UU |
| 7 | ऋ | 𑒇 | ṛ | /r̩/ | U+090B → U+11487 | LETTER VOCALIC R |
| 8 | ॠ | 𑒈 | ṝ | /r̩ː/ | U+0960 → U+11488 | LETTER VOCALIC RR |
| 9 | ऌ | 𑒉 | ḷ | /l̩/ | U+090C → U+11489 | LETTER VOCALIC L |
| 10 | ॡ | 𑒊 | ḹ | /l̩ː/ | U+0961 → U+1148A | LETTER VOCALIC LL |
| 11 | ए | 𑒋 | e | /eː/ | U+090F → U+1148B | LETTER E |
| 12 | ऐ | 𑒌 | ai | /ai/ | U+0910 → U+1148C | LETTER AI |
| 13 | ओ | 𑒍 | o | /oː/ | U+0913 → U+1148D | LETTER O |
| 14 | औ | 𑒎 | au | /au/ | U+0914 → U+1148E | LETTER AU |
|  | **Vowel signs** |  |  |  |  |  |
| 15 | ◌ा | ◌𑒰 | ā | /aː/ | U+093E → U+114B0 | VOWEL SIGN AA |
| 16 | ◌ि | ◌𑒱 | i | /i/ | U+093F → U+114B1 | VOWEL SIGN I |
| 17 | ◌ी | ◌𑒲 | ī | /iː/ | U+0940 → U+114B2 | VOWEL SIGN II |
| 18 | ◌ु | ◌𑒳 | u | /u/ | U+0941 → U+114B3 | VOWEL SIGN U |
| 19 | ◌ू | ◌𑒴 | ū | /uː/ | U+0942 → U+114B4 | VOWEL SIGN UU |
| 20 | ◌ृ | ◌𑒵 | ṛ | /r̩/ | U+0943 → U+114B5 | VOWEL SIGN VOCALIC R |
| 21 | ◌ॄ | ◌𑒶 | ṝ | /r̩ː/ | U+0944 → U+114B6 | VOWEL SIGN VOCALIC RR |
| 22 | ◌ॢ | ◌𑒷 | ḷ | /l̩/ | U+0962 → U+114B7 | VOWEL SIGN VOCALIC L |
| 23 | ◌ॣ | ◌𑒸 | ḹ | /l̩ː/ | U+0963 → U+114B8 | VOWEL SIGN VOCALIC LL |
| 24 | ◌े | ◌𑒹 | e | /eː/ | U+0947 → U+114B9 | VOWEL SIGN E |
| 25 | ◌ै | ◌𑒻 | ai | /ai/ | U+0948 → U+114BB | VOWEL SIGN AI |
| 26 | ◌ो | ◌𑒼 | o | /oː/ | U+094B → U+114BC | VOWEL SIGN O |
| 27 | ◌ौ | ◌𑒾 | au | /au/ | U+094C → U+114BE | VOWEL SIGN AU |
| 28 | ◌ॆ | ◌𑒺 | ĕ | /e/ | U+0946 → U+114BA | VOWEL SIGN SHORT E |
| 29 | ◌ॊ | ◌𑒽 | ŏ | /o/ | U+094A → U+114BD | VOWEL SIGN SHORT O |
|  | **Signs** |  |  |  |  |  |
| 30 | ◌ं | ◌𑓀 | ṃ | ◌̃ | U+0902 → U+114C0 | SIGN ANUSVARA |
| 31 | ◌ँ | ◌𑒿 | m̐ | ◌̃ | U+0901 → U+114BF | SIGN CANDRABINDU |
| 32 | ◌ः | ◌𑓁 | ḥ | /h/ | U+0903 → U+114C1 | SIGN VISARGA |
| 33 | ◌् | ◌𑓂 | (virāma) | — | U+094D → U+114C2 | SIGN VIRAMA |
| 34 | ◌़ | ◌𑓃 | (nukta) | — | U+093C → U+114C3 | SIGN NUKTA |
| 35 | ऽ | 𑓄 | ’ | — | U+093D → U+114C4 | SIGN AVAGRAHA |
| 36 | ॐ | 𑓇 | oṃ | /oːm/ | U+0950 → U+114C7 | OM |
|  | **Consonants** |  |  |  |  |  |
| 37 | क | 𑒏 | ka | /k/ | U+0915 → U+1148F | LETTER KA |
| 38 | ख | 𑒐 | kha | /kʰ/ | U+0916 → U+11490 | LETTER KHA |
| 39 | ग | 𑒑 | ga | /ɡ/ | U+0917 → U+11491 | LETTER GA |
| 40 | घ | 𑒒 | gha | /ɡʱ/ | U+0918 → U+11492 | LETTER GHA |
| 41 | ङ | 𑒓 | ṅa | /ŋ/ | U+0919 → U+11493 | LETTER NGA |
| 42 | च | 𑒔 | ca | /t͡ʃ/ | U+091A → U+11494 | LETTER CA |
| 43 | छ | 𑒕 | cha | /t͡ʃʰ/ | U+091B → U+11495 | LETTER CHA |
| 44 | ज | 𑒖 | ja | /d͡ʒ/ | U+091C → U+11496 | LETTER JA |
| 45 | झ | 𑒗 | jha | /d͡ʒʱ/ | U+091D → U+11497 | LETTER JHA |
| 46 | ञ | 𑒘 | ña | /ɲ/ | U+091E → U+11498 | LETTER NYA |
| 47 | ट | 𑒙 | ṭa | /ʈ/ | U+091F → U+11499 | LETTER TTA |
| 48 | ठ | 𑒚 | ṭha | /ʈʰ/ | U+0920 → U+1149A | LETTER TTHA |
| 49 | ड | 𑒛 | ḍa | /ɖ/ | U+0921 → U+1149B | LETTER DDA |
| 50 | ढ | 𑒜 | ḍha | /ɖʱ/ | U+0922 → U+1149C | LETTER DDHA |
| 51 | ण | 𑒝 | ṇa | /ɳ/ | U+0923 → U+1149D | LETTER NNA |
| 52 | त | 𑒞 | ta | /t̪/ | U+0924 → U+1149E | LETTER TA |
| 53 | थ | 𑒟 | tha | /t̪ʰ/ | U+0925 → U+1149F | LETTER THA |
| 54 | द | 𑒠 | da | /d̪/ | U+0926 → U+114A0 | LETTER DA |
| 55 | ध | 𑒡 | dha | /d̪ʱ/ | U+0927 → U+114A1 | LETTER DHA |
| 56 | न | 𑒢 | na | /n/ | U+0928 → U+114A2 | LETTER NA |
| 57 | प | 𑒣 | pa | /p/ | U+092A → U+114A3 | LETTER PA |
| 58 | फ | 𑒤 | pha | /pʰ/ | U+092B → U+114A4 | LETTER PHA |
| 59 | ब | 𑒥 | ba | /b/ | U+092C → U+114A5 | LETTER BA |
| 60 | भ | 𑒦 | bha | /bʱ/ | U+092D → U+114A6 | LETTER BHA |
| 61 | म | 𑒧 | ma | /m/ | U+092E → U+114A7 | LETTER MA |
| 62 | य | 𑒨 | ya | /j/ | U+092F → U+114A8 | LETTER YA |
| 63 | र | 𑒩 | ra | /r/ | U+0930 → U+114A9 | LETTER RA |
| 64 | ल | 𑒪 | la | /l/ | U+0932 → U+114AA | LETTER LA |
| 65 | व | 𑒫 | va | /ʋ/ | U+0935 → U+114AB | LETTER VA |
| 66 | श | 𑒬 | śa | /ʃ/ | U+0936 → U+114AC | LETTER SHA |
| 67 | ष | 𑒭 | ṣa | /ʂ/ | U+0937 → U+114AD | LETTER SSA |
| 68 | स | 𑒮 | sa | /s/ | U+0938 → U+114AE | LETTER SA |
| 69 | ह | 𑒯 | ha | /ɦ/ | U+0939 → U+114AF | LETTER HA |
|  | **Devanagari digits** |  |  |  |  |  |
| 70 | ० | 𑓐 | 0 | — | U+0966 → U+114D0 | DIGIT ZERO |
| 71 | १ | 𑓑 | 1 | — | U+0967 → U+114D1 | DIGIT ONE |
| 72 | २ | 𑓒 | 2 | — | U+0968 → U+114D2 | DIGIT TWO |
| 73 | ३ | 𑓓 | 3 | — | U+0969 → U+114D3 | DIGIT THREE |
| 74 | ४ | 𑓔 | 4 | — | U+096A → U+114D4 | DIGIT FOUR |
| 75 | ५ | 𑓕 | 5 | — | U+096B → U+114D5 | DIGIT FIVE |
| 76 | ६ | 𑓖 | 6 | — | U+096C → U+114D6 | DIGIT SIX |
| 77 | ७ | 𑓗 | 7 | — | U+096D → U+114D7 | DIGIT SEVEN |
| 78 | ८ | 𑓘 | 8 | — | U+096E → U+114D8 | DIGIT EIGHT |
| 79 | ९ | 𑓙 | 9 | — | U+096F → U+114D9 | DIGIT NINE |
|  | **ASCII digits** |  |  |  |  |  |
| 80 | 0 | 𑓐 | 0 | — | U+0030 → U+114D0 | DIGIT ZERO |
| 81 | 1 | 𑓑 | 1 | — | U+0031 → U+114D1 | DIGIT ONE |
| 82 | 2 | 𑓒 | 2 | — | U+0032 → U+114D2 | DIGIT TWO |
| 83 | 3 | 𑓓 | 3 | — | U+0033 → U+114D3 | DIGIT THREE |
| 84 | 4 | 𑓔 | 4 | — | U+0034 → U+114D4 | DIGIT FOUR |
| 85 | 5 | 𑓕 | 5 | — | U+0035 → U+114D5 | DIGIT FIVE |
| 86 | 6 | 𑓖 | 6 | — | U+0036 → U+114D6 | DIGIT SIX |
| 87 | 7 | 𑓗 | 7 | — | U+0037 → U+114D7 | DIGIT SEVEN |
| 88 | 8 | 𑓘 | 8 | — | U+0038 → U+114D8 | DIGIT EIGHT |
| 89 | 9 | 𑓙 | 9 | — | U+0039 → U+114D9 | DIGIT NINE |

**The Nasal conjuncts sheet.** The way a conjunct is drawn belongs to the font, not to the text; see [The anusvāra rule](#anusvara-rule).

| Varga | Nasal conjunct | Mithilakshara | IAST | Drawn in Noto Sans Tirhuta 2.003 | Example word | Example (Mithilakshara) |
|---|---|---|---|---|---|---|
| ka-varga | ङ्क | 𑒓𑓂𑒏 | ṅka | single ligature | अङ्क | 𑒁𑒓𑓂𑒏 |
| ka-varga | ङ्ख | 𑒓𑓂𑒐 | ṅkha | single ligature | शङ्ख | 𑒬𑒓𑓂𑒐 |
| ka-varga | ङ्ग | 𑒓𑓂𑒑 | ṅga | single ligature | गङ्गा | 𑒑𑒓𑓂𑒑𑒰 |
| ka-varga | ङ्घ | 𑒓𑓂𑒒 | ṅgha | single ligature | सङ्घ | 𑒮𑒓𑓂𑒒 |
| ka-varga | ङ्ङ | 𑒓𑓂𑒓 | ṅṅa | visible virāma | — | — |
| ca-varga | ञ्च | 𑒘𑓂𑒔 | ñca | single ligature | पञ्च | 𑒣𑒘𑓂𑒔 |
| ca-varga | ञ्छ | 𑒘𑓂𑒕 | ñcha | single ligature | वाञ्छा | 𑒫𑒰𑒘𑓂𑒕𑒰 |
| ca-varga | ञ्ज | 𑒘𑓂𑒖 | ñja | visible virāma | रञ्जन | 𑒩𑒘𑓂𑒖𑒢 |
| ca-varga | ञ्झ | 𑒘𑓂𑒗 | ñjha | visible virāma | झञ्झा | 𑒗𑒘𑓂𑒗𑒰 |
| ca-varga | ञ्ञ | 𑒘𑓂𑒘 | ñña | visible virāma | — | — |
| ṭa-varga | ण्ट | 𑒝𑓂𑒙 | ṇṭa | single ligature | घण्टा | 𑒒𑒝𑓂𑒙𑒰 |
| ṭa-varga | ण्ठ | 𑒝𑓂𑒚 | ṇṭha | single ligature | कण्ठ | 𑒏𑒝𑓂𑒚 |
| ṭa-varga | ण्ड | 𑒝𑓂𑒛 | ṇḍa | single ligature | दण्ड | 𑒠𑒝𑓂𑒛 |
| ṭa-varga | ण्ढ | 𑒝𑓂𑒜 | ṇḍha | single ligature | — | — |
| ṭa-varga | ण्ण | 𑒝𑓂𑒝 | ṇṇa | single ligature | — | — |
| ta-varga | न्त | 𑒢𑓂𑒞 | nta | single ligature | अन्त | 𑒁𑒢𑓂𑒞 |
| ta-varga | न्थ | 𑒢𑓂𑒟 | ntha | visible virāma | ग्रन्थ | 𑒑𑓂𑒩𑒢𑓂𑒟 |
| ta-varga | न्द | 𑒢𑓂𑒠 | nda | single ligature | वन्दना | 𑒫𑒢𑓂𑒠𑒢𑒰 |
| ta-varga | न्ध | 𑒢𑓂𑒡 | ndha | single ligature | बन्ध | 𑒥𑒢𑓂𑒡 |
| ta-varga | न्न | 𑒢𑓂𑒢 | nna | single ligature | अन्न | 𑒁𑒢𑓂𑒢 |
| pa-varga | म्प | 𑒧𑓂𑒣 | mpa | visible virāma | कम्प | 𑒏𑒧𑓂𑒣 |
| pa-varga | म्फ | 𑒧𑓂𑒤 | mpha | visible virāma | — | — |
| pa-varga | म्ब | 𑒧𑓂𑒥 | mba | half forms | अम्बर | 𑒁𑒧𑓂𑒥𑒩 |
| pa-varga | म्भ | 𑒧𑓂𑒦 | mbha | visible virāma | आरम्भ | 𑒂𑒩𑒧𑓂𑒦 |
| pa-varga | म्म | 𑒧𑓂𑒧 | mma | visible virāma | सम्मान | 𑒮𑒧𑓂𑒧𑒰𑒢 |

<a id="references"></a>

## References

- The Unicode Standard: code chart for the Tirhuta block (U+11480 to U+114DF), <https://www.unicode.org/charts/PDF/U11480.pdf>.
- Anshuman Pandey, *Towards an Encoding for the Maithili Script in ISO/IEC 10646* (2009), ISO/IEC JTC 1/SC 2/WG 2 document N3765.
- Script Source, entry for the Tirhuta script.
- Central Institute of Indian Languages, LIS-India: Maithili script and spelling.
- George A. Grierson, *An Introduction to the Maithili Dialect of the Bihari Language as Spoken in North Bihar* (2nd edition, 1909).
- Ramawatar Yadav, *A Reference Grammar of Maithili* (Mouton de Gruyter, 1996).
- Census of India 2011, language tables (C-16), including the statement of scheduled languages in descending order of speakers' strength, <https://new.census.gov.in/nada/index.php/catalog/42458/download/46089/C-16_25062018.pdf>.
- Constitution of India, Eighth Schedule, as amended by the Constitution (Ninety-second Amendment) Act, 2003.
- Wikipedia, [Maithili language](https://en.wikipedia.org/wiki/Maithili_language) and [Tirhuta script](https://en.wikipedia.org/wiki/Tirhuta_script), used for the overview, the timeline and the IPA values.
- Noto Sans Tirhuta, Noto project, <https://github.com/notofonts/tirhuta> (SIL Open Font License).
- Streamlit documentation, <https://docs.streamlit.io>.

Maintained by [@vijollobo](https://github.com/vijollobo).
