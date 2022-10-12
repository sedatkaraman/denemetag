# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

import os

from PIL import Image
from pyrogram import Client
from pyrogram.types import Message

from ...languages import get_str, lan
from ..helpers import admin, command, extract_user, reload


@Client.on_message(command(["stag"]))
@admin
async def stag(client: Client, message: Message):
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await reload(client, message)
    if message.chat.type == "private":
        return
    try:
        await message.delete()
    except Exception:
        pass
    if not message.reply_to_message:
        return await message.reply(LAN.STIC_NEED)
    else:
        if (
            message.reply_to_message.sticker
            or message.reply_to_message.document
            or message.reply_to_message.photo
        ):
            if len(message.command) <= 1:
                return await message.reply(LAN.NOT_USER)
            else:
                if message.reply_to_message.sticker:
                    file_name = message.reply_to_message.sticker.file_name
                    animation = message.reply_to_message.sticker.is_animated
                    video = message.reply_to_message.sticker.is_video
                    if file_name.endswith(".webp"):
                        file = await message.reply_to_message.download(
                            file_name="CallTone.webp"
                        )
                    elif animation:
                        file = await message.reply_to_message.download(
                            file_name="CallTone.tgs"
                        )
                    elif video:
                        return await message.reply(LAN.VIDEO_STIC)
                    user_id, _ = extract_user(message)
                    try:
                        user = await client.get_users(user_id)
                    except Exception:
                        return await message.reply(LAN.NO_USER)
                    await client.send_document(
                        chat_id=chat_id,
                        document=file,
                        # Idea Copyriht (C) 2022 @G4rip - < https://t.me/G4rip
                        # > - All Rights Reserved
                        caption=f"[ㅤㅤㅤㅤㅤㅤㅤㅤ](tg://user?id={user.id})",
                    )
                elif (
                    message.reply_to_message.document or message.reply_to_message.photo
                ):
                    final = "calltone.webp"
                    path_s = await message.reply_to_message.download()
                    im = Image.open(path_s)
                    im.save(final, "WEBP")
                    user_id, _ = extract_user(message)
                    try:
                        user = await client.get_users(user_id)
                    except Exception:
                        return await message.reply(LAN.NO_USER)
                    await client.send_document(
                        chat_id=chat_id,
                        document=final,
                        # Idea Copyriht (C) 2022 @G4rip - < https://t.me/G4rip
                        # > - All Rights Reserved
                        caption=f"[ㅤㅤㅤㅤㅤㅤㅤ](tg://user?id={user.id})",
                    )
                    os.remove(final)
                else:
                    return await message.reply(LAN.STIC_NEED)

        else:
            return await message.reply(LAN.STIC_NEED)
