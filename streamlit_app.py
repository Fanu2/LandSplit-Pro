import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Land Share Calculator", layout="wide")
st.title("📐 Land Share and Ownership Split Calculator (with Killa)")

# --- Conversion Functions ---

def parse_fraction(frac_str):
    """Convert a string fraction like 1/8 to float"""
    try:
        num, denom = map(int, re.findall(r'(\d+)', str(frac_str)))
        return num / denom
    except:
        return None

def marla_to_kms(total_marla):
    """Convert marla to Killa, Kanal, Marla, Sarshai"""
    total_kanal = total_marla / 20
    killa = int(total_kanal // 8)
    kanal = int(total_kanal % 8)
    marla = int(total_marla % 20)
    sarshai = int(round((total_marla - int(total_marla)) * 9))
    return killa, kanal, marla, sarshai

# --- Sidebar Input for Total Land Area ---

st.sidebar.header("Total Area Input")
kanal_input = st.sidebar.number_input("🧮 Kanal", min_value=0.0, step=1.0, value=0.0)
marla_input = st.sidebar.number_input("📏 Marla", min_value=0.0, max_value=19.99, step=1.0, value=0.0)

total_marla = kanal_input * 20 + marla_input
st.sidebar.markdown(f"📌 **Total Area in Marla:** `{total_marla:.2f}`")

# --- Input Mode Selection ---

input_mode = st.radio("Select Input Method", ["Paste Table", "Upload Excel"])

df = None

if input_mode == "Paste Table":
    pasted_data = st.text_area("Paste Excel-style table here (tab-separated):", height=200)
    if pasted_data:
        try:
            lines = pasted_data.strip().split("\n")
            data = [re.split(r'\t+', line) for line in lines]
            df = pd.DataFrame(data[1:], columns=data[0])
        except:
            st.error("⚠️ Error parsing pasted table. Please check format.")

elif input_mode == "Upload Excel":
    uploaded_file = st.file_uploader("Upload Excel file (.xlsx or .xls)", type=["xlsx", "xls"])
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
        except:
            st.error("⚠️ Error reading Excel file.")

# --- Process and Display Results ---

if df is not None:
    required_cols = ['Owners', 'Fraction / Share']
    if not all(col in df.columns for col in required_cols):
        st.error("⚠️ Input must contain 'Owners' and 'Fraction / Share' columns.")
    else:
        # Calculate share and convert
        df['Share'] = df['Fraction / Share'].apply(parse_fraction)
        df['Total Marla Share'] = df['Share'] * total_marla

        # Convert to Killa-Kanal-Marla-Sarshai
        converted = df['Total Marla Share'].apply(marla_to_kms)
        df['Killa'] = converted.apply(lambda x: x[0])
        df['Kanal'] = converted.apply(lambda x: x[1])
        df['Marla'] = converted.apply(lambda x: x[2])
        df['Sarshai'] = converted.apply(lambda x: x[3])

        df['Result Text'] = df.apply(
            lambda row: f"{row['Killa']}Ki-{row['Kanal']}K-{row['Marla']}M-{row['Sarshai']}S", axis=1
        )

        st.success("✅ Share calculation completed successfully!")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "land_share_result.csv", mime="text/csv")
