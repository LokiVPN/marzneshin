from datetime import datetime

from sqlalchemy import (
    String,
    Integer,
    Boolean,
    Column,
    sql,
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    and_,
    func,
)
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app_new.core.common.user import (
    UserDataUsageResetStrategy,
    UserExpireStrategy,
    UserStatus,
)
from app_new.db.models.base import Base, users_services


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    key = Column(String(64), unique=True)
    activated = Column(Boolean, nullable=False, default=True)
    enabled = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default=sql.true(),
    )
    removed = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=sql.false(),
    )
    services = relationship(
        "Service",
        secondary=users_services,
        back_populates="users",
        lazy="joined",
    )
    inbounds = relationship(
        "Inbound",
        secondary="join(users_services, inbounds_services, inbounds_services.c.service_id == users_services.c.service_id)"
        ".join(Inbound, Inbound.id == inbounds_services.c.inbound_id)",
        viewonly=True,
        distinct_target_key=True,
    )
    used_traffic = Column(BigInteger, default=0)
    lifetime_used_traffic = Column(
        BigInteger, default=0, server_default="0", nullable=False
    )
    traffic_reset_at = Column(DateTime)
    node_usages = relationship(
        "NodeUserUsage",
        back_populates="user",
        cascade="all,delete,delete-orphan",
    )
    data_limit = Column(BigInteger)
    data_limit_reset_strategy = Column(
        Enum(UserDataUsageResetStrategy),
        nullable=False,
        default=UserDataUsageResetStrategy.NO_RESET,
    )
    ip_limit = Column(Integer, nullable=False, default=-1)
    settings = Column(String(1024))
    expire_strategy = Column(
        Enum(UserExpireStrategy),
        nullable=False,
        default=UserExpireStrategy.NEVER,
    )
    expire_date = Column(DateTime)
    usage_duration = Column(BigInteger)
    activation_deadline = Column(DateTime)
    sub_updated_at = Column(DateTime)
    sub_last_user_agent = Column(String(512))
    sub_revoked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    note = Column(String(500))
    online_at = Column(DateTime)
    edit_at = Column(DateTime)

    is_telegram_premium = Column(Boolean, default=False)
    # Foreign key
    invited_by = Column(Integer, ForeignKey("users.id", name="fk_invited_by"))

    @property
    def service_ids(self):
        return [service.id for service in self.services]

    @hybrid_property
    def expired(self):
        if self.expire_strategy == "fixed_date":
            return self.expire_date < datetime.utcnow()
        return False

    @property
    def remaining_days(self):
        if self.expire_date:
            return (self.expire_date - datetime.utcnow()).days
        return None

    @expired.expression
    def expired(cls):
        return and_(
            cls.expire_strategy == "fixed_date", cls.expire_date < func.now()
        )

    @hybrid_property
    def data_limit_reached(self):
        if self.data_limit is not None:
            return self.used_traffic >= self.data_limit
        return False

    @data_limit_reached.expression
    def data_limit_reached(cls):
        return and_(
            cls.data_limit.isnot(None), cls.used_traffic >= cls.data_limit
        )

    @hybrid_property
    def is_active(self):
        return (
            self.enabled
            and not self.expired
            and not self.data_limit_reached
            and not self.removed
        )

    @is_active.expression
    def is_active(cls):
        return and_(
            cls.enabled == True,
            ~cls.expired,
            ~cls.data_limit_reached,
            ~cls.removed,
        )

    @property
    def status(self):
        return UserStatus.ACTIVE if self.is_active else UserStatus.INACTIVE

    @property
    def subscription_url(self):
        return f"/sub/{self.username}/{self.key}"
