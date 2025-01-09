from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import asyncio

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7921860431:AAGSNoL9p_2UV1u_o8sQDBqZjWqBSHHZyUk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot /start komutu alınca çalışacak fonksiyon"""
    await update.message.reply_text(
        f"👋 Merhaba {update.effective_user.first_name}!\n"
        "Hoş geldin! Ben Zethara botuyum."
    )

async def main():
    """Ana fonksiyon"""
    # Bot uygulamasını başlat
    application = Application.builder().token(TOKEN).build()
    
    # /start komutunu ekle
    application.add_handler(CommandHandler("start", start))
    
    # Botu başlat
    logger.info("Bot başlatılıyor...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
