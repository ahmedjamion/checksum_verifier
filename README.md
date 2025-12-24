# 🛡️ Checksum Verifier

A lightweight, multi-threaded desktop application built with Python and Tkinter for verifying file integrity. This tool allows users to calculate and compare file hashes to ensure data has not been corrupted or tampered with.

## ✨ Features

- **Multiple Algorithms**: Supports SHA-256, SHA-1, MD5, and SHA-512.
- **Multi-Threaded**: UI remains responsive while processing large files.
- **Real-Time Progress**: Dynamic progress bar with percentage updates.
- **Visual Validation**: Immediate "MATCH" or "MISMATCH" feedback with color coding.
- **Resource Efficient**: Processes files in small chunks to keep memory usage low.

## 🚀 Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/ahmedjamion/checksum_verifier.git
    cd checksum-verifier
    ```

2.  **Run the app**:
    ```bash
    python app/main.py
    ```

## 🛠️ Building the Standalone Executable

To create a single `.exe` file for Windows:

1.  **Install PyInstaller**:

    ```bash
    pip install pyinstaller
    ```

2.  **Run the build command**:
    ```bash
    pyinstaller --noconsole --onefile --add-data "assets;assets" --paths="app" --icon="assets/icon.ico" app/main.py
    ```

> **Note**: The `--add-data` flag is crucial for including the icon and other assets inside the executable.

## 📂 Project Structure

- `app/main.py`: The entry point that initializes the app.
- `app/ui.py`: Contains the `ChecksumApp` class and GUI logic.
- `app/hashing.py`: Contains the logic for file stream hashing.
- `app/constants.py`: Configuration for chunk sizes and algorithm lists.
- `assets/`: Storage for the application icon and images.

## 📝 Usage

1.  Click **Select File** to choose the file you wish to check.
2.  Select the **Algorithm** (e.g., SHA-256) used by the source.
3.  Paste the **Expected Checksum** provided by the developer/website.
4.  Click **Verify**. The app will calculate the hash and highlight the result in green (Match) or red (Mismatch).

---

_Created with ❤️ using Python and Tkinter._
