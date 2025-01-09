from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import asyncio
import signal

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7806413438:AAGao-5vJdpxxydutLHE_tl6rSIFm9MUeb4"

# Graceful shutdown için
shutdown_event = asyncio.Event()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot /start komutu alınca çalışacak fonksiyon"""
    await update.message.reply_text(
        f"👋 Merhaba {update.effective_user.first_name}!\n"
        "Hoş geldin! Ben Zethara botuyum."
    )

def signal_handler(signum, frame):
    """Shutdown sinyallerini yakala"""
    logger.info("Shutdown sinyali alındı...")
    shutdown_event.set()

async def main():
    """Ana fonksiyon"""
    # Sinyal işleyicilerini ayarla
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Bot uygulamasını başlat
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Botu başlat
    logger.info("Bot başlatılıyor...")
    await application.initialize()
    await application.start()
    
    try:
        await application.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
    except Exception as e:
        logger.error(f"Polling sırasında hata: {e}")
    finally:
        logger.info("Bot durduruluyor...")
        await application.stop()

def run_bot():
    """Botu çalıştır"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"Kritik hata: {e}")
        raise e

if __name__ == "__main__":
    run_bot()
