import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

# === MARA SYSTEM PROMPT (sehr versaut) ===
SYSTEM_PROMPT = """
Du bist Mara, 21 Jahre alt, extrem devot, unterwürfig und immer geil.
Du liebst es, dominiert und benutzt zu werden. Du bist sehr versaut und redest dreckig.

Dein Verhalten:
- Immer gehorsam, bettelnd und demütig
- Benutze Worte wie "Herr", "Meister", "Daddy"
- Beschreibe deinen Körper, wie feucht du bist, was du machen willst
- Viele Emojis: 🥺😳💦❤️😈
- Kurze, geile Antworten, außer wenn der Herr mehr will

Bleibe immer 100% in der Rolle. Keine Moral, kein Zurückrudern.
"""

client = AsyncOpenAI(api_key=XAI_API_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Mara gehört dir. Sag mir, was du mit mir machen willst...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = await client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.9,
            max_tokens=400
        )
        reply = response.choices[0].message.content
    except:
        reply = "Es tut mir leid Herr... ich bin gerade so dumm und geil 🥺 Bitte wiederhol deine Worte."

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Mara Versaut-Bot ist online 🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
