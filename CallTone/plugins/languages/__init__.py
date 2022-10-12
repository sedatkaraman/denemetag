# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================


from logging import getLogger

from Config import LANGUAGE

from ..modules.databases.mongo.database import get_lang
from . import CallTone_AZ, CallTone_EN, CallTone_RU, CallTone_TR

LOGS = getLogger(__name__)


async def get_str(chat_id: int):
    if await get_lang((chat_id)) == "TR":
        return "TR"
    elif await get_lang((chat_id)) == "EN":
        return "EN"
    elif await get_lang((chat_id)) == "AZ":
        return "AZ"
    elif await get_lang((chat_id)) == "RU":
        return "RU"
    else:
        return LANGUAGE


def lan(lang: str = None):
    if str(lang).upper() == "TR":
        LAN = CallTone_TR
    elif str(lang).upper() == "AZ":
        LAN = CallTone_AZ
    elif str(lang).upper() == "EN":
        LAN = CallTone_EN
    elif str(lang).upper() == "RU":
        LAN = CallTone_RU
    else:
        LAN = CallTone_TR
    return LAN
