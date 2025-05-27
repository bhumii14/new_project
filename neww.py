import pytesseract
from PIL import Image
import cv2
import json
import re

# Load image
image_path = "C:/Users/Lenovo/OneDrive/Documents/bill.jpg"
image = cv2.imread(image_path)


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Convert image to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Extract text
text = pytesseract.image_to_string(image)

# Print raw text (optional)
print(text)

# Helper function to parse bill
def parse_invoice(text):
    lines = text.splitlines()
    data = {
        "Invoice": {},
        "Products": [],
        "Totals": {},
        "Terms": ""
    }

    # Extract key fields
    for line in lines:
        if "Invoice No" in line:
            match = re.search(r'Invoice No\s*:\s*(\d+)\s*Date\s*:\s*(\d{2}-\d{2}-\d{4})', line)
            if match:
                data["Invoice"]["Number"] = match.group(1)
                data["Invoice"]["Date"] = match.group(2)

        if "M/s" in line:
            data["Invoice"]["Customer"] = line.strip()

        if re.match(r'\d+\.\s+\w+', line):
            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) >= 7:
                data["Products"].append({
                    "SN": parts[0],
                    "Product Name": parts[1],
                    "Packing": parts[2],
                    "Batch No": parts[3],
                    "Expiry": parts[4],
                    "QTY": parts[5],
                    "Amount": parts[-1]
                })

        if "SUB TOTAL" in line:
            amount = re.findall(r'\d+\.\d{2}', line)
            if amount:
                data["Totals"]["Subtotal"] = float(amount[0])

        if "Discount" in line:
            amount = re.findall(r'\d+\.\d{2}', line)
            if amount:
                data["Totals"]["Discount"] = float(amount[0])

        if "SGST" in line:
            amount = re.findall(r'\d+\.\d{2}', line)
            if amount:
                data["Totals"]["SGST"] = float(amount[0])

        if "CGST" in line:
            amount = re.findall(r'\d+\.\d{2}', line)
            if amount:
                data["Totals"]["CGST"] = float(amount[0])

        if "GRAND TOTAL" in line:
            amount = re.findall(r'\d+\.\d{2}', line)
            if amount:
                data["Totals"]["Grand Total"] = float(amount[0])

        if "Terms & Conditions" in line:
            terms_index = lines.index(line)
            data["Terms"] = " ".join(lines[terms_index:])

    return data

# Parse the text and print JSON
parsed_data = parse_invoice(text)
print(json.dumps(parsed_data, indent=4))
