"""Nuevo esquema relacional completo

Revision ID: 8a810bd62098
Revises: b85bd07b860c
Create Date: 2025-04-27 21:03:55.081201
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8a810bd62098'
down_revision = 'b85bd07b860c'
branch_labels = None
depends_on = None


def upgrade():
    # --- CREAR TABLAS NUEVAS NORMALIZADAS ---

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(80), nullable=False, unique=True),
        sa.Column('email', sa.String(120), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('first_name', sa.String(50)),
        sa.Column('last_name', sa.String(50)),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(80), nullable=False, unique=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'user_roles',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id'), primary_key=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'estudiantes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'docentes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), primary_key=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'cursos',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nombre', sa.String(100), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'criterios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('descripcion', sa.String(100), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'evaluaciones',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('estudiante_id', sa.Integer(), sa.ForeignKey('estudiantes.user_id'), nullable=False),
        sa.Column('docente_id', sa.Integer(), sa.ForeignKey('docentes.user_id'), nullable=False),
        sa.Column('curso_id', sa.Integer(), sa.ForeignKey('cursos.id'), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'calificaciones',
        sa.Column('evaluacion_id', sa.Integer(), sa.ForeignKey('evaluaciones.id'), primary_key=True),
        sa.Column('criterio_id', sa.Integer(), sa.ForeignKey('criterios.id'), primary_key=True),
        sa.Column('valor', sa.SmallInteger(), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'comentarios',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('evaluacion_id', sa.Integer(), sa.ForeignKey('evaluaciones.id'), nullable=False),
        sa.Column('tipo', sa.Enum('docente', 'curso', name='tipo_enum'), nullable=False),
        sa.Column('texto', sa.Text(), nullable=False),
        sa.Column('sentimiento', sa.String(20)),
        sa.Column('fecha', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )

    op.create_table(
        'docente_curso',
        sa.Column('docente_id', sa.Integer(), sa.ForeignKey('docentes.user_id'), primary_key=True),
        sa.Column('curso_id', sa.Integer(), sa.ForeignKey('cursos.id'), primary_key=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8mb4'
    )


def downgrade():
    # Borrar tablas nuevas en orden inverso
    op.drop_table('docente_curso')
    op.drop_table('comentarios')
    op.drop_table('calificaciones')
    op.drop_table('evaluaciones')
    op.drop_table('criterios')
    op.drop_table('cursos')
    op.drop_table('docentes')
    op.drop_table('estudiantes')
    op.drop_table('user_roles')
    op.drop_table('roles')
    op.drop_table('users')
