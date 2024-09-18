"""Creates tags_channels table

Revision ID: a4d1aaf4812f
Revises: 837c2d2e2921
Create Date: 2024-09-18 09:42:49.351168

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a4d1aaf4812f"
down_revision: Union[str, None] = "837c2d2e2921"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tags_channels",
        sa.Column(
            "channel_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("channels.id"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "tag_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("tags.id"),
            nullable=False,
            primary_key=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("tags_channels")
