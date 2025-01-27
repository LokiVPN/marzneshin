from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, sql, DateTime

from app_new.db.models.base import Base


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True)
    telegram_chat_id = Column(Integer, unique=True, index=True)
    username = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(128))
    enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=sql.true(),
    )
    all_services_access = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=sql.false(),
    )
    modify_users_access = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=sql.true(),
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sudo = Column(Boolean, default=False)
    password_reset_at = Column(DateTime)
