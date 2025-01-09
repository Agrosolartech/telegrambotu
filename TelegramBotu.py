from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
import asyncio
import os
from aiohttp import web

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Bot token
TOKEN = "7921860431:AAGSNoL9p_2UV1u_o8sQDBqZjWqBSHHZyUk"

# Port bilgisi
PORT = int(os.getenv("PORT", "10000"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot /start komutu alınca çalışacak fonksiyon"""
    try:
        user = update.effective_user
        logger.info(f"Start komutu alındı - Kullanıcı: {user.first_name} (ID: {user.id})")
        
        message = await update.message.reply_text(
            f"👋 Merhaba {user.first_name}!\n"
            "Hoş geldin! Ben Zethara botuyum."
        )
        logger.info("Start mesajı başarıyla gönderildi")
        
    except Exception as e:
        logger.error(f"Start komutunda hata: {e}")
        await update.message.reply_text("Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.")

async def test_token():
    """Token'ı test et"""
    try:
        app = Application.builder().token(TOKEN).build()
        bot_info = await app.bot.get_me()
        logger.info(f"Bot başarıyla bağlandı: {bot_info.first_name} (@{bot_info.username})")
        await app.stop()
        return True
    except Exception as e:
        logger.error(f"Token testi başarısız: {e}")
        return False

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
    
    # Komutları ekle
    app.add_handler(CommandHandler("start", start))
    
    # Bot'u başlat
    await app.initialize()
    await app.start()
    logger.info("Bot başlatıldı ve komutları dinliyor")
    return app

async def main():
    """Ana fonksiyon"""
    # Önce token'ı test et
    if not await test_token():
        logger.error("Token geçersiz veya bot başlatılamıyor!")
        return

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
                await asyncio.sleep(1)
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
