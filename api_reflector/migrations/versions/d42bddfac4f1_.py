"""convert response content to text field

Revision ID: d42bddfac4f1
Revises: 76feeb81949a
Create Date: 2022-02-01 16:32:13.067780

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d42bddfac4f1"
down_revision = "76feeb81949a"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("response", "content", type_=sa.Text)


def downgrade():
    op.alter_column("response", "content", type_=sa.String)
