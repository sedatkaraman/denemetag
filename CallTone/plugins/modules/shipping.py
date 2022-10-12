# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================


import random

from pyrogram import Client, filters
from pyrogram.types import Message

from ..languages import get_str, lan
from .helpers import admin, clean_mode, command

kalpler = "🧡 💛 💚 💙 💜 🤎 🖤 🤍 💔 💔 💔 ❣ 💕 💞 💓 💓 💗 💖 💘 💝".split()


@Client.on_message(command("ship") & ~filters.private)
@admin
async def ship(client: Client, message: Message):
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    mentions = ""
    new_users_dict = {}
    async for mentions in client.iter_chat_members(message.chat.id):
        if mentions["user"]["is_bot"]:
            pass
        if mentions["user"]["is_deleted"]:
            pass
        else:
            new_users_dict.update(
                {
                    mentions["user"]["id"]: dict(
                        first_name=mentions["user"]["first_name"],
                        status=mentions["status"],
                        username=mentions["user"]["username"],
                    )
                }
            )
    if len(new_users_dict.keys()) < 2:
        return
    m1_id = random.choice(list(new_users_dict.keys()))
    m2_id = random.choice(list(new_users_dict.keys()))
    oran = random.randint(1, 100)
    kalp = random.choice(kalpler)
    while m1_id == m2_id:
        m1_id = random.choice(list(new_users_dict.keys()))
    if new_users_dict[m1_id]["status"] == "creator":
        mention1 = f"👑 [{new_users_dict[m1_id]['first_name']}](tg://user?id={m1_id}) 👑"
    elif new_users_dict[m2_id]["status"] == "creator":
        mention2 = f"👑 [{new_users_dict[m2_id]['first_name']}](tg://user?id={m2_id}) 👑"
    else:
        mention1 = f"[{new_users_dict[m1_id]['first_name']}](tg://user?id={m1_id})"
        mention2 = f"[{new_users_dict[m2_id]['first_name']}](tg://user?id={m2_id})"

    if (
        new_users_dict[m1_id]["status"] == "creator"
        or new_users_dict[m1_id]["status"] == "creator"
    ):
        ship_text = LAN.SHIP_ADMIN
        oran = 100
        durum = 1
    elif oran <= 20:
        ship_text = LAN.SHIP_TEXT_1
        durum = 2
    elif oran <= 40:
        ship_text = LAN.SHIP_TEXT_2
        durum = 3
    elif oran <= 60:
        ship_text = LAN.SHIP_TEXT_3
        durum = 4
    elif oran <= 80:
        ship_text = LAN.SHIP_TEXT_4
        durum = 5
    else:
        ship_text = LAN.SHIP_TEXT_5
        durum = 6

    if durum == 1:
        h = ship_text.format(mention1, mention2)
    elif durum == 2:
        h = ship_text.format(mention1, mention2, oran)
    elif durum == 3:
        h = ship_text.format(mention1, kalp, mention2, oran)
    elif durum == 4:
        h = ship_text.format(mention1, kalp, mention2, oran)
    elif durum == 5:
        h = ship_text.format(mention1, kalp, mention2, oran)
    elif durum == 6:
        h = ship_text.format(mention1, kalp, mention2, oran)
    await client.send_message(message.chat.id, h)
    await clean_mode(message)

    new_users_dict.clear()
