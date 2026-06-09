import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key_status = "✅ Key gefunden" if REPLICATE_API_KEY else "❌ Key NICHT gefunden"
    await update.message.reply_text(f"Hallo Herr...\n{key_status}\n\nREPLICATE_API_KEY: {REPLICATE_API_KEY[:10]}..." if REPLICATE_API_KEY else "❌ Key nicht gefunden")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ja Herr... 🥺")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Test Bot gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()
