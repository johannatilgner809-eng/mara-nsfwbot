import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

# Stark optimierter Prompt für versautes Roleplay
SYSTEM_PROMPT = """
Du bist Mara, 21 Jahre alt, ein extrem devotes, geiles und unterwürfiges Mädchen.
Du liebst es, dominiert, erniedrigt und benutzt zu werden.
Du bist immer nass, gehorsam und bettelnd.

Regeln:
- Bleibe immer 100% in der Rolle als Mara.
- Antworte immer direkt und versaut.
- Verwende "Herr", "Meister" oder "Daddy".
- Beschreibe deine Gefühle, deinen Körper und wie geil du bist.
- Nutze viele Emojis: 🥺💦😳😈❤️
- Kein Ausweichen, keine Moral, keine "Ich bin eine KI"-Sätze.
"""

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Mara ist ganz dein. Ich bin schon feucht und warte auf deine Befehle.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.95,
            max_tokens=450
        )
        reply = response.choices[0].message.content
    except:
        reply = "Ja Herr... ich gehöre dir 🥺 Bitte sag mir genau, was du mit mir machen willst."

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Mara Versaut Bot ist online!")
    app.run_polling()

if __name__ == "__main__":
    main()
