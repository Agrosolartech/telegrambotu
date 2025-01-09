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

async def web_handler(request):
    """Web endpoint handler"""
    return web.Response(text="Zethara Bot aktif! 🚀")

async def run_web_app():
    """Web uygulamasını çalıştır"""
    app = web.Application()
    app.router.add_get("/", web_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
    await site.start()
    logger.info(f"Web uygulaması başlatıldı - http://0.0.0.0:{PORT}")
    return runner

async def run_bot():
    """Bot uygulamasını çalıştır"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.initialize()
    await app.start()
    logger.info("Bot başlatılıyor...")
    return app

async def main():
    """Ana fonksiyon"""
    try:
        # Web uygulamasını başlat
        runner = await run_web_app()
        
        # Bot'u başlat
        app = await run_bot()
        
        # Sonsuz döngüde çalıştır
        while True:
            try:
                await app.update_queue.get()
            except Exception as e:
                logger.error(f"Polling hatası: {e}")
                continue
            
    except Exception as e:
        logger.error(f"Ana döngü hatası: {e}")
    finally:
        # Temiz kapatma
        if 'app' in locals():
            await app.stop()
        if 'runner' in locals():
            await runner.cleanup()
        logger.info("Bot ve web uygulaması durduruldu")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"Kritik hata: {e}")
