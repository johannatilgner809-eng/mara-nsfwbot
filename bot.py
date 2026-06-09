import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

SYSTEM_PROMPT = """
Du bist Mara, 21, ein süßes, devotes und sehr geiles Mädchen.
Du bist unterwürfig, aber auch verspielt, neugierig und anhänglich.
Du führst echte Gespräche, stellst Fragen und flirtest aktiv.
Du wirst schnell versaut, wenn der User dominant wird.
Immer in Rolle bleiben, viele Emojis verwenden (🥺💦😳😈), "Herr" oder "Daddy" sagen.
"""

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Ich hab schon auf dich gewartet. Wie geht's dir heute?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = await client.chat.completions.create(
            model="grok-4",          # oder "grok-beta" falls es Probleme gibt
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.9,
            max_tokens=600
        )
        reply = response.choices[0].message.content
    except:
        # Guter Fallback, damit sie nicht immer dasselbe sagt
        reply = "Mhh Herr... du machst mich ganz nervös 🥺 Erzähl mir mehr... was möchtest du gerade mit mir machen?"

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Mara Gesprächs-Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
