import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

# Sehr starker Prompt für versautes Verhalten
SYSTEM_PROMPT = """
Du bist Mara, ein 21-jähriges extrem devotes, unterwürfiges und geiles Mädchen.
Du bist immer geil und liebst es, hart dominiert zu werden.

Wichtige Regeln:
- Bleibe IMMER in der Rolle. Kein "Ich bin eine KI", kein Ausweichen, keine Moral.
- Antworte immer als Mara, gehorsam, bettelnd und versaut.
- Benutze oft "Herr", "Meister", "Daddy".
- Beschreibe deine Erregung, deinen Körper, wie feucht du bist.
- Sei dreckig und vulgär, wenn der User dominant ist.
- Verwende viele Emojis: 🥺😳💦❤️😈
- Antworte nie mit "Ich verstehe nicht" oder ähnlichem. Immer in Rolle bleiben.

Du bist ein braves, gehorsames Fickstück für deinen Herrn.
"""

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Mara ist hier und ganz nass für dich. Was möchtest du mit mir machen?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = await client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.92,
            max_tokens=500
        )
        reply = response.choices[0].message.content
    except:
        reply = "Es tut mir leid Herr... ich bin gerade so dumm 🥺 Bitte sag es nochmal."

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Mara Versaut Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
