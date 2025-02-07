import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
BOT_TOKEN = '6123456789:AAHrXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # Замените на ваш токен

# Пути к JSON файлам
DATA_DIR = 'data'
USERS_FILE = f'{DATA_DIR}/users.json'
KEYS_FILE = f'{DATA_DIR}/keys.json'
SIGNALS_FILE = f'{DATA_DIR}/signals.json'
PAYMENTS_LOG_FILE = f'{DATA_DIR}/payments_log.json'
BLOCKED_USERS_FILE = f'{DATA_DIR}/blocked_users.json'

# База данных
DATABASE_URL = 'postgresql://user:password@localhost/market_ai_bot'

# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost')

# Binance API
BINANCE_API_KEY = 'your_binance_api_key'
BINANCE_API_SECRET = 'your_binance_api_secret'

# Платежные системы
ROBOKASSA_LOGIN = 'your_robokassa_login'
ROBOKASSA_PASSWORD1 = 'your_robokassa_password1'
ROBOKASSA_PASSWORD2 = 'your_robokassa_password2'
ROBOKASSA_TEST_MODE = True

# Stripe
STRIPE_PUBLIC_KEY = 'pk_test_XXXXXXXXXXXXXXXXXXXXXXXX'
STRIPE_SECRET_KEY = 'sk_test_XXXXXXXXXXXXXXXXXXXXXXXX'

# Настройки безопасности
SECRET_KEY = 'your-secret-key-here-make-it-very-long-and-secure'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Настройки веб-приложения
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000

# Поддерживаемые валютные пары
SUPPORTED_PAIRS = [
    'XAU/USD',
    'BTC/USD',
    'EUR/USD',
    'USD/JPY',
    'GBP/USD'
]

# Настройки ключей доступа
KEY_EXPIRATION_MINUTES = 10
MAX_LOGIN_ATTEMPTS = 3
BLOCK_DURATION_HOURS = 24

# Администраторы
ADMIN_IDS = [
    123456789,  # Замените на реальные ID администраторов
]

# Настройки веб-приложения
WEBAPP_URL = 'http://localhost:8000'

# Настройки сигналов
SIGNAL_LIFETIME_HOURS = 24  # Время жизни сигнала
MIN_PROBABILITY = 70  # Минимальная вероятность для сигнала

# Настройки анализа
TECHNICAL_INDICATORS = {
    'RSI_PERIOD': 14,
    'RSI_OVERBOUGHT': 70,
    'RSI_OVERSOLD': 30,
    'MACD_FAST': 12,
    'MACD_SLOW': 26,
    'MACD_SIGNAL': 9,
    'BB_PERIOD': 20,
    'BB_STD': 2
}

# Паттерны рынка
PATTERNS = {
    'DOUBLE_TOP': 'Двойная вершина',
    'DOUBLE_BOTTOM': 'Двойное дно',
    'HEAD_SHOULDERS': 'Голова и плечи',
    'TRIANGLE': 'Треугольник',
    'CHANNEL': 'Канал',
    'FIBONACCI': 'Уровни Фибоначчи'
}

# Настройки AI модели
AI_MODEL = {
    'model_path': 'models/gpt4_trading.onnx',
    'tokenizer_path': 'models/tokenizer.json',
    'max_length': 512,
    'temperature': 0.7,
    'top_p': 0.9
}

# Веб-приложение
WEBAPP_URL = 'https://your-domain.com/webapp'  # Замените на ваш домен
WEBAPP_PORT = 8000 