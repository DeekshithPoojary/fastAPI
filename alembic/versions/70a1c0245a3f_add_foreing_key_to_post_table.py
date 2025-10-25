"""Add foreing key to post table

Revision ID: 70a1c0245a3f
Revises: 82c2c59227f5
Create Date: 2025-10-25 15:19:35.964779

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70a1c0245a3f'
down_revision: Union[str, Sequence[str], None] = '82c2c59227f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table = "posts", referent_table = "users", local_cols = ['owner_id'], remote_cols = ['id'], ondelete = "CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
