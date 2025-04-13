import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import os
from PyPDF2 import PdfReader, PdfWriter

def encrypt_pdf(input_path, output_path, password):
    try:
        with open(input_path, 'rb') as f:
            reader = PdfReader(f)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(password)

            with open(output_path, 'wb') as f_out:
                writer.write(f_out)
        return True
    except Exception as e:
        return False, str(e)

def process_excel():
    excel_path = excel_file_path.get()
    output_dir = output_folder.get()

    if not excel_path or not os.path.exists(excel_path):
        messagebox.showerror("Error", "Please select a valid Excel file.")
        return

    if not output_dir:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    try:
        df = pd.read_excel(excel_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read Excel file:\n{e}")
        return

    required_cols = {"First Name", "Last Name", "Employee ID", "Password", "FileName"}
    if not required_cols.issubset(set(df.columns)):
        messagebox.showerror("Error", f"Missing required columns in Excel.\nRequired: {required_cols}")
        return

    result_box.delete("1.0", tk.END)

    for idx, row in df.iterrows():
        first_name = str(row['First Name']).strip()
        last_name = str(row['Last Name']).strip()
        password = str(row['Password']).strip()
        pdf_file = str(row['FileName']).strip()
        pdf_path = f"PDFs/{pdf_file}.pdf"
        cutoff = cutoff_date_txt.get().strip()

        if not os.path.exists(pdf_path):
            result_box.insert(tk.END, f"[❌] File not found: {pdf_path}\n")
            continue

        output_filename = f"PAXASIA-{last_name}-{first_name}-{cutoff}-PAYSLIP.pdf"
        output_path = os.path.join(output_dir, output_filename)

        result = encrypt_pdf(pdf_path, output_path, password)
        if result is True:
            result_box.insert(tk.END, f"[✅] {output_filename} encrypted.\n")
        else:
            result_box.insert(tk.END, f"[❌] Failed for {pdf_path} - {result[1]}\n")

    messagebox.showinfo("Done", "Batch encryption completed.")
    os.startfile(output_dir)

def browse_excel():
    filename = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])
    if filename:
        excel_file_path.set(filename)

def browse_output_folder():
    foldername = filedialog.askdirectory()
    if foldername:
        output_folder.set(foldername)

# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Payslip Bulk Encryptor")
# root.geometry("600x500")
root.resizable(False, False)

# Variables
excel_file_path = tk.StringVar()
output_folder = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
cutoff_date_txt = tk.StringVar(value="April 1-15")

# Widgets
tk.Label(root, text="Cut-Off Period/Date").grid(row=0, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=cutoff_date_txt, width=40).grid(row=0, column=1, padx=10)

tk.Label(root, text="Excel File:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=excel_file_path, width=50).grid(row=1, column=1, padx=10)
tk.Button(root, text="Browse", command=browse_excel).grid(row=1, column=2)

tk.Label(root, text="Output Folder:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Entry(root, textvariable=output_folder, width=50).grid(row=2, column=1, padx=10)
tk.Button(root, text="Browse", command=browse_output_folder).grid(row=2, column=2)

tk.Button(root, text="Encrypt PDFs", command=process_excel, bg="#4CAF50", fg="white", width=20).grid(row=3, column=1, pady=20)

tk.Label(root, text="Encryption Results:").grid(row=4, column=0, padx=10, sticky="nw")
result_box = scrolledtext.ScrolledText(root, width=70, height=15)
result_box.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

root.mainloop()
