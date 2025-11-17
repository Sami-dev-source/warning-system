# src/data_loader.py
import pandas as pd
import numpy as np
import yfinance as yf


class TradingDataCollector:
    def __init__(self):
        self.data = None
        self.symbol = "Unknown"

    def from_yfinance(self, ticker="AAPL"):
        """Download data from Yahoo Finance and convert to numpy array"""
        try:
            print(f"📡 Downloading {ticker} from Yahoo Finance...")
            df = yf.download(ticker, period="1y", progress=False)

            if df.empty:
                raise ValueError(f"No data found for ticker: {ticker}")

            # Use 'Close' price and convert to numpy
            self.data = df["Close"].values.astype(np.float64)
            self.symbol = ticker.upper()

            print(f"✅ Downloaded {len(self.data)} data points for {self.symbol}")
            return self.data

        except Exception as e:
            print(f"❌ Error downloading {ticker}: {e}")
            raise e

    def from_csv(self, file_path):
        """Load data from CSV file and convert to numpy array"""
        try:
            print(f"📁 Loading data from: {file_path}")
            df = pd.read_csv(file_path)

            if df.empty:
                raise ValueError("CSV file is empty")

            # Find price column (case insensitive)
            price_columns = ["Close", "close", "Price", "price", "Adj Close", "adj close", "Close Price"]
            found_column = None

            for col in price_columns:
                if col in df.columns:
                    found_column = col
                    self.data = df[col].values.astype(np.float64)
                    break

            if found_column is None:
                available_cols = ", ".join(df.columns)
                raise ValueError(f"No price column found! Available columns: {available_cols}")

            self.symbol = file_path.split("/")[-1].split(".")[0]
            print(f"✅ Loaded {len(self.data)} data points from {file_path}")
            return self.data

        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            raise e

    def get_numpy_array(self):
        """Return the numpy array with validation"""
        if self.data is None:
            raise ValueError("No data loaded! Please load data first.")
        return self.data

    def get_data_info(self):
        """Get information about loaded data"""
        if self.data is None:
            return "No data loaded"

        return {
            'symbol': self.symbol,
            'data_points': len(self.data),
            'shape': self.data.shape,
            'data_type': str(self.data.dtype),
            'first_value': self.data[0] if len(self.data) > 0 else None,
            'last_value': self.data[-1] if len(self.data) > 0 else None
        }