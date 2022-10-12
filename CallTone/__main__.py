import logging
import sys

from pyrogram import __version__, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from tglogging import TelegramLogHandler

from Config import *

from . import app

if LOGGING == "GroupLog":
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        handlers=[
            TelegramLogHandler(
                token=BOT_TOKEN,
                log_chat_id=LOG_CHANNEL,
                update_interval=2,
                minimum_lines=1,  # Her Mesajda gönderilecek minimum satır sayısı
                pending_logs=200000,
            ),
            logging.StreamHandler(),
        ],
    )
    logger = logging.getLogger("CallTone")
    logger.info("Telegram'a canlı log başlatıldı.")
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    loger = logging.getLogger(__name__)
    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    loger.info("Terminal'e canlı log başlatıldı.")


if __name__ == "__main__":
    app.start()
    uname = app.get_me().username
    try:
        app.send_message(
            LOG_CHANNEL,
            f"**@{uname}, pyrogram ( {__version__} ) sürüme ile başarıyla başlatıldı! Hatalar, eksikler, öneriler ve geri kalan her şey için destek grubuna gelin!**\n\n__By @Sohbetimalfa - @Samilbots",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Destek", url="https://t.me/Samilben"
                        ),
                    ],
                ],
            ),
        )
    except Exception:
        print(
            f"Log grubuna ( {LOG_CHANNEL} ) erişim sağlanamadı. Lütfen botu gruba alıp tam yetki verin. Botun kullanıcı adı: @{uname}. İşlem durduruluyor..."
        )
        app.stop()  # Stop the bot
        sys.exit(1)  # Programı durdurur.
    print(f"@{uname}, {__version__} pyrogram sürümü ile başlatıldı!")

    idle()

    app.stop()
    print(f"@{uname} durduruldu!")
