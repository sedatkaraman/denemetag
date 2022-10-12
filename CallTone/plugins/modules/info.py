# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from ..languages import get_str, lan
from .helpers import admin, command, extract_user, reload


@Client.on_message(command("id"))
async def id(bot: Client, message: Message):
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return await message.reply(LAN.NOT_INFO_DELETED)
        else:
            user = message.reply_to_message.from_user.id
            usr = await bot.get_users(user)
            await message.reply(LAN.IS_USER_ID.format(usr.first_name, user))
    else:
        if len(message.command) <= 1:

            await bot.send_message(
                message.chat.id,
                LAN.IS_GROUP_ID.format(message.chat.title, message.chat.id),
            )
        else:
            user_id, _ = extract_user(message)
            try:
                user = await bot.get_users(user_id)
            except Exception:
                return await message.reply(LAN.NO_USER)
            await bot.send_message(
                message.chat.id, LAN.IS_USER_ID.format(user.first_name, user.id)
            )


@Client.on_message(command("info"))
@admin
async def info(bot: Client, message: Message):
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await reload(bot, message)
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return await message.reply(LAN.NOT_INFO_DELETED)
        else:
            user_id = message.reply_to_message.from_user.id
            try:
                user = await bot.get_users(user_id)
            except Exception:
                return await message.reply(LAN.NO_USER)
            userid = user.id
            username = user.username
            first_name = user.first_name
            dc_id = user.dc_id
            infos = LAN.INFOS.format(
                first_name, userid, ("@" + username) if username else LAN.YOK, dc_id
            )
            await bot.send_message(
                message.chat.id,
                text=f"{infos}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                LAN.USER, url=f"tg://openmessage?user_id={userid}"
                            )
                        ]
                    ]
                ),
                disable_web_page_preview=True,
            )
    else:
        if not message.reply_to_message and len(message.command) <= 1:
            return await message.reply(LAN.NOT_USER_INFO)
        else:
            user_id, _ = extract_user(message)
            try:
                user = await bot.get_users(user_id)
            except Exception:
                return await message.reply(LAN.NO_USER)
            userid = user.id
            username = user.username
            first_name = user.first_name
            dc_id = user.dc_id
            infos = LAN.INFOS.format(
                first_name, userid, ("@" + username) if username else LAN.YOK, dc_id
            )
            await bot.send_message(
                message.chat.id,
                text=f"{infos}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                LAN.USER, url=f"tg://openmessage?user_id={userid}"
                            )
                        ]
                    ]
                ),
                disable_web_page_preview=True,
            )
