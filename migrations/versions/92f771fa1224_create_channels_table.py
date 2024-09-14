"""Create channels table

Revision ID: 92f771fa1224
Revises: 3bdc4107cfc3
Create Date: 2024-09-13 21:11:58.265177

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "92f771fa1224"
down_revision: Union[str, None] = "3bdc4107cfc3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("chat_identifier", sa.String, nullable=False),
        sa.Column("api_key", sa.String, nullable=True),
        sa.Column("channel_name", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column("deleted_at", sa.DateTime, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("channels")
