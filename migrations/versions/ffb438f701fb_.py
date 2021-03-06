"""empty message

Revision ID: ffb438f701fb
Revises: 24a769ccc776
Create Date: 2020-06-24 13:27:35.645834

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ffb438f701fb"
down_revision = "24a769ccc776"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("requests", schema=None) as batch_op:
        batch_op.add_column(sa.Column("target_bn_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_requests_target_bn_id_users"),
            "users",
            ["target_bn_id"],
            ["osu_uid"],
        )

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("allow_multiple_reqs", sa.Boolean(), nullable=False)
        )
        batch_op.add_column(sa.Column("is_bn", sa.Boolean(), nullable=False))
        batch_op.add_column(sa.Column("is_closed", sa.Boolean(), nullable=False))
        batch_op.create_index(
            batch_op.f("ix_users_allow_multiple_reqs"),
            ["allow_multiple_reqs"],
            unique=False,
        )
        batch_op.create_index(batch_op.f("ix_users_is_bn"), ["is_bn"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_users_is_closed"), ["is_closed"], unique=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_is_closed"))
        batch_op.drop_index(batch_op.f("ix_users_is_bn"))
        batch_op.drop_index(batch_op.f("ix_users_allow_multiple_reqs"))
        batch_op.drop_column("is_closed")
        batch_op.drop_column("is_bn")
        batch_op.drop_column("allow_multiple_reqs")

    with op.batch_alter_table("requests", schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f("fk_requests_target_bn_id_users"), type_="foreignkey"
        )
        batch_op.drop_column("target_bn_id")

    # ### end Alembic commands ###
