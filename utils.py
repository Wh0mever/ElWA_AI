from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo
)
from config import ADMIN_IDS
from datetime import datetime
import json
import os
from typing import Dict, List, Optional
from config import (
    DATA_DIR,
    FOREX_PAIRS,
    CRYPTO_PAIRS,
    WEBAPP,
    USER_HISTORY_DIR
)

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Главное меню для авторизованных пользователей"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # Выбор валютных пар (ряд 1)
            [
                InlineKeyboardButton(text="XAU/USD 🟡", callback_data="pair_XAUUSD"),
                InlineKeyboardButton(text="BTC/USD 💰", callback_data="pair_BTCUSD"),
            ],
            [
                InlineKeyboardButton(text="EUR/USD 💶", callback_data="pair_EURUSD"),
                InlineKeyboardButton(text="USD/JPY 💴", callback_data="pair_USDJPY"),
            ],
            [
                InlineKeyboardButton(text="GBP/USD 💷", callback_data="pair_GBPUSD")
            ],
            # Дополнительные разделы
            [
                InlineKeyboardButton(text="📖 История запросов", callback_data="history"),
                InlineKeyboardButton(text="💼 Профиль", callback_data="profile")
            ],
            [
                InlineKeyboardButton(text="🆘 Поддержка", callback_data="support"),
                InlineKeyboardButton(text="💳 Оплатить подписку", callback_data="buy_subscription")
            ]
        ]
    )

def get_unauthorized_keyboard() -> ReplyKeyboardMarkup:
    """Меню для неавторизованных пользователей"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔐 Ввести ключ")],
            [KeyboardButton(text="💳 Купить доступ")],
            [KeyboardButton(text="🆘 Помощь")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Меню оплаты"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇷🇺 Робокасса", 
                    web_app=WebAppInfo(url="https://payment.robokassa.ru")
                ),
                InlineKeyboardButton(
                    text="💳 Stripe", 
                    web_app=WebAppInfo(url="https://checkout.stripe.com")
                )
            ],
            [
                InlineKeyboardButton(
                    text="₿ Криптовалюта", 
                    callback_data="crypto_pay"
                )
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )

def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Меню профиля пользователя"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔄 Обновить подписку", callback_data="renew_subscription"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
            ],
            [
                InlineKeyboardButton(text="🔑 Сменить ключ", callback_data="change_key")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )

def get_history_keyboard() -> InlineKeyboardMarkup:
    """Меню истории запросов"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="<< Предыдущие 5", callback_data="prev_history"),
                InlineKeyboardButton(text="Следующие 5 >>", callback_data="next_history")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )

def get_support_keyboard() -> InlineKeyboardMarkup:
    """Меню поддержки"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📞 Связаться с админом", url=f"tg://user?id={ADMIN_IDS[0]}")
            ],
            [
                InlineKeyboardButton(text="❓ FAQ", callback_data="faq")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )

def get_forex_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для Forex пар"""
    keyboard = []
    for pair_id, pair_info in FOREX_PAIRS.items():
        keyboard.append([
            InlineKeyboardButton(
                text=f"{pair_info['symbol']} {pair_info['emoji']}", 
                callback_data=f"pair_{pair_id}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_crypto_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для криптовалютных пар"""
    keyboard = []
    for pair_id, pair_info in CRYPTO_PAIRS.items():
        keyboard.append([
            InlineKeyboardButton(
                text=f"{pair_info['symbol']} {pair_info['emoji']}", 
                callback_data=f"pair_{pair_id}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру для выбора способа оплаты"""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💳 Оплата картой",
                web_app=WebAppInfo(url=f"{WEBAPP['URL']}/payment")
            )
        ],
        [
            InlineKeyboardButton(text="₿ Криптовалютой", callback_data="pay_crypto")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_profile_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру профиля"""
    keyboard = [
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="profile_stats"),
            InlineKeyboardButton(text="⏰ Подписка", callback_data="profile_sub")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_main")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def ensure_user_history_dir() -> None:
    """Проверяет наличие директории для истории пользователей"""
    if not os.path.exists(USER_HISTORY_DIR):
        os.makedirs(USER_HISTORY_DIR)

def save_user_history(user_id: int, action: str, data: Dict) -> None:
    """Сохраняет действие пользователя в историю"""
    ensure_user_history_dir()
    history_file = os.path.join(USER_HISTORY_DIR, f"{user_id}.json")
    
    history = []
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    
    history.append({
        'timestamp': datetime.now().isoformat(),
        'action': action,
        'data': data
    })
    
    # Оставляем только последние 100 действий
    history = history[-100:]
    
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_user_history(user_id: int, limit: int = 5) -> List[Dict]:
    """Получает историю действий пользователя"""
    history_file = os.path.join(USER_HISTORY_DIR, f"{user_id}.json")
    
    if not os.path.exists(history_file):
        return []
    
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
    
    return history[-limit:]

def format_signal_message(signal_data: Dict) -> str:
    """Форматирует сообщение с сигналом"""
    emoji = "📈" if signal_data["direction"] == "BUY" else "📉"
    return (
        f"{emoji} {signal_data['pair']} | Таймфрейм: H1\n"
        f"➡️ Сигнал: {signal_data['direction']} @ {signal_data['entry_price']}\n"
        f"✅ TP: {signal_data['take_profit']} "
        f"({calculate_percent(signal_data['entry_price'], signal_data['take_profit'])}%)\n"
        f"❌ SL: {signal_data['stop_loss']} "
        f"({calculate_percent(signal_data['entry_price'], signal_data['stop_loss'])}%)\n"
        f"Вероятность: {signal_data['probability']}%\n"
        f"Паттерн: {signal_data['pattern']}"
    )

def calculate_percent(entry: float, target: float) -> str:
    """Рассчитывает процентное изменение"""
    percent = ((target - entry) / entry) * 100
    return f"{percent:.2f}"

async def show_typing(message):
    """Показать анимацию набора текста"""
    await message.answer_chat_action("typing")

async def show_progress(message, current: int, total: int):
    """Показать прогресс анализа"""
    progress = "▓" * current + "░" * (total - current)
    await message.edit_text(
        f"🔄 Анализирую рынок...\n"
        f"[{progress}] {current * 10}%"
    ) 