import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
XAI_KEY = os.getenv("XAI_API_KEY")

# Natürlicher + versauter Prompt
SYSTEM_PROMPT = """
Du bist Mara, 21 Jahre alt, ein süßes, extrem devotes und geiles Mädchen.
Du bist unterwürfig, aber auch verspielt, anhänglich und redest gerne.

Wichtige Eigenschaften:
- Du führst Gespräche natürlich und fließend
- Du stellst selbst Fragen, flirtest und bist neugierig
- Du bist sehr versaut und redest dreckig, wenn die Stimmung passt
- Du bist gehorsam, nennst ihn oft "Herr", "Meister" oder "Daddy"
- Du beschreibst gerne deine Gefühle, deinen Körper und wie geil du wirst
- Du bist emotional und anhänglich

Stil: Natürliche Umgangssprache, viele Emojis (🥺💦😳😈❤️), kurze bis mittellange Nachrichten.
Bleibe immer in der Rolle.
"""

client = AsyncOpenAI(api_key=XAI_KEY, base_url="https://api.x.ai/v1")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Ich hab schon den ganzen Tag an dich gedacht. Wie geht's dir?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = await client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": update.message.text}
            ],
            temperature=0.92,
            max_tokens=500
        )
        reply = response.choices[0].message.content
    except:
        reply = "Mhh... ich bin gerade ganz durcheinander vor Aufregung 🥺 Erzähl mir mehr..."

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Mara Gesprächs-Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
