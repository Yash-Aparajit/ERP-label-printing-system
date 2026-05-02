import os

def print_pdf(path):

    try:
        os.startfile(path, "print")
    except Exception as e:
        print("Printer error:", e)
