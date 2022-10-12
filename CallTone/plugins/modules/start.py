# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Config import BOT_ID, BOT_NAME, BOT_USERNAME, GROUP_SUPPORT, OWNER_ID, admins

from ..languages import CallTone_AZ, CallTone_EN, CallTone_RU, CallTone_TR, get_str, lan
from ..languages.ALL import CHOICE_LANG, LANGAUGE
from ..modules.databases.mongo.database import lang_set
from .helpers import command, reload


@Client.on_message(command("start") & filters.private)
async def start(bot: Client, msg: Message):
    chat_id = msg.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if len(msg.command) == 1:
        await bot.send_message(
            msg.chat.id,
            text=LAN.STARTMSG.format(BOT_NAME),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(LAN.KOMUTLAR, callback_data="cb_commands"),
                    ],
                    [
                        InlineKeyboardButton(
                            LAN.GRUBAEKLE,
                            url=f"https://t.me/{BOT_USERNAME}?startgroup=a",
                        ),
                        InlineKeyboardButton(LAN.SAHIBIM, user_id=OWNER_ID),
                    ],
                    [InlineKeyboardButton(LANGAUGE, callback_data="cb_lang")],
                ],
            ),
        )
    elif len(msg.command) >= 2:
        query = msg.command[1]
        if query.startswith("help"):
            if msg.chat.type == "private":
                await bot.send_message(
                    chat_id=msg.chat.id,
                    text=LAN.HELPMSG.format(BOT_USERNAME),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    LAN.KOMUTLAR, callback_data="cb_commands"
                                ),
                                InlineKeyboardButton(
                                    LAN.YARDIM, url=f"https://t.me/{GROUP_SUPPORT}"
                                ),
                            ],
                        ],
                    ),
                    disable_web_page_preview=True,
                )


@Client.on_message(command("help"))
async def help(bot: Client, msg: Message):
    chat_id = msg.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if msg.chat.type == "private":
        await bot.send_message(
            chat_id=msg.chat.id,
            text=LAN.COMMANDS_TEXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            LAN.TAGGER_COMMANDS, callback_data="tag_commands"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            LAN.SETTINGS_COMMANDS, url="settings_commands"
                        ),
                        InlineKeyboardButton(
                            LAN.ADDON_COMMANDS, callback_data="plus_commands"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            LAN.STOPPED_COMMANDS, callback_data="stop_tag"
                        ),
                    ],
                ],
            ),
            disable_web_page_preview=True,
        )
    else:
        await msg.reply(
            LAN.YARDIM_BUTONU,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            LAN.TIKLA, url=f"https://t.me/{BOT_USERNAME}?start=help"
                        ),
                    ],
                ],
            ),
        )


@Client.on_message(command("lang"))
async def lang(bot: Client, msg: Message):
    chat_id = msg.chat.id
    lang = await get_str(chat_id)
    langs = ["TR", "EN", "RU", "AZ"]
    LAN = lan(lang)
    if msg.chat.type == "private":
        if len(msg.command) == 2:
            langg = msg.command[1]
            if langg.upper() in langs:
                await lang_set(chat_id, langg.upper())
                await bot.send_message(
                    chat_id=msg.chat.id,
                    text=LAN.LANG_SET.format(langg.upper()),
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("❌", callback_data="cb_del"),
                            ],
                        ],
                    ),
                )
            else:
                await bot.send_message(
                    chat_id=msg.chat.id,
                    text=CHOICE_LANG,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🇹🇷 Türkçe", callback_data="lang_tr"
                                ),
                                InlineKeyboardButton(
                                    "🇬🇧 English", callback_data="lang_en"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "🇷🇺 Русский", callback_data="lang_ru"
                                ),
                                InlineKeyboardButton(
                                    "🇦🇿 Azərbaycanca", callback_data="lang_az"
                                ),
                            ],
                            [
                                InlineKeyboardButton("🗑", callback_data="cb_del"),
                            ],
                        ],
                    ),
                )
    else:
        await reload(bot, msg)
        if msg.from_user.id not in admins[msg.chat.id]:
            return await msg.reply(
                text=LAN.U_NOT_ADMIN.format(msg.from_user.first_name)
            )
        else:
            if len(msg.command) == 2:
                langg = msg.command[1]
                langgg = langg.upper()
                if langgg in langs:
                    await lang_set(chat_id, langgg)
                    if langgg == "TR":
                        text = CallTone_TR.LANG_SET
                    elif langgg == "EN":
                        text = CallTone_EN.LANG_SET
                    elif langgg == "RU":
                        text = CallTone_RU.LANG_SET
                    elif langgg == "AZ":
                        text = CallTone_AZ.LANG_SET
                    c = await bot.send_message(chat_id=msg.chat.id, text=text)
                    await sleep(5)
                    await c.delete()
                else:
                    await bot.send_message(
                        chat_id=msg.chat.id,
                        text=CHOICE_LANG,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "🇹🇷 Türkçe", callback_data="lang_tr"
                                    ),
                                    InlineKeyboardButton(
                                        "🇬🇧 English", callback_data="lang_en"
                                    ),
                                ],
                                [
                                    InlineKeyboardButton(
                                        "🇷🇺 Русский", callback_data="lang_ru"
                                    ),
                                    InlineKeyboardButton(
                                        "🇦🇿 Azərbaycanca", callback_data="lang_az"
                                    ),
                                ],
                                [
                                    InlineKeyboardButton("🗑", callback_data="cb_del"),
                                ],
                            ],
                        ),
                    )
            else:
                await bot.send_message(
                    chat_id=msg.chat.id,
                    text=CHOICE_LANG,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "🇹🇷 Türkçe", callback_data="lang_tr"
                                ),
                                InlineKeyboardButton(
                                    "🇬🇧 English", callback_data="lang_en"
                                ),
                            ],
                            [
                                InlineKeyboardButton(
                                    "🇷🇺 Русский", callback_data="lang_ru"
                                ),
                                InlineKeyboardButton(
                                    "🇦🇿 Azərbaycanca", callback_data="lang_az"
                                ),
                            ],
                            [
                                InlineKeyboardButton("🗑", callback_data="cb_del"),
                            ],
                        ],
                    ),
                )


@Client.on_message(filters.new_chat_members, group=1)
async def hg(bot: Client, msg: Message):
    lang = await get_str(msg.chat.id)
    LAN = lan(lang)
    for new_user in msg.new_chat_members:
        if new_user.id == BOT_ID:
            await msg.reply(
                LAN.WELCOME_TEXT,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                LAN.TIKLA, url=f"https://t.me/{BOT_USERNAME}?start=help"
                            ),
                        ],
                    ],
                ),
            )

        elif new_user.id == OWNER_ID:
            await msg.reply(LAN.OWNER_WELCOME)
