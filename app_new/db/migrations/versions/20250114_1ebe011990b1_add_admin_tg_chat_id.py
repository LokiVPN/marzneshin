"""add admin tg chat id

Revision ID: 1ebe011990b1
Revises: 753601c0a8a5
Create Date: 2025-01-14 12:47:02.144739

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1ebe011990b1"
down_revision = "5cd1b7a60126"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("admins") as batch_op:
        batch_op.add_column(
            sa.Column("telegram_chat_id", sa.Integer(), nullable=True)
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("admins") as batch_op:
        batch_op.drop_column("telegram_chat_id")
    # ### end Alembic commands ###
