"""add STORE value to action enum

Revision ID: bf9a283876e7
Revises: d42bddfac4f1
Create Date: 2023-10-06 12:53:08.277645

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "bf9a283876e7"
down_revision = "d42bddfac4f1"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE action ADD VALUE 'STORE' AFTER 'CALLBACK'")


def downgrade():
    pass
