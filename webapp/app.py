import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import stripe
from config import (
    WEBAPP,
    STRIPE_PUBLIC_KEY,
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET
)

# Инициализация FastAPI
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=WEBAPP['CORS_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")
templates = Jinja2Templates(directory="webapp/templates")

# Инициализация Stripe
stripe.api_key = STRIPE_SECRET_KEY

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    'Главная страница'
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "stripe_public_key": STRIPE_PUBLIC_KEY}
    )

@app.get("/payment", response_class=HTMLResponse)
async def payment_page(request: Request):
    'Страница оплаты'
    return templates.TemplateResponse(
        "payment.html",
        {"request": request, "stripe_public_key": STRIPE_PUBLIC_KEY}
    )

@app.post("/create-payment-intent")
async def create_payment(request: Request):
    'Создание платежа в Stripe'
    try:
        data = await request.json()
        intent = stripe.PaymentIntent.create(
            amount=data['amount'],
            currency='usd',
            payment_method_types=['card']
        )
        return {"clientSecret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/webhook")
async def webhook_received(request: Request):
    'Обработка вебхуков от Stripe'
    webhook_secret = STRIPE_WEBHOOK_SECRET
    request_data = await request.body()
    
    if webhook_secret:
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request_data,
                sig_header=signature,
                secret=webhook_secret
            )
            event_data = event['data']
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        event_type = event['type']
    else:
        try:
            event_data = json.loads(request_data)
            event_type = event_data['type']
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    
    return {"status": "success"}

@app.get("/success")
async def success_page(request: Request):
    'Страница успешной оплаты'
    return templates.TemplateResponse(
        "success.html",
        {"request": request}
    )

@app.get("/cancel")
async def cancel_page(request: Request):
    'Страница отмены оплаты'
    return templates.TemplateResponse(
        "cancel.html",
        {"request": request}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=WEBAPP['PORT'],
        reload=True
    ) 