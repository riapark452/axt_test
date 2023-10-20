"""init

Revision ID: 25dc50df906c
Revises: 
Create Date: 2023-10-20 03:24:25.690323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '25dc50df906c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('auth_refresh_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('auth_refresh_token',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(), nullable=False),
    sa.Column('expires_at', sa.DATETIME(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='auth_refresh_token_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='auth_refresh_token_pkey')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('password', sa.BLOB(), nullable=False),
    sa.Column('birthdate', sa.DATE(), nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), server_default=sa.text("'false'"), nullable=False),
    sa.Column('is_online', sa.BOOLEAN(), server_default=sa.text("'false'"), nullable=False),
    sa.Column('created_at', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    # ### end Alembic commands ###