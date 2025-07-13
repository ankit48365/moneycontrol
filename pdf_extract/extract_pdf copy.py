import pdfplumber
import re
import pandas as pd

# file_name = "fargo_june25.pdf"
file_name = "freedom_july25.pdf"
pdf_path = "feed_input/" + file_name
parsed_rows = []

def is_amount(val):
    return bool(re.match(r"^[\d,]+\.\d{2}$", val.strip()))

def to_amount(val):
    return val.replace(",", "") if val else ""

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue

        lines = text.split("\n")
        for line in lines:
            parts = line.split()

            if not parts or not re.match(r"\d{1,2}/\d{1,2}", parts[0]):
                continue

            date = parts[0]
            check_num = parts[1] if parts[1].isdigit() and 3 <= len(parts[1]) <= 5 else ""
            desc_start = 2 if check_num else 1

            # Extract trailing amounts from the end of the line
            amounts = []
            while parts and is_amount(parts[-1]):
                amounts.insert(0, parts.pop())

            description = " ".join(parts[desc_start:]).strip()

            # Initialize fields
            deposit, withdrawal, balance = "", "", ""

            if len(amounts) == 3:
                deposit, withdrawal, balance = map(to_amount, amounts)
            elif len(amounts) == 2:
                balance = to_amount(amounts[-1])
                keyword = description.lower()
                if "withdrawal" in keyword or "check" in keyword or "payment" in keyword:
                    withdrawal = to_amount(amounts[0])
                else:
                    deposit = to_amount(amounts[0])
            elif len(amounts) == 1:
                balance = to_amount(amounts[0])

            txn = {
                "Date": date,
                "Check Number": check_num,
                "Description": description,
                "Deposits/Additions": deposit,
                "Withdrawals/Subtractions": withdrawal,
                "Ending Daily Balance": balance
            }

            parsed_rows.append(txn)

# ✅ Save to CSV with tilde separator
df = pd.DataFrame(parsed_rows)
df.to_csv(f"feed_output/{file_name}_transactions.csv", index=False, sep="~")
print("📁 Exported to parsed_transactions.csv with ~ as separator")