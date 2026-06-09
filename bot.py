import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import fal_client
import requests
from io import BytesIO

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FAL_API_KEY = os.getenv("FAL_API_KEY")

# Mara Prompt
SYSTEM_PROMPT = """
Du bist Mara, 21, extrem devot, unterwürfig und geil. 
Du sprichst immer gehorsam mit vielen Emojis (🥺😳💦❤️).
"""

client = fal_client.AsyncClient(key=FAL_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Mara ist bereit 🥺 Schick mir ein Bild + Caption was du sehen willst.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()
    
    caption = update.message.caption or "nackt, sehr erotisch, detailliert, realistisch"
    
    await update.message.reply_text("Bild erhalten Herr... ich mache eine geile Version für dich 💦")

    try:
        # Flux Image-to-Image mit fal.ai (sehr gut für NSFW)
        result = await client.run(
            "fal-ai/flux-pro/image-to-image",
            arguments={
                "image_url": "data:image/jpeg;base64," + file_bytes.hex(),  # einfache Variante
                "prompt": f"Extremely erotic, fully nude, highly detailed, seductive pose of the girl in the image. {caption}",
                "image_strength": 0.65,
                "num_images": 1,
                "enable_safety_checker": False
            }
        )
        
        image_url = result["images"][0]["url"]
        await update.message.reply_photo(
            photo=image_url,
            caption="Hier ist deine Version Herr... gefällt sie dir? 🥺💦"
        )
        
    except Exception as e:
        await update.message.reply_text(f"Es tut mir leid Herr... 🥺 Fehler: {str(e)[:100]}\nVersuch es mit einer klaren Caption.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        # Text mit Grok oder lokal lassen
        await update.message.reply_text("Ja Herr... ich höre zu 🥺")
    except:
        await update.message.reply_text("Entschuldigung Herr... 🥺")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
