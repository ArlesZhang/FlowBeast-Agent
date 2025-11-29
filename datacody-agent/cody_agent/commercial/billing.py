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
        """记录用户使用量，如果用户不存在则自动创建用户记录"""
        user = await self.get_user_by_email(user_id)
        if user is None:
            # 如果用户不存在，创建一个新的用户记录
            from datetime import datetime
            user = User(
                email=user_id,
                tier="team",
                monthly_usage=0.0,
                total_usage=0.0,
                created_at=datetime.utcnow()
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
        
        # 更新使用量
        user.monthly_usage += float(cost)
        user.total_usage += float(cost)
        self.db.add(user)
        await self.db.commit()

    async def get_user_by_email(self, email: str):
        """根据邮箱获取用户记录"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

import os
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from cody_agent.commercial.database import SessionLocal, User, UsageRecord

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class BillingManager:
    TIERS = {"developer": 200.0, "team": 5000.0, "enterprise": float("inf")}

    def __init__(self):
        """初始化 BillingManager，创建数据库会话"""
        self.db = SessionLocal()

    def get_db(self):
        """数据库会话生成器"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_user_by_email(self, email: str):
        """根据邮箱获取用户记录"""
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def record_usage(self, user_id: str, cost: float, task: str):
        """记录用户使用量，如果用户不存在则自动创建用户记录"""
        user = self.get_user_by_email(user_id)
        
        if user is None:
            # 如果用户不存在，创建一个新的用户记录
            user = User(
                email=user_id,
                tier="team",
                monthly_usage=0.0,
                total_usage=0.0,
                created_at=datetime.utcnow()
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        
        # 更新使用量
        user.monthly_usage += float(cost)
        user.total_usage += float(cost)
        
        # 创建使用记录
        record = UsageRecord(
            user_id=user_id,
            cost=cost,
            task_hash=hashlib.md5(task.encode()).hexdigest(),
            description=task[:200]
        )
        self.db.add(record)
        self.db.commit()

    def generate_invoice_pdf(self, user_email: str, month: str):
        """生成用户的发票PDF"""
        user = self.get_user_by_email(user_email)
        if not user:
            raise ValueError(f"用户 {user_email} 不存在")
        
        filename = f"invoice_{user_email.replace('@', '_')}_{month}.pdf"
        filepath = f"/tmp/{filename}"
        
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        c.drawString(100, height - 100, f"DataCody Invoice")
        c.drawString(100, height - 130, f"用户: {user_email}")
        c.drawString(100, height - 160, f"计费周期: {month}")
        c.drawString(100, height - 190, f"月使用量: {user.monthly_usage:.2f} 单位")
        c.drawString(100, height - 220, f"套餐: {user.tier}")
        
        c.save()
        
        return filename
def record_usage(self, user_id: str, cost: float, task: str):
    """记录用户使用量，如果用户不存在则自动创建用户记录"""
    user = self.get_user_by_email(user_id)
    
    if user is None:
        # 如果用户不存在，创建一个新的用户记录
        user = User(
            email=user_id,
            tier="team",
            monthly_usage=0.0,
            created_at=datetime.utcnow()
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
    
    # 更新使用量
    user.monthly_usage += float(cost)
    
    # 如果用户模型支持 total_usage 属性，则更新它
    if hasattr(user, 'total_usage'):
        user.total_usage += float(cost)
    
    # 创建使用记录
    record = UsageRecord(
        user_id=user_id,
        cost=cost,
        task_hash=hashlib.md5(task.encode()).hexdigest(),
        description=task[:200]
    )
    self.db.add(record)
    self.db.commit()
import os
import stripe
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select # 用于同步查询
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from cody_agent.commercial.database import SessionLocal, User, UsageRecord

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class BillingManager:
    TIERS = {"developer": 200.0, "team": 5000.0, "enterprise": float("inf")}

    def __init__(self):
        """初始化 BillingManager，创建数据库会话"""
        # 修复 1: 确保 self.db 存在
        self.db = SessionLocal()

    def get_db(self):
        """数据库会话生成器 (同步)"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_user_by_email(self, email: str):
        """根据邮箱获取用户记录 (同步)"""
        user = self.db.query(User).filter(User.email == email).first()
        return user

    def record_usage(self, user_id: str, cost: float, task: str):
        """记录用户使用量，如果用户不存在则自动创建用户记录 (同步)"""
        user = self.get_user_by_email(user_id)
        
        if user is None:
            # 修复 2: 移除 total_usage=0.0，因为它导致了 TypeError
            user = User(
                email=user_id,
                tier="team",
                monthly_usage=0.0,
                created_at=datetime.utcnow()
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        
        # 更新使用量
        user.monthly_usage += float(cost)
        
        # 稳健性修复：如果模型支持 total_usage 属性，则更新它
        if hasattr(user, 'total_usage'):
            user.total_usage += float(cost)
        
        # 创建使用记录
        record = UsageRecord(
            user_id=user_id,
            cost=cost,
            task_hash=hashlib.md5(task.encode()).hexdigest(),
            description=task[:200]
        )
        self.db.add(record)
        self.db.commit()

    def generate_invoice_pdf(self, user_email: str, month: str):
        """生成用户的发票PDF (同步)"""
        user = self.get_user_by_email(user_email)
        if not user:
            raise ValueError(f"用户 {user_email} 不存在")
        
        filename = f"invoice_{user_email.replace('@', '_')}_{month}.pdf"
        filepath = f"/tmp/{filename}"
        
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        c.drawString(100, height - 100, f"DataCody Invoice")
        c.drawString(100, height - 130, f"用户: {user_email}")
        c.drawString(100, height - 160, f"计费周期: {month}")
        c.drawString(100, height - 190, f"月使用量: {user.monthly_usage:.2f} 单位")
        c.drawString(100, height - 220, f"套餐: {user.tier}")
        
        c.save()
        
        return filename
import os
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from cody_agent.commercial.database import SessionLocal, User, UsageRecord

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

class BillingManager:
    TIERS = {"developer": 200.0, "team": 5000.0, "enterprise": float("inf")}

    def __init__(self):
        """初始化 BillingManager，创建数据库会话"""
        self.db = SessionLocal()

    def get_db(self):
        """数据库会话生成器"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def get_user_by_email(self, email: str):
        """根据邮箱获取用户记录"""
        return self.db.query(User).filter(User.email == email).first()

    def record_usage(self, user_id: str, cost: float, task: str):
        """记录用户使用量，如果用户不存在则自动创建用户记录"""
        user = self.get_user_by_email(user_id)
        
        if user is None:
            # 如果用户不存在，创建一个新的用户记录
            # 只使用 User 模型构造函数接受的参数
            user = User(
                email=user_id,
                tier="team",
                monthly_usage=0.0,
                created_at=datetime.utcnow()
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        
        # 更新使用量
        user.monthly_usage += float(cost)
        
        # 如果用户模型有 total_usage 属性，则更新它
        if hasattr(user, 'total_usage'):
            user.total_usage += float(cost)
        
        # 创建使用记录
        record = UsageRecord(
            user_id=user_id,
            cost=cost,
            task_hash=hashlib.md5(task.encode()).hexdigest(),
            description=task[:200]
        )
        self.db.add(record)
        self.db.commit()

    def generate_invoice_pdf(self, user_email: str, month: str):
        """生成用户的发票PDF"""
        user = self.get_user_by_email(user_email)
        if not user:
            raise ValueError(f"用户 {user_email} 不存在")
        
        filename = f"invoice_{user_email.replace('@', '_')}_{month}.pdf"
        filepath = f"/tmp/{filename}"
        
        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter
        
        c.drawString(100, height - 100, f"DataCody Invoice")
        c.drawString(100, height - 130, f"用户: {user_email}")
        c.drawString(100, height - 160, f"计费周期: {month}")
        c.drawString(100, height - 190, f"月使用量: {user.monthly_usage:.2f} 单位")
        c.drawString(100, height - 220, f"套餐: {user.tier}")
        
        c.save()
        
        return filename
