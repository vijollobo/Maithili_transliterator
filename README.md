# Maithili

<img height="100" alt="image" src="https://github.com/user-attachments/assets/3c55d1d9-134c-4251-a240-4494e57b1732" />

Maithili is an Indo-Aryan language spoken in parts of India and Nepal. It is native to the Mithila region, which encompasses parts of the eastern Indian states of Bihar and Jharkhand as well as Nepal's Koshi and Madhesh Provinces. It is one of the 22 scheduled languages of India. It is the second most commonly spoken native Nepalese language constitutionally registered as one of the fourteen provincial official languages of Nepal.

# Maithili Script Transliterator

This project provides a **Streamlit-based web application** that allows users to transliterate text between **Devanagari** and **Mithilakshara**, with support for **English** as the interface language.  

A simple trilingual web app built with Streamlit that allows switching the app interface between:
* English
* Maithili (Devanagari)
* Maithili (Mithilakshara)

It provides script conversion utilities between Devanagari and Mithilakshara along with a user-friendly Streamlit frontend.

##  Features
- Transliterate Maithili text between **Devanagari** and **Mithilakshara**.  
- Trilingual interface with a dropdown for switching between:  
  - English  
  - Maithili (Devanagari)  
  - Maithili (Mithilakshara)  
- Simple and interactive **Streamlit frontend**.
- Dropdown at the top to switch app interface language.
- Instant script conversion with Streamlit. 

---

## Repository Structure
```
.
├── devanagari_to_mithilakshara.py   # Module for converting Devanagari script to Mithilakshara.
├── mithilakshara_to_devanagari.py   # Module for converting Mithilakshara script to Devanagari.
└── Maithili.py                      # Main Streamlit frontend application with trilingual support (English, Maithili-Devanagari, Maithili-Mithilakshara).
```

## Installation

1. Clone this repository:
 ```
git clone https://github.com/vijollobo/Maithili.git
cd Maithili
 ```

2. (Optional) Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```
3. Install dependencies:
```
pip install streamlit
```

## Usage
Run the Streamlit app with:
```
streamlit run Maithili.py
```

The app will start locally, and you can open it in your browser at:
```
http://localhost:8501
```
   
