"""empty message

Revision ID: 6afb61475f71
Revises: bca2e55d1955
Create Date: 2019-07-30 15:53:46.225831

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6afb61475f71'
down_revision = 'bca2e55d1955'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=2048), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('added', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.Column('source_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('document')
    # ### end Alembic commands ###