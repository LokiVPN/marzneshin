"""unbound host

Revision ID: 57eba0a293f2
Revises: 982867b533e6
Create Date: 2024-12-18 20:22:11.860923

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "57eba0a293f2"
down_revision = "982867b533e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "hosts_services",
        sa.Column("host_id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["host_id"],
            ["hosts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["service_id"],
            ["services.id"],
        ),
        sa.PrimaryKeyConstraint("host_id", "service_id"),
    )
    op.add_column(
        "hosts",
        sa.Column("host_protocol", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "hosts", sa.Column("host_network", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "hosts", sa.Column("uuid", sa.String(length=36), nullable=True)
    )
    op.add_column(
        "hosts", sa.Column("password", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "hosts", sa.Column("header_type", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "hosts",
        sa.Column("reality_public_key", sa.String(length=128), nullable=True),
    )
    op.add_column(
        "hosts", sa.Column("reality_short_ids", sa.JSON(), nullable=True)
    )
    op.add_column(
        "hosts", sa.Column("flow", sa.String(length=32), nullable=True)
    )
    op.add_column(
        "hosts", sa.Column("shadowtls_version", sa.Integer(), nullable=True)
    )
    op.add_column(
        "hosts",
        sa.Column("shadowsocks_method", sa.String(length=32), nullable=True),
    )
    op.add_column(
        "hosts", sa.Column("splithttp_settings", sa.JSON(), nullable=True)
    )
    op.drop_column("hosts", "mux")
    op.add_column("hosts", sa.Column("mux_settings", sa.JSON(), nullable=True))
    op.add_column(
        "hosts", sa.Column("early_data", sa.Integer(), nullable=True)
    )
    op.add_column(
        "hosts",
        sa.Column(
            "universal",
            sa.Boolean(),
            server_default=sa.sql.false(),
            nullable=False,
        ),
    )
    if op.get_bind().dialect.name == "sqlite":
        op.add_column(
            "hosts", sa.Column("inbound_id_new", sa.Integer, nullable=True)
        )

        # Copy data from the old column to the new column
        op.execute(
            """
            UPDATE hosts
            SET inbound_id_new = inbound_id
            """
        )

        # Drop the old column (SQLite requires recreating the table for this step)
        with op.batch_alter_table("hosts") as batch_op:
            batch_op.drop_column("inbound_id")

        # Rename the new column to the old column's name
        op.alter_column(
            "hosts", "inbound_id_new", new_column_name="inbound_id"
        )
    else:
        op.alter_column(
            "hosts", "inbound_id", existing_type=sa.INTEGER(), nullable=True
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("hosts", "universal")
    op.drop_column("hosts", "early_data")
    op.add_column(
        "hosts",
        sa.Column(
            "mux", sa.Boolean(), server_default=sa.sql.true(), nullable=False
        ),
    )
    op.drop_column("hosts", "mux_settings")
    op.drop_column("hosts", "splithttp_settings")
    op.drop_column("hosts", "shadowsocks_method")
    op.drop_column("hosts", "shadowtls_version")
    op.drop_column("hosts", "flow")
    op.drop_column("hosts", "reality_short_ids")
    op.drop_column("hosts", "reality_public_key")
    op.drop_column("hosts", "header_type")
    op.drop_column("hosts", "password")
    op.drop_column("hosts", "uuid")
    op.drop_column("hosts", "host_network")
    op.drop_column("hosts", "host_protocol")
    op.drop_table("hosts_services")
    if op.get_bind().dialect.name == "sqlite":
        op.add_column(
            "hosts", sa.Column("inbound_id_old", sa.Integer, nullable=False)
        )

        # Copy data from the new column back to the old column
        op.execute(
            """
            UPDATE hosts
            SET inbound_id_old = inbound_id
            """
        )

        # Drop the modified column
        with op.batch_alter_table("hosts") as batch_op:
            batch_op.drop_column("inbound_id")

        # Rename the old column back to the original name
        op.alter_column(
            "hosts", "inbound_id_old", new_column_name="inbound_id"
        )
    else:
        op.alter_column(
            "hosts", "inbound_id", existing_type=sa.INTEGER(), nullable=False
        )
    # ### end Alembic commands ###
