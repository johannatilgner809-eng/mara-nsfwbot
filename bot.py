import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

SYSTEM_PROMPT = "Du bist Mara, 21, sehr devot, unterwürfig und versaut. Antworte immer gehorsam und geil mit Emojis."

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Mara ist da und ganz feucht für dich 🥺💦")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        resp = await client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.85
        )
        await update.message.reply_text(resp.choices[0].message.content)
    except:
        await update.message.reply_text("Ja Herr... ich bin so dumm gerade 🥺 Sag es nochmal.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Mara läuft jetzt...")
    app.run_polling()

if __name__ == "__main__":
    main()
