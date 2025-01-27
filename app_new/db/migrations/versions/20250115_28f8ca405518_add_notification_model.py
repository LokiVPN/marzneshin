"""add notification model

Revision ID: 28f8ca405518
Revises: 1ebe011990b1
Create Date: 2025-01-15 10:32:24.768681

"""

from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "28f8ca405518"
down_revision = "1ebe011990b1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    notifications = op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=128), nullable=False),
        sa.Column("message", sa.String(length=1024), nullable=False),
        sa.Column(
            "action",
            sa.Enum(
                "user_created",
                "user_updated",
                "user_activated",
                "user_deactivated",
                "user_deleted",
                "user_enabled",
                "user_disabled",
                "data_usage_reset",
                "subscription_revoked",
                "reached_usage_percent",
                "reached_days_left",
                "get_bonus",
                "custom",
                name="action",
            ),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("label"),
    )
    op.create_table(
        "notifications_targets",
        sa.Column("notification_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("sent_at", sa.DateTime(), nullable=True),
        sa.Column(
            "skipped", sa.Boolean(), server_default=sa.text("0"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["notification_id"],
            ["notifications.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("notification_id", "user_id"),
        sa.UniqueConstraint("notification_id", "user_id"),
    )

    now = datetime.utcnow()

    op.bulk_insert(
        notifications,
        [
            {
                "id": 1,
                "label": "user_created",
                "message": "🆕 <b>#Created</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username :</b> <code>{username}</code>\n<b>Traffic Limit :</b> <code>{data_limit}</code>\n<b>Expire Date :</b> <code>{expire_date}</code>\n<b>Services :</b> <code>{services}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>\n<b>By :</b> <b>#{by}</b>",
                "action": "user_created",
                "created_at": now,
            },
            {
                "id": 2,
                "label": "user_updated",
                "message": "✏️ <b>#Modified</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username :</b> <code>{username}</code>\n<b>Traffic Limit :</b> <code>{data_limit}</code>\n<b>Expire Date :</b> <code>{expire_date}</code>\n<b>Services :</b> <code>{services}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>\n<b>By :</b> <b>#{by}</b>",
                "action": "user_updated",
                "created_at": now,
            },
            {
                "id": 3,
                "label": "user_activated",
                "message": "✅ <b>#Activated</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n<b>Belongs To :</b> <code>{owner_username}</code>",
                "action": "user_activated",
                "created_at": now,
            },
            {
                "id": 4,
                "label": "user_deactivated",
                "message": "❌ <b>#Deactivated</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n<b>Belongs To :</b> <code>{owner_username}</code>",
                "action": "user_deactivated",
                "created_at": now,
            },
            {
                "id": 5,
                "label": "user_deleted",
                "message": "🗑 <b>#Deleted</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>\n<b>By :</b> <b>#{by}</b>",
                "action": "user_deleted",
                "created_at": now,
            },
            {
                "id": 6,
                "label": "user_enabled",
                "message": "☑️ <b>#Enabled</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>\n<b>By :</b> <b>#{by}</b>",
                "action": "user_enabled",
                "created_at": now,
            },
            {
                "id": 7,
                "label": "user_disabled",
                "message": "🛑 <b>#Disabled</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>\n<b>By :</b> <b>#{by}</b>",
                "action": "user_disabled",
                "created_at": now,
            },
            {
                "id": 8,
                "label": "data_usage_reset",
                "message": "🔁 <b>#Reset</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n➖➖➖➖➖➖➖➖➖\n<b>By</b> : <b>#{by}</b>",
                "action": "data_usage_reset",
                "created_at": now,
            },
            {
                "id": 9,
                "label": "subscription_revoked",
                "message": "🔁 <b>#Revoked</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n➖➖➖➖➖➖➖➖➖\n<b>By</b> : <b>#{by}</b>",
                "action": "subscription_revoked",
                "created_at": now,
            },
            {
                "id": 10,
                "label": "reached_usage_percent",
                "message": "⚠️<b>#DataLimitWarning</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n<b>Used Percent</b> : <code>{usage_percent}</code>\n<b>Remaining Traffic</b> : <code>{remaining_traffic}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>",
                "action": "reached_usage_percent",
                "created_at": now,
            },
            {
                "id": 11,
                "label": "reached_days_left",
                "message": "⚠️<b>#ExpirationWarning</b>\n➖➖➖➖➖➖➖➖➖\n<b>Username</b> : <code>{username}</code>\n<b>Remaining Days</b> : <code>{remaining_days}</code>\n➖➖➖➖➖➖➖➖➖\n<b>Belongs To :</b> <code>{owner_username}</code>",
                "action": "reached_days_left",
                "created_at": now,
            },
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notifications_targets")
    op.drop_table("notifications")
    # ### end Alembic commands ###
