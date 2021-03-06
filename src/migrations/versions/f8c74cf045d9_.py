"""empty message

Revision ID: f8c74cf045d9
Revises: 
Create Date: 2018-05-16 11:19:53.691327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8c74cf045d9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('version', sa.String(length=128), nullable=False),
    sa.Column('created_by', sa.String(length=128), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=True),
    sa.Column('origin', sa.String(length=128), nullable=True),
    sa.Column('source_url', sa.String(length=128), nullable=True),
    sa.Column('content', sa.String(length=128), nullable=True),
    sa.Column('ext_link', sa.String(length=128), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('license',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=128), nullable=False),
    sa.Column('identifier', sa.String(length=128), nullable=False),
    sa.Column('fsf_free_libre', sa.Boolean(), nullable=True),
    sa.Column('osi_approved', sa.Boolean(), nullable=True),
    sa.Column('license_category', sa.String(length=128), nullable=True),
    sa.Column('license_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('identifier')
    )
    op.create_table('components',
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('child_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['child_id'], ['component.id'], ),
    sa.ForeignKeyConstraint(['parent_id'], ['component.id'], )
    )
    op.create_table('licenses',
    sa.Column('component_id', sa.Integer(), nullable=True),
    sa.Column('license_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['component.id'], ),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], )
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('version', sa.String(length=128), nullable=False),
    sa.Column('license_id', sa.Integer(), nullable=True),
    sa.Column('owner', sa.String(length=128), nullable=True),
    sa.Column('approver', sa.String(length=128), nullable=True),
    sa.Column('approval_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['license_id'], ['license.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.Column('relation', sa.String(length=128), nullable=True),
    sa.Column('modification', sa.Boolean(), nullable=True),
    sa.Column('delivery', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['component.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('product_id', 'component_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('product')
    op.drop_table('licenses')
    op.drop_table('components')
    op.drop_table('license')
    op.drop_table('component')
    # ### end Alembic commands ###
