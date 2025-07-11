import pdfplumber
import pandas as pd
import yaml
import os
import re

# Get absolute path to the YAML next to the script
script_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(script_dir, "wf_pdf_template.yaml")

# Load config safely
with open(yaml_path) as f:
    config = yaml.safe_load(f)
expected_columns = config["expected_columns"]

all_rows = []

with pdfplumber.open("input_feed/061625Fargo.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages):
        table = page.extract_table()
        if table:
            print(f"✅ Found table on page {page_num + 1}")
            all_rows.extend(table)

# # 🧪 DEBUG: Inspect if text is present or scanned images
# for page_num, page in enumerate(pdf.pages):
#     print(f"Page {page_num + 1} text preview:", page.extract_text())

for page_num, page in enumerate(pdf.pages):
    text = page.extract_text()
    if "Transaction History" in text or "Statement Period" in text:
        print(f"\n📄 Full Text from Page {page_num + 1}:\n{text}")


lines = text.split("\n")
for line in lines:
    if re.search(config["patterns"]["date"], line):
        print("🔎 Found transaction line:", line)

match = re.match(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})", line)

if match:
    date = match.group(1)
    description = match.group(2)
    amount1 = match.group(3)
    amount2 = match.group(4)

    print(f"📅 Date: {date}")
    print(f"📝 Description: {description}")
    print(f"💸 Amount 1: {amount1}")
    print(f"💰 Amount 2: {amount2}")
else:
    print("❌ No match found on line:", line)


# # 🧪 DEBUG: Inspect structure of extracted rows
# print("\n🔍 Previewing extracted rows:")
# for i, row in enumerate(all_rows[:10]):  # Show first 10 rows
#     print(f"Row {i} ({len(row)} cols): {row}")

# # Filter to only rows matching expected column count
# valid_rows = [row for row in all_rows if isinstance(row, list) and len(row) == len(expected_columns)]

# # Create DataFrame
# if valid_rows:
#     df = pd.DataFrame(valid_rows, columns=expected_columns)
#     df.to_csv("statement_output.csv", index=False)
#     print("📁 Saved cleaned output to statement_output.csv")
# else:
#     print("⚠️ No valid rows matching column config found.")