import streamlit as st
import math

# --- 1. App Configuration ---
st.set_page_config(page_title="Timber Volume Calculator", page_icon="🪵", layout="centered")

# --- 2. Initialize Session State (Memory for the list) ---
if 'logs' not in st.session_state:
    st.session_state.logs = []

# --- 3. The Math Logic (Your original logic adapted) ---
def calculate_volume(girth_feet, girth_inches, length_feet, length_indicator):
    # Width (Girth) Calculation: Convert everything to inches
    # Your logic: f = int(w[0])*12 + remainder
    total_girth_inches = (girth_feet * 12) + girth_inches
    
    # Height (Length) Calculation: Rounding logic
    # Your logic: if 2nd digit >= 5, add 0.5 to feet
    final_length = length_feet
    if length_indicator >= 5:
        final_length += 0.5
    else:
        final_length += 0.0
        
    # Volume Formula: (w * w * h) / 2304
    vol = (total_girth_inches * total_girth_inches * final_length) / 2304
    
    # Truncate/Round to 2 decimal places
    return math.trunc(vol * 100) / 100

# --- 4. User Interface ---
st.title("🪵 Timber Volume Calculator")
st.markdown("Calculate cubic feet (CFT) using the **Quarter Girth Rule**.")

# Create two columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Girth (Width)")
    g_feet = st.number_input("Feet", min_value=0, value=0, key="gf")
    g_inches = st.number_input("Inches", min_value=0, value=0, key="gi")

with col2:
    st.subheader("Length (Height)")
    l_feet = st.number_input("Feet", min_value=0, value=0, key="lf")
    l_inch = st.number_input("Inches (Rounding digit)", min_value=0, max_value=11, value=0, help="If this is 5 or more, length adds 0.5", key="li")

# Calculate Button
if st.button("Add Log", type="primary", use_container_width=True):
    if g_feet == 0 and g_inches == 0:
        st.error("Please enter a Girth size.")
    else:
        result = calculate_volume(g_feet, g_inches, l_feet, l_inch)
        
        # Add to history
        new_log = {
            "id": len(st.session_state.logs) + 1,
            "girth": f"{g_feet}' {g_inches}\"",
            "length": f"{l_feet}.{l_inch}",
            "volume": result
        }
        st.session_state.logs.append(new_log)
        st.success(f"Calculated Volume: {result} CFT")

# --- 5. Results Table & Total ---
st.divider()
st.subheader("📝 Log List")

if st.session_state.logs:
    # Display data in a clean table
    st.dataframe(st.session_state.logs, use_container_width=True)
    
    # Calculate Total
    total_vol = sum(item['volume'] for item in st.session_state.logs)
    st.markdown(f"### Total Volume: :green[{total_vol:.2f} CFT]")
    
    # Clear Button
    if st.button("Clear All"):
        st.session_state.logs = []
        st.rerun()
else:
    st.info("No logs added yet.")