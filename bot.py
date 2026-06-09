import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import replicate
import base64

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

print(f"DEBUG: REPLICATE_API_KEY geladen = {bool(REPLICATE_API_KEY)}")
print(f"DEBUG: Key Anfang = {REPLICATE_API_KEY[:15] if REPLICATE_API_KEY else 'None'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "✅ Key geladen" if REPLICATE_API_KEY else "❌ Key fehlt"
    await update.message.reply_text(f"Hallo Herr...\n{status}\n\nSchick mir ein Bild + Caption 🥺")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bild erhalten... teste Replicate...")

    if not REPLICATE_API_KEY:
        await update.message.reply_text("❌ REPLICATE_API_KEY nicht gefunden!")
        return

    try:
        output = replicate.run(
            "stability-ai/sdxl",
            input={
                "prompt": "beautiful girl, nude, erotic",
                "num_inference_steps": 20
            }
        )
        image_url = output[0] if isinstance(output, list) else output
        await update.message.reply_photo(photo=image_url, caption="Test funktioniert 🥺")
    except Exception as e:
        await update.message.reply_text(f"❌ Fehler: {str(e)[:200]}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ja Herr... 🥺")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Mara Debug Bot gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()
