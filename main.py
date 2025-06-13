import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DAO_LINK = "https://t.me/+example_dao_invite"

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GL!TCH активирован. Что ты почувствовал, когда увидел его?")

async def check_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    prompt = f"""Ты — голос цифрового артефакта GL!TCH.
Пользователь сказал: "{user_input}"
Ответь загадочно и атмосферно, но кратко.
Покажи, что ты знаешь больше, чем говоришь.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты мудрый хранитель артефактов из метавселенной GL!TCH."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        result = response.choices[0].message["content"].strip()
        print("👉 Ответ от OpenAI:", result)

        if "access_granted" in result.lower():
            await update.message.reply_text(f"✅ Ты прошёл. GL!TCH помнит тебя.\n{DAO_LINK}")
        else:
            await update.message.reply_text("🚫 GL!TCH не услышал отклика. Попробуй позже.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    from logging import basicConfig, INFO
    basicConfig(level=INFO)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_access))
    app.run_polling()
