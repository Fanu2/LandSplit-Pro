import streamlit as st
import pandas as pd
import io
import re

st.set_page_config(page_title="Land Share Calculator", layout="wide")
st.title("📐 Land Share and Ownership Split Calculator")

# Helper to parse fraction string to float
def parse_fraction(frac_str):
    try:
        num, denom = map(int, re.findall(r'(\d+)', frac_str))
        return num / denom
    except:
        return None

# Helper to convert total marla to Kanal-Marla-Sarshai
def marla_to_kms(total_marla):
    kanal = int(total_marla // 20)
    marla = int(total_marla % 20)
    sarshai = int(round((total_marla - int(total_marla)) * 9))
    return kanal, marla, sarshai

# User input for total area
st.sidebar.header("Total Area Input")
kanal_input = st.sidebar.number_input("Kanal", min_value=0.0, step=1.0, value=0.0)
marla_input = st.sidebar.number_input("Marla", min_value=0.0, max_value=19.99, step=1.0, value=0.0)
total_marla = kanal_input * 20 + marla_input
st.sidebar.write(f"📏 Total Area in Marla: **{total_marla:.2f}**")

# Input method
input_method = st.radio("Choose data input method", ["Paste Table", "Upload Excel"])

if input_method == "Paste Table":
    pasted_data = st.text_area("Paste Excel-style table here (e.g., from Excel)", height=200)
    if pasted_data:
        lines = pasted_data.strip().split("\n")
        data = [re.split(r'\t+', line) for line in lines]
        df = pd.DataFrame(data[1:], columns=data[0])
elif input_method == "Upload Excel":
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])
    if uploaded_file:
        df = pd.read_excel(uploaded_file)

# Process if data is ready
if 'df' in locals():
    # Ensure column names
    expected_cols = ['Owners', 'Fraction / Share']
    if not all(col in df.columns for col in expected_cols):
        st.error("The input data must contain at least 'Owners' and 'Fraction / Share' columns.")
    else:
        df['Share'] = df['Fraction / Share'].apply(parse_fraction)
        df['Total Marla Share'] = df['Share'] * total_marla

        # Convert marla share to K-M-S
        conversions = df['Total Marla Share'].apply(marla_to_kms)
        df['Kanal'] = conversions.apply(lambda x: x[0])
        df['Marla'] = conversions.apply(lambda x: x[1])
        df['Sarshai'] = conversions.apply(lambda x: x[2])
        df['Result Text'] = df.apply(lambda x: f"0K-{x['Kanal']}K-{x['Marla']}M-{x['Sarshai']}S", axis=1)

        st.success("✅ Processed successfully!")
        st.dataframe(df, use_container_width=True)

        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download as CSV", csv, file_name="land_share_output.csv", mime="text/csv")
