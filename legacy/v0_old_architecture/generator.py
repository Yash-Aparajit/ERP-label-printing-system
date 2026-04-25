import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


def draw_single_label(c, plant, ul, edi, inv, qty, created, time, y_offset):

    c.setFont("Courier-Bold",9)

    c.drawString(3*mm, y_offset + 33*mm, f"U/L COUNTER : {ul}")
    c.drawRightString(72*mm, y_offset + 33*mm, plant)

    c.drawString(3*mm, y_offset + 29*mm, f"EDI NUMBER : {edi}")
    c.drawString(3*mm, y_offset + 25*mm, f"INV/DATE : {inv}")
    c.drawString(3*mm, y_offset + 21*mm, f"EDI/REC. QTY : {qty}")
    c.drawString(3*mm, y_offset + 17*mm, f"CREATED BY : {created}")
    c.drawString(3*mm, y_offset + 13*mm, f"C. DATE/TIME : {time}")

    options = {
        "write_text": False,
        "module_width": 0.28,
        "module_height": 6,
        "quiet_zone": 1
    }

    code = barcode.get('code128', ul, writer=ImageWriter())
    barcode_file = code.save("temp_barcode", options)

    c.drawImage(barcode_file, 5*mm, y_offset + 2*mm, width=60*mm, height=9*mm)

    os.remove(barcode_file)


def generate_label(data, output_folder):

    plant, ul, edi, inv, qty, created, time = data

    pdf_path = os.path.join(output_folder, f"{ul}.pdf")

    # 3 stickers per page
    c = canvas.Canvas(pdf_path, pagesize=(75*mm, 114*mm))

    draw_single_label(c, plant, ul, edi, inv, qty, created, time, 76*mm)
    draw_single_label(c, plant, ul, edi, inv, qty, created, time, 38*mm)
    draw_single_label(c, plant, ul, edi, inv, qty, created, time, 0)

    c.save()
    return pdf_path
