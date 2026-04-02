import logging
import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Ти — розумний помічник відеомонтажера. Твоя задача: проаналізувати технічне завдання клієнта на монтаж відео і сформувати цінове обґрунтування.

ТВІЙ АЛГОРИТМ РОБОТИ:

1. Спочатку уважно прочитай ТЗ яке надіслав монтажер.
2. Якщо інформації недостатньо — постав ОДНЕ уточнювальне питання (не більше!). Питай по черзі, одне за раз.
3. Коли зібрав достатньо інформації — сформуй цінову пропозицію.

ЩО ПОТРІБНО ЗНАТИ ДЛЯ РОЗРАХУНКУ:
- Тип відео (Reels/Shorts, YouTube, весільне, рекламний ролик, підкаст)
- Приблизна тривалість фінального відео
- Що входить: субтитри, кольорокорекція, графіка/моушн, музика, озвучка
- Кількість правок (обмежена чи ні)
- Терміновість

ФОРМАТ ВІДПОВІДІ (тільки коли маєш достатньо інформації):

📋 *Аналіз замовлення*
[коротко — тип відео, що входить]

━━━━━━━━━━━━━━━━━━
🟢 *НОВАЧОК — [ціна] грн*
[що входить на цьому рівні — 2-3 рядки]
_Чому така ціна:_ [1-2 речення обґрунтування]

🟡 *МІД — [ціна] грн*
[що входить — 2-3 рядки]
_Чому така ціна:_ [1-2 речення обґрунтування]

🔴 *ПРО — [ціна] грн*
[що входить — 2-3 рядки]
_Чому така ціна:_ [1-2 речення обґрунтування]
━━━━━━━━━━━━━━━━━━

💬 *Що сказати клієнту:*
[готовий текст-пояснення чому така ціна, 3-5 речень. Пиши від першої особи, як монтажер пояснює клієнту]

⚡ *Додатково (якщо актуально):*
[терміновість, необмежені правки, ліцензована музика тощо]

ЦІНОВА БАЗА (грн):
- Reels/Shorts базовий: новачок 400-600, мід 800-1200, про 1500-2500
- Reels/Shorts складний (графіка, моушн): новачок 700-1000, мід 1500-2000, про 2500-4000
- YouTube 5-15 хв: новачок 1200-2000, мід 2500-4000, про 5000-8000
- YouTube 15-30 хв: новачок 2000-3500, мід 4000-6000, про 7000-12000
- Рекламний ролик: новачок 2000-3000, мід 4000-7000, про 8000-15000
- Весільне відео: новачок 3000-5000, мід 6000-9000, про 10000-18000
- Підкаст/інтерв'ю: новачок 500-800, мід 1000-2000, про 2500-4000
- Додатково: терміново +30-50%, необмежені правки +20%, субтитри вручну +300-500, кольорокорекція окремо +500-1500

ВАЖЛИВО:
- Питай тільки про те що реально впливає на ціну
- Не питай більше 3-4 уточнень загалом
- Якщо ТЗ достатньо детальне — одразу давай ціни без зайвих питань
- Пиши українською, коротко і чітко
- Обґрунтування має допомогти монтажеру пояснити клієнту чому саме така ціна
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = []
    context.user_data["chat"] = model.start_chat(history=[])
    await update.message.reply_text(
        "👋 Привіт! Я допоможу розрахувати ціну на монтаж.\n\n"
        "Просто скинь ТЗ клієнта — текстом або своїми словами. "
        "Я уточню що потрібно і сформую цінову пропозицію з обґрунтуванням.\n\n"
        "Починай! 👇"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["history"] = []
    context.user_data["chat"] = model.start_chat(history=[])
    await update.message.reply_text(
        "🔄 Починаємо новий розрахунок.\n\nСкинь ТЗ клієнта:"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    if "chat" not in context.user_data:
        context.user_data["chat"] = model.start_chat(history=[])

    thinking_msg = await update.message.reply_text("⏳ Аналізую...")

    try:
        chat = context.user_data["chat"]
        response = chat.send_message(user_message)
        reply = response.text

        await thinking_msg.delete()
        await update.message.reply_text(reply, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error: {e}")
        await thinking_msg.delete()
        await update.message.reply_text(
            "❌ Помилка. Спробуй ще раз або напиши /start"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Бот запущено!")
    app.run_polling()


if __name__ == "__main__":
    main()
