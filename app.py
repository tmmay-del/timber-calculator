import streamlit as st
import math

# --- App Setup ---
st.set_page_config(page_title="Timber Calculator", page_icon="🪵")
st.title("🪵 Timber Calculator")

# --- Memory for the Total List ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Your Exact Logic (Adapted for App) ---
def process_width(w_str):
    # Logic: First digit * 12 + the rest of the digits as a number
    if not w_str or not w_str.isdigit():
        return 0
    
    # Your code: f = int(w[0])*12
    first_digit = int(w_str[0])
    f = first_digit * 12
    
    # Your code: ww = w[1:] -> convert to int
    rest_str = w_str[1:]
    m = 0
    if len(rest_str) > 0:
        m = int(rest_str)
        
    return f + m

def process_height(h_str):
    # Logic: First digit is feet. Second digit determines if we add 0.5.
    if not h_str or not h_str.isdigit() or len(h_str) < 2:
        return 0
        
    f = int(h_str[0])
    indicator = int(h_str[1])
    
    if indicator >= 5:
        f = f + 0.5
    else:
        f = f + 0
        
    return f

# --- User Inputs (Text Boxes) ---
col1, col2 = st.columns(2)

with col1:
    # We use text_input so they can type "504" directly
    w_input = st.text_input("Enter Width Code", placeholder="e.g. 504")

with col2:
    h_input = st.text_input("Enter Height Code", placeholder="e.g. 106")

# --- Calculate Button ---
if st.button("Calculate", type="primary"):
    # 1. Run your logic
    if w_input and h_input:
        w_val = process_width(w_input)
        h_val = process_height(h_input)
        
        # 2. Your Formula: (w*w*h)/2304
        # Note: Your code used w_val twice for width
        a = (w_val * w_val * h_val) / 2304
        
        # 3. Rounding
        answer = math.trunc(a * 100) / 100
        
        # 4. Save to history
        st.session_state.history.append({
            "input_w": w_input,
            "input_h": h_input,
            "result": answer
        })
        
        st.success(f"{h_input} * {w_input} = {answer}")
    else:
        st.error("Please enter both numbers.")

# --- Show Total ---
st.divider()
st.subheader("Total List")

if st.session_state.history:
    total_sum = 0
    for item in st.session_state.history:
        st.text(f"Input: {item['input_h']} * {item['input_w']}  |  Result: {item['result']}")
        total_sum += item['result']
        
    st.markdown(f"### Total: :green[{total_sum:.2f}]")
    
    if st.button("Clear List"):
        st.session_state.history = []
        st.rerun()