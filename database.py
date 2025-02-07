import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from config import USERS_FILE, KEYS_FILE, SIGNALS_FILE

def ensure_json_files():
    """Создание JSON файлов если они не существуют"""
    default_data = {
        USERS_FILE: {},
        KEYS_FILE: {},
        SIGNALS_FILE: []
    }
    
    for file_path, default_value in default_data.items():
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(default_value, f, ensure_ascii=False, indent=4)

def load_json(file_path: str) -> dict:
    """Загрузка данных из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        ensure_json_files()
        return load_json(file_path)

def save_json(file_path: str, data: dict):
    """Сохранение данных в JSON файл"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, default=str)

class JsonDB:
    @staticmethod
    def get_user(telegram_id: int) -> Optional[dict]:
        """Получение пользователя по telegram_id"""
        users = load_json(USERS_FILE)
        return users.get(str(telegram_id))

    @staticmethod
    def save_user(telegram_id: int, user_data: dict):
        """Сохранение данных пользователя"""
        users = load_json(USERS_FILE)
        users[str(telegram_id)] = user_data
        save_json(USERS_FILE, users)

    @staticmethod
    def get_key(key: str) -> Optional[dict]:
        """Получение ключа доступа"""
        keys = load_json(KEYS_FILE)
        return keys.get(key)

    @staticmethod
    def save_key(key: str, key_data: dict):
        """Сохранение ключа доступа"""
        keys = load_json(KEYS_FILE)
        keys[key] = key_data
        save_json(KEYS_FILE, keys)

    @staticmethod
    def save_signal(signal_data: dict):
        """Сохранение торгового сигнала"""
        signals = load_json(SIGNALS_FILE)
        signal_data['created_at'] = datetime.utcnow().isoformat()
        signals.append(signal_data)
        save_json(SIGNALS_FILE, signals)

    @staticmethod
    def get_signals(pair: Optional[str] = None, limit: int = 10) -> List[dict]:
        """Получение последних сигналов"""
        signals = load_json(SIGNALS_FILE)
        if pair:
            signals = [s for s in signals if s['pair'] == pair]
        return sorted(signals, key=lambda x: x['created_at'], reverse=True)[:limit]

# Создаем файлы при импорте модуля
ensure_json_files() 