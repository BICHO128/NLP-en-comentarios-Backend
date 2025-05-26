"""Initial — esquema actual

Revision ID: a7aa011ff997
Revises: 
Create Date: 2025-05-14 12:43:53.847543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7aa011ff997'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'fk_eval_docentecurso',
        'evaluaciones', 'docente_curso',
        ['docente_id','curso_id'],
        ['docente_id','curso_id'],
        ondelete='CASCADE',
        onupdate='CASCADE'
    )



def downgrade():
    op.drop_constraint('fk_eval_docentecurso', 'evaluaciones', type_='foreignkey')
