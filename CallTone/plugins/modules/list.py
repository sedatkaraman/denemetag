# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

import os

from pyrogram import Client, filters
from pyrogram.types import Message

from Config import COMMAND, admins

from ..languages import get_str, lan
from ..modules.helpers import admin, clean_mode, reload


@Client.on_message(filters.command(commands=["liste", "list"], prefixes=COMMAND))
@admin
async def liste(c: Client, m: Message):
    ment = m.from_user.mention  # mention
    chat = m.chat.id  # chat id
    lang = await get_str(chat)  # language
    LAN = lan(lang)  # language
    if m.chat.type == "private":  # if private
        return  # return
    await reload(c, m)  # reload
    if m.from_user.id not in admins[m.chat.id]:  # if user not admin
        # send message
        a = await c.send_message(chat, LAN.U_NOT_ADMIN.format(ment))
        await clean_mode(a, m)
        return  # return
    # send message
    s = await c.send_message(chat, LAN.WAIT_FOR_LIST.format(ment))
    total = 0
    deleted = 0
    bots = 0
    async for user in c.iter_chat_members(chat):  # for user in chat
        if user.user.is_deleted:  # if user is deleted
            deleted += 1  # add deleted
        elif user.user.is_bot:  # if user is bot
            bots += 1  # add bot
        else:  # if user is not bot and not deleted
            total += 1  # add user
            with open("CallTone.txt", "a") as f:  # open file
                # write user id and name
                f.write(f"{user.user.id}|{user.user.first_name}\n")
    sohbet = await c.get_chat(chat)  # get chat
    await s.delete()  # delete message
    await m.delete()  # delete message
    await c.send_document(  # send document
        chat_id=chat,  # chat id
        document="CallTone.txt",  # file
        thumb="CallTone.jpg",  # file
        caption=LAN.CAPTION_CALLTONE_TXT.format(
            sohbet.title, total, deleted, bots
        ),  # caption
    )  # send document
    os.remove("CallTone.txt")  # remove file
