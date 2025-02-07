import asyncio
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

from config import (
    BOT_TOKEN,
    ADMIN_IDS,
    FOREX_PAIRS,
    CRYPTO_PAIRS,
    WEBAPP,
    MAX_LOGIN_ATTEMPTS,
    BLOCK_DURATION_HOURS
)
from utils import (
    get_main_keyboard,
    get_forex_keyboard,
    get_crypto_keyboard,
    get_unauthorized_keyboard,
    get_payment_keyboard,
    get_profile_keyboard,
    save_user_history,
    get_user_history,
    format_signal_message,
    show_typing
)
from keys import (
    verify_key,
    mark_key_as_used,
    is_user_blocked,
    increment_login_attempts,
    reset_login_attempts,
    get_remaining_block_time,
    create_key
)
from market_api import market_api
from ai_model import ai_model

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    
    # Проверяем блокировку
    if is_user_blocked(user_id):
        remaining = get_remaining_block_time(user_id)
        if remaining:
            hours = remaining.total_seconds() / 3600
            await message.answer(
                f"⛔️ Вы заблокированы на {hours:.1f} часов из-за превышения попыток входа."
            )
            return
    
    # Приветственное сообщение
    await message.answer(
        "👋 Добро пожаловать в Market AI Analyst!\n\n"
        "🤖 Я помогу вам анализировать рынок с помощью искусственного интеллекта "
        "и технических индикаторов.\n\n"
        "🔐 Для доступа к функциям бота введите ключ или приобретите его.",
        reply_markup=get_unauthorized_keyboard()
    )

@dp.message(lambda message: message.text == "🔐 Ввести ключ")
async def enter_key(message: types.Message):
    """Обработка ввода ключа"""
    await message.answer(
        "Введите ваш ключ доступа в формате XXXX-XXXX-XXXX"
    )

@dp.message(lambda message: len(message.text) == 14 and message.text.count('-') == 2)
async def check_key(message: types.Message):
    """Проверка введенного ключа"""
    user_id = message.from_user.id
    key = message.text.upper()
    
    # Проверяем блокировку
    if is_user_blocked(user_id):
        remaining = get_remaining_block_time(user_id)
        if remaining:
            hours = remaining.total_seconds() / 3600
            await message.answer(
                f"⛔️ Вы заблокированы на {hours:.1f} часов из-за превышения попыток входа."
            )
            return
    
    # Проверяем ключ
    if verify_key(key):
        mark_key_as_used(key)
        reset_login_attempts(user_id)
        await message.answer(
            "✅ Ключ активирован успешно!\n"
            "Теперь вы можете использовать все функции бота.",
            reply_markup=get_main_keyboard(user_id in ADMIN_IDS)
        )
        save_user_history(user_id, "key_activated", {"key": key})
    else:
        attempts = increment_login_attempts(user_id)
        remaining = MAX_LOGIN_ATTEMPTS - attempts
        
        if remaining > 0:
            await message.answer(
                f"❌ Неверный ключ. Осталось попыток: {remaining}"
            )
        else:
            await message.answer(
                "⛔️ Превышено количество попыток. "
                f"Вы заблокированы на {BLOCK_DURATION_HOURS} часов."
            )

@dp.callback_query(lambda c: c.data == "asset_forex")
async def show_forex_pairs(callback: types.CallbackQuery):
    """Показ списка Forex пар"""
    await callback.message.edit_text(
        "📈 Выберите валютную пару:",
        reply_markup=get_forex_keyboard()
    )

@dp.callback_query(lambda c: c.data == "asset_crypto")
async def show_crypto_pairs(callback: types.CallbackQuery):
    """Показ списка криптовалютных пар"""
    await callback.message.edit_text(
        "🪙 Выберите криптовалютную пару:",
        reply_markup=get_crypto_keyboard()
    )

@dp.callback_query(lambda c: c.data.startswith("pair_"))
async def analyze_pair(callback: types.CallbackQuery):
    """Анализ выбранной пары"""
    pair_id = callback.data.split('_')[1]
    user_id = callback.from_user.id
    
    # Определяем тип пары и получаем символ
    if pair_id in FOREX_PAIRS:
        pair_info = FOREX_PAIRS[pair_id]
        data = await market_api.get_forex_data(pair_info['symbol'])
    else:
        pair_info = CRYPTO_PAIRS[pair_id]
        data = await market_api.get_crypto_data(pair_info['symbol'])
    
    # Анализируем данные
    await callback.message.edit_text(
        "🔄 Анализирую рынок...\n"
        "⏳ Это может занять несколько секунд."
    )
    
    # Генерируем сигнал
    signal = ai_model.generate_signal(data)
    signal['pair'] = pair_info['symbol']
    
    # Сохраняем в историю
    save_user_history(user_id, "analysis", signal)
    
    # Отправляем результат
    await callback.message.edit_text(
        format_signal_message(signal),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
        ])
    )

@dp.callback_query(lambda c: c.data == "history")
async def show_history(callback: types.CallbackQuery):
    """Показ истории запросов"""
    user_id = callback.from_user.id
    history = get_user_history(user_id)
    
    if not history:
        await callback.message.edit_text(
            "📝 История пуста",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
            ])
        )
        return
    
    text = "📖 Последние запросы:\n\n"
    for item in history:
        if item['action'] == "analysis":
            text += f"🕒 {item['timestamp']}\n"
            text += format_signal_message(item['data']) + "\n\n"
    
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")]
        ])
    )

@dp.callback_query(lambda c: c.data == "profile")
async def show_profile(callback: types.CallbackQuery):
    """Показ профиля пользователя"""
    await callback.message.edit_text(
        "👤 Ваш профиль",
        reply_markup=get_profile_keyboard()
    )

@dp.message(lambda message: message.text == "💳 Купить доступ")
async def show_payment_options(message: types.Message):
    """Показ вариантов оплаты"""
    await message.answer(
        "💳 Выберите способ оплаты:",
        reply_markup=get_payment_keyboard()
    )

@dp.callback_query(lambda c: c.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.edit_text(
        "🤖 Главное меню",
        reply_markup=get_main_keyboard(callback.from_user.id in ADMIN_IDS)
    )

@dp.message(Command("admin"))
async def cmd_admin(message: types.Message):
    """Админ-панель"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ У вас нет доступа к этой команде.")
        return
    
    key, expires_at = create_key()
    await message.answer(
        f"🔑 Новый ключ создан:\n\n"
        f"Ключ: `{key}`\n"
        f"Истекает: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}",
        parse_mode="Markdown"
    )

async def main():
    """Запуск бота"""
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        await market_api.close()

if __name__ == "__main__":
    asyncio.run(main()) 