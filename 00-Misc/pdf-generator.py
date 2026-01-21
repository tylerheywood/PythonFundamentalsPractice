from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path


def main() -> None:
    output_path = Path("sample.pdf")

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    # Page 1
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 72, "Sample PDF for Text Extraction")
    c.drawString(72, height - 100, "Invoice Number: INV-00123")
    c.drawString(72, height - 120, "Supplier: Example Supplies Ltd")
    c.drawString(72, height - 140, "Total Amount: £1,234.56")
    c.showPage()

    # Page 2
    c.setFont("Helvetica", 12)
    c.drawString(72, height - 72, "Page 2 — Additional Notes")
    c.drawString(72, height - 100, "This page contains simple text.")
    c.drawString(72, height - 120, "It should extract cleanly.")
    c.showPage()

    c.save()
    print(f"Created {output_path.resolve()}")


if __name__ == "__main__":
    main()
