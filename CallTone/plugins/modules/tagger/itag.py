# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from random import choice

from pyrogram import Client
from pyrogram.types import Message

from ...languages import get_str, lan
from ..helpers import admin, command, emojiler, extract_user, reload


@Client.on_message(command(["itag"]))
@admin
async def itag(client: Client, message: Message):
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await reload(client, message)
    if message.chat.type == "private":
        return
    try:
        await message.delete()
    except BaseException:
        pass
    if message.reply_to_message:
        if message.reply_to_message.from_user.id == message.chat.id:
            return await message.reply(LAN.CANT_TAG_ANONIM)
        else:
            user_id = message.reply_to_message.from_user.id
    else:
        user_id, _ = extract_user(message)
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await message.reply(LAN.NO_USER)
        await client.send_message(
            chat_id, f"[{choice(emojiler)}](tg://user?id={user.id})"
        )
