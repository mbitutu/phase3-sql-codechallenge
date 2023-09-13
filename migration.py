from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('star_rating', sa.Integer(), nullable=False),
        sa.Column('restaurant_id', sa.Integer(), sa.ForeignKey('restaurants.id')),
        sa.Column('customer_id', sa.Integer(), sa.ForeignKey('customers.id')),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('reviews')

