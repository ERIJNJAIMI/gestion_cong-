"""Add new fields to Employee model

Revision ID: 7486cd1bd3fd
Revises: 
Create Date: 2024-07-09 23:46:23.448120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7486cd1bd3fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
   # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('prenom', sa.String(length=50), nullable=True),
    sa.Column('grade', sa.String(length=50), nullable=True),
    sa.Column('tel', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('leaverequest',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('leave_type', sa.String(length=50), nullable=False),
    sa.Column('start_date', sa.String(length=50), nullable=False),
    sa.Column('end_date', sa.String(length=50), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('reason', sa.String(length=200), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('date_demande', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['username'], ['employee.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leaverequest')
    op.drop_table('employee')
    # ### end Alembic commands ###