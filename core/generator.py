import os
import tempfile
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


def draw_label(c, plant, ul, edi, inv, qty, created, time):

    ul = ul.strip()

    c.setFont("Courier-Bold", 9)

    c.drawString(3 * mm, 34 * mm, f"U/L COUNTER  : {ul}")
    c.drawRightString(72 * mm, 34 * mm, plant)
    c.drawString(3 * mm, 30 * mm, f"EDI NUMBER   : {edi}")
    c.drawString(3 * mm, 26 * mm, f"INV/DATE     : {inv}")
    c.drawString(3 * mm, 22 * mm, f"EDI/REC. QTY : {qty}")
    c.drawString(3 * mm, 18 * mm, f"CREATED BY   : {created}")
    c.drawString(3 * mm, 14 * mm, f"C. DATE/TIME : {time}")

    options = {
        "write_text": False,
        "module_width": 0.16,
        "module_height": 6,
        "quiet_zone": 0.2
    }

    code = barcode.get("code128", ul, writer=ImageWriter())
    temp_dir = tempfile.gettempdir()
    barcode_path = os.path.join(temp_dir, f"temp_barcode_{ul}")

    barcode_file = None

    try:
        barcode_file = code.save(barcode_path, options)
        c.drawImage(barcode_file, 14 * mm, 2 * mm, width=40 * mm, height=7 * mm)
    finally:
        if barcode_file and os.path.exists(barcode_file):
            os.remove(barcode_file)


def generate_label(data, output_folder):

    plant, ul, edi, inv, qty, created, time = [x.strip() for x in data]

    pdf_path = os.path.join(output_folder, f"{ul}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=(75 * mm, 38 * mm))

    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    draw_label(c, plant, ul, edi, inv, qty, created, time)

    c.save()

    return pdf_path
