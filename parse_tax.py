import pdfplumber
import json
import re

pdf_path = r"C:\Users\user\.gemini\antigravity-ide\brain\d392eaec-9ba3-4f53-82f7-7316f40af8d9\media__1787881112518.pdf"

tax_brackets = []

def parse_val(v):
    if not v or v.strip() == '-' or v.strip() == '':
        return 0
    v = v.replace(',', '').strip()
    try:
        return int(v)
    except:
        return 0

with pdfplumber.open(pdf_path) as pdf:
    # Table starts from page 2 (index 1)
    for i in range(1, len(pdf.pages)):
        page = pdf.pages[i]
        table = page.extract_table()
        if not table:
            continue
        
        for row in table:
            if not row or len(row) < 3:
                continue
            
            # The row must start with two numbers (min, max) in thousands
            col0 = row[0].replace(',', '').strip() if row[0] else ""
            if not col0.isdigit():
                continue
                
            min_val = int(col0) * 1000
            
            col1 = row[1].replace(',', '').strip() if row[1] else ""
            if col1.isdigit():
                max_val = int(col1) * 1000
            else:
                max_val = float('inf') # the last row might not have max
                
            taxes = [parse_val(x) for x in row[2:]]
            tax_brackets.append({
                "min": min_val,
                "max": max_val,
                "taxes": taxes
            })

with open("c:/Users/user/anti/tax_table.js", "w", encoding="utf-8") as f:
    f.write("const TAX_BRACKETS = " + json.dumps(tax_brackets, indent=2) + ";\n")
print(f"Extracted {len(tax_brackets)} brackets.")
