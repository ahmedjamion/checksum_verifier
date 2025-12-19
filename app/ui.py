# app/ui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .hashing import compute_checksum, verify_checksum
from .constants import ALGORITHMS

class ChecksumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checksum Verifier")
        self.geometry("600x250")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # ---- File selection ----
        tk.Label(self, text="File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.file_entry = tk.Entry(self, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text="Browse...", command=self.browse_file).grid(row=0, column=2, padx=5, pady=5)

        # ---- Algorithm selection ----
        tk.Label(self, text="Algorithm:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.algorithm_var = tk.StringVar(value="sha256")
        self.algorithm_dropdown = ttk.Combobox(self, values=ALGORITHMS, textvariable=self.algorithm_var, state="readonly")
        self.algorithm_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # ---- Expected checksum ----
        tk.Label(self, text="Expected Checksum:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.expected_entry = tk.Entry(self, width=50)
        self.expected_entry.grid(row=2, column=1, padx=5, pady=5)

        # ---- Compute button ----
        tk.Button(self, text="Compute", command=self.compute).grid(row=3, column=1, padx=5, pady=10)

        # ---- Result display ----
        self.result_var = tk.StringVar()
        self.result_label = tk.Label(self, textvariable=self.result_var, font=("Arial", 12))
        self.result_label.grid(row=4, column=0, columnspan=3, pady=10)

        # ---- Optional progress bar ----
        self.progress = ttk.Progressbar(self, orient="horizontal", length=500, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3, pady=5)

    # ---- Browse file dialog ----
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    # ---- Compute checksum and display result ----
    def compute(self):
        file_path = self.file_entry.get()
        algorithm = self.algorithm_var.get()
        expected = self.expected_entry.get().strip()

        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        try:
            computed_hash = compute_checksum(file_path, algorithm)

            if expected:
                match, _ = verify_checksum(file_path, expected, algorithm)
                self.result_var.set(f"{computed_hash}  →  {'MATCH' if match else 'MISMATCH'}")
                self.result_label.config(fg="green" if match else "red")
            else:
                self.result_var.set(computed_hash)
                self.result_label.config(fg="black")

        except Exception as e:
            messagebox.showerror("Error", str(e))
