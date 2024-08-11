import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load variabel lingkungan dari file .env
load_dotenv()

# Fungsi untuk mendapatkan token dari variabel lingkungan
def get_token() -> str:
    return os.getenv('TELEGRAM_BOT_TOKEN')

# Fungsi untuk membaca kalimat dari file dan memilih secara acak
def get_random_response() -> str:
    with open('random.txt', 'r') as file:
        lines = file.readlines()
    return random.choice(lines).strip()

# Fungsi untuk menangani perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Halo! Saya adalah bot Anda.')

# Fungsi untuk menangani pesan teks dengan kalimat acak dari file
async def respond_with_random(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()  # Ubah pesan ke huruf kecil
    keyword = 'aku cinta kamu'  # Kata kunci dalam huruf kecil

    if keyword in user_message:
        response = get_random_response()
        await update.message.reply_text(response)
    else:
        await update.message.reply_text(update.message.text)  # Balas dengan pesan asli

# Fungsi utama
def main() -> None:
    TOKEN = get_token()
    if TOKEN is None:
        print("Token tidak ditemukan! Periksa file .env.")
        return

    application = Application.builder().token(TOKEN).build()

    # Daftarkan handler untuk perintah /start
    application.add_handler(CommandHandler("start", start))

    # Daftarkan handler untuk semua pesan teks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_with_random))

    # Mulai bot
    application.run_polling()

if __name__ == '__main__':
    main()