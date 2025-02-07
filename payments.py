import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import hmac
import requests
import stripe
from config import (
    DATA_DIR,
    ROBOKASSA_LOGIN,
    ROBOKASSA_PASSWORD1,
    ROBOKASSA_PASSWORD2,
    ROBOKASSA_TEST_MODE,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    CRYPTO_ADDRESSES,
    WEBAPP
)

# Инициализация Stripe
stripe.api_key = STRIPE_SECRET_KEY

# Пути к файлам
PAYMENTS_LOG_FILE = os.path.join(DATA_DIR, 'payments_log.json')

def ensure_payment_files():
    """Проверяет наличие необходимых файлов"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(PAYMENTS_LOG_FILE):
        with open(PAYMENTS_LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def log_payment(user_id: int, amount: float, payment_system: str, status: str, details: Dict = None) -> None:
    """Логирует информацию о платеже"""
    ensure_payment_files()
    
    with open(PAYMENTS_LOG_FILE, 'r', encoding='utf-8') as f:
        payments = json.load(f)
    
    payments.append({
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'amount': amount,
        'payment_system': payment_system,
        'status': status,
        'details': details or {}
    })
    
    with open(PAYMENTS_LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(payments, f, ensure_ascii=False, indent=2)

def get_user_payments(user_id: int) -> List[Dict]:
    """Получает историю платежей пользователя"""
    if not os.path.exists(PAYMENTS_LOG_FILE):
        return []
    
    with open(PAYMENTS_LOG_FILE, 'r', encoding='utf-8') as f:
        payments = json.load(f)
    
    return [p for p in payments if p['user_id'] == user_id]

def create_robokassa_link(amount: float, description: str) -> str:
    """Создает ссылку для оплаты через Робокассу"""
    # Формируем подпись
    signature = hashlib.md5(
        f"{ROBOKASSA_LOGIN}:{amount}:0:{ROBOKASSA_PASSWORD1}".encode()
    ).hexdigest()
    
    # Формируем ссылку
    base_url = "https://auth.robokassa.ru/Merchant/Index.aspx"
    params = {
        "MerchantLogin": ROBOKASSA_LOGIN,
        "OutSum": amount,
        "InvId": "0",
        "Description": description,
        "SignatureValue": signature,
        "IsTest": int(ROBOKASSA_TEST_MODE)
    }
    
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base_url}?{query}"

def verify_robokassa_signature(amount: str, inv_id: str, signature: str) -> bool:
    """Проверяет подпись уведомления от Робокассы"""
    expected = hashlib.md5(
        f"{amount}:{inv_id}:{ROBOKASSA_PASSWORD2}".encode()
    ).hexdigest()
    
    return signature.lower() == expected.lower()

async def create_stripe_payment(amount: float, currency: str = 'usd') -> Dict:
    """Создает платеж в Stripe"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Конвертируем в центы
            currency=currency,
            payment_method_types=['card'],
            metadata={'integration_check': 'accept_a_payment'}
        )
        return {
            'client_secret': intent.client_secret,
            'payment_id': intent.id
        }
    except stripe.error.StripeError as e:
        print(f"Ошибка Stripe: {e}")
        return None

def verify_stripe_signature(payload: bytes, sig_header: str) -> bool:
    """Проверяет подпись вебхука от Stripe"""
    try:
        stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return True
    except Exception as e:
        print(f"Ошибка проверки подписи Stripe: {e}")
        return False

async def check_crypto_payment(tx_hash: str, expected_amount: float, currency: str) -> bool:
    """Проверяет криптовалютный платеж"""
    if currency == 'BTC':
        return await check_bitcoin_payment(tx_hash, expected_amount)
    elif currency == 'USDT':
        return await check_usdt_payment(tx_hash, expected_amount)
    return False

async def check_bitcoin_payment(tx_hash: str, expected_amount: float) -> bool:
    """Проверяет Bitcoin транзакцию"""
    try:
        # Получаем информацию о транзакции через Blockchain.info API
        url = f"https://blockchain.info/rawtx/{tx_hash}"
        response = requests.get(url)
        if response.status_code != 200:
            return False
        
        tx_data = response.json()
        
        # Проверяем получателя и сумму
        for output in tx_data['out']:
            if output['addr'] == CRYPTO_ADDRESSES['BTC']:
                amount_btc = output['value'] / 100000000  # Конвертируем сатоши в BTC
                return abs(amount_btc - expected_amount) < 0.00001
        
        return False
    except Exception as e:
        print(f"Ошибка проверки Bitcoin платежа: {e}")
        return False

async def check_usdt_payment(tx_hash: str, expected_amount: float) -> bool:
    """Проверяет USDT транзакцию"""
    try:
        # Получаем информацию о транзакции через Etherscan API
        # Примечание: требуется API ключ Etherscan для продакшена
        url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}"
        response = requests.get(url)
        if response.status_code != 200:
            return False
        
        tx_data = response.json()
        if tx_data['status'] != '1':
            return False
        
        # Проверяем получателя и сумму
        # Примечание: требуется декодирование данных USDT контракта
        return True  # Упрощенная проверка для примера
    except Exception as e:
        print(f"Ошибка проверки USDT платежа: {e}")
        return False

# Инициализация при импорте
ensure_payment_files() 