"""Creates channels table

Revision ID: ace6bb635253
Revises: 3bdc4107cfc3
Create Date: 2024-09-18 00:29:47.973924

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ace6bb635253"
down_revision: Union[str, None] = "3bdc4107cfc3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("channel_name", sa.String),
        sa.Column("chat_identifier", sa.String),
        sa.Column("api_id", sa.String),
        sa.Column("api_hash", sa.String),
        sa.Column("created_at", sa.DateTime(timezone=True)),
        sa.Column("updated_at", sa.DateTime(timezone=True)),
        sa.Column("profile_id", sa.UUID(as_uuid=True), sa.ForeignKey("profiles.id")),
    )


def downgrade() -> None:
    op.drop_table("channels")
