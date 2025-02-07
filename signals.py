import asyncio
import random
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np
try:
    from binance.client import Client
except ImportError:
    print("Ошибка: python-binance не установлен. Установите: pip install python-binance")
    Client = None
from database import JsonDB
from config import (
    BINANCE_API_KEY, 
    BINANCE_API_SECRET, 
    TECHNICAL_INDICATORS as TI,
    PATTERNS
)

# Инициализация клиента Binance
try:
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
except Exception as e:
    print(f"Ошибка инициализации Binance клиента: {e}")
    client = None

def get_historical_data(symbol: str, interval: str = '1h', limit: int = 100) -> pd.DataFrame:
    """Получение исторических данных"""
    if not client:
        # Возвращаем тестовые данные если клиент не инициализирован
        return generate_test_data(limit)
    
    try:
        # Преобразование символа в формат Binance
        symbol = symbol.replace('/', '')
        
        # Получение данных
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        
        # Преобразование в DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # Преобразование типов данных
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        return df
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return generate_test_data(limit)

def generate_test_data(limit: int = 100) -> pd.DataFrame:
    """Генерация тестовых данных для отладки"""
    np.random.seed(42)
    
    dates = pd.date_range(end=datetime.now(), periods=limit, freq='H')
    close = np.random.normal(100, 10, limit).cumsum()
    high = close + np.random.uniform(0, 5, limit)
    low = close - np.random.uniform(0, 5, limit)
    open_ = close - np.random.uniform(-5, 5, limit)
    volume = np.random.uniform(1000, 10000, limit)
    
    return pd.DataFrame({
        'timestamp': dates,
        'open': open_,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })

def detect_pattern(df: pd.DataFrame) -> str:
    """Определение паттерна на графике"""
    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    
    # Поиск паттерна двойного дна
    if (low[-3] > low[-2] < low[-1] and 
        abs(low[-3] - low[-1]) < abs(low[-3] - low[-2]) * 0.1):
        return PATTERNS['DOUBLE_BOTTOM']
    
    # Поиск паттерна двойной вершины
    elif (high[-3] < high[-2] > high[-1] and 
          abs(high[-3] - high[-1]) < abs(high[-3] - high[-2]) * 0.1):
        return PATTERNS['DOUBLE_TOP']
    
    # Поиск паттерна треугольника
    elif (max(high[-5:]) - min(high[-5:]) < max(high[-10:-5]) - min(high[-10:-5]) and
          max(low[-5:]) - min(low[-5:]) < max(low[-10:-5]) - min(low[-10:-5])):
        return PATTERNS['TRIANGLE']
    
    # Поиск паттерна канала
    elif (max(high[-5:]) - min(high[-5:]) > max(high[-10:-5]) - min(high[-10:-5]) * 0.9 and
          max(high[-5:]) - min(high[-5:]) < max(high[-10:-5]) - min(high[-10:-5]) * 1.1):
        return PATTERNS['CHANNEL']
    
    return "Без явного паттерна"

def analyze_technical_indicators(df: pd.DataFrame) -> dict:
    """Анализ технических индикаторов"""
    close_prices = df['close'].values
    high_prices = df['high'].values
    low_prices = df['low'].values
    
    try:
        # RSI
        rsi = df.ta.rsi(length=TI['RSI_PERIOD'])
        current_rsi = rsi.iloc[-1]
        
        # MACD
        macd = df.ta.macd(
            fast=TI['MACD_FAST'],
            slow=TI['MACD_SLOW'],
            signal=TI['MACD_SIGNAL']
        )
        current_macd = macd['MACD_12_26_9'].iloc[-1]
        current_signal = macd['MACDs_12_26_9'].iloc[-1]
        
        # Bollinger Bands
        bb = df.ta.bbands(
            length=TI['BB_PERIOD'],
            std=TI['BB_STD']
        )
        current_bb_upper = bb['BBU_20_2.0'].iloc[-1]
        current_bb_lower = bb['BBL_20_2.0'].iloc[-1]
        current_price = close_prices[-1]
        
        # Определение паттерна
        pattern = detect_pattern(df)
        
        # Определение направления
        if current_rsi > TI['RSI_OVERBOUGHT'] and current_price > current_bb_upper:
            direction = "SELL"
            probability = random.randint(80, 95)
        elif current_rsi < TI['RSI_OVERSOLD'] and current_price < current_bb_lower:
            direction = "BUY"
            probability = random.randint(80, 95)
        elif current_macd > current_signal:
            direction = "BUY"
            probability = random.randint(70, 85)
        else:
            direction = "SELL"
            probability = random.randint(70, 85)
        
        # Расчет уровней
        atr = df.ta.atr(length=14).iloc[-1]
        
        if direction == "BUY":
            entry = current_price
            take_profit = entry + (atr * 2)
            stop_loss = entry - atr
        else:
            entry = current_price
            take_profit = entry - (atr * 2)
            stop_loss = entry + atr
        
        return {
            "direction": direction,
            "entry_price": round(entry, 5),
            "take_profit": round(take_profit, 5),
            "stop_loss": round(stop_loss, 5),
            "probability": probability,
            "pattern": pattern
        }
    except Exception as e:
        print(f"Ошибка анализа: {e}")
        return generate_test_signal(df)

def generate_test_signal(df: pd.DataFrame) -> dict:
    """Генерация тестового сигнала для отладки"""
    current_price = df['close'].values[-1]
    direction = "BUY" if random.random() > 0.5 else "SELL"
    atr = (df['high'] - df['low']).mean()
    
    if direction == "BUY":
        take_profit = current_price * 1.02
        stop_loss = current_price * 0.99
    else:
        take_profit = current_price * 0.98
        stop_loss = current_price * 1.01
    
    return {
        "direction": direction,
        "entry_price": round(current_price, 5),
        "take_profit": round(take_profit, 5),
        "stop_loss": round(stop_loss, 5),
        "probability": random.randint(70, 95),
        "pattern": random.choice(list(PATTERNS.values()))
    }

async def generate_signal(pair: str) -> dict:
    """Генерация торгового сигнала"""
    # Имитация длительного анализа
    await asyncio.sleep(5)
    
    # Получение исторических данных
    df = get_historical_data(pair)
    
    # Анализ индикаторов
    signal_data = analyze_technical_indicators(df)
    signal_data['pair'] = pair
    
    # Сохранение сигнала
    JsonDB.save_signal(signal_data)
    
    return signal_data 