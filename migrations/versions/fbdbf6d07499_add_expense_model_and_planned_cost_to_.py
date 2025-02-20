"""Add Expense model and planned_cost to Task

Revision ID: fbdbf6d07499
Revises: 
Create Date: 2025-02-15 22:32:04.021460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbdbf6d07499'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('assignee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('assignee_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('task_type', sa.String(length=50), nullable=False),
    sa.Column('planned_cost', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['assignee_id'], ['assignee.id'], ),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('month', sa.String(length=20), nullable=False),
    sa.Column('invoice_number', sa.String(length=50), nullable=False),
    sa.Column('actual_cost', sa.Float(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('expense')
    op.drop_table('task')
    op.drop_table('assignee')
    op.drop_table('department')
    # ### end Alembic commands ###
