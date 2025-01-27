from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum
from sqlalchemy.orm import relationship

from app_new.core.common.payment import Currency
from app_new.db.models.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")
    amount = Column(Integer, nullable=False)
    currency = Column(Enum(Currency), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime)
    telegram_payment_charge_id = Column(String(64))
    provider_payment_charge_id = Column(String(64))

    @property
    def completed(self):
        return self.paid_at is not None
