# Бот-калькулятор ціни на монтаж відео

## Що це?
Telegram-бот який аналізує ТЗ клієнта і генерує цінову пропозицію (новачок / мід / про) з готовим обґрунтуванням для клієнта.

---

## Як запустити (покроково)

### Крок 1 — Створи бота в Telegram
1. Відкрий Telegram → знайди @BotFather
2. Напиши `/newbot`
3. Придумай назву (наприклад: Калькулятор монтажу)
4. Придумай username (латиниця, закінчується на bot): наприклад `montage_price_bot`
5. Скопіюй та збережи токен — виглядає так: `7412345678:AAHxxxxxxxx`

### Крок 2 — Отримай API-ключ Anthropic
1. Зайди на https://console.anthropic.com
2. Зареєструйся
3. API Keys → Create Key → скопіюй ключ
4. Поповни баланс від $5 (вистачить на сотні запитів)

### Крок 3 — Завантаж файли на GitHub
1. Зайди на https://github.com → зареєструйся якщо немає акаунту
2. New repository → назви `montage-price-bot` → Create repository
3. Натисни "uploading an existing file"
4. Перетягни всі 3 файли: `bot.py`, `requirements.txt`, `Procfile`
5. Натисни "Commit changes"

### Крок 4 — Запусти на Railway
1. Зайди на https://railway.app → Login with GitHub
2. New Project → Deploy from GitHub repo
3. Вибери `montage-price-bot`
4. Зайди у Variables і додай дві змінні:
   - `BOT_TOKEN` = твій токен від BotFather
   - `ANTHROPIC_API_KEY` = твій ключ від Anthropic
5. Railway автоматично запустить бота

### Крок 5 — Тестуй!
Знайди свого бота в Telegram і напиши /start

---

## Команди бота
- `/start` — почати роботу
- `/reset` — почати новий розрахунок (скинути діалог)

---

## Як користуватись
1. Скинь ТЗ клієнта текстом
2. Бот задасть уточнювальні питання (одне за раз)
3. Отримаєш готову цінову пропозицію з трьома рівнями і обґрунтуванням
4. Скопіюй текст для клієнта

---

## Якщо щось не працює
- Перевір що правильно вставив BOT_TOKEN і ANTHROPIC_API_KEY у Railway Variables
- Перевір що є баланс на рахунку Anthropic
- Перезапусти деплой у Railway (кнопка Redeploy)
