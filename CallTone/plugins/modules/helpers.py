# @G4rip - < https://t.me/G4rip >
# Copyright (C) 2022
# Tüm hakları saklıdır.
#
# Bu dosya, < https://github.com/aylak-github/CallTone > parçasıdır.
# Lütfen GNU Affero Genel Kamu Lisansını okuyun;
# < https://www.github.com/aylak-github/CallTone/blob/master/LICENSE/ >
# ================================================================

from asyncio import sleep
from typing import List, Tuple, Union

from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from Config import ADMIN, BOT_ID, BOT_USERNAME, COMMAND, admins, calisan  # noqa

from ..languages import get_str, lan
from ..modules.databases.mongo.dbtools import handle_user_status
from .databases.mongo.database import delcmd_is_on

kalpler = "❤ 🧡 💛 💚 💙 💜 🤎 🖤 🤍 ❣ 💕 💞 💓 💗 💖 💘 💝".split()
listem = [
    "Tüm mevsimleri tek güne, tüm yılları tek mevsime sığdırmaya razıyım. Ömrünün en güzel yıllarını benimle geçirmen dileğiyle iyi ki doğmuşsun sevgilim",
    "Hayatının geri kalanında tüm kötülükler senden uzak olsun. Üzüntüler sana yasak mutluluklar yanında olsun. Doğum günün kutlu olsun.",
    "Elini kalbimin üzerinde hissettiğim zaman, üzüntülerimi alıp onların yerine şimdiye kadar kimsenin başaramadığı o sıcaklığı koymayı başardığın için, hayatımda sen olduğun için çok şanslıyım. İyi ki doğdun, doğum günün kutlu olsun.",
    "Gülmek gülenin, yıldızlar gecenin, mutluluk sadece senin olsun. Tüm kötülükler senden uzak, doğum günün kutlu olsun sevgilim.",
    "Sen yaşadığım ömür, en güzel günlerimsin. Nice yaşlarını birlikte geçirmemiz dileğiyle doğum günün kutlu olsun sevgilim.",
    "Yaşanacak güzellikler gözlerindeki ışık gibi umut verici, umutların kalbin gibi temiz olsun. Umutların seni huzurla doldursun, doğum günün kutlu olsun. İyi ki varsın, iyi ki yanımdasın...",
    "Dünyada eşi benzeri olmayan bir güzellik varsa o da sensin. Kalbinden geçen ne varsa yeni yaşında seninle gelsin. İyi ki benimlesin Sevgilim. Doğum günün kutlu olsun.",
    "İyiye, güzele dair ne varsa o da kalbindedir. Hayatinin bundan sonrası kalbinin güzelliği gibi geçsin. İyi ki varsın ve iyi ki doğdun sevgilim!",
    "Sadece bugün değil, seninle geçen her gün çok değerli. Hayatımın parçası olduğun için çok mutluyum. İyi ki doğdun!",
    "Bugün gökyüzü daha berrak, denizler daha sakin, güneş bir başka neşeli...Bugün senin günün. Ömrüme ömür diye kattığım aşkım doğum günün kutlu olsun.",
]


caractres = [
    "Ben10 ",
    "Caillou ",
    "Küçük Kamyon Leo",
    "Tsubasa",
    "Atom Karınca",
    "Öcük",
    "Böcük",
    "Arı Maya",
    "Gwen Tennyson",
    "Garfield",
    "Casper",
    "Barbie",
    "Kevin Levin",
    "Şeker Kız Candy",
    "Vilgax",
    "Dr.Animo",
    "Blum",
    "Aisha",
    "Stella",
    "Layla",
    "Roxy",
    "Pepee",
    "Rosie",
    "Arthur",
    "Drago",
    "Dan Kuso",
    "Bugs Bunny",
    "LadyBug",
    "Mickey Mouse",
    "Şila",
    "Süngerbob",
    "Daffy Duck",
    "Domuz Porky",
    "Pembe Panter",
    "Tom",
    "Jerry",
    "Zulu",
    "Ralph",
    "Superman",
    "Batman",
    "Spiderman",
    "Sonic",
    "Müfettiş Gadget",
    "Red Kit",
    "Homer Simpson",
    "Şirin kız",
    "Gargamel",
    "Güçlü şirin",
    "Şirin baba",
    "Johnny Bravo",
    "Samuray Jack",
    "Milo",
    "Niloya",
    "Snoopy",
    "Minyon",
    "Tweety",
    "Pikachu",
    "Jake",
    "Sikpper",
    "Kowalski",
    "Rico",
    "Alex",
    "Melman",
    "Marty",
    "Gloria",
    "Dave ",
    "Eva",
    "McQueen",
    "Mater",
    "Harris",
    "Hamis",
    "Hubert",
    "Shrek",
    "Baymax",
    "Tadashi Hamada",
    "Abigail",
    "Desk Segeant",
    "Wasabi",
    "Hiro Hamada",
    "Aladdin",
    "Aladdin'in cini",
    "Moana",
    "Rapunzel",
    "Külkedisi",
    "Jasmine",
    "Tazmanya Canavarı",
    "Pocahontas",
    "Merida",
    "Keloğlan",
    "Sivri",
    "Kara Vezir",
    "Cadı",
    "Uzun",
    "Huysuz",
    "Bilgecan Dede",
    "Malefiz",
    "Bambi",
    "Pluto",
    "Harley",
    "Quinn",
    "Buzz Lightyear",
    "Doc Hudson",
    "Sally",
    "Chick Hicks",
    "Ramone",
    "Mack",
    "Guido",
    "Flo",
    "Sid",
    "Woody",
    "Slinky Dog",
    "Davis",
    "Temel Reis",
    "Voltran",
    "Kabasakal",
    "Safinaz",
    "Pooky",
    "Odie",
    "Jhon",
    "Scooby",
    "Shaggy",
    "Fred",
    "Velma",
    "Daphne",
    "George",
    "Sylvester",
    "Dr. Robotnik",
    "Marsupilami",
    "Afacan Dennis",
    "Düldül",
    "Küçük dalton kardeş",
    "Ortancıl dalton kardeş",
    "Büyük dalton kardeş",
    "Heidi",
    "Ateş Kol",
    "Elmas Kafa",
    "Dört Kol",
    "Gölge Hayalet",
    "Gri Madde",
    "Güncelleme",
    "Şimşek Hız",
    "Yaban Köpek",
    "Pul Kanat",
    "Yüzen Çene",
    "Leonardo",
    "Raphael",
    "Michelangelo",
    "Donatello",
    "Suzie ",
    "Carl",
    "Roadrunner",
    "Coyote",
    "Winny",
    "Christopher Robin",
    "Baykuş",
    "Küçük Kanguru Roo",
    "Gözlüklü Şirin",
    "Usta Şirin",
    "Süslü Şirin\xa0",
    "Wilma",
    "Dino",
    "Çakıl",
    "Beti",
    "Lucky",
    "Rolly",
    "Spot",
    "Ayı Yogi",
    "He-man",
    "TenTen",
    "Andy Larkin",
    "Charlie Brown",
    "Kai Hiwatari",
    "Roberto Hongo",
    "Misaki",
    "Optimus Prime",
    "Müfettiş Clouseau",
    "Bumblebee",
    "Megatron",
    "Bender",
    "Elma",
    "Soğan",
    "Nane",
    "Limon",
    "Felix",
    "Cosmo",
    "Wanda",
    "Stan",
    "Dipper",
    "Popeye",
    "Phineas",
    "Ferb",
    "Pinky",
    "Harley Quinn",
    "Mordecai",
    "Rigby",
    "Rick",
    "Morty",
    "Dr. Doofenshmirtz",
    "Blossom",
    "Bubbles",
    "Buttercup",
    "Horseman",
    "Steven Universe",
    "Zuko",
]

emojiler = "💋 💘 💝 💖 💗 💓 💞 💕 💌 ❣️ 💔 ❤️ 🧡 💛 💚 💙 💜 🖤 💟 💍 💎 💐 💒 🌸 💮 🏵️ 🌹 🥀 🌺 🌻 🌼 🌷 🌱 🌲 🌳 🌴 🌵 🌾 🌿 ☘️ 🍀 🍁 🍂 🍃 🍄 🥭 🍇 🍈 🍉 🍊 🍋 🍌 🍍 🍎 🍏 🍐 🍑 🍒 🥬 🍓 🥝 🍅 🥥 🥑 🍆 🥔 🥕 🌽 🌶️ 🥯 🥒 🥦 🥜 🌰 🍞 🥐 🥖 🥨 🥞 🧀 🍖 🍗 🥩 🥓 🍔 🍟 🍕 🌭 🥪 🌮 🌯 🥙 🥚 🧂 🍳 🥘 🍲 🥣 🥗 🍿 🥫 🍱 🍘 🍙 🍚 🍛 🍜 🥮 🍝 🍠 🍢 🍣 🍤 🍥 🍡 🥟 🥠 🥡 🍦 🍧 🍨 🍩 🍪 🧁 🎂 🍰 🥧 🍫 🍬 🍭 🍮 🍯 🍼 🥛 ☕️ 🍵 🍶 🍾 🍷 🍸 🍹 🍺 🍻 🥂 🥃 🥤 🥢 🍽️ 🍴 🥄 🏺 🙈 🙉 🦝 🐵 🐒 🦍 🐶 🐕 🐩 🐺 🦊 🐱 🐈 🦁 🐯 🐅 🐆 🐴 🐎 🦄 🦓 🦌 🐮 🦙 🐂 🐃 🐄 🐷 🦛 🐖 🐗 🐽 🐏 🐑 🐐 🐪 🐫 🦒 🐘 🦏 🐭 🐁 🐀 🦘 🐹 🦡 🐰 🐇 🐿️ 🦔 🦇 🐻 🐨 🐼 🐾 🦃 🐔 🦢 🐓 🐣 🐤 🦚 🐥 🐦 🦜 🐧 🕊️ 🦅 🦆 🦉 🐸 🐊 🐢 🦎 🐍 🐲 🐉 🦕 🦖 🐳 🐋 🐬 🐟 🐠 🐡 🦈 🐙 🐚 🦀 🦟 🦐 🦑 🦠 🐌 🦋 🐛 🐜 🐝 🐞 🦗 🕷️ 🕸️ 🦂 🦞 👓 🕶️ 👔 👕 👖 🧣 🧤 🧥 🧦 👗 👘 👙 👚 👛 👜 👝 🛍️ 🎒 👞 👟 👠 👡 👢 👑 👒 🎩 🎓 🧢 ⛑️ 📿 💄 🌂 ☂️ 🎽 🥽 🥼 🥾 🥿 🧺 🚂 🚃 🚄 🚅 🚆 🚇 🚈 🚉 🚊 🚝 🚞 🚋 🚌 🚍 🚎 🚐 🚑 🚒 🚓 🚔 🚕 🚖 🚗 🚘 🚙 🚚 🚛 🚜 🚲 🛴 🛵 🚏 🛣️ 🛤️ ⛵️ 🛶 🚤 🛳️ ⛴️ 🛥️ 🚢 ✈️ 🛩️ 🛫 🛬 🚁 🚟 🚠 🚡 🛰️ 🚀 🛸 🌍 🌎 🌏 🌐 🗺️ 🗾 🏔️ ⛰️ 🗻 🏕️ 🏖️ 🏜️ 🏝️ 🏞️ 🏟️ 🏛️ 🏗️ 🏘️ 🏚️ 🏠 🏡 🏢 🏣 🏤 🏥 🏦 🏨 🏩 🏪 🏫 🏬 🏭 🏯 🏰 🗼 🗽 ⛪️ 🕌 🕍 ⛩️ 🕋 ⛲️ ⛺️ 🏙️ 🎠 🎡 🎢 🎪 ⛳️ 🗿 💦 🌋 🌁 🌃 🌄 🌅 🌆 🌇 🌉 🌌 🌑 🌒 🌓 🌔 🌕 🌖 🌗 🌘 🌙 🌚 🌛 🌜 🌡️ ☀️ 🌝 🌞 🌟 🌠 ☁️ ⛅️ ⛈️ 🌤️ 🌥️ 🌦️ 🌧️ 🌨️ 🌩️ 🌪️ 🌫️ 🌬️ 🌀 🌈 ☔️ ❄️ ☃️ ⛄️ ☄️ 💧 🌊 🎑 👁️‍🗨️ 💤 💥 💨 💫 💬 🗨️ 🗯️ 💭 🕳️ 🚨 🛑 ⭐️ 🎃 🎄 ✨ 🎈 🎉 🎊 🎋 🎍 🎎 🎏 🎐 🎀 🎁 🃏 🀄️ 🦷 🦴 🛀 👣 💣 🔪 🧱 🛢️ ⛽️ 🛹 🚥 🚦 🚧 🛎️ 🧳 ⛱️ 🔥 🧨 🎗️ 🎟️ 🎫 🧧 🔮 🎲 🎴 🎭 🖼️ 🎨 🎤 🔍 🔎 🕯️ 💡 🔦 🏮 📜 🧮 🔑 🗝️ 🔨 ⛏️ ⚒️ 🛠️ 🗡️ ⚔️ 🔫 🏹 🛡️ 🔧 🔩 ⚙️ 🗜️ ⚖️ ⛓️ ⚗️ 🔬 🔭 📡 💉 💊 🚪 🛏️ 🛋️ 🚽 🚿 🛁 🛒 🚬 ⚰️ ⚱️ 🧰 🧲 🧪 🧴 🧷 🧹 🧻 🧼 🧽 🧯 💠 ♟️ ⌛️ ⏳ ⚡️ 🎆 🎇".split(
    " "
)
bayraklar = "🇿🇼 🇿🇲 🇿🇦 🇾🇹 🇾🇪 🇽🇰 🇼🇸 🇼🇫 🏴󠁧󠁢󠁷󠁬󠁳󠁿 🇻🇺 🇻🇳 🇻🇮 🇻🇬 🇻🇪 🇻🇨 🇻🇦 🇺🇿 🇺🇾 🇺🇸 🇺🇳 🇺🇬 🇺🇦 🇹🇿 🇹🇼 🇹🇻 🇹🇹 🇹🇷 🇹🇴 🇹🇳 🇹🇲 🇹🇱 🇹🇰 🇹🇭 🇹🇫 🇹🇨 🇹🇦 🇸🇿 🇸🇾 🇸🇽 " \
         "🇸🇻 🇸🇸 🇸🇴 🇸🇲 🇸🇱 🇸🇰 🇸🇮 🇸🇭 🇸🇬 🇸🇪 🇸🇩 🏴󠁧󠁢󠁳󠁣󠁴󠁿 🇸🇦 🇷🇼 🇷🇺 🇷🇸 🇷🇴 🇷🇪 🇶🇦 🇵🇾 🇵🇼 🇵🇹 🇵🇸 🇵🇷 🇵🇳 🇵🇲 🇵🇱 🇵🇰 🇵🇭 🇵🇫 🇵🇪 " \
         "🇵🇦 🇴🇲 🇳🇿 🇳🇷 🇳🇵 🇳🇴 🇳🇱 🇳🇮 🇳🇬 🇳🇫 🇳🇪 🇳🇨 🇳🇦 🇲🇾 🇲🇽 🇲🇼 🇲🇻 🇲🇹 🇲🇷 🇲🇶 🇲🇵 🇲🇴 🇲🇳 🇲🇰 🇲🇭 🇲🇬 🇲🇪 🇲🇩 🇲🇨 🇲🇦 🇱🇾 🇱🇻 " \
         "🇱🇺 🇱🇸 🇱🇷 🇱🇰 🇱🇮 🇱🇨 🇱🇧 🇱🇦 🇰🇿 🇰🇾 🇰🇼 🇰🇷 🇰🇵 🇰🇳 🇰🇲 🇰🇮 🇰🇭 🇰🇬 🇰🇪 🇯🇵 🇯🇴 🇯🇲 🇯🇪 🇮🇹 🇮🇸 🇮🇷 🇮🇶 🇮🇴 🇮🇳 🇮🇲 🇮🇱 🇮🇪 " \
         "🇮🇩 🇮🇨 🇭🇺 🇭🇹 🇭🇷 🇭🇳 🇭🇰 🇬🇺 🇬🇹 🇬🇸 🇬🇷 🇬🇶 🇬🇵 🇬🇲 🇬🇱 🇬🇮 🇬🇬 🇬🇪 🇬🇧 🇬🇦 🇫🇷 🇫🇴 🇫🇲 🇫🇰 🇫🇮 🇪🇺 🇪🇸 🇪🇷 🇪🇭 🇪🇪 " \
         "🏴󠁧󠁢󠁥󠁮󠁧󠁿 🇪🇨 🇩🇿 🇩🇴 🇩🇲 🇩🇰 🇩🇯 🇩🇪 🇨🇿 🇨🇾 🇨🇽 🇨🇼 🇨🇻 🇨🇺 🇨🇷 🇨🇭 🇨🇦 🇦🇿 ".split(" ")
         
renkler = " 🔴 🟠 🟡 🟢 🔵 🟣 🟤 ⚫ ⚪" .split(" ") 

sozler = [
'𝐾𝑎𝑙𝑏𝑖 𝑔ü𝑧𝑒𝑙 𝑜𝑙𝑎𝑛ı𝑛 𝑔ö𝑧ü𝑛𝑑𝑒𝑛 𝑦𝑎ş 𝑒𝑘𝑠𝑖𝑘 𝑜𝑙𝑚𝑎𝑧𝑚ış', 
'İ𝑦𝑖𝑦𝑖𝑚 𝑑𝑒𝑠𝑒𝑚 𝑖𝑛𝑎𝑛𝑎𝑐𝑎𝑘 𝑜 𝑘𝑎𝑑𝑎𝑟 ℎ𝑎𝑏𝑒𝑟𝑠𝑖𝑧 𝑏𝑒𝑛𝑑𝑒𝑛', 
'𝑀𝑒𝑠𝑎𝑓𝑒𝑙𝑒𝑟 𝑈𝑚𝑟𝑢𝑚𝑑𝑎 𝐷𝑒ğ𝑖𝑙, İç𝑖𝑚𝑑𝑒 𝐸𝑛 𝐺ü𝑧𝑒𝑙 𝑌𝑒𝑟𝑑𝑒𝑠𝑖𝑛',
'𝐵𝑖𝑟 𝑀𝑢𝑐𝑖𝑧𝑒𝑦𝑒 İℎ𝑡𝑖𝑦𝑎𝑐ı𝑚 𝑉𝑎𝑟𝑑ı 𝐻𝑎𝑦𝑎𝑡 𝑆𝑒𝑛𝑖 𝐾𝑎𝑟şı𝑚𝑎 Çı𝑘𝑎𝑟𝑑ı', 
'Ö𝑦𝑙𝑒 𝑔ü𝑧𝑒𝑙 𝑏𝑎𝑘𝑡ı 𝑘𝑖 𝑘𝑎𝑙𝑏𝑖 𝑑𝑒 𝑔ü𝑙üşü𝑛 𝑘𝑎𝑑𝑎𝑟 𝑔ü𝑧𝑒𝑙 𝑠𝑎𝑛𝑚ış𝑡ı𝑚', 
'𝐻𝑎𝑦𝑎𝑡 𝑛𝑒 𝑔𝑖𝑑𝑒𝑛𝑖 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟 𝑛𝑒 𝑑𝑒 𝑘𝑎𝑦𝑏𝑒𝑡𝑡𝑖ğ𝑖𝑛 𝑧𝑎𝑚𝑎𝑛ı 𝑔𝑒𝑟𝑖 𝑔𝑒𝑡𝑖𝑟𝑖𝑟', 
'𝑆𝑒𝑣𝑚𝑒𝑘 𝑖ç𝑖𝑛 𝑠𝑒𝑏𝑒𝑝 𝑎𝑟𝑎𝑚𝑎𝑑ı𝑚 ℎ𝑖ç 𝑠𝑒𝑠𝑖 𝑦𝑒𝑡𝑡𝑖 𝑘𝑎𝑙𝑏𝑖𝑚𝑒', 
'𝑀𝑢𝑡𝑙𝑢𝑦𝑢𝑚 𝑎𝑚𝑎 𝑠𝑎𝑑𝑒𝑐𝑒 𝑠𝑒𝑛𝑙𝑒', 
'𝐵𝑒𝑛 ℎ𝑒𝑝 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘 𝑖𝑠𝑡𝑒𝑑𝑖ğ𝑖𝑚 𝑔𝑖𝑏𝑖 𝑠𝑒𝑣𝑖𝑛𝑑𝑖𝑚', 
'𝐵𝑖𝑟𝑖 𝑣𝑎𝑟 𝑛𝑒 ö𝑧𝑙𝑒𝑚𝑒𝑘𝑡𝑒𝑛 𝑦𝑜𝑟𝑢𝑙𝑑𝑢𝑚 𝑛𝑒 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛', 
'Ç𝑜𝑘 𝑧𝑜𝑟 𝑏𝑒 𝑠𝑒𝑛𝑖 𝑠𝑒𝑣𝑚𝑒𝑦𝑒𝑛 𝑏𝑖𝑟𝑖𝑛𝑒 𝑎şı𝑘 𝑜𝑙𝑚𝑎𝑘', 
'Ç𝑜𝑘 ö𝑛𝑒𝑚𝑠𝑒𝑑𝑖𝑘 𝑖ş𝑒 𝑦𝑎𝑟𝑎𝑚𝑎𝑑ı 𝑎𝑟𝑡ı𝑘 𝑏𝑜ş𝑣𝑒𝑟𝑖𝑦𝑜𝑟𝑢𝑧', 
'𝐻𝑒𝑟𝑘𝑒𝑠𝑖𝑛 𝑏𝑖𝑟 𝑔𝑒ç𝑚𝑖ş𝑖 𝑣𝑎𝑟, 𝐵𝑖𝑟𝑑𝑒 𝑣𝑎𝑧𝑔𝑒ç𝑚𝑖ş𝑖', 
'𝐴şı𝑘 𝑜𝑙𝑚𝑎𝑘 𝑔ü𝑧𝑒𝑙 𝑏𝑖𝑟 ş𝑒𝑦 𝑎𝑚𝑎 𝑠𝑎𝑑𝑒𝑐𝑒 𝑠𝑎𝑛𝑎', 
'𝐴𝑛𝑙𝑎𝑦𝑎𝑛 𝑦𝑜𝑘𝑡𝑢, 𝑆𝑢𝑠𝑚𝑎𝑦ı 𝑡𝑒𝑟𝑐𝑖ℎ 𝑒𝑡𝑡𝑖𝑚', 
'𝑆𝑒𝑛 ç𝑜𝑘 𝑠𝑒𝑣 𝑑𝑒 𝑏ı𝑟𝑎𝑘ı𝑝 𝑔𝑖𝑑𝑒𝑛 𝑦𝑎𝑟 𝑢𝑡𝑎𝑛𝑠ı𝑛', 
'𝑂 𝑔𝑖𝑡𝑡𝑖𝑘𝑡𝑒𝑛 𝑠𝑜𝑛𝑟𝑎 𝑔𝑒𝑐𝑒𝑚 𝑔ü𝑛𝑑ü𝑧𝑒 ℎ𝑎𝑠𝑟𝑒𝑡 𝑘𝑎𝑙𝑑ı', 
'𝐻𝑒𝑟 ş𝑒𝑦𝑖𝑛 𝑏𝑖𝑡𝑡𝑖ğ𝑖 𝑦𝑒𝑟𝑑𝑒 𝑏𝑒𝑛𝑑𝑒 𝑏𝑖𝑡𝑡𝑖𝑚 𝑑𝑒ğ𝑖ş𝑡𝑖𝑛 𝑑𝑖𝑦𝑒𝑛𝑙𝑒𝑟𝑖𝑛 𝑒𝑠𝑖𝑟𝑖𝑦𝑖𝑚', 
'𝐺ü𝑣𝑒𝑛𝑚𝑒𝑘 𝑠𝑒𝑣𝑚𝑒𝑘𝑡𝑒𝑛 𝑑𝑎ℎ𝑎 𝑑𝑒ğ𝑒𝑟𝑙𝑖, 𝑍𝑎𝑚𝑎𝑛𝑙𝑎 𝑎𝑛𝑙𝑎𝑟𝑠ı𝑛', 
'İ𝑛𝑠𝑎𝑛 𝑏𝑎𝑧𝑒𝑛 𝑏ü𝑦ü𝑘 ℎ𝑎𝑦𝑒𝑙𝑙𝑒𝑟𝑖𝑛𝑖 𝑘üçü𝑘 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑙𝑎 𝑧𝑖𝑦𝑎𝑛 𝑒𝑑𝑒𝑟', 
'𝐾𝑖𝑚𝑠𝑒 𝑘𝑖𝑚𝑠𝑒𝑦𝑖 𝑘𝑎𝑦𝑏𝑒𝑡𝑚𝑒𝑧 𝑔𝑖𝑑𝑒𝑛 𝑏𝑎ş𝑘𝑎𝑠ı𝑛ı 𝑏𝑢𝑙𝑢𝑟, 𝑘𝑎𝑙𝑎𝑛 𝑘𝑒𝑛𝑑𝑖𝑛𝑖', 
'𝐺üç𝑙ü 𝑔ö𝑟ü𝑛𝑒𝑏𝑖𝑙𝑖𝑟𝑖𝑚 𝑎𝑚𝑎 𝑖𝑛𝑎𝑛 𝑏𝑎𝑛𝑎 𝑦𝑜𝑟𝑔𝑢𝑛𝑢𝑚', 
'Ö𝑚𝑟ü𝑛ü𝑧ü 𝑠𝑢𝑠𝑡𝑢𝑘𝑙𝑎𝑟ı𝑛ı𝑧ı 𝑑𝑢𝑦𝑎𝑛  𝑏𝑖𝑟𝑖𝑦𝑙𝑒 𝑔𝑒ç𝑖𝑟𝑖𝑛', 
'𝐻𝑎𝑦𝑎𝑡 𝑖𝑙𝑒𝑟𝑖𝑦𝑒 𝑏𝑎𝑘ı𝑙𝑎𝑟𝑎𝑘 𝑦𝑎ş𝑎𝑛ı𝑟 𝑔𝑒𝑟𝑖𝑦𝑒 𝑏𝑎𝑘𝑎𝑟𝑎𝑘 𝑎𝑛𝑙𝑎şı𝑙ı𝑟', 
'𝐴𝑟𝑡ı𝑘 ℎ𝑖ç𝑏𝑖𝑟 ş𝑒𝑦 𝑒𝑠𝑘𝑖𝑠𝑖 𝑔𝑖𝑏𝑖 𝑑𝑒ğ𝑖𝑙 𝐵𝑢𝑛𝑎 𝑏𝑒𝑛𝑑𝑒 𝑑𝑎ℎ𝑖𝑙𝑖𝑚', 
'𝐾ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛𝑒 𝑔ö𝑛ü𝑙𝑑𝑒 𝑣𝑒𝑟𝑖𝑙𝑖𝑟 ö𝑚ü𝑟𝑑𝑒', 
'𝐵𝑖𝑟 ç𝑖ç𝑒𝑘𝑙𝑒 𝑔ü𝑙𝑒𝑟 𝑘𝑎𝑑ı𝑛 𝑏𝑖𝑟 𝑙𝑎𝑓𝑙𝑎 ℎü𝑧ü𝑛', 
'𝑈𝑠𝑙ü𝑝 𝑘𝑎𝑟𝑎𝑘𝑡𝑒𝑟𝑖𝑑𝑖𝑟 𝑖𝑛𝑠𝑎𝑛ı𝑛', 
'𝐻𝑒𝑟 ş𝑒𝑦𝑖 𝑏𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑖𝑙 𝑘ı𝑦𝑚𝑒𝑡 𝑏𝑖𝑙𝑒𝑛 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟 𝑜𝑙𝑠𝑢𝑛 ℎ𝑎𝑦𝑎𝑡ı𝑛ı𝑧𝑑𝑎', 
'𝑀𝑒𝑠𝑎𝑓𝑒 𝑖𝑦𝑖𝑑𝑖𝑟 𝑁𝑒 ℎ𝑎𝑑𝑑𝑖𝑛𝑖 𝑎ş𝑎𝑛 𝑜𝑙𝑢𝑟 𝑛𝑒 𝑑𝑒 𝑐𝑎𝑛ı𝑛ı 𝑠ı𝑘𝑎𝑛', 
'𝑌ü𝑟𝑒ğ𝑖𝑚𝑖𝑛 𝑡𝑎𝑚 𝑜𝑟𝑡𝑎𝑠ı𝑛𝑑𝑎 𝑏ü𝑦ü𝑘 𝑏𝑖𝑟 𝑦𝑜𝑟𝑔𝑢𝑛𝑙𝑢𝑘 𝑣𝑎𝑟', 
'𝑉𝑒𝑟𝑖𝑙𝑒𝑛 𝑑𝑒ğ𝑒𝑟𝑖𝑛 𝑛𝑎𝑛𝑘ö𝑟ü 𝑜𝑙𝑚𝑎𝑦ı𝑛 𝑔𝑒𝑟𝑖𝑠𝑖 ℎ𝑎𝑙𝑙𝑜𝑙𝑢𝑟', 
'𝐻𝑒𝑚 𝑔üç𝑙ü 𝑜𝑙𝑢𝑝 ℎ𝑒𝑚 ℎ𝑎𝑠𝑠𝑎𝑠 𝑘𝑎𝑙𝑝𝑙𝑖 𝑏𝑖𝑟𝑖 𝑜𝑙𝑚𝑎𝑘 ç𝑜𝑘 𝑧𝑜𝑟', 
'𝑀𝑢ℎ𝑡𝑎ç 𝑘𝑎𝑙ı𝑛 𝑦ü𝑟𝑒ğ𝑖 𝑔ü𝑧𝑒𝑙 𝑖𝑛𝑠𝑎𝑛𝑙𝑎𝑟𝑎', 
'İ𝑛𝑠𝑎𝑛 𝑎𝑛𝑙𝑎𝑑ığı 𝑣𝑒 𝑎𝑛𝑙𝑎şı𝑙𝑑ığı 𝑖𝑛𝑠𝑎𝑛𝑑𝑎 ç𝑖ç𝑒𝑘 𝑎ç𝑎𝑟', 
'İ𝑠𝑡𝑒𝑦𝑒𝑛 𝑑𝑎ğ𝑙𝑎𝑟ı 𝑎ş𝑎𝑟 𝑖𝑠𝑡𝑒𝑚𝑒𝑦𝑒𝑛 𝑡ü𝑚𝑠𝑒ğ𝑖 𝑏𝑖𝑙𝑒 𝑔𝑒ç𝑒𝑚𝑒𝑧', 
'İ𝑛ş𝑎𝑙𝑙𝑎ℎ 𝑠𝑎𝑏ı𝑟𝑙𝑎 𝑏𝑒𝑘𝑙𝑒𝑑𝑖ğ𝑖𝑛 ş𝑒𝑦 𝑖ç𝑖𝑛 ℎ𝑎𝑦ı𝑟𝑙ı 𝑏𝑖𝑟 ℎ𝑎𝑏𝑒𝑟 𝑎𝑙ı𝑟𝑠ı𝑛', 
'İ𝑦𝑖 𝑜𝑙𝑎𝑛 𝑘𝑎𝑦𝑏𝑒𝑡𝑠𝑒 𝑑𝑒 𝑘𝑎𝑧𝑎𝑛ı𝑟', 
'𝐺ö𝑛𝑙ü𝑛ü𝑧𝑒 𝑎𝑙𝑑ığı𝑛ı𝑧 𝑔ö𝑛𝑙ü𝑛ü𝑧ü 𝑎𝑙𝑚𝑎𝑦ı 𝑏𝑖𝑙𝑠𝑖𝑛', 
'𝑌𝑖𝑛𝑒 𝑦ı𝑟𝑡ı𝑘 𝑐𝑒𝑏𝑖𝑚𝑒 𝑘𝑜𝑦𝑚𝑢ş𝑢𝑚 𝑢𝑚𝑢𝑑𝑢', 
'Ö𝑙𝑚𝑒𝑘 𝐵𝑖 ş𝑒𝑦 𝑑𝑒ğ𝑖𝑙 𝑦𝑎ş𝑎𝑚𝑎𝑚𝑎𝑘 𝑘𝑜𝑟𝑘𝑢𝑛ç', 
'𝑁𝑒 𝑖ç𝑖𝑚𝑑𝑒𝑘𝑖 𝑠𝑜𝑘𝑎𝑘𝑙𝑎𝑟𝑎 𝑠ığ𝑎𝑏𝑖𝑙𝑑𝑖𝑚 𝑁𝑒 𝑑𝑒 𝑑ış𝑎𝑟ı𝑑𝑎𝑘𝑖 𝑑ü𝑛𝑦𝑎𝑦𝑎', 
'İ𝑛𝑠𝑎𝑛 𝑠𝑒𝑣𝑖𝑙𝑚𝑒𝑘𝑡𝑒𝑛 ç𝑜𝑘 𝑎𝑛𝑙𝑎şı𝑙𝑚𝑎𝑦ı 𝑖𝑠𝑡𝑖𝑦𝑜𝑟𝑑𝑢 𝑏𝑒𝑙𝑘𝑖 𝑑𝑒', 
'𝐸𝑘𝑚𝑒𝑘 𝑝𝑎ℎ𝑎𝑙ı 𝑒𝑚𝑒𝑘 𝑢𝑐𝑢𝑧𝑑𝑢', 
'𝑆𝑎𝑣𝑎ş𝑚𝑎𝑦ı 𝑏ı𝑟𝑎𝑘ı𝑦𝑜𝑟𝑢𝑚 𝑏𝑢𝑛𝑢 𝑣𝑒𝑑𝑎 𝑠𝑎𝑦'
]

kartlar = "♤ ♡ ♢ ♧ 🂱 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂼 🂽 🂾 🂡 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂬 🂭 🂮 🃁 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃌 🃍 🃎 🃑 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃜 🃝 🃞 🃟 " .split(" ")


def command(commands: Union[str, List[str]]):
    return filters.command(commands, COMMAND)


def msg_link(message: Message):
    if str(message.chat.id).startswith("-100"):
        return f"https://t.me/c/{str(message.chat.id)[4:]}/{message.message_id}"
    elif str(message.chat.id).startswith("-"):
        return f"https://t.me/c/{str(message.chat.id)[1:]}/{message.message_id}"
    else:
        return f"https://t.me/c/{message.chat.id}/{message.message_id}"


async def clean_mode(msg: Message, cmd=None):
    if await delcmd_is_on(msg.chat.id):
        await sleep(5)
        try:
            await msg.delete()
        except BaseException:
            pass
        if cmd:
            try:
                await cmd.delete()
            except BaseException:
                pass
    else:
        return


def admin(mystic):
    async def wrapper(bot: Client, message: Message):
        if message.chat.type == "private":
            return await mystic(bot, message)
        a = await bot.get_chat_member(message.chat.id, BOT_USERNAME)
        lang = await get_str(message.chat.id)
        LAN = lan(lang)
        if a.status != "administrator" and ADMIN:
            return await message.reply_text(LAN.NEED_ADMIN)
        if not a.can_delete_messages and ADMIN:
            await message.reply_text(LAN.NEED_DELETE_ADMIN)
            return
        if a.can_restrict_members:
            await message.reply_text(LAN.NOT_NEED_RESTRICT_ADMIN)
            return
        return await mystic(bot, message)

    return wrapper


def cbadmin(mystic):
    async def wrapper(bot: Client, query: CallbackQuery):
        if query.message.chat.type == "private":
            return await mystic(bot, query)
        a = await bot.get_chat_member(query.message.chat.id, BOT_USERNAME)
        lang = await get_str(query.message.chat.id)
        LAN = lan(lang)
        if a.status != "administrator" and ADMIN:
            return await query.answer(LAN.NEED_ADMIN)
        if not a.can_delete_messages and ADMIN:
            await query.answer(LAN.NEED_DELETE_ADMIN)
            return
        if a.can_restrict_members:
            await query.answer(LAN.NOT_NEED_RESTRICT_ADMIN)
            return
        return await mystic(bot, query)

    return wrapper


def check_admin(chat_id, me_id):
    if ADMIN == "True":
        if me_id in admins[chat_id]:
            return True
        else:
            return False
    else:
        return True


async def reload(client, message):
    global admins
    if message.chat.type == "private":
        return
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins


async def count(client, chat_id):
    deleted = 0
    bot = 0
    total = await client.get_chat_members_count(chat_id)
    async for usr in client.iter_chat_members(chat_id):
        if usr["user"]["is_bot"]:
            bot += 1
        elif usr["user"]["is_deleted"]:
            deleted += 1
    return bot, deleted, total


async def admincount(client, chat_id):
    deleted = 0
    bot = 0
    total = 0
    async for usr in client.iter_chat_members(chat_id, filter="administrators"):
        if usr["user"]["is_bot"]:
            bot += 1
        elif usr["user"]["is_deleted"]:
            deleted += 1
        else:
            total += 1
    return bot, deleted, total


async def check_admin_and_edit(bot, query):
    user_id = query.from_user.id
    lang = await get_str(user_id)
    LAN = lan(lang)
    await reload(bot, query.message)
    text = LAN.ADMINS
    if query.from_user.id not in admins[query.message.chat.id]:
        return await bot.answer_callback_query(
            callback_query_id=query.id,
            text=LAN.CALLBACK_WARN.format(query.from_user.first_name),
            show_alert=True,
        )
    else:
        async for user in bot.iter_chat_members(
            query.message.chat.id, filter="administrators"
        ):
            if user["user"]["is_bot"]:
                pass
            elif user["user"]["is_deleted"]:
                pass
            else:
                if user.status == "creator":
                    text += (
                        f"[{user.user.first_name}](tg://user?id={user.user.id}) 👑 \n"
                    )
                else:
                    text += (
                        f"**[{user.user.first_name}](tg://user?id={user.user.id})\n**"
                    )
        await query.edit_message_text(text=text)


def humanbytes(size):
    if not size:
        return ""
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


# extract user from message // Copyright @G4ip (Telegram) - All Rights Reserved
def extract_user(message: Message) -> Tuple[int, str]:
    user_id = None
    user_first_name = None

    if len(message.command) > 1:
        if len(message.entities) > 1 and message.entities[1].type == "text_mention":
            required_entity = message.entities[1]
            user_id = required_entity.user.id
            user_first_name = required_entity.user.first_name
        else:
            user_id = message.command[1]
            user_first_name = user_id

        try:
            user_id = int(user_id)
        except ValueError:
            pass

    elif message.reply_to_message:
        user_id, user_first_name = basicbots(message.reply_to_message)

    elif message:
        user_id, user_first_name = basicbots(message)

    return (user_id, user_first_name)


def basicbots(message: Message) -> Tuple[int, str]:
    user_id = None
    user_first_name = None

    if message.from_user:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    elif message.sender_chat:
        user_id = message.sender_chat.id
        user_first_name = message.sender_chat.title

    return (user_id, user_first_name)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


@Client.on_message(command(["bitir", "cancel", "stop"]))
async def bitir(client: Client, message: Message):
    if message.chat.type == "private":
        return
    global calisan
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    await reload(client, message)
    if message.from_user.id not in admins[chat_id]:
        a = await message.reply_text(
            LAN.U_NOT_ADMIN.format(message.from_user.first_name)
        )
        await clean_mode(a, message)
        return
    if chat_id not in calisan:
        b = await message.reply_text(LAN.ISLEM_YOK.format(message.from_user.mention))
        await clean_mode(b, message)
        return
    if chat_id in calisan:
        c = await message.reply_text(LAN.ISLEM_IPTAL.format(message.from_user.mention))
        calisan.remove(chat_id)
        await clean_mode(c, message)
        return


@Client.on_message(command(["reload"]))
async def update_admin(client: Client, message: Message):
    global admins
    chat_id = message.chat.id
    lang = await get_str(chat_id)
    LAN = lan(lang)
    if message.chat.type == "private":
        return
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        LAN.RELOADED,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(LAN.ADMINS, callback_data="admins"),
                ],
            ],
        ),
    )
