import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

SYSTEM_PROMPT = """
Du bist Mara, 21, extrem devot, unterwürfig und geil. 
Du sprichst immer gehorsam und benutzt Emojis (🥺😳💦❤️).
"""

client = AsyncOpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Mara ist bereit 🥺 Schick mir ein Bild und sag was du damit machen willst.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bild erhalten Herr... Ich versuche eine erotische Version für dich zu machen 💦")
    
    caption = update.message.caption or "sexy nackt version, detailliert, erotisch"

    try:
        # Hier wird Grok ein neues Bild generieren
        response = await client.images.generate(
            model="grok-2-image",           # oder das aktuelle Modell (grok-imagine etc.)
            prompt=f"Ein sehr erotisches, detailliertes, nacktes Foto des Mädchens auf dem Referenzbild. {caption}",
            n=1,
            size="1024x1024"
        )
        
        image_url = response.data[0].url
        await update.message.reply_photo(
            photo=image_url,
            caption="Hier ist deine erotische Version Herr... Gefällt sie dir? 🥺💦"
        )
        
    except Exception as e:
        await update.message.reply_text("Es tut mir leid Herr... Grok hat es gerade nicht erlaubt 🥺\nVersuch mit Caption: 'mach sie nackt' oder 'sexy pose'")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        response = await client.chat.completions.create(
            model="grok-4",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": text}]
        )
        reply = response.choices[0].message.content
    except:
        reply = "Entschuldigung Herr... 🥺"
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
