"""Add last few columns to the posts table

Revision ID: 06b6cc03af97
Revises: 70a1c0245a3f
Create Date: 2025-10-25 15:31:16.689414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06b6cc03af97'
down_revision: Union[str, Sequence[str], None] = '70a1c0245a3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text('now()')),)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
