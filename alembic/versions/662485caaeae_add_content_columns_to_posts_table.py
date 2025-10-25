"""Add content columns to posts table

Revision ID: 662485caaeae
Revises: 477278e6da14
Create Date: 2025-10-25 15:02:44.150280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '662485caaeae'
down_revision: Union[str, Sequence[str], None] = '477278e6da14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'Content')

    pass
