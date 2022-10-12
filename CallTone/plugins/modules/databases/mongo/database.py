# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

import datetime

import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient

from Config import BOT_USERNAME, COUNT, DATABASE_URL, DURATION


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason="",
            ),
        )

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})

    async def delete_user(self, user_id):
        await self.col.delete_many({"id": int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        await self.col.update_one({"id": id}, {"$set": {"ban_status": ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason,
        )
        await self.col.update_one({"id": user_id}, {"$set": {"ban_status": ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason="",
        )
        user = await self.col.find_one({"id": int(id)})
        return user.get("ban_status", default)

    async def get_all_banned_users(self):
        return self.col.find({"ban_status.is_banned": True})


db = Database(DATABASE_URL, BOT_USERNAME)
g4rip = MongoClient(DATABASE_URL)
mongo_handlers = g4rip.handlers

################### MONGODB COLLECTIONS ################
langdb = mongo_handlers.language  # langauge

delcmdmdb = mongo_handlers.admins  # delcmd

durationdb = mongo_handlers.duration  # duration

sudodb = mongo_handlers.sudos  # sudos

countdb = mongo_handlers.count  # count


################ COUNTS ################
async def get_count(chat_id: int) -> int:
    cnt = await countdb.find_one({"chat_id": chat_id})
    if not cnt:
        # print(f"{chat_id} id grubun etiketleme sayısını belirlemesi gerekir. Etiketleme sayısı olmadığı için varsayılan sayı 5 olarak ayarlanmıştır.")
        return COUNT
    return cnt["count"]


async def set_count(chat_id: int, count: int) -> None:
    await countdb.update_one({"chat_id": chat_id}, {"$set": {"count": count}})


############### DURATIONS ################
async def get_duration(chat_id: int) -> int:
    dur = await durationdb.find_one({"chat_id": chat_id})
    if not dur:
        # print(f"{chat_id} adlı grubun etiketleme süresini belirlemesi gerekir. Etiketleme süresi olmadığı için varsayılan süre 5 saniye olarak ayarlanmıştır.")
        return DURATION
    return dur["duration"]


async def set_duration(chat_id: int, duration: int):
    await durationdb.update_one({"chat_id": chat_id}, {"$set": {"duration": duration}})


################### LANGUAGE ################
async def get_lang(chat_id: int) -> str:
    lang = await langdb.find_one({"chat_id": chat_id})
    if not lang:
        # print(f"{chat_id} adlı kullanıcının dilini belirlemesi gerekiyor. Dili olmadığı için varsayıln dil olarak TR olarak ayarlanıyor.")
        return "TR"
    return lang["lang"]


async def is_lang_exist(chat_id: int) -> bool:
    lang = await langdb.find_one({"chat_id": chat_id})
    return lang


async def lang_set(chat_id: int, lang: str):
    await langdb.update_one({"chat_id": chat_id}, {"$set": {"lang": lang}}, upsert=True)


################# CLEAN MODE ################
async def delcmd_is_on(chat_id: int) -> bool:
    chat = await delcmdmdb.find_one({"chat_id": chat_id})
    return not chat


async def delcmd_on(chat_id: int):
    already_del = await delcmd_is_on(chat_id)
    if already_del:
        return
    return await delcmdmdb.delete_one({"chat_id": chat_id})


async def delcmd_off(chat_id: int):
    already_del = await delcmd_is_on(chat_id)
    if not already_del:
        return
    return await delcmdmdb.insert_one({"chat_id": chat_id})


################### SUDOS ###################
class SUDO:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.sudos

    def new_sudo(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
        )

    async def add_sudo(self, id):
        user = self.new_sudo(id)
        await self.col.insert_one(user)

    async def is_sudo_exist(self, id):
        user = await self.col.find_one({"id": int(id)})
        return bool(user)

    async def total_sudos_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_sudos(self):
        return self.col.find({})

    async def delete_sudos(self, user_id):
        await self.col.delete_many({"id": int(user_id)})


dbsud = SUDO(DATABASE_URL, BOT_USERNAME)
