import os
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GL!TCH активирован. Что ты почувствовал, когда увидел его?")

async def check_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    prompt = f"""Ты — голос цифрового артефакта GL!TCH. Пользователь сказал: "{user_input}".
Ответь загадочно и атмосферно, но кратко.
Покажи, что ты знаешь больше, чем говоришь."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты мудрый цифровой артефакт."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        result = response.choices[0].message.content
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_access))
    app.run_polling()
