"""make active field non-nullable

Revision ID: 6e3e075b2257
Revises: e9a5828830a8
Create Date: 2021-09-20 13:55:17.854683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6e3e075b2257"
down_revision = "e9a5828830a8"
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
