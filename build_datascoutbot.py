import os, textwrap, json

BASE = os.getcwd()

# ساختار پوشه‌ها
dirs = [
    "app/bot", "app/scraper", "app/web_demo", "app/database",
    "data/samples", "data/results"
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# فایل requirements.txt
reqs = """aiogram>=3.2.0
requests
beautifulsoup4
streamlit
sqlite3-binary
python-dotenv
pandas
"""
open("requirements.txt", "w").write(reqs)

# نمونه .env
open(".env.example", "w").write("BOT_TOKEN=your_telegram_bot_token_here\n")

# فایل docker-compose.yml
compose = textwrap.dedent("""
version: "3.9"
services:
  bot:
    build: .
    command: python app/bot/main.py
    volumes:
      - .:/app
  web:
    build: .
    command: streamlit run app/web_demo/app.py
    ports:
      - "8501:8501"
""")
open("docker-compose.yml", "w").write(compose)

# --- کد ربات تلگرام ---
bot_code = textwrap.dedent("""
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio, sqlite3, os
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer("سلام 👋\\nمن DataScoutBot هستم. با /search می‌تونی جست‌وجوی داده تستی انجام بدی.")

@dp.message(Command("search"))
async def search(msg: types.Message):
    await msg.answer("🔍 نتایج تستی: [Example Product A, Example Product B]")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
""")
open("app/bot/main.py", "w").write(bot_code)

# --- ماژول اسکرپر ---
scraper_code = textwrap.dedent("""
import requests, pandas as pd
from bs4 import BeautifulSoup

def scrape(keyword="book"):
    url = f"https://books.toscrape.com/catalogue/category/books_1/page-1.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    titles = [a.text.strip() for a in soup.select("h3 a")]
    df = pd.DataFrame({"title": titles})
    df.to_csv("data/results/sample.csv", index=False)
    print("✅ Scraping finished. Saved to data/results/sample.csv")

if __name__ == "__main__":
    scrape()
""")
open("app/scraper/run_scraper.py", "w").write(scraper_code)

# --- web_demo Streamlit ---
web_code = textwrap.dedent("""
import streamlit as st
import pandas as pd
from app.scraper.run_scraper import scrape

st.title("🧭 DataScoutBot Web Demo")
if st.button("Run Scraper"):
    scrape()
    st.success("Scraper run complete. Check data/results/sample.csv")
""")
open("app/web_demo/app.py", "w").write(web_code)

# --- README دوزبانه ---
readme = textwrap.dedent("""
# DataScoutBot

🔹 A professional demo project combining a Telegram bot, web scraper, and simple web dashboard.

---

## راهنمای فارسی

**DataScoutBot** ترکیبی از:
- ربات تلگرام (aiogram)
- ماژول اسکرپر (BeautifulSoup)
- دمو تحت‌وب (Streamlit)
- دیتابیس SQLite

📘 مراحل راه‌اندازی:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
python app/bot/main.py
طراحی و توسعه: shahpari2kht

“”")

open(“README.md”, “w”).write(readme)

print(“📦 DataScoutBot Project successfully generated at”, BASE)
