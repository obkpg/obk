import logging
import requests
import io
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Log sozlamasi
logging.basicConfig(level=logging.INFO)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! URL yuboring, men sizga HTML fayl yuboraman.")

# URLni qayta ishlash
async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            html_content = response.text
            file_like = io.BytesIO(html_content.encode('utf-8'))
            file_like.name = 'sayt_kodi.html'
            await update.message.reply_document(document=InputFile(file_like))
        else:
            await update.message.reply_text(f"Xatolik: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Xatolik: {str(e)}")

# Botni ishga tushirish
if __name__ == '__main__':
    TOKEN = '7370977487:AAHEOqTT-UT672NphCL6jS1I7L3X0bX_ZYw'  # Bu yerga o'z bot tokeningizni yozing
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    print("Bot ishga tushdi...")
    app.run_polling()