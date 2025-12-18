import streamlit as st
import math

# --- App Setup ---
st.set_page_config(page_title="Timber Calculator", page_icon="🪵")
st.title("🪵 Timber Calculator")

# --- Memory ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Logic (Your exact Formula) ---
def process_width(w_str):
    # Logic: 504 -> 5 feet * 12 + 4 inches
    if not w_str or not w_str.isdigit(): return 0
    
    first_digit = int(w_str[0])
    rest_str = w_str[1:]
    m = int(rest_str) if rest_str else 0
    
    return (first_digit * 12) + m

def process_height(h_str):
    # Logic: 106 -> 10 feet. If 2nd digit >= 5, add 0.5
    if not h_str or not h_str.isdigit() or len(h_str) < 2: return 0
    
    f = int(h_str[0])
    indicator = int(h_str[1])
    
    return f + 0.5 if indicator >= 5 else f

# --- User Inputs ---
st.write("Enter the dimension codes directly:")

col1, col2 = st.columns(2)

# Height First (as requested)
with col1:
    h_input = st.text_input("1. Height Code", placeholder="e.g. 106")

# Width Second
with col2:
    w_input = st.text_input("2. Width Code", placeholder="e.g. 504")

# --- Calculate Button ---
if st.button("Calculate", type="primary"):
    if w_input and h_input:
        try:
            w_val = process_width(w_input)
            h_val = process_height(h_input)
            
            # Your Formula: (w * w * h) / 2304
            # (Using width twice as per your original logic)
            a = (w_val * w_val * h_val) / 2304
            
            # Truncate/Round
            answer = math.trunc(a * 100) / 100
            
            # Save to history
            st.session_state.history.append({
                "h": h_input, "w": w_input, "res": answer
            })
            
            st.success(f"Result: {answer}")
        except:
            st.error("Invalid input. Please enter numbers only.")
    else:
        st.error("Please enter both numbers.")

# --- History Table ---
if st.session_state.history:
    st.divider()
    st.subheader("History")
    total = 0
    
    # Show list
    for item in st.session_state.history:
        st.text(f"H:{item['h']} * W:{item['w']} = {item['res']}")
        total += item['res']
        
    st.markdown(f"### Total: :green[{total:.2f}]")
    
    # Clear Button
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()