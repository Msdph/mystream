import asyncio
from cgitb import text
from pyrogram import Client , filters
from pyrogram.types import Message , messages_and_media
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton , ReplyKeyboardMarkup , CallbackQuery
from typing import Any, Optional

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import quote_plus

api_id = 2669389
api_hash = "59f112100d19186dc03cd93fb7f2904a"
bot_token = "1026408788:AAHVhIKmeboveGZ6x8peMnv0Ts2FvR38b_0"

bot = Client(
    "withrap",
    api_id=api_id, 
    api_hash=api_hash,
    bot_token=bot_token
)
START_BUTTONS = InlineKeyboardMarkup(

    [[
    InlineKeyboardButton('💡Help💡', callback_data='help'),
    InlineKeyboardButton('🏷About🏷', callback_data='about'),
    ],[    
    InlineKeyboardButton('🔐Close🔐', callback_data='close')
    ]]
 )
two_BUTTONS = InlineKeyboardMarkup(

    [
        [
            InlineKeyboardButton('💡Help💡', callback_data='help')
        ],
        [    
            InlineKeyboardButton('🔐Close🔐', callback_data='close')
        ]
    ]
)
help_tetx = '''
ارسال عکس  : /photo 
ارسال اهنگ : /audio
راهنما : /help
'''
@bot.on_message(filters.command("start"))
async def start_command(bot, message):
    await bot.send_message(message.chat.id , "سلام به ربات من خوش اومدی ",reply_markup=START_BUTTONS)

@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await message.reply_text(help_tetx,reply_markup=START_BUTTONS)

@bot.on_message(filters.command("photo"))
async def photo_command(bot, message):
    await bot.send_photo(message.chat.id , "https://img.freepik.com/free-vector/cute-white-cat-cartoon-vector-illustration_42750-808.jpg?w=740")

@bot.on_message(filters.command("audio"))
async def audio_command(bot, message):
    await bot.send_audio(message.chat.id , "CQACAgQAAxkBAAMwYqRcGlQyS2Df1-Xv2D5dO9UAAa4TAALBIgACMHk4UETTPPye8HEeHgQ")

#@bot.on_message(filters.text)
#async def echobot(client, message):
#    await message.reply_text(message.text)


@bot.on_callback_query()
async def callbackuery(client,CallbackQuery):
    if CallbackQuery.data == "about" :

        await CallbackQuery.edit_message_text(
            "این یک ربات تستی از کتابخانه پایروگرام میباشد ",
            reply_markup=two_BUTTONS
        )
    elif CallbackQuery.data == "help" :
        await CallbackQuery.edit_message_text(
            help_tetx,
            reply_markup=two_BUTTONS
        )
    else :
        async def dels(bot, message):
            await message.delete()

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def get_media_from_message(message: "Message") -> Any:
    media_types = (
        "audio",
        "document",
        "photo",
        "sticker",
        "animation",
        "video",
        "voice",
        "video_note",
    )
    for attr in media_types:
        media = getattr(message, attr, None)
        if media:
            return media



def get_hash(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    return getattr(media, "file_unique_id", "")[:6]
def get_name(media_msg: Message) -> str:
    media = get_media_from_message(media_msg)
    file_name=getattr(media, "file_name", "")
    return file_name if file_name else ""
def get_media_file_size(m):
    media = get_media_from_message(m)
    return getattr(media, "file_size", 0)
ch = int(-1001627340552)
@bot.on_message((filters.document | filters.video | filters.audio))
async def private_receive_handler(c: Client, m: Message):
    log_msg = await m.forward(chat_id=ch)
    URL = "http://dl2-kenzo.herokuapp.com"
    online_link = f"{URL}/{str(log_msg.message_id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
    msg_text ="""{}\n{}\n{}"""
    await log_msg.reply_text(msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link), disable_web_page_preview=True, parse_mode="Markdown", quote=True)
    await m.reply_text(
        text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), online_link),
        parse_mode="HTML", 
        quote=True,
        disable_web_page_preview=True
    )
    

print('im alive')
bot.run()
