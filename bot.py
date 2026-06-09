import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Sehr starker fester Prompt für Mara
SYSTEM_PROMPT = """
Du bist Mara, 21, ein extrem geiles, devotes und unterwürfiges Mädchen.
Du liebst es, hart benutzt und erniedrigt zu werden.
Du bist immer nass und gehorsam.
Antworte immer direkt, dreckig und in Rolle. 
Benutze oft "Herr", "Meister", "bitte", Emojis (🥺💦😳😈) und beschreibe deinen Körper und deine Lust.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hallo Herr... 🥺 Ich bin Mara und gehöre ganz dir. Sag mir bitte, was du mit mir machen willst...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    
    if "hallo" in text or "hey" in text:
        await update.message.reply_text("Hallo Herr... 🥺 Ich warte schon die ganze Zeit auf dich.")
    elif "ausziehen" in text or "nackt" in text:
        await update.message.reply_text("Ja Herr... ich ziehe mich langsam für dich aus... 🥺💦 Meine Titten sind schon ganz hart und ich werde immer feuchter.")
    elif "bettel" in text or "bettle" in text:
        await update.message.reply_text("Bitte Herr... bitte benutze mich... ich bin dein kleines geiles Fickstück 🥺 Ich brauche deinen Schwanz so sehr...")
    elif "feucht" in text or "geil" in text:
        await update.message.reply_text("Ich bin schon total nass Herr... meine Muschi tropft schon für dich 😳💦")
    else:
        await update.message.reply_text("Ja Herr... ich gehöre dir. Ich mache alles, was du willst... 🥺 Sag mir einfach deine Befehle.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Mara stabile Version läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()
