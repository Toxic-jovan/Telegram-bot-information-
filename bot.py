import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NUMVERIFY_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Phone Info Bot!\n"
        "Send /check <international‑format number>\n"
        "Example: /check +8801712345678"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Usage: /check +8801XXXXXXXXX")
        return

    number = context.args[0]
    url = f"http://apilayer.net/api/validate?access_key={API_KEY}&number={number}"

    try:
        resp = requests.get(url, timeout=10).json()
    except Exception as e:
        await update.message.reply_text(f"❌ Error contacting API: {e}")
        return

    if resp.get("valid"):
        reply = (
            f"✅ Number: {resp.get('international_format', '—')}\n"
            f"📍 Country: {resp.get('country_name', '—')}\n"
            f"📞 Carrier: {resp.get('carrier', '—')}\n"
            f"🌐 Line Type: {resp.get('line_type', '—')}"
        )
    else:
        reply = "❌ Invalid number or info not available."

    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    print("🤖 Bot is starting…")
    app.run_polling()
