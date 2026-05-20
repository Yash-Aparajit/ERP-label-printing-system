import win32print


PRINTER_NAME = "BIXOLON SLP-TX400"


def get_printer_status():

    try:

        handle = win32print.OpenPrinter(PRINTER_NAME)

        info = win32print.GetPrinter(handle, 2)

        status = info["Status"]

        win32print.ClosePrinter(handle)

        if status == 0:
            return "Ready"

        if status & win32print.PRINTER_STATUS_PAUSED:
            return "Paused"

        if status & win32print.PRINTER_STATUS_OFFLINE:
            return "Offline"

        if status & win32print.PRINTER_STATUS_ERROR:
            return "Error"

        return "Busy"

    except:

        return "Not Found"
