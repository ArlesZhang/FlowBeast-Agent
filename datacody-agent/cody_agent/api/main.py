from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from cody_agent.api.middleware.auth import get_current_user, create_access_token
from cody_agent.compiler.core import CommercialCompiler
from cody_agent.commercial.billing import BillingManager
from pydantic import BaseModel
from datetime import datetime
import stripe
import os

# ==================== FastAPI App ====================
app = FastAPI(title="DataCody Commercial API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

compiler = CommercialCompiler()
billing = BillingManager()

# ==================== Models ====================
class Task(BaseModel):
    task: str
    project_id: str = None

class Login(BaseModel):
    email: str
    password: str

# ==================== Routes ====================
@app.post("/v1/auth/login")
async def login(form: Login):
    # 模拟登录，直接返回 token（生产环境请接入真实用户系统）
    token = create_access_token({"sub": form.email, "tier": "team"})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/v1/compile")
async def compile(task: Task, user = Depends(get_current_user)):
    result = await compiler.compile_with_billing(
        task=task.task,
        user_id=user["sub"],
        tier=user.get("tier", "developer"),
        project_id=task.project_id
    )
    return result

@app.post("/v1/billing/checkout")
async def checkout(user = Depends(get_current_user)):
    session = stripe.checkout.Session.create(
        customer_email=user["sub"],
        payment_method_types=["card"],
        line_items=[{"price": "price_1Q...", "quantity": 1}],  # 替换成你的 Price ID
        mode="subscription",
        success_url="https://datacody.ai/success",
        cancel_url="https://datacody.ai/cancel"
    )
    return {"url": session.url}

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request): # <-- 关键：添加函数定义和 request 参数
    payload = await request.body()         # <-- 关键：修复缩进为 4 个空格
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        if event["type"] == "checkout.session.completed":
            print("Payment succeeded!")
        return {"status": "success"}
    except Exception as e:
        print(e)
        return {"status": "error"}, 400

@app.get("/v1/billing/invoice")
async def invoice(month: str = None, user = Depends(get_current_user)):
    month_str = month or datetime.now().strftime("%Y-%m")
    pdf_path = await billing.generate_invoice_pdf(user["sub"], month_str)
    return {"invoice_url": f"/invoices/{pdf_path}"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "DataCody Commercial API"}
