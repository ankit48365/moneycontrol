import pdfplumber
import re

pdf_path = "input_feed/061625Fargo.pdf"
# transaction_pattern = re.compile(r"(\d{2}/\d{2}/\d{4})\s+(.*?)\s+([\d,]+\.\d{2})\s+([\d,]+\.\d{2})")
transaction_pattern = re.compile(r"^(\d{1,2}/\d{1,2})\s+(.*?)\s+([\d,]+\.\d{2})(?:\s+([\d,]+\.\d{2}))?$")

# with pdfplumber.open("input_feed/061625Fargo.pdf") as pdf:
#     for page_num, page in enumerate(pdf.pages):
#         text = page.extract_text()
#         if text:
#             print(f"\n📄 Raw text from Page {page_num + 1}:")
#             lines = text.split("\n")
#             for i, line in enumerate(lines[:30]):  # first 30 lines for brevity
#                 print(f"Line {i}: {line}")


with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        if not text:
            continue

        target_keywords = ["Transaction History", "Statement Period"]

        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if not text or not any(kw in text for kw in target_keywords):
                continue  # Skip pages without relevant data

            print(f"\n📄 Processing Page {page_num + 1}")
            lines = text.split("\n")
            matches = []
            for line in lines:
                match = transaction_pattern.match(line)
                if match:
                    txn = {
                        "Date": match.group(1),
                        "Description": match.group(2),
                        "Amount": match.group(3),
                        "Balance": match.group(4) if match.lastindex == 4 else None
                    }
                    matches.append(txn)
                    print(f"✅ Parsed: {txn}")
                else:
                    print(f"❌ Not matched: {line}")

        # print(f"\n📄 Processing Page {page_num + 1}")

        # lines = text.split("\n")
        # for line in lines:
        #     match = transaction_pattern.match(line)
        #     if match:
        #         date = match.group(1)
        #         desc = match.group(2)
        #         debit = match.group(3)
        #         credit = match.group(4)

        #         print(f"✅ Match: {date} | {desc} | Debit: {debit} | Credit: {credit}")
        #     else:
        #         print(f"❌ No match: {line}")



