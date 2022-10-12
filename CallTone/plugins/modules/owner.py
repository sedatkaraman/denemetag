# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================


import asyncio
import os
import shutil
import traceback

import psutil
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid, UserIsBlocked, UserIsBot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Config import BOT_USERNAME, GROUP_SUPPORT, LOG_CHANNEL, OWNER_ID, calisan

from ..languages import get_str, lan
from ..modules.databases.mongo.database import db, dbsud
from ..modules.databases.mongo.dbtools import main_broadcast_handler
from .helpers import command, extract_user, humanbytes


@Client.on_message(
    command(["allsudo", "listsudo", "sudolist", "sudolistesi", "sudoliste"])
)
async def aall_sudo(bot: Client, msg: Message):
    sudos = await dbsud.get_all_sudos()
    text = ""
    async for user in sudos:
        # print(user, user['id'])
        try:
            usr = await bot.get_users(user["id"])
        except FloodWait as e:
            await asyncio.sleep(e.x)
            usr = await bot.get_users(user["id"])
        except PeerIdInvalid:
            await dbsud.delete_sudos(usr.id)
        except UserIsBlocked:
            await dbsud.delete_sudos(usr.id)
        except UserIsBot:
            await dbsud.delete_sudos(usr.id)
        if usr.first_name is None:
            await dbsud.delete_sudos(usr.id)
            continue
        text += f"**[{usr.first_name}](tg://user?id={usr.id})** [ `{usr.id}` ]\n"
    await bot.send_message(
        msg.chat.id,
        text=text,
    )


@Client.on_message(command("addsudo"))
async def add_sudo(bot: Client, msg: Message):
    if msg.from_user.id == OWNER_ID:
        if len(msg.command) >= 2 or msg.reply_to_message:
            user_id, user_first_name = extract_user(msg)
            try:
                user = await bot.get_users(user_id)
            except BaseException:
                await bot.send_message(msg.chat.id, "Kullanıcı bulunamadı.")
                return
            if await dbsud.is_sudo_exist(user.id):
                await bot.send_message(
                    msg.chat.id,
                    f"Bu kullanıcı [ [{user.first_name}](tg://user?id={user.id}) ] zaten sudo'ya eklenmiş.",
                )
            else:
                await dbsud.add_sudo(user.id)
                await bot.send_message(
                    msg.chat.id,
                    f"[{user.first_name}](tg://user?id={user.id})  sudo olarak eklendi.",
                )
        else:
            return await bot.send_message(
                msg.chat.id,
                "Kullanım: /addsudo [id/kullanıcı adı/mention/birinin mesajını yanıtlayarak]",
            )
    else:
        return await bot.send_message(
            msg.chat.id, "Bu komutu sadece sahibim kullanabilir."
        )


@Client.on_message(command("delsudo"))
async def delf_sudo(bot: Client, msg: Message):
    if msg.from_user.id == OWNER_ID:
        if len(msg.command) >= 2 or msg.reply_to_message:
            user_id, user_first_name = extract_user(msg)
            try:
                user = await bot.get_users(user_id)
            except BaseException:
                await bot.send_message(msg.chat.id, "Kullanıcı bulunamadı.")
                return
            if await dbsud.is_sudo_exist(user.id) is None:
                await bot.send_message(
                    msg.chat.id,
                    f"Bu kullanıcı [ [{user_first_name}](tg://user?id={user.id}) ] zaten sudo'ya eklenmemiş.",
                )
            else:
                await dbsud.delete_sudos(user.id)
                await bot.send_message(
                    msg.chat.id,
                    f"[{user_first_name}](tg://user?id={user.id})  sudo olarak silindi.",
                )
        else:
            return await bot.send_message(
                msg.chat.id, "Kullanım: /delsudo [id/kullanıcı adı/mention]"
            )
    else:
        return await bot.send_message(
            msg.chat.id, "Bu komutu sadece sahibim kullanabilir."
        )


@Client.on_message(command("stats"))
async def botstats(bot: Client, message: Message):
    if await dbsud.is_sudo_exist(message.from_user.id) is False:
        # await bot.send_message(message.chat.id, "Bu komutu sadece sudo
        # kullanabilir.")
        return
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    lol = await bot.send_message(
        message.chat.id, LAN.WAIT_FOR_STATS.format(message.from_user.mention)
    )
    all_users = await db.get_all_users()
    groups = 0
    pms = 0
    async for user in all_users:
        if str(user["id"]).startswith("-"):
            groups += 1
        else:
            pms += 1
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    total_users = await db.total_users_count()
    await lol.edit(
        text=LAN.STATS.format(
            BOT_USERNAME,
            total_users,
            groups,
            pms,
            total,
            used,
            disk_usage,
            free,
            cpu_usage,
            ram_usage,
            len(calisan),
        ),
        parse_mode="markdown",
    )


@Client.on_message(filters.command("broadcast") & filters.reply)
async def broadcast_handler_open(_, m: Message):
    if await dbsud.is_sudo_exist(m.from_user.id) is False:
        return
    await main_broadcast_handler(m, db)


@Client.on_message(filters.command("block"))
async def ban(c: Client, m: Message):
    if await dbsud.is_sudo_exist(m.from_user.id) is False:
        return
    chat_id = m.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
        if len(m.command) <= 1:
            ban_duration = 9999
            ban_reason = LAN.BAN_REASON_1.format(BOT_USERNAME, GROUP_SUPPORT)
        elif len(m.command) > 2:
            ban_duration = 9999
            ban_reason = " ".join(m.command[1:])
    else:
        if len(m.command) <= 1:
            return await m.reply(LAN.NOT_USER)
        elif len(m.command) == 2:
            user_id = int(m.command[1])
            ban_duration = 9999
            ban_reason = LAN.BAN_REASON_1.format(BOT_USERNAME, GROUP_SUPPORT)
        elif len(m.command) > 2:
            user_id = int(m.command[1])
            ban_duration = 9999
            ban_reason = " ".join(m.command[2:])

        if str(user_id).startswith("-"):
            ban_log_text = LAN.BAN_REASON_2.format(
                m.from_user.mention, user_id, ban_duration, ban_reason
            )
            try:
                await c.send_message(
                    user_id,
                    LAN.BAN_REASON_3.format(
                        ban_reason,
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    LAN.SUPPORT_GROUP,
                                    url=f"https://t.me/{GROUP_SUPPORT}",
                                )
                            ]
                        ]
                    ),
                )
                await c.leave_chat(user_id)
                ban_log_text += LAN.BAN_REASON_4
            except BaseException:
                traceback.print_exc()
                ban_log_text += LAN.BAN_REASON_5.format(traceback.format_exc())
        else:
            ban_log_text = LAN.BAN_REASON_6.format(
                m.from_user.mention, user_id, ban_duration, ban_reason
            )
            try:
                await c.send_message(
                    user_id,
                    LAN.BAN_REASON_7.format(ban_reason),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    LAN.SUPPORT_GROUP,
                                    url=f"https://t.me/{GROUP_SUPPORT}",
                                )
                            ]
                        ]
                    ),
                )
                await c.leave_chat(user_id)
                ban_log_text += LAN.BAN_REASON_8
            except BaseException:
                traceback.print_exc()
                ban_log_text += LAN.BAN_REASON_9.format(traceback.format_exc())
        await db.ban_user(user_id, ban_duration, ban_reason)
        await c.send_message(LOG_CHANNEL, ban_log_text)
        await m.reply_text(ban_log_text, quote=True)


@Client.on_message(filters.command("unblock"))
async def unban(c: Client, m: Message):
    if await dbsud.is_sudo_exist(m.from_user.id) is False:
        return
    chat_id = m.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if m.reply_to_message:
        user_id = m.reply_to_message.from_user.id
    else:
        if len(m.command) <= 1:
            return await m.reply(LAN.BAN_REASON_10.format(m.from_user.mention))
        else:
            user_id = int(m.command[1])
    unban_log_text = LAN.BAN_REASON_11.format(m.from_user.mention, user_id)
    if not str(user_id).startswith("-"):
        try:
            await c.send_message(user_id, LAN.BAN_REASON_12)
            unban_log_text += LAN.BAN_REASON_8
        except BaseException:
            traceback.print_exc()
            unban_log_text += LAN.BAN_REASON_9.format(traceback.format_exc())
    await db.remove_ban(user_id)
    await c.send_message(LOG_CHANNEL, unban_log_text)
    await m.reply_text(unban_log_text, quote=True)


@Client.on_message(filters.command("blocklist"))
async def _banned_usrs(_, m: Message):
    if await dbsud.is_sudo_exist(m.from_user.id) is False:
        return
    chat_id = m.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ""
    async for banned_user in all_banned_users:
        user_id = banned_user["id"]
        ban_duration = banned_user["ban_status"]["ban_duration"]
        banned_on = banned_user["ban_status"]["banned_on"]
        ban_reason = banned_user["ban_status"]["ban_reason"]
        banned_usr_count += 1
        text += LAN.BAN_REASON_13.format(user_id, ban_duration, banned_on, ban_reason)
    reply_text = LAN.BAN_REASON_14.format(banned_usr_count, text)
    if len(reply_text) > 4096:
        with open("banned-user-list.txt", "w") as f:
            f.write(reply_text)
        await m.reply_document("banned-user-list.txt", True)
        os.remove("banned-user-list.txt")
        return
    await m.reply_text(reply_text, True)
