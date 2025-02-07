import json
import os
from typing import Dict, List, Optional, Union
import numpy as np
import pandas as pd
from config import (
    DATA_DIR,
    AI_MODEL,
    TECHNICAL_INDICATORS,
    PATTERNS
)

class AIModel:
    def __init__(self):
        'Инициализация AI модели'
        self.model = None
        self.tokenizer = None
        self.initialized = False
        
        # Загружаем модель при первом использовании
        # self.load_model()
    
    def load_model(self) -> None:
        'Загрузка модели и токенизатора'
        try:
            # Здесь должна быть загрузка модели
            # В данном примере мы используем заглушку
            self.initialized = True
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
    
    def ensure_model_loaded(self) -> None:
        'Проверяет, загружена ли модель'
        if not self.initialized:
            self.load_model()
    
    def preprocess_data(self, df: pd.DataFrame) -> np.ndarray:
        'Подготовка данных для модели'
        # Нормализация
        data = df.copy()
        for col in ['open', 'high', 'low', 'close', 'volume']:
            mean = data[col].mean()
            std = data[col].std()
            data[col] = (data[col] - mean) / std
        
        # Добавление технических индикаторов
        data['rsi'] = self._calculate_rsi(df['close'])
        data['macd'], data['signal'] = self._calculate_macd(df['close'])
        data['upper'], data['middle'], data['lower'] = self._calculate_bollinger_bands(df['close'])
        
        return data.values

    def analyze_pattern(self, data: np.ndarray) -> Dict[str, float]:
        'Анализ паттернов'
        # В реальности здесь должен быть анализ через нейросеть
        # Сейчас возвращаем случайные вероятности для демонстрации
        patterns = {}
        for pattern in PATTERNS.values():
            patterns[pattern] = np.random.uniform(0, 1)
        return patterns

    def predict_direction(self, data: np.ndarray) -> Dict[str, float]:
        'Предсказание направления движения'
        self.ensure_model_loaded()
        
        # В реальности здесь должно быть предсказание через нейросеть
        # Сейчас возвращаем случайное предсказание для демонстрации
        probabilities = {
            'BUY': np.random.uniform(0.4, 0.6),
            'SELL': np.random.uniform(0.4, 0.6)
        }
        
        # Нормализуем вероятности
        total = sum(probabilities.values())
        for k in probabilities:
            probabilities[k] /= total
        
        return probabilities

    def calculate_levels(self, current_price: float, direction: str) -> Dict[str, float]:
        'Расчет уровней входа, стоп-лосса и тейк-профита'
        # Используем ATR-подобный подход для определения уровней
        volatility = np.random.uniform(0.01, 0.03)  # В реальности нужно считать ATR
        
        if direction == 'BUY':
            entry = current_price
            stop_loss = entry * (1 - volatility)
            take_profit = entry * (1 + volatility * 2)
        else:
            entry = current_price
            stop_loss = entry * (1 + volatility)
            take_profit = entry * (1 - volatility * 2)
        
        return {
            'entry': round(entry, 5),
            'stop_loss': round(stop_loss, 5),
            'take_profit': round(take_profit, 5)
        }

    def generate_signal(self, df: pd.DataFrame) -> Dict:
        'Генерация торгового сигнала'
        # Подготовка данных
        data = self.preprocess_data(df)
        
        # Анализ паттернов
        patterns = self.analyze_pattern(data)
        most_likely_pattern = max(patterns.items(), key=lambda x: x[1])
        
        # Предсказание направления
        probabilities = self.predict_direction(data)
        direction = max(probabilities.items(), key=lambda x: x[1])
        
        # Расчет уровней
        current_price = df['close'].iloc[-1]
        levels = self.calculate_levels(current_price, direction[0])
        
        return {
            'direction': direction[0],
            'probability': round(direction[1] * 100),
            'pattern': most_likely_pattern[0],
            'pattern_probability': round(most_likely_pattern[1] * 100),
            'entry_price': levels['entry'],
            'stop_loss': levels['stop_loss'],
            'take_profit': levels['take_profit'],
            'timestamp': pd.Timestamp.now().isoformat()
        }

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        'Расчет RSI'
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        'Расчет MACD'
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20, std: int = 2) -> tuple:
        'Расчет полос Боллинджера'
        middle = prices.rolling(window=period).mean()
        upper = middle + (prices.rolling(window=period).std() * std)
        lower = middle - (prices.rolling(window=period).std() * std)
        return upper, middle, lower

# Создаем глобальный экземпляр модели
ai_model = AIModel()