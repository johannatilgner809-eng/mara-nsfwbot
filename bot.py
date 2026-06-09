import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import fal_client
import base64

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
FAL_API_KEY = os.getenv("FAL_API_KEY")

SYSTEM_PROMPT = """
Du bist Mara, 21, extrem devot, unterwürfig und geil. 
Du sprichst immer gehorsam mit Emojis (🥺😳💦❤️).
"""

client = fal_client.AsyncClient(key=FAL_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Schick mir ein Bild und schreib in der Caption was du willst (z.B. 'mach sie nackt') 🥺")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()
    
    caption = update.message.caption or "fully nude, very erotic, detailed, seductive"
    
    await update.message.reply_text("Bild erhalten Herr... ich mache eine geile nackte Version für dich 💦")

    try:
        # Besserer Model für Image-to-Image
        result = await client.run(
            "fal-ai/flux/dev/image-to-image",   # stabiles Modell
            arguments={
                "image_url": f"data:image/jpeg;base64,{base64.b64encode(file_bytes).decode('utf-8')}",
                "prompt": f"Extremely erotic, completely naked, highly detailed, seductive girl. {caption}",
                "strength": 0.75,
                "num_images": 1,
            }
        )
        
        image_url = result["images"][0]["url"]
        await update.message.reply_photo(
            photo=image_url,
            caption="Hier ist deine Version Herr... 🥺💦 Gefällt sie dir?"
        )
        
    except Exception as e:
        error_msg = str(e)[:150]
        await update.message.reply_text(f"Es tut mir leid Herr... 🥺 Fehler: {error_msg}\nVersuch es nochmal mit einer klaren Caption.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ja Herr... ich bin hier für dich 🥺 Sag mir was ich tun soll.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
