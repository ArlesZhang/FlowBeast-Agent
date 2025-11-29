import os
import stripe
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from cody_agent.commercial.database import SessionLocal, User, UsageRecord
from datetime import datetime
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class BillingManager:
    TIERS = {"developer": 200.0, "team": 5000.0, "enterprise": float("inf")}

    def get_db(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def record_usage(self, user_id: str, cost: float, task: str):
        db: Session = next(self.get_db())
        record = UsageRecord(
            id=hashlib.md5(str(datetime.utcnow()).encode()).hexdigest(),
            user_id=user_id,
            cost=cost,
            task_hash=hashlib.md5(task.encode()).hexdigest(),
            description=task[:200]
        )
        db.add(record)
        user = db.query(User).filter(User.id == user_id).first()
        user.monthly_usage += float(cost)
        db.commit()

    async def check_and_get_remaining(self, user_id: str) -> dict:
        db: Session = next(self.get_db())
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"allowed": True, "remaining": 200.0}
        limit = self.TIERS[user.tier]
        remaining = max(0, limit - user.monthly_usage)
        return {"allowed": remaining >= 0.1, "remaining": remaining, "tier": user.tier}

    async def generate_invoice_pdf(self, user_id: str, month: str) -> str:
        db: Session = next(self.get_db())
        records = db.query(UsageRecord).filter(UsageRecord.user_id == user_id).all()
        filename = f"invoice_{user_id}_{month}.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 750, f"DataCody Invoice for {month}")
        y = 700
        total = 0
        for record in records:
            c.drawString(100, y, f"{record.timestamp}: Cost {record.cost} - Task {record.description[:50]}")
            total += record.cost
            y -= 20
        c.drawString(100, y - 20, f"Total: ${total:.2f}")
        c.save()
        return filename
