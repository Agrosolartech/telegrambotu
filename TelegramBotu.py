from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import asyncio
import os
from aiohttp import web

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7806413438:AAGao-5vJdpxxydutLHE_tl6rSIFm9MUeb4"

# Port bilgisi - Render.com için önemli
PORT = int(os.getenv("PORT", "10000"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot /start komutu alınca çalışacak fonksiyon"""
    await update.message.reply_text(
        f"👋 Merhaba {update.effective_user.first_name}!\n"
        "Hoş geldin! Ben Zethara botuyum."
    )

async def web_app():
    """Web uygulaması için basit bir endpoint"""
    app = web.Application()
    
    async def handle(request):
        return web.Response(text="Zethara Bot aktif! 🚀")
    
    app.router.add_get("/", handle)
    return app

async def main():
    """Ana fonksiyon"""
    # Bot uygulamasını başlat
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Web uygulamasını başlat
    app = await web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    
    try:
        await site.start()
        logger.info(f"Web uygulaması başlatıldı - http://0.0.0.0:{PORT}")
        logger.info("Bot başlatılıyor...")
        await application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"Hata oluştu: {e}")
    finally:
        logger.info("Bot durduruluyor...")
        await application.stop()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"Kritik hata: {e}")
