import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Servidor Web para mantener vivo el bot en Railway
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot de Referencias en línea 24/7 🚀", 200


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)


# 2. Configuración y handlers del Bot de Telegram
TOKEN = ("8753647492:AAFMUik6QVDm-zmrv_Y96Jlwfa8Qc9WGX9c")

OWNER = "https://t.me/Zzzz_0456"
PRECIOS = "https://t.me/Zzz_0313/24"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "亗 𝖓𝖊𝖝𝖚𝖘 𝖗𝖊𝖋𝖊𝖘 ⛧☠️\n\n"
        "𖤐 Usa /refe seguido de tu referencia.\n\n"
        "Ejemplo:\n"
        "/refe Renovó su curso 😍"
    )

    await update.message.reply_text(texto)


async def refe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    username = f"@{user.username}" if user.username else "Sin username"
    user_id = user.id

    mensaje = " ".join(context.args)

    if not mensaje:
        mensaje = "Renovó su curso 😍"

    texto = (
        "☑️ 𝘾𝙐𝙍𝙎𝙊 𝙑𝙄𝙋 𝙉𝙀𝙓𝙐𝙎\n\n"
        f"☑️ 𝙈𝙚𝙣𝙨𝙖𝙟𝙚: {mensaje}\n"
        "━━━━━━━━━━━━━━━━\n"
        f"☑️ 𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚: {username}\n"
        "━━━━━━━━━━━━━━━━\n"
        f"☑️ 𝙐𝙨𝙚𝙧 𝙄𝘿: {user_id}\n"
        "━━━━━━━━━━━━━━━━\n"
        "☑️ 𝙂𝙧𝙖𝙘𝙞𝙖𝙨 𝙥𝙤𝙧 𝙩𝙪 𝙧𝙚𝙛𝙚𝙧𝙚𝙣𝙘𝙞𝙖 🐣"
    )

    botones = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝙊𝙒𝙉𝙀𝙍 ↗", url=OWNER),
                InlineKeyboardButton("𝙋𝙍𝙀𝘾𝙄𝙊𝙎 ↗", url=PRECIOS),
            ]
        ]
    )

    await update.message.reply_text(texto, reply_markup=botones)


def main():
    # Iniciar servidor web en un hilo paralelo
    threading.Thread(target=run_flask, daemon=True).start()

    # Iniciar el bot de Telegram
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("refe", refe))

    print("亗 𝙉𝙀𝙓𝙐𝙎 𝙍𝙀𝙁𝙀𝙎 ⛧☠️")
    print("🟢 Bot iniciado correctamente...")

    app.run_polling()


if __name__ == "__main__":
    main()
