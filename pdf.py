import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os
    
def encrypt_pdf(input_path, output_path, user_password):
    """Encrypts a PDF file with a user password."""
    try:
        with open(input_path, 'rb') as input_file:
            reader = PyPDF2.PdfReader(input_file)
            writer = PyPDF2.PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            writer.encrypt(user_password)

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

        return True
    except Exception as e:
        messagebox.showerror("Encrypt Error", f"An error occurred: {e}")
        return False

def browse_file():
    """Opens a file dialog to select a PDF file and populates suggested password."""
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    file_path.set(filename)

    if filename:
        try:
            base_name = os.path.basename(filename)
            name_without_extension = os.path.splitext(base_name)[0]
            employee_id = name_without_extension.split('_')[0]  # Extract employee ID
            if len(employee_id) >= 8:
                 password.set(employee_id)
                 repeat_password.set(employee_id)

            else:

                 password.set("Password123")
                 repeat_password.set("Password123") # if it is less than 8 characters just set it to password123
        except:
            password.set("Password123")
            repeat_password.set("Password123")

def reset_form():
    """Resets the form fields to their initial state."""
    file_path.set("")
    password.set("")
    repeat_password.set("")

def process_file():
    """Processes the selected file and adds a password, overwriting the original."""
    input_pdf_path = file_path.get()
    user_password = password.get().strip()
    repeat_user_password = repeat_password.get().strip()

    if not input_pdf_path:
        messagebox.showerror("Error", "Please select a PDF file.")
        return

    if len(user_password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long.")
        return

    if user_password != repeat_user_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    # Encrypt the PDF, overwriting the original
    if encrypt_pdf(input_pdf_path, input_pdf_path, user_password):  # Use input_pdf_path as output_path
        messagebox.showinfo("Success", f"PDF {os.path.basename(input_pdf_path)} overwritten with password protection.")
        reset_form() # Reset the form ONLY on success
    else:
        messagebox.showerror("Error", "PDF encryption failed.")

def toggle_password_visibility():
    """Toggles the visibility of the password fields."""
    if password_visible.get():
        password_entry.config(show="")
        repeat_password_entry.config(show="")
    else:
        password_entry.config(show="*")
        repeat_password_entry.config(show="*")


# --- GUI Setup ---
root = tk.Tk()
root.title("PDF Payslip Protector")

#Set the resizable property False
root.resizable(False, False)

# --- Variables ---
file_path = tk.StringVar()
password = tk.StringVar()
repeat_password = tk.StringVar()
password_visible = tk.BooleanVar()  # Track password visibility

# --- Widgets ---
# File Selection
file_label = tk.Label(root, text="Select PDF File:")
file_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

file_entry = tk.Entry(root, textvariable=file_path, width=50)
file_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Password Input
password_label = tk.Label(root, text="Password (8+ characters):")
password_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
password_entry = tk.Entry(root, textvariable=password, width=30, show="*")
password_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

repeat_password_label = tk.Label(root, text="Repeat Password:")
repeat_password_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
repeat_password_entry = tk.Entry(root, textvariable=repeat_password, width=30, show="*")
repeat_password_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

# Show Password Checkbox
show_password_check = tk.Checkbutton(root, text="Show Password", variable=password_visible, command=toggle_password_visibility)
show_password_check.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)


# Process Button
process_button = tk.Button(root, text="Protect PDF", command=process_file)
process_button.grid(row=4, column=1, pady=10)

root.mainloop()
