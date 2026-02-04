"""
Goal

Build a calm, auditable probe that answers:

“What kind of PDF am I dealing with?”

Inputs

One local PDF file path (hardcode it for now)

Outputs

Example shape :

File: invoice_sample.pdf
Pages: 3

Page 1
  has_text_layer: True
  extracted_char_count: 1243
  preview: "INVOICE DATE 12/03/2025 ..."

Page 2
  has_text_layer: False
  extracted_char_count: 0
  preview: ""

Page 3
  has_text_layer: True
  extracted_char_count: 412
  preview: "Terms and conditions ..."

Summary
  total_chars: 1655
  pages_with_text_layer: 2
  pages_without_text_layer: 1
"""

import pdfplumber
from pathlib import Path

path = Path(
    r"/Users/tylerheywood/PycharmProjects/PythonFundamentalsPractice/00-Misc/sample invoices/invoice_3.pdf"
)


def preview_text(text: str, limit: int = 60) -> str:
    one_line = " ".join(text.split())  # collapse whitespace/newlines
    return one_line[:limit] + (
        "..." if len(one_line) > limit else ""
    )  # if line is longer than limit show "..."


print(f"File: {path.name}")

total_chars = 0
pages_with_text = 0
pages_without_text = 0

with pdfplumber.open(path) as pdf:
    print(f"Pages: {len(pdf.pages)}\n")

    for page_index, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        char_count = len(text)
        has_text_layer = len(page.chars) > 0  # more reliable than text alone

        total_chars += char_count
        if has_text_layer:
            pages_with_text += 1
        else:
            pages_without_text += 1

        print(f"Page {page_index}")
        print(f"  has_text_layer: {has_text_layer}")
        print(f"  extracted_char_count: {char_count}")
        print(f'  preview: "{preview_text(text)}"\n')

print("Summary")
print(f"  total_chars: {total_chars}")
print(f"  pages_with_text_layer: {pages_with_text}")
print(f"  pages_without_text_layer: {pages_without_text}")
