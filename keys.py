import json
import os
import random
import string
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from config import (
    DATA_DIR,
    KEY_EXPIRATION_MINUTES,
    MAX_LOGIN_ATTEMPTS,
    BLOCK_DURATION_HOURS
)

# Пути к файлам
ACTIVE_KEYS_FILE = os.path.join(DATA_DIR, 'active_keys.json')
BLOCKED_USERS_FILE = os.path.join(DATA_DIR, 'blocked_users.json')

def ensure_key_files():
    'Проверяет наличие необходимых файлов'
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(ACTIVE_KEYS_FILE):
        with open(ACTIVE_KEYS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    if not os.path.exists(BLOCKED_USERS_FILE):
        with open(BLOCKED_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump({}, f)

def generate_key() -> str:
    'Генерирует новый ключ доступа'
    chars = string.ascii_uppercase + string.digits
    parts = []
    for _ in range(3):
        part = ''.join(random.choice(chars) for _ in range(4))
        parts.append(part)
    return '-'.join(parts)

def save_key(key: str, expires_at: datetime) -> None:
    'Сохраняет ключ в файл'
    ensure_key_files()
    
    with open(ACTIVE_KEYS_FILE, 'r', encoding='utf-8') as f:
        keys = json.load(f)
    
    keys.append({
        'key': key,
        'expires_at': expires_at.isoformat(),
        'is_used': False
    })
    
    with open(ACTIVE_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)

def create_key() -> Tuple[str, datetime]:
    'Создает новый ключ доступа'
    key = generate_key()
    expires_at = datetime.now() + timedelta(minutes=KEY_EXPIRATION_MINUTES)
    save_key(key, expires_at)
    return key, expires_at

def verify_key(key: str) -> bool:
    'Проверяет валидность ключа'
    ensure_key_files()
    
    with open(ACTIVE_KEYS_FILE, 'r', encoding='utf-8') as f:
        keys = json.load(f)
    
    for k in keys:
        if k['key'] == key and not k['is_used']:
            expires_at = datetime.fromisoformat(k['expires_at'])
            if datetime.now() <= expires_at:
                return True
    return False

def mark_key_as_used(key: str) -> None:
    'Помечает ключ как использованный'
    ensure_key_files()
    
    with open(ACTIVE_KEYS_FILE, 'r', encoding='utf-8') as f:
        keys = json.load(f)
    
    for k in keys:
        if k['key'] == key:
            k['is_used'] = True
            break
    
    with open(ACTIVE_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(keys, f, ensure_ascii=False, indent=2)

def cleanup_expired_keys() -> None:
    'Удаляет просроченные ключи'
    ensure_key_files()
    
    with open(ACTIVE_KEYS_FILE, 'r', encoding='utf-8') as f:
        keys = json.load(f)
    
    current_time = datetime.now()
    valid_keys = []
    
    for k in keys:
        expires_at = datetime.fromisoformat(k['expires_at'])
        if current_time <= expires_at:
            valid_keys.append(k)
    
    with open(ACTIVE_KEYS_FILE, 'w', encoding='utf-8') as f:
        json.dump(valid_keys, f, ensure_ascii=False, indent=2)

def is_user_blocked(user_id: int) -> bool:
    'Проверяет, заблокирован ли пользователь'
    ensure_key_files()
    
    with open(BLOCKED_USERS_FILE, 'r', encoding='utf-8') as f:
        blocked = json.load(f)
    
    if str(user_id) in blocked:
        blocked_until = datetime.fromisoformat(blocked[str(user_id)]['blocked_until'])
        if datetime.now() <= blocked_until:
            return True
        else:
            # Если блокировка истекла, удаляем запись
            del blocked[str(user_id)]
            with open(BLOCKED_USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(blocked, f, ensure_ascii=False, indent=2)
    return False

def increment_login_attempts(user_id: int) -> int:
    'Увеличивает счетчик неудачных попыток входа'
    ensure_key_files()
    
    with open(BLOCKED_USERS_FILE, 'r', encoding='utf-8') as f:
        blocked = json.load(f)
    
    user_id_str = str(user_id)
    if user_id_str not in blocked:
        blocked[user_id_str] = {'attempts': 0}
    
    blocked[user_id_str]['attempts'] = blocked[user_id_str].get('attempts', 0) + 1
    
    # Если превышено максимальное количество попыток, блокируем
    if blocked[user_id_str]['attempts'] >= MAX_LOGIN_ATTEMPTS:
        blocked[user_id_str]['blocked_until'] = (
            datetime.now() + timedelta(hours=BLOCK_DURATION_HOURS)
        ).isoformat()
    
    with open(BLOCKED_USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(blocked, f, ensure_ascii=False, indent=2)
    
    return blocked[user_id_str]['attempts']

def reset_login_attempts(user_id: int) -> None:
    'Сбрасывает счетчик неудачных попыток входа'
    ensure_key_files()
    
    with open(BLOCKED_USERS_FILE, 'r', encoding='utf-8') as f:
        blocked = json.load(f)
    
    user_id_str = str(user_id)
    if user_id_str in blocked:
        del blocked[user_id_str]
        
        with open(BLOCKED_USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(blocked, f, ensure_ascii=False, indent=2)

def get_remaining_block_time(user_id: int) -> Optional[timedelta]:
    'Возвращает оставшееся время блокировки'
    ensure_key_files()
    
    with open(BLOCKED_USERS_FILE, 'r', encoding='utf-8') as f:
        blocked = json.load(f)
    
    user_id_str = str(user_id)
    if user_id_str in blocked and 'blocked_until' in blocked[user_id_str]:
        blocked_until = datetime.fromisoformat(blocked[user_id_str]['blocked_until'])
        remaining = blocked_until - datetime.now()
        return remaining if remaining.total_seconds() > 0 else None
    return None

# Инициализация при импорте
ensure_key_files()