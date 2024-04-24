"""increase max email length

Revision ID: 5a0e2dba21cc
Revises: db92b562700f
Create Date: 2024-04-24 11:03:59.138509

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5a0e2dba21cc'
down_revision = 'db92b562700f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
               type_=sa.Text(length=100000),
               existing_nullable=False)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_bin', length=320),
               type_=sa.String(length=512),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.String(length=512),
               type_=mysql.VARCHAR(charset='utf8mb3', collation='utf8mb3_bin', length=320),
               existing_nullable=False)

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.alter_column('content',
               existing_type=sa.Text(length=100000),
               type_=mysql.MEDIUMTEXT(collation='utf8mb3_bin'),
               existing_nullable=False)

    # ### end Alembic commands ###
