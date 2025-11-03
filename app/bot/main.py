import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

# مسیرهای داخلی پروژه
from app.scraper.scraper import scrape_books
from app.web_demo.bridge import notify_dashboard

# ===================== تنظیمات اولیه =====================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from dotenv import load_dotenv
load_dotenv()  # ✅ این خط فایل .env را لود می‌کند

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ متغیر BOT_TOKEN در فایل .env تنظیم نشده است.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ===================== دستور start =====================
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "سلام 👋\n"
        "من DataScoutBot هستم.\n"
        "برای جمع‌آوری اطلاعات از سایت نمونه از دستور /scrape استفاده کن."
    )

# ===================== دستور scrape =====================
@router.message(Command("scrape"))
async def cmd_scrape(message: Message):
    try:
        await message.answer("⏳ در حال جمع‌آوری داده‌ها... لطفاً چند لحظه صبر کنید.")
        # اجرای async اسکرپر
        csv_path = await scrape_books()
        # ارسال فایل به کاربر
        file = FSInputFile(csv_path)
        await message.answer_document(file, caption="✅ داده‌ها با موفقیت جمع‌آوری شدند.")
        # اطلاع به داشبورد
        await asyncio.to_thread(notify_dashboard, csv_path)
    except Exception as e:
        logger.error(f"❌ خطا در اجرای scrape: {e}")
        await message.answer(f"⚠️ خطا در جمع‌آوری داده‌ها:\n{e}")

# ===================== اجرای ربات =====================
async def main():
    logger.info("✅ DataScoutBot started polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
