import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 1. Servidor Web Anti-Sleep (Flask)
web_app = Flask(__name__)


@web_app.route("/")
def home():
    return "Bot de Referencias Nexus activo 24/7 🚀", 200


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host="0.0.0.0", port=port)


# 2. Configuración general
TOKEN = ("8753647492:AAFMUik6QVDm-zmrv_Y96Jlwfa8Qc9WGX9c")
CANAL_DESTINO = os.getenv("CANAL_ID", "-1004469723581")

OWNER = "[https://t.me/Zzzz_0456](https://t.me/Zzzz_0456)"
PRECIOS = "[https://t.me/c/4469723581/3](https://t.me/c/4469723581/3)"
LINK_CANAL_REFES = "[https://t.me/+MM3aX30TIyk5OWY5](https://t.me/+MM3aX30TIyk5OWY5)"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "亗 𝖓𝖊𝖝𝖚𝖘 𝖗𝖊𝖋𝖊𝖘 ⛧☠️\n\n"
        "𖤐 Usa /ref seguido de tu referencia.\n"
        "𖤐 O responde a una foto enviando /ref para publicar la imagen.\n\n"
        "Ejemplo:\n"
        "/ref Cliente confiable 😍"
    )
    await update.message.reply_text(texto)


async def procesar_ref(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message

    username = f"@{user.username}" if user.username else "Sin username"
    user_id = user.id

    # 1. Extraer el mensaje escrito junto al comando /ref
    raw_text = message.text or message.caption or ""
    partes = raw_text.split(maxsplit=1)
    mensaje_comando = partes[1].strip() if len(partes) > 1 else ""

    # 2. Extraer texto y/o foto del mensaje respondido (reply)
    mensaje_respondido = ""
    foto_id = None

    if message.reply_to_message:
        reply = message.reply_to_message
        mensaje_respondido = (reply.text or reply.caption or "").strip()
        if reply.photo:
            foto_id = reply.photo[-1].file_id

    # Si la foto se envió directamente en el mismo mensaje con /ref
    if not foto_id and message.photo:
        foto_id = message.photo[-1].file_id

    # 3. Dar prioridad al mensaje del /ref, si no hay, tomar el mensaje respondido
    mensaje_final = mensaje_comando or mensaje_respondido

    linea_mensaje = f"☑️ 𝙈𝙚𝙣𝙨𝙖𝙟𝙚: {mensaje_final}\n" if mensaje_final else ""

    texto_canal = (
        "☑️ 𝘾𝙐𝙍𝙎𝙊 𝙑𝙄𝙋 𝙉𝙀𝙓𝙐𝙎\n\n"
        f"{linea_mensaje}"
        f"☑️ 𝙐𝙨𝙚𝙧𝙣𝙖𝙢𝙚: {username}\n"
        "━━━━━━━━━━━━━━━━\n"
        f"☑️ 𝙐𝙨𝙚𝙧 𝙄𝘿: {user_id}\n"
        "━━━━━━━━━━━━━━━━\n"
        "☑️ 𝙂𝙧𝙖𝙘𝙞𝙖𝙨 𝙥𝙤𝙧 𝙩𝙪 𝙧𝙚𝙛𝙚𝙧𝙚𝙣𝙘𝙞𝙖 🐣"
    )

    botones_canal = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝙊𝙒𝙉𝙀𝙍 ↗", url=OWNER),
                InlineKeyboardButton("𝙋𝙍𝙀𝘾𝙄𝙊𝙎 ↗", url=PRECIOS),
            ]
        ]
    )

    boton_unirse = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 𝙐𝙣𝙞𝙧𝙨𝙚 𝙖𝙡 𝘾𝙖𝙣𝙖𝙡 𝙙𝙚 𝙍𝙚𝙛𝙚𝙧𝙚𝙣𝙘𝙞𝙖𝙨 ↗",
                    url=LINK_CANAL_REFES,
                )
            ]
        ]
    )

    try:
        # Enviar al canal con foto (si existe) + el texto
        if foto_id:
            await context.bot.send_photo(
                chat_id=CANAL_DESTINO,
                photo=foto_id,
                caption=texto_canal,
                reply_markup=botones_canal,
            )
        else:
            await context.bot.send_message(
                chat_id=CANAL_DESTINO,
                text=texto_canal,
                reply_markup=botones_canal,
            )

        # Confirmación al usuario con botón de canal
        await update.message.reply_text(
            "✅ ¡Tu referencia ha sido publicada con éxito!\n\n"
            "Únete a nuestro canal para ver todas las referencias publicadas 👇",
            reply_markup=boton_unirse,
        )

    except Exception as e:
        print(f"Error al enviar al canal: {e}")
        await update.message.reply_text(
            "⚠️ Ocurrió un error al enviar la referencia. Verifica que el bot sea administrador en el canal."
        )


def main():
    threading.Thread(target=run_flask, daemon=True).start()

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ref", procesar_ref))
    app.add_handler(
        MessageHandler(filters.PHOTO & filters.Regex(r"^/ref"), procesar_ref)
    )

    print("亗 𝙉𝙀𝙓𝙐𝙎 𝙍𝙀𝙁𝙀𝙎 ⛧☠️")
    print("🟢 Bot iniciado correctamente...")

    app.run_polling()


if __name__ == "__main__":
    main()
