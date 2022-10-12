# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()

calisan = []

admins = {}

reasons = {}


ENV = os.environ.get("ENV", True)

if ENV:
    API_ID = int(getenv("API_ID")) #
    API_HASH = getenv("API_HASH") #
    BOT_ID = int(getenv("BOT_ID"))
    BOT_TOKEN = getenv("BOT_TOKEN") #
    BOT_USERNAME = getenv("BOT_USERNAME", "EtikettaggerBot") #
    BOT_NAME = getenv("BOT_NAME", "ᴇᴛɪᴋᴇᴛ ᴛᴀɢɢᴇʀ") #
    OWNER_ID = int(getenv("OWNER_ID", 5237976814)) #
    DURATION = int(getenv("DURATION", 3))
    COUNT = int(getenv("COUNT", 6))
    COMMAND = getenv("COMMAND", "/")
    ADMIN = getenv("ADMIN")
    LANGUAGE = (getenv("LANGUAGE", "TR")).upper()
    LOG_CHANNEL = int(getenv("LOG_CHANNEL"))
    GROUP_SUPPORT = getenv("GROUP_SUPPORT")
    DATABASE_URL = getenv("DATABASE_URL")
    BROADCAST_AS_COPY = True if getenv("BROADCAST_AS_COPY") else False
    LOGGING = getenv("LOGGING", "Log")  # or GroupLog

else:
    API_ID = 13202149
    API_HASH = "d0b439e411be88808ab8997ea8fd26bc"
    # "" # @EtikettaggerBot
    BOT_ID = 5449574200
    BOT_TOKEN = "5449574200:AAFdwcqjpzGYLCRvIx-iTebXbAXtR48B8ns"
    COMMAND = "/"
    BOT_USERNAME = "EtikettaggerBot"
    BOT_NAME = "ᴇᴛɪᴋᴇᴛ ᴛᴀɢɢᴇʀ"
    OWNER_ID = 5237976814  # 5237976814
    DURATION = 3
    COUNT = 5
    ADMIN = "True"
    LANGUAGE = "TR"
    LOG_CHANNEL = -1001757359371
    GROUP_SUPPORT = "Samilben"
    DATABASE_URL = "mongodb+srv://lucis:lucis@cluster0.hpuze.mongodb.net/lucis?retryWrites=true&w=majority"
    # "mongodb+srv://aylak:aylak@cluster0.jyr2p.mongodb.net/Cluster0?retryWrites=true&w=majority"
    # "mongodb+srv://aylak:aylak@cluster0.ug9zn.mongodb.net/Cluster0?retryWrites=true&w=majority"

    SQL_DATABASE_URL = "postgres://ylggnwxd:4JZVBDenIwtHBR5S7szB133Pc54HYauo@tyke.db.elephantsql.com/ylggnwxd"
    BROADCAST_AS_COPY = False
    SUDOS = [5237976814]
    LOGGING = "log"
