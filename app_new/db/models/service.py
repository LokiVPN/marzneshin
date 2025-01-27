from sqlalchemy import String, Integer, Boolean, Column
from sqlalchemy.orm import relationship

from app_new.db.models.base import (
    Base,
    admins_services,
    inbounds_services,
    users_services,
)


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    is_public = Column(Boolean, default=False, nullable=False)
    admins = relationship(
        "Admin", secondary=admins_services, back_populates="services"
    )
    users = relationship(
        "User", secondary=users_services, back_populates="services"
    )
    inbounds = relationship(
        "Inbound", secondary=inbounds_services, back_populates="services"
    )

    @property
    def inbound_ids(self):
        return [inbound.id for inbound in self.inbounds]

    @property
    def user_ids(self):
        return [user.id for user in self.users if not user.removed]
