# 🏷️ ERP Label Auto Print

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Description

Automated system that monitors ERP-generated TXT files, converts them into barcode-enabled labels, and prints them instantly to a fixed printer—eliminating manual intervention and reducing operational errors.

---

## 🚀 Key Features

- 📂 Auto-detect incoming ERP TXT files
- 🧾 Generate structured PDF labels
- 🔢 Code128 barcode generation
- 🖨️ Direct printing to fixed printer (no default dependency)
- 📊 SQLite logging system
- 🔍 Search and filter logs
- 📤 Export logs to Excel
- ❌ Error handling and file routing
- 🔁 Duplicate UL detection
- 📈 Dashboard with live stats

---

## 🏗️ Workflow

ERP TXT → Watcher → Parser → PDF Generator → Printer → Database → UI

---

## 📁 Project Structure

label_app/
│
├── app.py
├── core/
│   └── generator.py
├── database/
│   └── db.py
├── services/
│   └── printer.py
├── ui/
│   ├── dashboard.py
│   ├── logs.py
│   └── sidebar.py
├── assets/
│   └── logo.png
├── stickers/
│   ├── yet_to_print/
│   ├── pdf/
│   └── error_files/

---

## ⚙️ Installation

### 1. Install Python
Python 3.11.x

### 2. Install Dependencies
pip install ttkbootstrap reportlab python-barcode pillow watchdog pywin32 pandas openpyxl

### 3. Run Application
python app.py

---

## 🖨️ Printer Setup

- Install label printer driver (e.g., BIXOLON SLP-TX400)
- Ensure printer name matches in code:

PRINTER_NAME = "BIXOLON SLP-TX400"

---

## 📌 How It Works

1. ERP drops .txt file into:
   stickers/yet_to_print/

2. System automatically:
   - detects file
   - parses data
   - generates PDF label
   - prints label
   - logs entry

3. Invalid files are moved to error folder.

---

## 📊 Database

- SQLite-based
- Year-wise database:
  labels_2026.db
  labels_2027.db

---

## 🔐 Reliability Features

- File completion detection
- Duplicate UL protection
- Error isolation
- Safe print execution
- Logging and traceability

---

## ⚡ Future Improvements

- EXE packaging (PyInstaller)
- Config-based printer selection
- Multi-printer support
- Cloud backup
- Real-time monitoring dashboard

---

## 📄 License

MIT License
