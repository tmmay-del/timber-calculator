import streamlit as st
import math
import easyocr
import numpy as np
from PIL import Image

# --- App Configuration ---
st.set_page_config(page_title="Timber Calculator", page_icon="🪵")
st.title("🪵 Timber Calculator")

# --- Initialize Memory ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- OCR Reader (Loads once to save time) ---
@st.cache_resource
def load_reader():
    return easyocr.Reader(['en'])

# --- Logic Functions (Your Math) ---
def process_width(w_str):
    # Logic: First digit * 12 + rest
    if not w_str or not w_str.isdigit(): return 0
    first_digit = int(w_str[0])
    rest_str = w_str[1:]
    m = int(rest_str) if rest_str else 0
    return (first_digit * 12) + m

def process_height(h_str):
    # Logic: First digit = feet. Second digit = indicator (>=5 adds 0.5)
    if not h_str or not h_str.isdigit() or len(h_str) < 2: return 0
    f = int(h_str[0])
    indicator = int(h_str[1])
    return f + 0.5 if indicator >= 5 else f

# --- UI: Image Uploader ---
st.info("📸 **Optional:** Upload a photo of handwritten dimensions (e.g., '20*10')")
uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])

# Default values for text boxes
default_h = ""
default_w = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', width=300)
    
    with st.spinner('Reading numbers from image...'):
        reader = load_reader()
        # Convert image to numpy array for EasyOCR
        image_np = np.array(image)
        result = reader.readtext(image_np, detail=0)
        
        # Look for pattern "Number * Number"
        found = False
        for text in result:
            if "*" in text:
                parts = text.split("*")
                if len(parts) == 2:
                    # Assume Format: Height * Width
                    default_h = parts[0].strip()
                    default_w = parts[1].strip()
                    st.success(f"Found dimensions: Height {default_h}, Width {default_w}")
                    found = True
                    break
        if not found:
            st.warning("Could not find 'Number * Number' pattern clearly.")

# --- UI: Manual Inputs (Swapped Order) ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    h_input = st.text_input("1. Enter Height Code", value=default_h, placeholder="e.g. 106")

with col2:
    w_input = st.text_input("2. Enter Width Code", value=default_w, placeholder="e.g. 504")

# --- Calculate Button ---
if st.button("Calculate", type="primary"):
    if w_input and h_input:
        try:
            w_val = process_width(w_input)
            h_val = process_height(h_input)
            
            # Formula
            a = (w_val * w_val * h_val) / 2304
            answer = math.trunc(a * 100) / 100
            
            st.session_state.history.append({
                "h": h_input, "w": w_input, "res": answer
            })
            st.success(f"Result: {answer}")
        except:
            st.error("Invalid numbers entered.")
    else:
        st.error("Please enter both numbers.")

# --- History Table ---
if st.session_state.history:
    st.divider()
    st.subheader("History")
    total = 0
    for item in st.session_state.history:
        st.text(f"H:{item['h']} * W:{item['w']} = {item['res']}")
        total += item['res']
    st.markdown(f"### Total: :green[{total:.2f}]")