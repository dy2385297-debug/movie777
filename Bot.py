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
        "🎬 *Auto-Download Bot is Online!*\n\n"
        "Send me any movie link, and I will generate your secure blog download link!",
        parse_mode="Markdown"
    )

@dp.message()
async def process_movie_links(message: Message):
    text = message.text
    if text and text.startswith(("http://", "https://")):
        try:
            import urllib.parse
            # बाहिरबाट आएको असली लिङ्कलाई इन्कोड गर्ने
            encoded_url = urllib.parse.quote(text, safe='')

            # तपाईंको ब्लगको डोमेन र डाउनलोड पेजको लिङ्क बनाउने
            clean_link = f"https://movize7cr.blogspot.com/p/download.html?url={encoded_url}"
        except Exception:
            clean_link = text

        response_msg = (
            f"🔗 *Secure Blog Download Link Generated!*\n\n"
            f"📌 *Copy this link:*\n`{clean_link}`\n\n"
            f"👉 यो लिङ्क आफ्नो ब्लग वा पोस्टमा राख्नुहोस्!"
        )
        await message.answer(response_msg, parse_mode="Markdown")
    else:
        await message.answer("⚠️ कृपया http:// वा https:// बाट सुरु हुने सही मुभी लिङ्क पठाउनुहोस् है दाइ!")

async def main():
    bot = Bot(token=TOKEN)
    logging.info("Starting Telegram Bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
