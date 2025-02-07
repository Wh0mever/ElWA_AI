import random
import string
from datetime import datetime, timedelta
from typing import Tuple
from database import JsonDB
from config import KEY_EXPIRATION_MINUTES, MAX_LOGIN_ATTEMPTS, BLOCK_DURATION_HOURS

def generate_access_key() -> str:
    """Генерация уникального ключа доступа в формате XXXX-XXXX-XXXX"""
    chars = string.ascii_uppercase + string.digits
    sections = []
    
    for _ in range(3):
        section = ''.join(random.choice(chars) for _ in range(4))
        sections.append(section)
    
    return '-'.join(sections)

def create_access_key() -> str:
    """Создание нового ключа доступа"""
    while True:
        key = generate_access_key()
        if not JsonDB.get_key(key):
            break
    
    expires_at = (datetime.utcnow() + timedelta(minutes=KEY_EXPIRATION_MINUTES)).isoformat()
    key_data = {
        'created_at': datetime.utcnow().isoformat(),
        'expires_at': expires_at,
        'is_used': False,
        'user_id': None
    }
    
    JsonDB.save_key(key, key_data)
    return key

def validate_access_key(key: str, telegram_id: int) -> Tuple[bool, str]:
    """Проверка ключа доступа и привязка к пользователю"""
    # Проверяем блокировку пользователя
    user = JsonDB.get_user(telegram_id)
    if user and user.get('is_blocked', False):
        blocked_until = datetime.fromisoformat(user['blocked_until'])
        if blocked_until > datetime.utcnow():
            return False, "⛔️ Ваш аккаунт заблокирован. Попробуйте позже."
        else:
            user['is_blocked'] = False
            user['login_attempts'] = 0
            JsonDB.save_user(telegram_id, user)

    # Проверяем ключ
    key_data = JsonDB.get_key(key)
    if not key_data:
        handle_failed_attempt(telegram_id)
        return False, "❌ Неверный ключ! Попробуйте еще раз."

    if key_data['is_used']:
        return False, "⚠️ Этот ключ уже использован."

    expires_at = datetime.fromisoformat(key_data['expires_at'])
    if expires_at < datetime.utcnow():
        return False, "⏰ Срок действия ключа истек."

    # Создаем или обновляем пользователя
    if not user:
        user = {
            'created_at': datetime.utcnow().isoformat(),
            'is_active': True,
            'login_attempts': 0,
            'is_blocked': False,
            'blocked_until': None
        }
    
    user['last_activity'] = datetime.utcnow().isoformat()
    JsonDB.save_user(telegram_id, user)

    # Обновляем ключ
    key_data['is_used'] = True
    key_data['user_id'] = telegram_id
    JsonDB.save_key(key, key_data)

    return True, "✅ Ключ успешно активирован!"

def handle_failed_attempt(telegram_id: int):
    """Обработка неудачной попытки ввода ключа"""
    user = JsonDB.get_user(telegram_id)
    if not user:
        user = {
            'created_at': datetime.utcnow().isoformat(),
            'is_active': False,
            'login_attempts': 1,
            'is_blocked': False,
            'blocked_until': None
        }
    else:
        user['login_attempts'] = user.get('login_attempts', 0) + 1
        if user['login_attempts'] >= MAX_LOGIN_ATTEMPTS:
            user['is_blocked'] = True
            user['blocked_until'] = (datetime.utcnow() + 
                                   timedelta(hours=BLOCK_DURATION_HOURS)).isoformat()
    
    JsonDB.save_user(telegram_id, user)

def check_user_access(telegram_id: int) -> bool:
    """Проверка доступа пользователя к боту"""
    user = JsonDB.get_user(telegram_id)
    return bool(user and user.get('is_active', False)) 