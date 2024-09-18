"""Creates tags table

Revision ID: 837c2d2e2921
Revises: ace6bb635253
Create Date: 2024-09-18 04:38:40.344485

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "837c2d2e2921"
down_revision: Union[str, None] = "ace6bb635253"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tags",
        sa.Column(
            "id",
            sa.UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column(
            "profile_id",
            sa.UUID(as_uuid=True),
            sa.ForeignKey("profiles.id"),
        ),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("tags")
