# 🧾 PDF Payslip Bulk Encryptor

A simple GUI-based Python tool to **encrypt multiple PDF files** (like payslips) using passwords from an Excel file.  
Each encrypted file is saved with a filename format like: **PAXASIA-{LastName}-{FirstName}-{CutOffDate}-PAYSLIP.pdf**

---

## 📦 Features

- 🔒 Encrypts each PDF using a unique password from Excel
- 🧾 Reads employee info, passwords, and filenames from a spreadsheet
- 📁 Outputs encrypted files in a selected folder
- ✅ Friendly GUI (built with `tkinter`)
- 📋 Scrollable results log with success/failure messages

---

## 📁 Excel Format

Your Excel file **must** contain the following column headers:

| First Name | Last Name | Employee ID | Password | FileName  |
|------------|------------|-------------|----------|-----------|
| John       | Doe        | 001         | pass123  | john_doe  |
| Jane       | Smith      | 002         | mypass   | jane_smith|

- `FileName` should **not** include the `.pdf` extension
- PDFs must be placed in a folder named `PDFs` (next to the script)

---

## 🚀 How to Use

1. 📁 Place your **PDF files** in a folder called `PDFs` (same directory as the script).
2. 📊 Prepare your **Excel file** as described above.
3. 🛠 Run the Python script:
   ```bash
   python your_script_name.py
