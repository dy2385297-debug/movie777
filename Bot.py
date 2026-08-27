import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8918391629:AAG53o_5RoHTvvGjxwQWuvIthL2mIyfywGI"

dp = Dispatcher()
# Movie links storage database
movie_database = {}

@dp.message(Command("start"))
async def start_cmd(message: types.Message, command: CommandObject):
    args = command.args 
    
    if args and args.isdigit():
        movie_id = int(args)
        if movie_id in movie_database:
            original_movie_link = movie_database[movie_id]
            
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📥 Download Movie File Now", url=original_movie_link)] 
                ]
            )
            await message.answer(
                "🎬 **NepalFlix Secure Download System**\n\nYour movie is ready! Click the button below to download:",
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            await message.answer("⚠️ This movie link has expired or is invalid. Please generate a new one.")
    else:
        await message.answer("NepalFlix Bot Active! Please send a movie link.")

@dp.message()
async def handle_link(message: types.Message):
    incoming_text = message.text
    if incoming_text and incoming_text.startswith("http"):
        msg_id = message.message_id
        movie_database[msg_id] = incoming_text
        
        new_link = f"https://t.me/NepalFlixUploaderBot?start={msg_id}"
        
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📥 Get Download Link via Bot", url=new_link)]
            ]
        )
        
        response_text = (
            f"✅ **Movie Link Secured & Generated!**\n\n"
            f"🔗 **Shareable Link (For your Website):**\n`{new_link}`\n\n"
            f"👇 Click below to test the download:"
        )
        await message.answer(response_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await message.answer("Please send a valid movie link starting with http.")

async def main():
    bot = Bot(token=TOKEN)
    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())