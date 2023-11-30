import threading

from flask import Flask, request
from pyrogram import Client, idle, filters
from os import getenv
from dotenv import load_dotenv
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from actions import get_live_games, get_standings, format_games
import json

load_dotenv()

api = Flask(__name__)

chat_ids_file = 'chat_ids.json'

# Load existing chat IDs from the file
try:
    with open(chat_ids_file, 'r') as file:
        interacted_chat_ids = set(json.load(file))
except FileNotFoundError:
    interacted_chat_ids = set()

@api.route("/")
def hello_world():
    return "Nice"


@api.route("/send_message", methods=["POST"])
def send_group_message():
    data = request.get_json()
    print(data)
    games = data.get("data")
    message = "Atualização de placar!"
    if not games:
        message += "Digite /jogos para ver resultados ao vivo"
    else:
        message += " " + str(format_games(games))
    try:
        for chat_id in interacted_chat_ids:
            print(chat_id, message)
            bot.send_message(chat_id, text=message)
        return "Message sent to the group!"
    except Exception as e:
        return f"Error sending message: {str(e)}"

bot = Client(
        'tester',
        api_id=getenv('bot_ID'),
        api_hash=getenv('API_HASH'),
        bot_token=getenv('BOT_TOKEN')
    )

@bot.on_message(filters.command('projeto'))
async def projeto(client, message):
    inline_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('URL 🔗', url='https://github.com/joaowinderfeldbussolotto/brasileirao-telegram-bot.git')
            ]
        ]
    )
    await message.reply('Projeto no gitHub', reply_markup=inline_markup)

@bot.on_message(filters.command("jogos"))
def jogos_command(client, message):
    message.reply_text(get_live_games())


@bot.on_message(filters.command("tabela"))
def tabela_command(client, message):
    message.reply_text(get_standings())


menu_markup = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Jogos Ao Vivo", callback_data="ver_jogos"),
            InlineKeyboardButton("Ver Tabela", callback_data="ver_tabela"),
        ]
    ]
)



@bot.on_message()
def start_command(client, message):
    chat_id = message.chat.id
    interacted_chat_ids.add(chat_id)
    with open(chat_ids_file, 'w') as file:
        json.dump(list(interacted_chat_ids), file)


    message.reply_text('Bem-vindo ao Bot do Brasileirão!\n'
                    'Digite **/start** para iniciar o bot! 🤖\n'
                    'Digite **/jogos** para ver os jogos ao vivo\n'
                    'Digite **/tabela** para ver a tabela do campeonato\n'
                    'Digite **/projeto** para ver o projeto no GitHub 💻\n'
                    'Digite qualquer outra coisa para ver o menu de opções\n'
                    'Escolha uma opção:', reply_markup=menu_markup)

@bot.on_callback_query()
def callback_query_handler(client, query):
    chat_id = query.message.chat.id

    if query.data == "ver_jogos":
        client.send_message(
            chat_id=chat_id,
            text=get_live_games()
        )
    elif query.data == "ver_tabela":
        client.send_message(
            chat_id=chat_id,
            text=get_standings()
        )        
    else:
        client.send_message(
            chat_id=chat_id,
            text="Opção não reconhecida. Escolha uma opção válida:",
            reply_markup=menu_markup,
        )


bot.start()
threading.Thread(target=api.run, daemon=True).start()
idle()
bot.stop()
