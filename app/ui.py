import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
from hashing import compute_checksum
from constants import ALGORITHMS
from resource_path import resource_path


class ChecksumApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Checksum Verifier")

        icon_path = resource_path("assets/icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        self.geometry("600x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # ---- File selection ----
        self.select_file = tk.Frame(self)
        self.select_file.pack(pady=10)

        tk.Label(self.select_file, text="File to Verify").pack()
        self.file_entry = tk.Entry(self.select_file, width=50)
        self.file_entry.pack(side=tk.LEFT, padx=(0, 5))

        self.select_button = tk.Button(
            self.select_file, text="Select File", command=self.browse_file
        )
        self.select_button.pack(side=tk.LEFT)

        # ---- Algorithm selection ----
        self.select_algorithm = tk.Frame(self)
        self.select_algorithm.pack(pady=10)

        tk.Label(self.select_algorithm, text="Select Algorithm").pack()
        self.algorithm_var = tk.StringVar(value="sha256")

        self.algorithm_dropdown = ttk.Combobox(
            self.select_algorithm,
            values=ALGORITHMS,
            textvariable=self.algorithm_var,
            state="readonly",
        )
        self.algorithm_dropdown.pack()

        # ---- Expected checksum ----
        self.expected_checksum = tk.Frame(self)
        self.expected_checksum.pack(pady=10)

        tk.Label(self.expected_checksum, text="Expected Checksum").pack()
        self.expected_entry = tk.Entry(self.expected_checksum, width=60)
        self.expected_entry.pack()

         # ---- Verify and Clear buttons ----
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=5)

        self.verify_button = tk.Button(buttons_frame, text="Verify", command=self.compute)
        self.verify_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(buttons_frame, text="Clear", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # ---- Result display ----
        self.result = tk.Frame(self)
        self.result.pack(pady=10)

        self.result_hash_var = tk.StringVar()
        self.result_hash = tk.Label(
            self.result, textvariable=self.result_hash_var, font=("Arial", 12)
        )
        self.result_hash.pack()

        self.result_status_var = tk.StringVar()
        self.result_status = tk.Label(
            self.result, textvariable=self.result_status_var, font=("Arial", 12)
        )
        self.result_status.pack()

        # ---- Progress bar ----
        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=400, mode="determinate"
        )
        self.progress.pack(pady=5)

        self.progress_percent = tk.Label(self, text="0%")
        self.progress_percent.pack()
        self.progress_percent.pack_forget() 

    # ---- Browse file dialog ----
    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)

    # ---- Compute checksum ----
    def compute(self, event=None):
        if self.verify_button['state'] == 'disabled':
            return
        
        file_path = self.file_entry.get()
        algorithm = self.algorithm_var.get()
        expected = self.expected_entry.get().strip()

        if not file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        if not expected:
            messagebox.showerror("Error", "Please provide expected checksum.")
            return
        
        # Reset UI
        self.progress["value"] = 0
        self.progress["maximum"] = 100
        self.result_hash_var.set("")
        self.result_status_var.set("")
        
        self.progress_percent.pack()

        self.verify_button.config(state="disabled")
        self.select_button.config(state="disabled")
        self.clear_button.config(state="disabled")

        # Start worker thread
        Thread(
            target=self._compute_worker,
            args=(file_path, algorithm, expected),
            daemon=True,
        ).start()

    def _compute_worker(self, file_path, algorithm, expected):
        try:
            def progress_callback(percent):
                self.after(0, self._update_progress, percent)

            computed_hash = compute_checksum(
                file_path, algorithm, progress_callback
            )

            match = computed_hash.lower() == expected.lower()
            result_status = "MATCH" if match else "MISMATCH"
            color = "green" if match else "red"

            self.after(
                0,
                self._update_result,
                computed_hash,
                result_status,
                color,
            )

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            self.after(0, lambda: self.select_button.config(state="normal"))
            self.after(0, lambda: self.verify_button.config(state="normal"))
            self.after(0, lambda: self.clear_button.config(state="normal"))

    def _update_result(self, result_hash, result_status, color):
        self.result_hash_var.set(result_hash)
        self.result_status_var.set(result_status)
        self.result_hash.config(fg=color)
        self.result_status.config(fg=color)
        self.progress["value"] = 0
        self.progress_percent.pack_forget()

    def _update_progress(self, percent):
        self.progress["value"] = percent
        self.progress_percent.config(text=f"{percent:.1f}%")

    def clear_fields(self):
        self.file_entry.delete(0, tk.END)
        self.expected_entry.delete(0, tk.END)
        self.result_hash_var.set("")
        self.result_status_var.set("")
        self.progress["value"] = 0
        self.progress_percent.pack_forget() 
        self.algorithm_var.set("sha256")  # Optional: reset algorithm to default
