"""try adding blogpages into db

Revision ID: 3034565ad1a6
Revises: 61cb86c64c6b
Create Date: 2024-06-06 07:01:54.186528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3034565ad1a6'
down_revision = '61cb86c64c6b'
branch_labels = None
depends_on = None


def upgrade():
    pass
    # ### commands auto generated by Alembic - please adjust! ###
#    op.create_table('blogpage',
#    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
#    sa.Column('url_path', sa.String(length=50), nullable=False),
#    sa.Column('title', sa.String(length=50), nullable=False),
#    sa.Column('subtitle', sa.String(length=100), nullable=True),
#    sa.Column('meta_description', sa.String(length=500), nullable=True),
#    sa.Column('color_html_class', sa.String(length=100), nullable=True),
#    sa.Column('login_required', sa.Boolean(), nullable=False),
#    sa.Column('unpublished', sa.Boolean(), nullable=False),
#    sa.Column('writeable', sa.Boolean(), nullable=False),
#    sa.PrimaryKeyConstraint('id')
#    )
#    with op.batch_alter_table('post', schema=None) as batch_op:
#        batch_op.add_column(sa.Column('blogpage_id', sa.Integer(), nullable=False))
#        batch_op.alter_column('content',
#               existing_type=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
#               type_=sa.Text(length=100000),
#               existing_nullable=False)
#        batch_op.create_foreign_key(None, 'blogpage', ['blogpage_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
#    with op.batch_alter_table('post', schema=None) as batch_op:
#        batch_op.drop_constraint(None, type_='foreignkey')
#        batch_op.alter_column('content',
#               existing_type=sa.Text(length=100000),
#               type_=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
#               existing_nullable=False)
#        batch_op.drop_column('blogpage_id')
#
#    op.drop_table('blogpage')
#    # ### end Alembic commands ###
