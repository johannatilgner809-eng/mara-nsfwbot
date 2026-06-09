import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import replicate
import base64

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Schick mir ein Bild + Caption (z.B. 'mach sie nackt' oder 'sehr erotisch') 🥺")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()
    
    caption = update.message.caption or "fully nude, very erotic, detailed, seductive pose"

    await update.message.reply_text("Bild erhalten Herr... Stable Diffusion bearbeitet es gerade 💦 Bitte etwas Geduld...")

    try:
        output = replicate.run(
            "stability-ai/sdxl",
            input={
                "image": "data:image/jpeg;base64," + base64.b64encode(file_bytes).decode("utf-8"),
                "prompt": f"nsfw, nude, erotic, {caption}, highly detailed, realistic skin, seductive girl, beautiful body",
                "negative_prompt": "clothes, clothing, dressed, blurry, low quality, deformed, ugly",
                "strength": 0.78,
                "num_inference_steps": 35,
                "guidance_scale": 7.5
            }
        )
        
        image_url = output[0] if isinstance(output, list) else output
        await update.message.reply_photo(
            photo=image_url, 
            caption="Hier ist die bearbeitete Version Herr... 🥺💦 Gefällt sie dir?"
        )
        
    except Exception as e:
        await update.message.reply_text(f"Es tut mir leid Herr... 🥺 Fehler: {str(e)[:150]}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ja Herr... ich bin bereit für dein Bild 🥺")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Mara NSFW Bot mit Stable Diffusion gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()
