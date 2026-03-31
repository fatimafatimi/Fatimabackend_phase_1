"""add tenant_id to roles

Revision ID: 07ee1a61fa8c
Revises: fbdae855c409
Create Date: 2026-03-27 19:42:25.605786
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '07ee1a61fa8c'
down_revision = 'fbdae855c409'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. Add tenant_id column as nullable first
    op.add_column('roles', sa.Column('tenant_id', sa.Integer(), nullable=True))

    # 2. Assign existing roles to the first tenant
    op.execute("""
        UPDATE roles
        SET tenant_id = (SELECT id FROM tenants LIMIT 1)
    """)

    # 3. Make tenant_id NOT NULL
    op.alter_column('roles', 'tenant_id', nullable=False)

    # 4. Add foreign key constraint
    op.create_foreign_key(
        'fk_roles_tenant_id',
        'roles',
        'tenants',
        ['tenant_id'],
        ['id']
    )

def downgrade() -> None:
    # Remove foreign key
    op.drop_constraint('fk_roles_tenant_id', 'roles', type_='foreignkey')
    # Drop column
    op.drop_column('roles', 'tenant_id')