import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import aiohttp
import pandas as pd
try:
    from binance.client import Client as BinanceClient
except ImportError:
    print("Binance client не установлен. Выполните: pip install python-binance")
    BinanceClient = None
from config import (
    BINANCE_API_KEY,
    BINANCE_API_SECRET,
    OANDA_API_KEY,
    ALPHA_VANTAGE_API_KEY,
    FOREX_PAIRS,
    CRYPTO_PAIRS
)

# Инициализация клиентов
binance_client = None
if BinanceClient:
    try:
        binance_client = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
    except Exception as e:
        print(f"Ошибка инициализации Binance клиента: {e}")

class MarketAPI:
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_timeout = 60  # секунды
    
    async def ensure_session(self):
        'Проверяет наличие сессии и создает новую если нужно'
        if self.session is None:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        'Закрывает сессию'
        if self.session:
            await self.session.close()
            self.session = None
    
    def is_cache_valid(self, key: str) -> bool:
        'Проверяет валидность кэша'
        if key not in self.cache:
            return False
        
        cache_time = self.cache[key]['timestamp']
        if datetime.now() - cache_time > timedelta(seconds=self.cache_timeout):
            return False
        
        return True
    
    async def get_forex_data(self, symbol: str, interval: str = '1h', limit: int = 100) -> pd.DataFrame:
        'Получает данные Forex'
        # Пробуем OANDA
        try:
            data = await self._get_oanda_data(symbol, interval, limit)
            if data is not None:
                return data
        except Exception as e:
            print(f"Ошибка OANDA API: {e}")
        
        # Если OANDA не работает, используем Alpha Vantage
        try:
            return await self._get_alpha_vantage_data(symbol, interval, limit)
        except Exception as e:
            print(f"Ошибка Alpha Vantage API: {e}")
            return self._generate_test_data(limit)
    
    async def get_crypto_data(self, symbol: str, interval: str = '1h', limit: int = 100) -> pd.DataFrame:
        'Получает данные криптовалют'
        if not binance_client:
            return self._generate_test_data(limit)
        
        try:
            # Преобразуем символ в формат Binance
            symbol = symbol.replace('/', '')
            
            # Получаем данные
            klines = binance_client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
            
            # Преобразуем в DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ])
            
            # Преобразуем типы данных
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            return df
        except Exception as e:
            print(f"Ошибка Binance API: {e}")
            return self._generate_test_data(limit)
    
    async def _get_oanda_data(self, symbol: str, interval: str, limit: int) -> Optional[pd.DataFrame]:
        'Получает данные через OANDA API'
        await self.ensure_session()
        
        # Формируем URL
        base_url = "https://api-fxtrade.oanda.com/v3"
        endpoint = f"/instruments/{symbol}/candles"
        
        # Параметры запроса
        params = {
            'granularity': interval.upper(),
            'count': limit
        }
        
        # Заголовки
        headers = {
            'Authorization': f'Bearer {OANDA_API_KEY}',
            'Accept-Datetime-Format': 'RFC3339'
        }
        
        async with self.session.get(f"{base_url}{endpoint}", params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                # Преобразуем в DataFrame
                candles = []
                for candle in data['candles']:
                    candles.append({
                        'timestamp': pd.to_datetime(candle['time']),
                        'open': float(candle['mid']['o']),
                        'high': float(candle['mid']['h']),
                        'low': float(candle['mid']['l']),
                        'close': float(candle['mid']['c']),
                        'volume': float(candle['volume'])
                    })
                
                return pd.DataFrame(candles)
            
            return None
    
    async def _get_alpha_vantage_data(self, symbol: str, interval: str, limit: int) -> pd.DataFrame:
        'Получает данные через Alpha Vantage API'
        await self.ensure_session()
        
        # Формируем URL
        base_url = "https://www.alphavantage.co/query"
        
        # Параметры запроса
        params = {
            'function': 'FX_INTRADAY' if interval.endswith('m') else 'FX_DAILY',
            'from_symbol': symbol.split('/')[0],
            'to_symbol': symbol.split('/')[1],
            'interval': interval if interval.endswith('m') else None,
            'apikey': ALPHA_VANTAGE_API_KEY,
            'outputsize': 'compact'
        }
        
        async with self.session.get(base_url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                
                # Получаем временной ряд
                time_series = data.get(
                    f"Time Series FX ({interval})" if interval.endswith('m')
                    else "Time Series FX (Daily)"
                )
                
                if not time_series:
                    return self._generate_test_data(limit)
                
                # Преобразуем в DataFrame
                df = pd.DataFrame.from_dict(time_series, orient='index')
                df.index = pd.to_datetime(df.index)
                df.columns = ['open', 'high', 'low', 'close', 'volume']
                
                # Преобразуем типы данных
                for col in df.columns:
                    df[col] = df[col].astype(float)
                
                return df.iloc[-limit:]
            
            return self._generate_test_data(limit)
    
    def _generate_test_data(self, limit: int = 100) -> pd.DataFrame:
        'Генерирует тестовые данные'
        import numpy as np
        
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

# Создаем глобальный экземпляр API
market_api = MarketAPI() 