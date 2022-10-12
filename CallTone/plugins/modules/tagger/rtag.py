# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from asyncio import sleep
from random import choice

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Config import ADMIN, BOT_USERNAME, COMMAND, admins, calisan, reasons  # noqa

from ...languages import get_str, lan
from ...modules.helpers import count, reload
from ..databases.mongo.database import get_count, get_duration
from ..helpers import admin, clean_mode, emojiler, renkler


@Client.on_message(filters.command(commands="rtag", prefixes=COMMAND))
@admin
async def rtag(client: Client, message: Message):
    global calisan
    global reasons
    global admins
    chat_id = message.chat.id
    user_id = message.from_user.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await reload(client, message)

    if message.chat.type == "private":
        return

    if message.from_user.id not in admins[message.chat.id]:
        not_admin = await message.reply_text(
            LAN.U_NOT_ADMIN.format(message.from_user.mention)
        )
        await clean_mode(not_admin, message)
        return

    if chat_id in calisan:
        c = await message.reply_text(
            LAN.ZATEN_CALISIYORUM.format(message.from_user.mention)
        )
        await clean_mode(c, message)
        return

    else:
        if message.reply_to_message:
            if message.reply_to_message.text:
                reason = message.reply_to_message.text
                tip = "1"
            else:
                reason = ""
                tip = "0"
        else:
            if len(message.command) <= 1:
                reason = ""
                tip = "0"
            else:
                reason = message.text.split(None, 1)[1]
                tip = "1"
        COUNT = await get_count(chat_id)
        reasons[chat_id] = reason
        m = await client.send_message(
            chat_id,
            LAN.ASK_RENK_TAG, #TODO HER TAGA ÖZEL DİL KEYİ
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            LAN.TEKLI, callback_data=f"rtag 1|{user_id}|{tip}"
                        ),
                        InlineKeyboardButton(
                            LAN.COKLU.format(COUNT),
                            callback_data=f"rtag {COUNT}|{user_id}|{tip}",
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "❌", callback_data=f"rtag 0|{user_id}|{tip}"
                        ),
                    ],
                ],
            ),
        )
        await sleep(15)
        if chat_id not in calisan:
            try:
                await m.edit(
                    LAN.ASK_ADMINS_TAG_TIMEOUT.format(
                        message.from_user.mention, "`/rtag`"
                    )
                )
            except Exception:
                return
            await clean_mode(m, message)
            return
        else:
            return


@Client.on_callback_query(filters.regex(pattern=r"rtag"))
async def rcommands(bot: Client, query: CallbackQuery):
    global admins
    global reasons
    global calisan
    q = query.data
    chat = int(query.message.chat.id)
    lang = await get_str(chat)
    LAN = lan(lang)
    DURATION = await get_duration(chat)
    typed_ = str(q).split()[1]
    sayi = int(typed_.split("|")[0])
    useer_id = typed_.split("|")[1]
    tip = typed_.split("|")[2]

    if sayi == 0:
        del reasons[chat]
        await query.message.edit_text(
            LAN.CALISMA_DURDUR.format(query.from_user.mention)
        )
        await sleep(DURATION)
        await query.message.delete()
        return

    if chat in calisan:
        await query.message.edit(
            LAN.ZATEN_CALISIYORUM.format(query.message.from_user.mention)
        )
        await clean_mode(query.message)
        return

    if tip == "1":
        reason = reasons[chat]
    elif tip == "0":
        reason = ""

    name = await bot.get_users(int(useer_id))
    if int(useer_id) == int(query.from_user.id):
        if chat not in calisan:
            calisan.append(chat)
        await query.message.delete()
        bots, deleted, toplam = await count(bot, chat)
        etiketlenecek = toplam - (bots + deleted)
        started = await bot.send_message(
            chat,
            LAN.TAG_START.format(
                query.from_user.mention, "Renklerle Tag", etiketlenecek, DURATION
            ),
        )
        usrnum = 0
        usrtxt = ""
        etiketlenen = 0
        async for usr in bot.iter_chat_members(chat):
            if usr["user"]["is_bot"]:
                pass
            elif usr["user"]["is_deleted"]:
                pass
            else:
                emoji = choice(renkler)
                usrnum += 1
                usrtxt += f"[{emoji}](tg://user?id={usr.user.id}) ,"
                etiketlenen += 1

                if usrnum == int(sayi):
                    if sayi == 1:
                        text = f"📢 **{reason}** {usrtxt}"
                    else:
                        text = f"📢 **{reason}**\n\n{usrtxt}"
                    await bot.send_message(chat, text=text)
                    await sleep(DURATION)
                    usrnum = 0
                    usrtxt = ""

                if etiketlenen == etiketlenecek:
                    calisan.remove(chat)
                    del reasons[chat]
                    stoped = await bot.send_message(
                        chat,
                        LAN.TAG_STOPED.format(
                            "Renklerle Tag",
                            etiketlenen,
                            DURATION,
                            query.from_user.mention,
                        ),
                    )
                    await clean_mode(started, stoped)
                    return

                if chat not in calisan:
                    del reasons[chat]
                    stopped = await bot.send_message(
                        chat,
                        LAN.TAG_STOPED.format(
                            "Renklerle Tag",
                            etiketlenen,
                            DURATION,
                            query.from_user.mention,
                        ),
                    )
                    await clean_mode(started, stopped)
                    return
    else:
        return await bot.answer_callback_query(
            callback_query_id=query.id,
            text=LAN.rtag_DONT_U.format(name.first_name),
            show_alert=True,
        )
