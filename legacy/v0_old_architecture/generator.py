import os
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import barcode
from barcode.writer import ImageWriter


def draw_label(c, plant, ul, edi, inv, qty, created, time):

    c.setFont("Courier-Bold",9)

    c.drawString(3*mm,34*mm,f"U/L COUNTER : {ul}")
    c.drawRightString(72*mm,34*mm,plant)

    c.drawString(3*mm,30*mm,f"EDI NUMBER : {edi}")
    c.drawString(3*mm,26*mm,f"INV/DATE : {inv}")
    c.drawString(3*mm,22*mm,f"EDI/REC. QTY : {qty}")
    c.drawString(3*mm,18*mm,f"CREATED BY : {created}")
    c.drawString(3*mm,14*mm,f"C. DATE/TIME : {time}")

    options = {
        "write_text": False,
        "module_width": 0.28,
        "module_height": 6,
        "quiet_zone": 1
    }

    code = barcode.get('code128', ul, writer=ImageWriter())
    barcode_file = code.save("temp_barcode", options)

    c.drawImage(barcode_file,5*mm,2*mm,width=60*mm,height=9*mm)

    os.remove(barcode_file)


def generate_label(data, output_folder):

    plant, ul, edi, inv, qty, created, time = data

    pdf_path = os.path.join(output_folder, f"{ul}.pdf")

    # correct sticker size
    c = canvas.Canvas(pdf_path, pagesize=(75*mm,38*mm))

    # page 1
    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    # page 2
    draw_label(c, plant, ul, edi, inv, qty, created, time)
    c.showPage()

    # page 3
    draw_label(c, plant, ul, edi, inv, qty, created, time)

    c.save()

    return pdf_path

