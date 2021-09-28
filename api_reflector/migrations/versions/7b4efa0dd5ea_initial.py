"""initial migration

Revision ID: 7b4efa0dd5ea
Revises: 
Create Date: 2021-09-23 10:19:07.622146

"""
import sqlalchemy as sa
from alembic import op

revision = "7b4efa0dd5ea"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "endpoint",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("method", sa.Enum("GET", "POST", "PUT", "DELETE", "PATCH", name="method"), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("method", "path"),
    )
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "response",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("endpoint_id", sa.Integer(), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["endpoint_id"],
            ["endpoint.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "response_action",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.Enum("DELAY", name="action"), nullable=False),
        sa.Column("arguments", sa.ARRAY(sa.String()), nullable=False),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["response.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "response_rule",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("response_id", sa.Integer(), nullable=False),
        sa.Column(
            "operator",
            sa.Enum(
                "EQUAL",
                "NOT_EQUAL",
                "LESS_THAN",
                "LESS_THAN_EQUAL",
                "GREATER_THAN",
                "GREATER_THAN_EQUAL",
                "IS_EMPTY",
                "IS_NOT_EMPTY",
                "CONTAINS",
                "NOT_CONTAINS",
                name="operator",
            ),
            nullable=False,
        ),
        sa.Column("arguments", sa.ARRAY(sa.String()), nullable=False),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["response.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "response_tag",
        sa.Column("response_id", sa.Integer(), nullable=True),
        sa.Column("tag_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["response_id"],
            ["response.id"],
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tag.id"],
        ),
    )


def downgrade():
    op.drop_table("response_tag")
    op.drop_table("response_rule")
    op.drop_table("response_action")
    op.drop_table("response")
    op.drop_table("tag")
    op.drop_table("endpoint")
