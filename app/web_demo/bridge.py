import time
from pathlib import Path
import os

def notify_dashboard(file_path: str):
    """
    ثبت آخرین فایل جدید در فایل مرکزی برای اطلاع دادن به Streamlit.
    """
    base_dir = Path(__file__).resolve().parent  # مسیر مطلق پوشه web_demo
    marker_file = base_dir / "latest_scrape.txt"
    with open(marker_file, "w", encoding="utf-8") as f:
        f.write(os.path.abspath(file_path))
    print(f"🔁 Dashboard notified with new data file: {file_path}")
