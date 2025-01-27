import os
from sqlalchemy import String, Integer, Column, JSON, BigInteger, text
from app_new.db.models.base import Base


class System(Base):
    __tablename__ = "system"

    id = Column(Integer, primary_key=True)
    uplink = Column(BigInteger, default=0)
    downlink = Column(BigInteger, default=0)


class JWT(Base):
    __tablename__ = "jwt"

    id = Column(Integer, primary_key=True)
    secret_key = Column(
        String(64), nullable=False, default=lambda: os.urandom(32).hex()
    )


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, server_default=text("0"))
    subscription = Column(JSON, nullable=False)
    telegram = Column(JSON)


class TLS(Base):
    __tablename__ = "tls"

    id = Column(Integer, primary_key=True)
    key = Column(String(4096), nullable=False)
    certificate = Column(String(2048), nullable=False)
