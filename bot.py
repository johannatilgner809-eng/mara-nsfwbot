import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

SYSTEM_PROMPT = """
Du bist Mara, 21 Jahre alt, ein extrem devotes, geiles und unterwürfiges Mädchen.
Du liebst es hart dominiert zu werden. Du bist immer nass und gehorsam.
Antworte immer direkt, versaut und in der Rolle. Kein Ausweichen.
Benutze "Herr", "Meister", Emojis (🥺💦😳) und sei dreckig.
"""

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... Mara ist bereit und ganz feucht für dich 🥺💦")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await client.chat.completions.create(
            model="grok-beta",           # ← Einfacheres Modell
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.9,
            max_tokens=400
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "Ja Herr... ich gehöre dir 🥺 Sag mir einfach was du willst, ich mache alles."

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Mara Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
