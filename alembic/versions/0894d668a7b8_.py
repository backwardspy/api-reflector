"""add human-friendly names for endpoints and responses

Revision ID: 0894d668a7b8
Revises: ab3e47fb856c
Create Date: 2021-09-17 14:03:52.089863

"""
from alembic import op
import sqlalchemy as sa


revision = "0894d668a7b8"
down_revision = "ab3e47fb856c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("endpoint", sa.Column("name", sa.String(), nullable=False))
    op.add_column("response", sa.Column("name", sa.String(), nullable=False))


def downgrade():
    op.drop_column("response", "name")
    op.drop_column("endpoint", "name")
