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
        "🎬 *Movie Bot is Online!*\n\n"
        "Send me any movie or video link, and I will generate a secured link for you!",
        parse_mode="Markdown"
    )

@dp.message()
async def process_movie_links(message: Message):
    text = message.text
    if text and text.startswith(("http://", "https://")):
        clean_link = text
        
        response_msg = (
            f"✅ *Link Processed Successfully!*\n\n"
            f"🔗 *Generated Link:*\n`{clean_link}`"
        )
        await message.answer(response_msg, parse_mode="Markdown")
    else:
        await message.answer("⚠️ Please send a valid movie link starting with http:// or https://")

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

