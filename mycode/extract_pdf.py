import pdfplumber
import re
import pandas as pd

pdf_path = "feed_input/061625Fargo.pdf"

# Flexible pattern to match: date, description, amount(s)
transaction_pattern = re.compile(
    r"^(\d{1,2}/\d{1,2})\s+(.*?)\s+([\d,]+\.\d{2})(?:\s+([\d,]+\.\d{2}))?$"
)
parsed_rows = []
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue

        lines = text.split("\n")
        print(f"\n📄 Page {page_num + 1}: Inspecting {len(lines)} lines")

        for line in lines:
            match = transaction_pattern.match(line)

            if match:
                txn = {
                    "Date": match.group(1),
                    "Description": match.group(2),
                    "Amount": match.group(3),
                    "Balance": match.group(4) if match.lastindex == 4 else None
                }
                print(f"✅ Parsed: {txn}")
                parsed_rows.append(txn)

            else:
                # Optional: Only print lines that resemble transactions
                if re.match(r"\d{1,2}/\d{1,2}", line):
                    print(f"❌ Transaction-like but no match: {line}")
            
# ✅ After all pages: Convert to DataFrame
df = pd.DataFrame(parsed_rows)
df.to_csv("feed_output/parsed_transactions.csv", index=False, sep="~")

print("📁 Exported parsed data to parsed_transactions.csv")

