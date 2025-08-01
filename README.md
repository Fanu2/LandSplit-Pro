# 📐 Land Share and Ownership Split Calculator (with Killa Support)

A user-friendly **Streamlit** web app that helps calculate and visualize land share distribution based on owner fractions. Ideal for **rural estate management**, **property inheritance planning**, or **land revenue departments** working with units like **Killa, Kanal, Marla, and Sarshai** (Punjab region standard).

---

## 🚀 Features

- 📥 Accepts input via **Excel file upload** or **copy-pasted table**
- 🧮 Converts **fractional land shares** to **Killa-Kanal-Marla-Sarshai**
- 📊 Instant results with downloadable CSV
- 🔢 Works with both whole and fractional entries (e.g. `1/2`, `3/8`)

---

## 🖥️ How to Use

### 1. Set Total Land Area
From the **sidebar**, input total land:
- **Kanal** (e.g., 12)
- **Marla** (e.g., 8)

📝 *Note: 1 Kanal = 20 Marlas, and 1 Killa = 8 Kanals*

### 2. Choose Input Method
You can either:

#### Option A: **Paste Table**
Paste a tab-separated table like this:
Owners Fraction / Share
Amar 1/4
Balbir 1/2
Charan 1/4

> You can copy directly from Excel and paste here.

#### Option B: **Upload Excel File**
Upload a `.xlsx` or `.xls` file with at least these two columns:
- `Owners`
- `Fraction / Share`

🧾 Example Excel format:

| Owners | Fraction / Share |
|--------|------------------|
| Amar   | 1/4              |
| Balbir | 1/2              |
| Charan | 1/4              |

---

## ✅ Output

After processing, you’ll get a table like this:

| Owners | Share | Total Marla Share | Killa | Kanal | Marla | Sarshai | Result Text      |
|--------|-------|-------------------|--------|--------|--------|----------|------------------|
| Amar   | 0.25  | 25.00             | 0      | 1      | 5      | 0        | 0Ki-1K-5M-0S     |
| Balbir | 0.5   | 50.00             | 0      | 3      | 10     | 0        | 0Ki-3K-10M-0S    |
| Charan | 0.25  | 25.00             | 0      | 1      | 5      | 0        | 0Ki-1K-5M-0S     |

- 💾 Click **Download CSV** to export results.

---

## ⚙️ Technical Notes

- Built using **Streamlit**, **Pandas**, and **Regex**
- Automatically handles fractional shares like `3/7` or `5/16`
- Supports both **manual** and **automated** data input

---

## 📦 Requirements

To run locally:

```bash
pip install streamlit pandas openpyxl
streamlit run app.py

