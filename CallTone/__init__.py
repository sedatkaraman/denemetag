# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================


import logging
import sys
from logging import INFO

from pyrogram import Client, __version__, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tglogging import TelegramLogHandler

from Config import *

app = Client(
    "CallTone",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="CallTone/plugins"),
)


app.storage.SESSION_STRING_FORMAT = ">B?256sQ?"
