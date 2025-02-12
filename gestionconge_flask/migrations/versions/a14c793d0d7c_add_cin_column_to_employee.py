"""Add cin column to Employee

Revision ID: a14c793d0d7c
Revises: <correct_previous_revision_id>
Create Date: <timestamp>

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a14c793d0d7c'
down_revision = '7486cd1bd3fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('cin', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('matricule', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('nom', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('responsable', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('utilisateur', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('mot_de_passe', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('adresse', sa.String(length=100), nullable=True))
    op.add_column('employee', sa.Column('date_naiss', sa.Date(), nullable=True))
    op.add_column('employee', sa.Column('date_debut', sa.Date(), nullable=True))
    op.add_column('employee', sa.Column('nom_entite', sa.String(length=50), nullable=True))
    op.add_column('employee', sa.Column('id_service', sa.Integer(), nullable=True))
    op.add_column('employee', sa.Column('jrs_total', sa.Integer(), nullable=True))
    op.add_column('employee', sa.Column('jrs_restant', sa.Integer(), nullable=True))
    op.create_unique_constraint('uq_employee_cin', 'employee', ['cin'])
    op.create_unique_constraint('uq_employee_utilisateur', 'employee', ['utilisateur'])
    op.create_unique_constraint('uq_employee_matricule', 'employee', ['matricule'])
    op.drop_column('employee', 'grade')
    op.drop_column('employee', 'tel')
    op.drop_column('employee', 'password')
    op.drop_column('employee', 'email')
    op.drop_column('employee', 'role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('role', sa.VARCHAR(length=50), nullable=True))
    op.add_column('employee', sa.Column('email', sa.VARCHAR(length=50), nullable=True))
    op.add_column('employee', sa.Column('password', sa.VARCHAR(length=50), nullable=True))
    op.add_column('employee', sa.Column('tel', sa.VARCHAR(length=50), nullable=True))
    op.add_column('employee', sa.Column('grade', sa.VARCHAR(length=50), nullable=True))
    op.drop_constraint('uq_employee_cin', 'employee', type_='unique')
    op.drop_constraint('uq_employee_utilisateur', 'employee', type_='unique')
    op.drop_constraint('uq_employee_matricule', 'employee', type_='unique')
    op.drop_column('employee', 'jrs_restant')
    op.drop_column('employee', 'jrs_total')
    op.drop_column('employee', 'id_service')
    op.drop_column('employee', 'nom_entite')
    op.drop_column('employee', 'date_debut')
    op.drop_column('employee', 'date_naiss')
    op.drop_column('employee', 'adresse')
    op.drop_column('employee', 'mot_de_passe')
    op.drop_column('employee', 'utilisateur')
    op.drop_column('employee', 'responsable')
    op.drop_column('employee', 'nom')
    op.drop_column('employee', 'matricule')
    op.drop_column('employee', 'cin')
    # ### end Alembic commands ###
