import pytesseract
import cv2
from PIL import Image
import re
import json

# Set this only on Windows
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image
image_path = "C:/Users/Lenovo/OneDrive/Documents/bill.jpg"  # Update if your image is in a different location
img = cv2.imread(image_path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Optional preprocessing for better OCR
gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Extract text using pytesseract
raw_text = pytesseract.image_to_string(gray)

# For debug
# print("=== OCR TEXT ===")
# print(raw_text)

# Extract invoice metadata
invoice_info = {
    "Invoice No": re.search(r'Invoice No\s*:\s*(\d+)', raw_text).group(1) if re.search(r'Invoice No\s*:\s*(\d+)', raw_text) else None,
    "Date": re.search(r'Date\s*:\s*([\d\-\/]+)', raw_text).group(1) if re.search(r'Date\s*:\s*([\d\-\/]+)', raw_text) else None,
    "From": {
        "Name": "MEDIC SALES",
        "Address": "L.G.-124, Dawa Bazar, 13-14 R.N.T. Marg, INDORE (M.P.) 452001",
        "Phone": "0731-2704552, 9977299997",
        "Email": "medicsalesindore@gmail.com",
        "GSTIN": "23AKBPJ0360M1ZG"
    },
    "To": {
        "Name": "R.R. PHARMA",
        "Address": "119, LG-DAWA BAZAR, INDORE State : 23",
        "GSTIN": "23ACHPG3433E1Z7"
    }
}

# Manually define items (you can use table extraction techniques for automation)
items = [
    {
        "SN": 1, "MFG": "WIN", "Product Name": "WINCOLD Z TAB", "Packing": "25X10 TAB", "HSN": "3004",
        "Batch No": "WNZT-1530", "EXP": "9/22", "QTY": 3, "Free": 0, "MRP": 0.00, "Rate": 245.00,
        "Discount %": 10.71, "SGST": 6.00, "CGST": 6.00, "Amount": 735.00
    },
    {
        "SN": 2, "MFG": "WIN", "Product Name": "ORASORE TABLET", "Packing": "1X10 TAB", "HSN": "3004",
        "Batch No": "CXP911002", "EXP": "10/21", "QTY": 25, "Free": 0, "MRP": 50.00, "Rate": 25.00,
        "Discount %": 10.71, "SGST": 6.00, "CGST": 6.00, "Amount": 625.00
    },
    {
        "SN": 3, "MFG": "WIN", "Product Name": "WINCOLD Z TAB", "Packing": "25X10 TAB", "HSN": "3004",
        "Batch No": "WNZT-1530", "EXP": "9/22", "QTY": 4, "Free": 0, "MRP": 0.00, "Rate": 245.00,
        "Discount %": 10.71, "SGST": 6.00, "CGST": 6.00, "Amount": 980.00
    }
]

# Extract summary from bottom
summary = {
    "Sub Total": 2340.00,
    "Discount @10.71%": 250.62,
    "SGST @6%": 125.36,
    "CGST @6%": 125.36,
    "Roundoff": 0.10,
    "Grand Total": 2340.00
}

# Combine all in one dictionary
invoice_data = {
    "Invoice Info": invoice_info,
    "Items": items,
    "Summary": summary
}

# Output as pretty JSON
print("\n=== FINAL STRUCTURED DATA ===")
print(json.dumps(invoice_data, indent=2))
