from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'new_revision_id_here'
down_revision = '07ee1a61fa8c'
branch_labels = None
depends_on = None

def upgrade():
    # Add tenant_id as nullable first
    op.add_column('permissions', sa.Column('tenant_id', sa.Integer(), nullable=True))

    # Assign existing permissions to the default tenant
    op.execute("""
        UPDATE permissions
        SET tenant_id = (SELECT id FROM tenants LIMIT 1)
    """)

    # Make it NOT NULL
    op.alter_column('permissions', 'tenant_id', nullable=False)

    # Add foreign key constraint
    op.create_foreign_key(
        'fk_permissions_tenant_id',
        'permissions',
        'tenants',
        ['tenant_id'],
        ['id']
    )

def downgrade():
    op.drop_constraint('fk_permissions_tenant_id', 'permissions', type_='foreignkey')
    op.drop_column('permissions', 'tenant_id')