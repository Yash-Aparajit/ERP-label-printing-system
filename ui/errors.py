import os
import shutil
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

ERROR_FOLDER = os.path.join(BASE_DIR, "error_files")
INPUT_FOLDER = os.path.join(BASE_DIR, "yet_to_print")

def create_errors(parent):

    frame = ttk.Frame(parent)

    table_frame = ttk.Frame(frame)
    table_frame.pack(fill="both", expand=True, padx=15, pady=15)

    tree = ttk.Treeview(
        table_frame,
        columns=("File","Action"),
        show="headings"
    )

    tree.heading("File", text="Error File")
    tree.heading("Action", text="Retry")

    tree.pack(fill="both", expand=True)

    def load_errors():

        for i in tree.get_children():
            tree.delete(i)

        if not os.path.exists(ERROR_FOLDER):
            return

        for file in os.listdir(ERROR_FOLDER):

            if file.endswith(".txt"):

                tree.insert("", "end", values=(file,"Retry"))

    def retry():

        item = tree.selection()

        if not item:
            return

        file = tree.item(item)["values"][0]

        src = os.path.join(ERROR_FOLDER,file)
        dst = os.path.join(INPUT_FOLDER,file)

        shutil.move(src,dst)

        load_errors()

    retry_btn = ttk.Button(
        frame,
        text="Retry Selected",
        command=retry
    )

    retry_btn.pack(pady=10)

    load_errors()

    return frame
