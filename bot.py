import threading

from flask import Flask
from pyrogram import Client, idle
from os import getenv
from dotenv import load_dotenv
from pyrogram.types import Message

load_dotenv()

app = Flask(__name__)

bot = Client(
        'tester',
        api_id=getenv('bot_ID'),
        api_hash=getenv('API_HASH'),
        bot_token=getenv('BOT_TOKEN')
    )


@app.route("/")
def hello_world():
    return "Nice"

@bot.on_message()
async def messages(client, message: Message):
    print(message.chat.username, message.text)
    await message.reply(message.text)


bot.start()
threading.Thread(target=app.run, daemon=True).start()
idle()
bot.stop()