"""Add Admin model inheriting from Employee

Revision ID: 353712a713d3
Revises: f51e6172d57f
Create Date: 2024-07-22 15:19:46.353003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '353712a713d3'
down_revision = 'f51e6172d57f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=50), nullable=True))
        batch_op.create_foreign_key(None, 'employee', ['id'], ['id'])
        batch_op.drop_column('utilisateur')
        batch_op.drop_column('matricule')
        batch_op.drop_column('mot_de_passe')
        batch_op.drop_column('id_service')
        batch_op.drop_column('nom_entite')
        batch_op.drop_column('adresse')
        batch_op.drop_column('jrs_restant')
        batch_op.drop_column('responsable')
        batch_op.drop_column('nom')
        batch_op.drop_column('username')
        batch_op.drop_column('jrs_total')
        batch_op.drop_column('date_naiss')
        batch_op.drop_column('id_type_emp')
        batch_op.drop_column('prenom')
        batch_op.drop_column('date_debut')
        batch_op.drop_column('cin')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cin', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('date_debut', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('prenom', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('id_type_emp', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('date_naiss', sa.DATETIME(), nullable=False))
        batch_op.add_column(sa.Column('jrs_total', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=50), nullable=True))
        batch_op.add_column(sa.Column('nom', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('responsable', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('jrs_restant', sa.INTEGER(), nullable=False))
        batch_op.add_column(sa.Column('adresse', sa.VARCHAR(length=200), nullable=False))
        batch_op.add_column(sa.Column('nom_entite', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('id_service', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('mot_de_passe', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('matricule', sa.VARCHAR(length=50), nullable=False))
        batch_op.add_column(sa.Column('utilisateur', sa.VARCHAR(length=50), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('role')

    # ### end Alembic commands ###
