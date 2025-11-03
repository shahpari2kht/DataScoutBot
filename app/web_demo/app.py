# ===============================================
# 📊 DataScoutBot Dashboard (Streamlit)
# طراحی و توسعه: shahpari2kht
# ===============================================

import streamlit as st
import pandas as pd
import os
import time
import threading
from pathlib import Path


# ===================== تنظیمات صفحه =====================
st.set_page_config(page_title="📊 DataScout Dashboard", page_icon="📈")


# ===================== مشخصات مسیرها =====================
BASE_DIR = Path(__file__).resolve().parent
SIGNAL_FILE = BASE_DIR / "latest_scrape.txt"


# ===================== مانیتورینگ Auto‑Refresh =====================
def monitor_file():
    """Watch for file changes and auto‑refresh the Streamlit app."""
    last_mod = None
    while True:
        try:
            if SIGNAL_FILE.exists():
                mod_time = os.path.getmtime(SIGNAL_FILE)
                if last_mod != mod_time:
                    last_mod = mod_time
                    time.sleep(1)  # صبر کوتاه برای اینکه فایل کامل نوشته شود
                    try:
                        st.rerun()  # ورژن جدید Streamlit
                    except Exception:
                        st.experimental_rerun()  # fallback برای نسخه‌های قدیمی
        except Exception:
            pass
        time.sleep(2)


# اجرای Thread مانیتورینگ فقط یک بار
if "file_watcher" not in st.session_state:
    watcher_thread = threading.Thread(target=monitor_file, daemon=True)
    watcher_thread.start()
    st.session_state["file_watcher"] = True


# ===================== سرآیند داشبورد =====================
st.title("📊 DataScout Dashboard")
st.write("🤖 داده‌ها بر اساس آخرین اسکرپ از سایت به‌روزرسانی می‌شوند.")


# ===================== بررسی وجود فایل =====================
if not SIGNAL_FILE.exists():
    st.warning("هنوز داده‌ای جمع‌آوری نشده — دستور /scrape را در تلگرام ارسال کن.")
    st.stop()

csv_path = SIGNAL_FILE.read_text().strip()
if not csv_path or not os.path.exists(csv_path):
    st.error("فایل داده‌ی CSV فعلی پیدا نشد.")
    st.stop()


# ===================== بارگذاری داده =====================
df = pd.read_csv(csv_path)

if df.empty:
    st.warning("داده‌ای در فایل یافت نشد.")
    st.stop()

st.success(f"✅ داده‌ها از فایل: `{os.path.basename(csv_path)}` بارگذاری شدند.")


# ===================== نمایش داده و نمودار =====================
tab1, tab2 = st.tabs(["📄 جدول داده‌ها", "📈 نمودار قیمت‌ها"])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    # اطمینان از وجود ستون قیمت
    price_col = None
    for c in df.columns:
        if "Price" in c:
            price_col = c
            break

    if price_col:
        df_sorted = df.sort_values(by=price_col)
        st.line_chart(df_sorted[price_col], y_label="Price (£)", color="#4E79A7")
    else:
        st.warning("ستون قیمت در داده‌ها پیدا نشد.")


# ===================== بخش پایانی =====================
st.caption("طراحی و توسعه: **shahpari2kht** | 2025 ©")
