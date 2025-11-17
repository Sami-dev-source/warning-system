# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

# Fix import path - add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import TradingDataCollector


class TradingDataGUI:
    def __init__(self, root):
        self.root = root
        self.collector = TradingDataCollector()
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Sami & Mostafa – Trading Data Loader")
        self.root.geometry("520x300")
        self.root.configure(bg="#f0f8ff")

        # Title
        title = tk.Label(self.root, text="Financial Data Collector",
                         font=("Arial", 16, "bold"), bg="#f0f8ff", fg="#2c3e50")
        title.pack(pady=20)

        # Ticker input
        tk.Label(self.root, text="Enter ticker (AAPL, TSLA, BTC-USD...)",
                 font=("Arial", 12), bg="#f0f8ff").pack(pady=10)

        self.entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.entry.insert(0, "AAPL")
        self.entry.pack(pady=10)

        # Buttons
        self.download_btn = tk.Button(self.root, text="Download from Yahoo Finance",
                                      command=self.download, bg="#4CAF50", fg="white",
                                      font=("Arial", 11, "bold"), height=2)
        self.download_btn.pack(fill="x", padx=80, pady=10)

        self.csv_btn = tk.Button(self.root, text="Load Local CSV File",
                                 command=self.load_csv, bg="#2196F3", fg="white",
                                 font=("Arial", 11, "bold"), height=2)
        self.csv_btn.pack(fill="x", padx=80, pady=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Ready to load data...",
                                     font=("Arial", 10), bg="#f0f8ff", fg="#7f8c8d")
        self.status_label.pack(pady=10)

    def download(self):
        """Download data from Yahoo Finance"""
        try:
            ticker = self.entry.get().strip() or "AAPL"
            self.status_label.config(text=f"Downloading {ticker}...", fg="#f39c12")
            self.root.update()

            data = self.collector.from_yfinance(ticker)
            info = self.collector.get_data_info()

            messagebox.showinfo("SUCCESS",
                                f"Downloaded {ticker}\n"
                                f"Data points: {len(data)}\n"
                                f"Shape: {info['shape']}\n"
                                f"→ NumPy array ready for analysis!")

            self.status_label.config(text=f"✅ {ticker} loaded: {len(data)} points", fg="#27ae60")

        except Exception as e:
            error_msg = f"Failed to download {ticker}:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="❌ Download failed", fg="#e74c3c")

    def load_csv(self):
        """Load data from CSV file"""
        try:
            path = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if path:
                self.status_label.config(text=f"Loading {os.path.basename(path)}...", fg="#f39c12")
                self.root.update()

                data = self.collector.from_csv(path)
                info = self.collector.get_data_info()

                messagebox.showinfo("SUCCESS",
                                    f"Loaded {os.path.basename(path)}\n"
                                    f"Data points: {len(data)}\n"
                                    f"Shape: {info['shape']}\n"
                                    f"→ NumPy array ready for analysis!")

                self.status_label.config(text=f"✅ CSV loaded: {len(data)} points", fg="#27ae60")

        except Exception as e:
            error_msg = f"Failed to load CSV:\n{str(e)}"
            messagebox.showerror("Error", error_msg)
            self.status_label.config(text="❌ CSV load failed", fg="#e74c3c")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TradingDataGUI(root)
    root.mainloop()