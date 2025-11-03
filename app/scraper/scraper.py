import asyncio
import aiohttp
import pandas as pd
import os
from bs4 import BeautifulSoup
from datetime import datetime


async def fetch_page(session, url):
    """دریافت محتوای HTML از صفحه با aiohttp"""
    async with session.get(url) as response:
        return await response.text()


async def scrape_books():
    """اسکرپ از سایت books.toscrape.com و ذخیره در CSV"""
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    async with aiohttp.ClientSession() as session:
        # تعدادی صفحه محدود (مثلاً ۳ صفحه) برای تست
        for page in range(1, 4):
            url = base_url.format(page)
            html = await fetch_page(session, url)
            soup = BeautifulSoup(html, "html.parser")

            books = soup.find_all("article", class_="product_pod")
            for book in books:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text.strip()
                availability = book.find("p", class_="instock availability").text.strip()
                rating = book.p["class"][1] if len(book.p["class"]) > 1 else "Not Rated"

                all_books.append({
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "rating": rating,
                    "source": url
                })

    # اطمینان از وجود پوشه data
    os.makedirs("data", exist_ok=True)

    # ایجاد DataFrame و حذف داده‌های تکراری
    df = pd.DataFrame(all_books)
    df = df.drop_duplicates()

    # ساخت مسیر فایل خروجی با برچسب زمان
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/books_{timestamp}.csv"

    # ذخیره فایل
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"✅ Data scraped and saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    asyncio.run(scrape_books())
