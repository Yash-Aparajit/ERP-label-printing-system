import os
import time


def print_pdf(path):

    try:

        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF not found: {path}")

        # small delay to ensure file write completion
        time.sleep(0.2)

        os.startfile(path, "print")

    except Exception as e:

        print("Printer error:", e)
