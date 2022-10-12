# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from datetime import datetime

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..languages import get_str, lan
from .helpers import clean_mode, command


@Client.on_message(command("ping"))
async def pingy(client, message):

    start = datetime.now()
    hmm = await message.reply("`Pong!`")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await clean_mode(message)
    await hmm.edit(
        f"**█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄**",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"Ping!: {round(ms)}ms", callback_data="ping")],
            ],
        ),
    )


async def ping(bot, query):
    start = datetime.now()
    chat_id = query.message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await bot.answer_callback_query(
        callback_query_id=query.id, text=LAN.PING_CB_TEXT, show_alert=True
    )
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await query.edit_message_text(
        f"**█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Ping!: {round(ms)}ms", callback_data="ping")]]
        ),
    )
