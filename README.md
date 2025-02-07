# 🤖 ELWA AI - Market Analysis Bot

[![GitHub stars](https://img.shields.io/github/stars/Wh0mever/ElWA_AI)](https://github.com/Wh0mever/ElWA_AI/stargazers)
[![GitHub license](https://img.shields.io/github/license/Wh0mever/ElWA_AI)](https://github.com/Wh0mever/ElWA_AI/blob/main/LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat&logo=telegram&logoColor=white)](https://t.me/ctrltg)
[![Website](https://img.shields.io/badge/Website-whomever.tech-blue)](https://whomever.tech)

<div align="center">
  <h1>🤖 📊 💹</h1>
  <br/>
  <p><i>🚀 Умный анализ рынка с использованием искусственного интеллекта</i></p>
</div>

## 📊 Возможности

- 🎯 **Умный анализ рынка**: Использование продвинутых алгоритмов для анализа рыночных данных
- 📈 **Технические индикаторы**: RSI, MACD, Bollinger Bands и другие
- 🔍 **Распознавание паттернов**: Автоматическое определение рыночных паттернов
- 💰 **Торговые сигналы**: Точки входа, Take Profit и Stop Loss
- 🔐 **Безопасность**: Система авторизации с одноразовыми ключами
- 📱 **Веб-интерфейс**: Современный адаптивный дизайн

## 🚀 Быстрый старт

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/Wh0mever/ElWA_AI.git
cd ElWA_AI
```

2. **Установите зависимости**
```bash
pip install -r requirements.txt
```

3. **Настройте конфигурацию**
- Создайте файл `.env` на основе `.env.example`
- Заполните необходимые API ключи и настройки

4. **Запустите бота**
```bash
python Bot.py
```

## 📦 Зависимости

- Python 3.8+
- pandas-ta
- python-binance
- aiogram
- FastAPI
- Stripe
- SQLAlchemy
- Redis

## 🛠 Структура проекта

```
ElWA_AI/
├── Bot.py                # Основной файл бота
├── config.py            # Конфигурация
├── database.py          # Работа с базой данных
├── market_api.py        # API для работы с рынком
├── signals.py           # Генерация сигналов
├── ai_model.py          # AI модель
├── utils.py            # Вспомогательные функции
├── webapp/             # Веб-интерфейс
│   ├── app.py
│   ├── templates/
│   └── static/
└── data/               # Данные
    ├── users.json
    └── signals.json
```

## 💡 Использование

1. **Запустите бота в Telegram**
   - Найдите бота по имени
   - Отправьте команду `/start`
   - Введите ключ доступа

2. **Выберите валютную пару**
   - XAU/USD (Золото)
   - BTC/USD (Биткоин)
   - EUR/USD
   - USD/JPY
   - GBP/USD

3. **Получите анализ**
   - Технические индикаторы
   - Рыночные паттерны
   - Точки входа
   - Уровни Take Profit и Stop Loss

## 🔒 Безопасность

- Система блокировки после 3 неудачных попыток
- Одноразовые ключи с ограниченным временем действия
- Шифрование важных данных
- Безопасное хранение API ключей

## 🌐 API Интеграции

- Binance API для криптовалют
- Forex API для валютных пар
- Stripe для платежей
- Redis для кэширования

## 👨‍💻 Разработка

Для участия в разработке:

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📝 Лицензия

MIT License. Подробности в файле [LICENSE](LICENSE)

## 📞 Контакты

- Website: [whomever.tech](https://whomever.tech)
- GitHub: [@Wh0mever](https://github.com/wh0mever)
- Telegram: [@ctrltg](https://t.me/ctrltg)

## ⭐ Поддержка проекта

Если вам нравится проект, не забудьте поставить звезду на GitHub! 