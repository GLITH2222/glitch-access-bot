import logging
import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# 🔑 Получение токенов
TELEGRAM_TOKEN = os.getenv("7994558952:AAGzyoeYGz3_PIJHy9MopWSkJ3WxXYDdIvs")
OPENAI_API_KEY = os.getenv("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")
DAO_LINK = "https://t.me/+example_dao_invite"

# 🔧 Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# 🚀 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GL!TCH активирован. Что ты почувствовал, когда увидел его?")

# 🧠 Проверка фразы и ответ от OpenAI
async def check_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print("📥 Входящий текст:", user_input)  # лог запроса

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
        result = response.choices[0].message["content"].strip().lower()
        print("📤 Ответ от OpenAI:", result)  # лог ответа

        if "access_granted" in result:
            await update.message.reply_text(f"✅ Ты прошёл. GL!TCH помнит тебя.\n{DAO_LINK}")
        else:
            await update.message.reply_text("🚫 GL!TCH не услышал отклика. Попробуй позже.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")
        print("❌ Ошибка OpenAI:", e)  # лог ошибки

# ▶️ Запуск
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_access))
    app.run_polling()
