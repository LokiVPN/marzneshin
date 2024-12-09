"""drop notification reminders table

Revision ID: 79271458a973
Revises: be0032100c07
Create Date: 2024-11-27 04:43:24.448736

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "79271458a973"
down_revision = "be0032100c07"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notification_reminders")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notification_reminders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column(
            "type",
            sa.Enum("expiration_date", "data_usage", name="remindertype"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###
