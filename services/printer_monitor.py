import win32print


def get_printer_status():

    try:

        printer_name = win32print.GetDefaultPrinter()
        handle = win32print.OpenPrinter(printer_name)

        try:
            info = win32print.GetPrinter(handle, 2)
            status = info["Status"]
        finally:
            win32print.ClosePrinter(handle)

        if status == 0:
            return "Ready"

        if status & win32print.PRINTER_STATUS_PAUSED:
            return "Paused"

        if status & win32print.PRINTER_STATUS_OFFLINE:
            return "Offline"

        if status & win32print.PRINTER_STATUS_PAPER_OUT:
            return "Out of Paper"

        if status & win32print.PRINTER_STATUS_ERROR:
            return "Error"

        return "Busy"

    except Exception:

        return "Not Found"
