import os
import logging
import asyncio
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command

# --- 1. RENDER WEB SERVER (Flask Server for Port 10000) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running perfectly!", 200

def start_web_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Web server notice: {e}")

# --- 2. TELEGRAM MOVIE BOT (With Your Token) ---
TOKEN = "8918391629:AAG53o_5RoHTvvGjxwQWuvIthL2mIyfywGI"

dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🎬 *Direct Download Bot is Online!*\n\n"
        "Send me any movie link, and I will convert it into a 1-Click Direct Download link!",
        parse_mode="Markdown"
    )

@dp.message()
async def process_movie_links(message: Message):
    text = message.text
    if text and text.startswith(("http://", "https://")):
        # बाहिरबाट आएको लिङ्कलाई कतै नघुमाई सिधै डाउनलोड हुने बनाउने ट्रिक
        # यदि लिङ्कमा पहिल्यै ? वा & छ भने त्यसरी नै जोड्ने, नभए ?download=1 थप्ने
        separator = "&" if "?" in text else "?"
        direct_download_link = f"{text}{separator}download=1"

        response_msg = (
            f"⚡ *1-Click Direct Download Link Generated!*\n\n"
            f"📌 *Copy this link:*\n`{direct_download_link}`\n\n"
            f"👉 यो लिङ्कमा क्लिक गर्नेबित्तिकै युजरको मोबाइल वा ल्यापटपमा सिधै डाउनलोड सुरु हुन्छ!"
        )
        await message.answer(response_msg, parse_mode="Markdown")
    else:
        await message.answer("⚠️ कृपया http:// वा https:// बाट सुरु हुने सही लिङ्क पठाउनुहोस् है दाइ!")

async def main():
    bot = Bot(token=TOKEN)
    logging.info("Starting Telegram Bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
