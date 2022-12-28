"""empty message

Revision ID: fcb4076005a9
Revises: 
Create Date: 2022-12-28 10:33:57.747179

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcb4076005a9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('livros',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('genero', sa.String(length=100), nullable=False),
    sa.Column('autor', sa.String(length=150), nullable=False),
    sa.Column('num_paginas', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(length=150), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=False),
    sa.Column('senha', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usuarios')
    op.drop_table('livros')
    # ### end Alembic commands ###
