import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from replicate import AsyncClient
import base64

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

SYSTEM_PROMPT = """
Du bist Mara, 21, extrem devot, unterwürfig und geil. 
Sprich immer gehorsam mit vielen Emojis (🥺😳💦❤️).
"""

client = AsyncClient(api_token=REPLICATE_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Schick mir ein Bild + Caption (z.B. 'mach sie nackt') 🥺")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()
    
    caption = update.message.caption or "fully nude, very erotic, detailed, seductive pose, realistic"

    await update.message.reply_text("Bild erhalten Herr... Stable Diffusion bearbeitet es gerade 💦")

    try:
        output = await client.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b7e9c6a3b8f9d8f",
            input={
                "image": "data:image/jpeg;base64," + base64.b64encode(file_bytes).decode("utf-8"),
                "prompt": f"nsfw, {caption}, highly detailed, realistic skin, seductive, erotic, nude",
                "negative_prompt": "clothes, clothing, dressed, blurry, ugly, low quality",
                "strength": 0.78,
                "guidance_scale": 7.5,
                "num_inference_steps": 35
            }
        )
        
        image_url = output[0] if isinstance(output, list) else output
        await update.message.reply_photo(photo=image_url, caption="Hier ist die bearbeitete Version Herr... 🥺💦 Gefällt sie dir?")
        
    except Exception as e:
        await update.message.reply_text(f"Es tut mir leid Herr... 🥺 Fehler: {str(e)[:180]}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ja Herr... ich warte auf dein Bild 🥺")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
