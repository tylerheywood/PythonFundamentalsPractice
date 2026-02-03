# tools/generate_po_test_pdfs.py
from __future__ import annotations

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Output folder (change if you want)
OUT_DIR = Path(__file__).resolve().parents[1] / "generated_test_pdfs"

# 6 valid QAHE POs (digits part only)
PO_DIGITS_LIST = [
    "030156",
    "030155",
    "030154",
    "030153",
    "030152",
    "030151",
]

# Each entry uses a format your detector supports
TEMPLATES = [
    ("01_purchase_order_digits.pdf",         lambda d: f"Purchase order: {d}"),
    ("02_purchase_order_po_dash_digits.pdf", lambda d: f"Purchase order: PO-{d}"),
    ("03_po_colon_digits.pdf",               lambda d: f"PO: {d}"),
    ("04_po_hash_colon_digits.pdf",          lambda d: f"PO #: {d}"),
    ("05_po_dash_digits.pdf",                lambda d: f"PO-{d}"),
    ("06_qahe_spaced_po_only.pdf",            lambda d: f"QAHE - PO - {d}"),
]


def write_pdf(path: Path, lines: list[str]) -> None:
    """
    Generates a simple text-layer PDF (pdfplumber-readable).
    """
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4

    y = height - 80
    c.setFont("Helvetica", 12)

    for line in lines:
        c.drawString(60, y, line)
        y -= 18

    c.showPage()
    c.save()


def _invoice_block(*, invoice_no: str, supplier: str, total_line: str, include_net_vat: bool) -> list[str]:
    """
    Build an invoice-ish header + value block.
    - total_line lets us test different label variants that your extractor supports.
    - include_net_vat lets us test the explicit net/vat rule.
    """
    lines = [
        "INVOICE (Test Fixture)",
        f"Invoice Number: {invoice_no}",
        f"Supplier: {supplier}",
        "Invoice Date: 2026-01-23",
        "",
    ]

    if include_net_vat:
        # Triggers EXPLICIT_NET_VAT_BLOCK (Rule A)
        lines += [
            "Net Amount: £100.00",
            "VAT Amount: £20.00",
            "Total Amount: £120.00",
        ]
    else:
        # Triggers LABELED_TOTAL / SINGLE_TOTAL_LINE depending on label
        lines += [
            total_line,
        ]

    lines += [""]  # spacer
    return lines


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------
    # Acceptance fixtures (end-to-end sanity for your pipeline)
    # ---------------------------------------------------------------------
    fixtures = []

    # A) VALID PO + labelled total (decimals + £) => should extract gross_total and validate PO
    fixtures.append(
        (
            "A_valid_po_labeled_total.pdf",
            _invoice_block(
                invoice_no="INV-VALID-001",
                supplier="QAHE-S000000",
                total_line="Invoice Total: £123.45",
                include_net_vat=False,
            )
            + [
                "Purchase order: 030156",
                "",
                "Thank you for your business.",
            ],
        )
    )

    # B) INVALID PO + labelled total => should extract gross_total but fail PO validation (not in master / not open)
    fixtures.append(
        (
            "B_invalid_po_labeled_total.pdf",
            _invoice_block(
                invoice_no="INV-INVALID-001",
                supplier="QAHE-S000000",
                total_line="Invoice Total: £67.89",
                include_net_vat=False,
            )
            + [
                "Purchase order: 999999",  # choose a PO you know won't be in po_master
                "",
                "Thank you for your business.",
            ],
        )
    )

    # C) PO present but total is an integer (PO-like) => should NOT be parsed as money (prevents false positives)
    fixtures.append(
        (
            "C_po_like_total_integer_should_not_parse.pdf",
            _invoice_block(
                invoice_no="INV-NEG-001",
                supplier="QAHE-S000000",
                total_line="Invoice Total: 123456",  # no decimals -> should NOT parse
                include_net_vat=False,
            )
            + [
                "PO: 030155",
                "",
                "This file is meant to ensure totals parsing does NOT treat PO-like integers as £.",
            ],
        )
    )

    # D) Explicit net/vat/total block => should parse via EXPLICIT_NET_VAT_BLOCK
    fixtures.append(
        (
            "D_explicit_net_vat_total_block.pdf",
            _invoice_block(
                invoice_no="INV-NETVAT-001",
                supplier="QAHE-S000000",
                total_line="(unused)",
                include_net_vat=True,
            )
            + [
                "PO #: 030154",
                "",
                "Thank you for your business.",
            ],
        )
    )

    # E) Alternative label variants => should still parse totals
    fixtures.append(
        (
            "E_total_due_label_variant.pdf",
            _invoice_block(
                invoice_no="INV-LABEL-001",
                supplier="QAHE-S000000",
                total_line="Total Due: £210.00",
                include_net_vat=False,
            )
            + [
                "PO-030153",
                "",
                "Thank you for your business.",
            ],
        )
    )

    fixtures.append(
        (
            "F_amount_due_label_variant.pdf",
            _invoice_block(
                invoice_no="INV-LABEL-002",
                supplier="QAHE-S000000",
                total_line="Amount Due: £99.99",
                include_net_vat=False,
            )
            + [
                "QAHE - PO - 030152",
                "",
                "Thank you for your business.",
            ],
        )
    )

    # ---------------------------------------------------------------------
    # Keep your original 6 PO-format PDFs too (now with realistic money blocks)
    # These are useful for verifying PO detection formats in bulk.
    # We'll make them use mixed money formats to broaden coverage.
    # ---------------------------------------------------------------------
    if len(PO_DIGITS_LIST) != len(TEMPLATES):
        raise ValueError("PO_DIGITS_LIST and TEMPLATES must be the same length (6).")

    money_variants = [
        "Invoice Total: £123.45",  # labeled
        "Total: 88.88",            # single total line (no £)
        "Total £16,618.44",        # comma format
        "Total Due: £210.00",      # labeled variant
        "Amount Due: £99.99",      # labeled variant
        "Invoice Total: £67.89",   # labeled
    ]

    for i, (digits, (filename, make_line)) in enumerate(zip(PO_DIGITS_LIST, TEMPLATES), start=1):
        if not (digits.isdigit() and len(digits) == 6):
            raise ValueError(f"Invalid PO digits: {digits!r}")

        po_line = make_line(digits)
        total_line = money_variants[i - 1]

        lines = (
            _invoice_block(
                invoice_no=f"INV-POFMT-{i:03d}",
                supplier="QAHE-S000000",
                total_line=total_line,
                include_net_vat=False,
            )
            + [
                po_line,
                "",
                "Thank you for your business.",
            ]
        )

        fixtures.append((f"POFMT_{filename}", lines))

    # ---------------------------------------------------------------------
    # Write all PDFs
    # ---------------------------------------------------------------------
    for filename, lines in fixtures:
        write_pdf(OUT_DIR / filename, lines)

    print(f"Generated {len(fixtures)} PDFs in: {OUT_DIR}")


if __name__ == "__main__":
    main()
