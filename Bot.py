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
        "🎬 *Movie Safe Link Bot is Online!*\n\n"
        "Send me any movie direct download link, and I will generate a secure clean link for your blog!",
        parse_mode="Markdown"
    )

@dp.message()
async def process_movie_links(message: Message):
    text = message.text
    if text and text.startswith(("http://", "https://")):
        try:
            import urllib.parse
            # बाहिरबाट आएको ठूलो/जोखिमपूर्ण लिङ्कलाई पूर्ण रूपमा इन्कोड गर्ने
            encoded_url = urllib.parse.quote(text, safe='')

            # ब्लगलाई अनपब्लिश हुनबाट बचाउन र सुरक्षित राख्न क्लिन रिडाइरेक्ट लिङ्क बनाउने
            # (तपाईंले यहाँ चाहेको ट्र्याकिङ वा रिडाइरेक्ट स्ट्रक्चर प्रयोग गर्न सक्नुहुन्छ)
            clean_link = f"https://my-redirect-safe.blogspot.com/p/download.html?url={encoded_url}"
        except Exception:
            clean_link = text

        response_msg = (
            f"🛡️ *Safe Download Link Generated!*\n\n"
            f"📌 *Copy this link for your blog:*\n`{clean_link}`\n\n"
            f"👉 यो लिङ्कले ब्लगलाई अनपब्लिश हुनबाट बचाउँछ र युजरले क्लिक गर्दा सजिलै डाउनलोड हुन्छ!"
        )
        await message.answer(response_msg, parse_mode="Markdown")
    else:
        await message.answer("⚠️ कृपया http:// वा https:// बाट सुरु हुने सही लिङ्क पठाउनुहोस् है दाइ!")

async def main():
    bot = Bot(token=TOKEN)
    logging.info("Starting Telegram Bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Start background web server for Render port check
    server_thread = threading.Thread(target=start_web_server, daemon=True)
    server_thread.start()

    # Start Telegram bot main process
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
