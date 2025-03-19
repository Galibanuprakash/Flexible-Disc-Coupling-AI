import streamlit as st
import pandas as pd
import google.generativeai as genai
import math

# Configure Google Gemini API
GEMINI_API_KEY = "AIzaSyCFbnID7J4KnD-hoveRc37CEx_MV9eXUEk"
genai.configure(api_key=GEMINI_API_KEY)

# Load Excel data
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file, sheet_name="Main-Data")
        df.columns = df.iloc[0]  # Set first row as column headers
        df = df[1:].reset_index(drop=True)  # Cleaned data
        
        # Convert numeric columns safely, replacing invalid values with NaN
        numeric_cols = ["Speed (RPM)", "Power (kW)"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        
        return df.dropna(subset=numeric_cols)  # Drop rows with NaN in essential columns
    return None

# Streamlit UI
st.title("Flexible Disc Coupling Finder")

# File Upload
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    df = load_data(uploaded_file)
    st.success("File uploaded successfully!")
else:
    df = None
    st.warning("Please upload an Excel file to proceed.")

# User Inputs
speed = st.number_input("Enter Required Speed (RPM)", min_value=0, step=10)
torque = st.number_input("Enter Required Torque (kNm) (Leave blank if entering Power)", min_value=0.0, step=0.1, value=None)
power = st.number_input("Enter Required Power (kW) (Leave blank if entering Torque)", min_value=0.0, step=0.1, value=None)

# Calculate power if torque is provided
if torque is not None and torque > 0:
    power = (2 * math.pi * speed * torque) / 60  # Power calculation
    st.write(f"Calculated Power: {power:.2f} kW")

if st.button("Find Best Coupling") and df is not None:
    if power is not None:
        # Filter exact matches for speed and power
        df_filtered = df[(df["Speed (RPM)"] == speed) & (df["Power (kW)"] == power)]
        
        if not df_filtered.empty:
            st.success("Best Matching Coupling:")
            st.write(df_filtered.to_dict(orient="records"))
        else:
            st.error("No exact match found for the given Speed and Power.")
    else:
        st.error("Please enter either Torque or Power to proceed.")
