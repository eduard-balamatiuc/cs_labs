import streamlit as st
from collections import Counter
import json
from datetime import datetime
import pandas as pd

# Set page configuration to wide mode
st.set_page_config(
    page_title="Cipher Decoder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS to maximize width usage
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .element-container {
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_substitutions' not in st.session_state:
    st.session_state.current_substitutions = {}
if 'frequencies' not in st.session_state:
    st.session_state.frequencies = {}
if 'decoded_text' not in st.session_state:
    st.session_state.decoded_text = ""
if 'ciphertext' not in st.session_state:
    st.session_state.ciphertext = ""
if 'current_attempt_index' not in st.session_state:
    st.session_state.current_attempt_index = None

letter_frequencies = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23, "G": 2.01, "H": 6.09, "I": 6.97, "J": 0.15,
    "K": 0.77, "L": 4.03, "M": 2.41, "N": 6.75, "O": 7.51, "P": 1.93, "Q": 0.09, "R": 5.99, "S": 6.33, "T": 9.06,
    "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15, "Y": 1.97, "Z": 0.07
}

def frequency_analysis(text):
    text = text.upper()
    counter = Counter(char for char in text if char.isalpha())
    total = sum(counter.values())
    frequency = {char: (count / total) * 100 for char, count in counter.items()}
    return frequency

def decode(ciphertext, substitution_dict):
    decoded_text = ""
    for char in ciphertext:
        if char.upper() in substitution_dict:
            decoded_char = substitution_dict[char.upper()]
            decoded_text += decoded_char.lower() if char.islower() else decoded_char.upper()
        else:
            decoded_text += char
    return decoded_text

def update_decoded_text():
    if st.session_state.ciphertext and st.session_state.current_substitutions:
        st.session_state.decoded_text = decode(
            st.session_state.ciphertext,
            st.session_state.current_substitutions
        )

def save_attempt():
    attempt = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ciphertext': st.session_state.ciphertext,
        'substitutions': st.session_state.current_substitutions.copy(),
        'decoded_text': st.session_state.decoded_text,
        'frequencies': st.session_state.frequencies
    }
    st.session_state.history.append(attempt)
    st.session_state.current_attempt_index = len(st.session_state.history) - 1
    update_decoded_text()

def load_attempt(idx):
    attempt = st.session_state.history[idx]
    st.session_state.ciphertext = attempt['ciphertext']
    st.session_state.current_substitutions = attempt['substitutions'].copy()
    st.session_state.frequencies = attempt['frequencies']
    st.session_state.current_attempt_index = idx
    update_decoded_text()

def on_text_change():
    if st.session_state.text_input != st.session_state.ciphertext:
        st.session_state.ciphertext = st.session_state.text_input
        st.session_state.frequencies = frequency_analysis(st.session_state.ciphertext)
        update_decoded_text()

def on_substitution_change(letter, new_value):
    if new_value and new_value.isalpha():
        st.session_state.current_substitutions[letter] = new_value.upper()
    elif new_value == "":
        st.session_state.current_substitutions.pop(letter, None)
    update_decoded_text()

st.title("Monoalphabetic Cipher - Frequency Analysis")

# Create three columns for main layout
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    # Input Section
    st.text_area(
        "Enter the ciphertext:",
        value=st.session_state.ciphertext,
        key="text_input",
        height=300,
        on_change=on_text_change
    )

with col2:
    # Frequency Analysis Section
    if st.session_state.frequencies:
        st.subheader("Letter Frequencies")
        freq_df = pd.DataFrame([st.session_state.frequencies]).T
        freq_df.columns = ['Frequency (%)']
        st.dataframe(freq_df, height=300)

        if st.button("Auto-substitute", use_container_width=True):
            for letter in sorted(st.session_state.frequencies.keys()):
                closest = min(letter_frequencies, 
                            key=lambda x: abs(letter_frequencies[x] - st.session_state.frequencies[letter]))
                st.session_state.current_substitutions[letter] = closest
            update_decoded_text()

with col3:
    # Decoded Text Section
    if st.session_state.decoded_text:
        st.text_area(
            "Decoded Text:",
            value=st.session_state.decoded_text,
            height=300,
            disabled=True,
            key="decoded_output"
        )

# Substitutions Section
if st.session_state.frequencies:
    st.subheader("Letter Substitutions")
    cols = st.columns(13)  # More columns for better space usage
    for idx, letter in enumerate(sorted(st.session_state.frequencies.keys())):
        col_idx = idx % 13
        with cols[col_idx]:
            current_value = st.session_state.current_substitutions.get(letter, '')
            new_value = st.text_input(
                f"'{letter}'",
                value=current_value,
                key=f"sub_{letter}",
                max_chars=1,
                on_change=on_substitution_change,
                args=(letter, current_value)
            ).upper()

# Action buttons in a row
col_save, col_export, col_import = st.columns([1, 1, 1])

with col_save:
    if st.button("Save Current Attempt", use_container_width=True):
        save_attempt()
        st.success("Attempt saved! Check the sidebar to load previous attempts.")

with col_export:
    if st.button("Export Substitutions", use_container_width=True):
        st.download_button(
            "Download Substitutions",
            data=json.dumps(st.session_state.current_substitutions),
            file_name="substitutions.json",
            mime="application/json",
            use_container_width=True
        )

with col_import:
    uploaded_file = st.file_uploader("Import Substitutions", type="json")
    if uploaded_file is not None:
        st.session_state.current_substitutions = json.load(uploaded_file)
        update_decoded_text()
        st.success("Substitutions imported successfully!")

# Sidebar for history
with st.sidebar:
    st.header("Decoding History")
    if st.session_state.history:
        for idx, attempt in enumerate(st.session_state.history):
            is_current = idx == st.session_state.current_attempt_index
            button_label = f"{'▶ ' if is_current else ''}Attempt {idx + 1} - {attempt['timestamp']}"
            if st.button(button_label, key=f"history_{idx}", use_container_width=True):
                load_attempt(idx)