# 🏷️ ERP Label Auto Print

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Description

ERP Label Auto Print is a production-grade automation tool designed for warehouse and manufacturing environments.  
It continuously monitors ERP-generated `.txt` files, converts them into structured barcode labels, and prints them instantly to a fixed label printer.

The system eliminates manual label generation, reduces human errors, and ensures consistent, real-time printing operations.

---

## 🎯 Problem Statement

In many factory environments:

- Labels are generated manually from ERP data  
- Printing is inconsistent and error-prone  
- Operators select wrong printers or forget steps  
- There is no reliable logging or traceability  

This system solves all of the above by fully automating the workflow.

---

## 🚀 Key Features

- 📂 Real-time folder monitoring (watchdog-based)
- 🧾 Automated PDF label generation (ReportLab)
- 🔢 Code128 barcode generation for UL tracking
- 🖨️ Direct printing to fixed printer (no default dependency)
- 📊 SQLite logging system with year-wise databases
- 🔍 Fast search and filtering of logs
- 📤 Excel export (pandas + openpyxl)
- ❌ Error handling with file isolation
- 🔁 Duplicate UL detection (prevents reprocessing)
- 📈 Dashboard showing live stats and latest activity
- ⚡ Lightweight and fast execution

---

## 🏗️ System Workflow

ERP System → TXT File → Watcher → Parser → PDF Generator → Printer → Database → UI Dashboard

---

## 📁 Project Structure

label_app/
│
├── app.py                  → Main application entry point
│
├── core/
│   └── generator.py        → PDF + barcode generation logic
│
├── database/
│   └── db.py               → SQLite operations (logs, search, export)
│
├── services/
│   └── printer.py          → Printer handling (fixed printer logic)
│
├── ui/
│   ├── dashboard.py        → Dashboard view
│   ├── logs.py             → Logs table UI
│   └── sidebar.py          → Navigation UI
│
├── assets/
│   └── logo.png
│
├── stickers/
│   ├── yet_to_print/       → ERP input folder
│   ├── pdf/                → Generated labels
│   └── error_files/        → Failed / invalid files

---

## ⚙️ Installation Guide

### 1. Install Python

Recommended version:

Python 3.11.x

Avoid newer versions due to dependency instability.

---

### 2. Install Dependencies

Run:

pip install ttkbootstrap reportlab python-barcode pillow watchdog pywin32 pandas openpyxl

---

### 3. Run Application

Navigate to project folder:

python app.py

---

## 🖨️ Printer Setup

1. Install your label printer driver (example: BIXOLON SLP-TX400)
2. Ensure printer name matches exactly in code:

PRINTER_NAME = "BIXOLON SLP-TX400"

3. Keep printer online and ready

⚠️ Important:  
The system bypasses default printer and always prints to this fixed printer.

---

## 📌 How It Works

1. ERP exports a `.txt` file into:

   stickers/yet_to_print/

2. System automatically:
   - detects file creation
   - waits until file is fully written
   - parses required fields
   - generates barcode label PDF
   - sends print command
   - logs entry in database

3. If file is invalid:
   - moved to `error_files/`
   - error logged

---

## 📊 Database Design

- SQLite-based lightweight database
- Auto-generated yearly files:

labels_2026.db  
labels_2027.db  

### Stored Data:

- UL Counter
- Plant
- EDI Number
- Quantity
- Timestamp
- Status (SUCCESS / ERROR)
- PDF Path

---

## 🔐 Reliability & Safety Features

- ✔ File completion detection (prevents partial reads)
- ✔ Duplicate UL protection (no double printing)
- ✔ Error isolation (bad files moved safely)
- ✔ Controlled print execution
- ✔ Logging for traceability
- ✔ Non-blocking background processing

---

## ⚡ Performance

- Processes files in real-time
- Minimal latency between file drop → print
- Handles continuous ERP output
- Designed for multi-hour continuous operation

---

## 🧠 Design Decisions

- **SQLite** → lightweight, zero-config database  
- **Watchdog** → real-time file monitoring  
- **ReportLab** → precise label formatting  
- **Fixed printer logic** → eliminates user error  
- **Threaded worker** → prevents UI blocking  

---

## ⚠️ Known Limitations

- Windows-only (due to printer integration)
- Depends on installed PDF handler for printing
- Printer must be pre-configured

---

## 🔮 Future Improvements

- EXE packaging (PyInstaller for no-Python deployment)
- Config file for printer selection
- Multi-printer routing logic
- Centralized logging / cloud backup
- Live monitoring dashboard (web-based)
- Auto-update system

---

## 🧪 Testing Checklist

Before deployment:

- ✔ Printer installed and tested manually
- ✔ TXT file format validated
- ✔ Folder paths correct
- ✔ Database writable
- ✔ All dependencies installed

---

## 📄 License

MIT License

---

## 👨‍💻 Author

By Yash Aparajit

---
