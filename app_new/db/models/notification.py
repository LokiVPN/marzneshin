from datetime import datetime

from sqlalchemy import (
    UniqueConstraint,
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Boolean,
    sql,
    String,
)
from sqlalchemy.orm import relationship

from app_new.db.models.base import Base


class NotificationTarget(Base):
    __tablename__ = "notifications_targets"
    __table_args__ = (UniqueConstraint("notification_id", "user_id"),)

    notification_id = Column(
        Integer, ForeignKey("notifications.id"), primary_key=True
    )
    notification = relationship("Notification", back_populates="targets")
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User")
    sent_at = Column(DateTime)
    skipped = Column(Boolean, default=False, server_default=sql.false())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    label = Column(String(128), nullable=False, unique=True)
    message = Column(String(1024), nullable=False)
    targets = relationship("NotificationTarget", back_populates="notification")
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)

    @property
    def completed(self):
        return self.finished_at is not None

    @property
    def user_ids(self):
        return [
            target.user.id
            for target in self.targets
            if not target.user.removed
        ]
