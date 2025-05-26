# C:\PROYECTO DE NLP\BACKEND\documentacion\evaluacion\models.py

from datetime import datetime

from sqlalchemy import ForeignKeyConstraint
from documentacion.evaluacion.extensions import db, bcrypt  # Esta es la correcta
# from flask_sqlalchemy import SQLAlchemy

def convertir_calificacion_a_numerica(valor: str) -> int:
    mapa = {
        "Excelente": 5,
        "Bueno": 4,
        "Regular": 3,
        "Malo": 2,
        "Pésimo": 1
    }
    return mapa.get(valor, 0)  # Devuelve 0 si no coincide


# # Inicializar SQLAlchemy
# db = SQLAlchemy()

# Asociación M:N entre Docente y Curso
docente_curso = db.Table(
    'docente_curso',
    db.Column('docente_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('curso_id',   db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)

# Usuarios
class User(db.Model):
    __tablename__ = 'users'
    
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column('password', db.String(255), nullable=False)
    created_at    = db.Column(db.DateTime,  default=datetime.now)
    first_name    = db.Column(db.String(30))
    last_name     = db.Column(db.String(30))
    active        = db.Column(db.Boolean,   default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relaciones
    
    # Roles que parten del usuario
    role = db.relationship('Role', back_populates='users')
    
    # Cursos que imparte (solo usuarios con rol docente)
    cursos = db.relationship(
        'Curso', secondary=docente_curso,
        back_populates='docentes'
    )
    
    # Evaluaciones donde actúa como estudiante
    evaluciones = db.relationship(
        'Evaluacion',
        foreign_keys='Evaluacion.estudiante_id',
        back_populates='estudiante',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    
    # Evaluaciones donde actúa como docente
    evaluaciones = db.relationship(
        'Evaluacion',
        foreign_keys='Evaluacion.docente_id',
        back_populates='docente',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )    
    
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plaintext):
        # Guarda en la columna 'password' con bcrypt
        self.password_hash = bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password_hash, plaintext)
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}
    
# Roles
class Role(db.Model):
    __tablename__ = 'roles'

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(80), unique=True, nullable=False)

    # Relación 1:N → User
    users     = db.relationship('User', back_populates='role', cascade='all, delete-orphan')

    __table_args__ = {'extend_existing': True}
    
# Cursos
class Curso(db.Model):
    __tablename__ = 'cursos'
    id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre  = db.Column(db.String(100), nullable=False)

    docentes    = db.relationship('User', secondary=docente_curso, back_populates='cursos')
    evaluaciones = db.relationship('Evaluacion', back_populates='curso', cascade='all, delete-orphan')
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}

# Criterios de evaluación
class Criterio(db.Model):
    __tablename__ = 'criterios'
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False)

    calificaciones = db.relationship('Calificacion', back_populates='criterio', cascade='all, delete-orphan')
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}

# Evaluaciones
class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    
    __table_args__ = (
        # FK compuesta: (docente_id, curso_id) debe existir en docente_curso
        ForeignKeyConstraint(
            ['docente_id', 'curso_id'],
            ['docente_curso.docente_id', 'docente_curso.curso_id'],
            ondelete='CASCADE',
            onupdate='CASCADE'
        ),
        {'extend_existing': True}
    )
    
    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudiante_id  = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    docente_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    curso_id       = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha          = db.Column(db.DateTime, default=datetime.now)

    estudiante     = db.relationship('User', foreign_keys=[estudiante_id],back_populates='evaluaciones')
    
    docente        = db.relationship('User', foreign_keys=[docente_id], back_populates='evaluaciones')
    
    curso          = db.relationship('Curso', back_populates='evaluaciones')
    
    calificaciones = db.relationship('Calificacion', back_populates='evaluacion', cascade='all, delete-orphan')
    
    comentarios    = db.relationship('Comentario', back_populates='evaluacion', cascade='all, delete-orphan')
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}

# Calificaciones (pivot Evaluación×Criterio)
class Calificacion(db.Model):
    __tablename__ = 'calificaciones'
    evaluacion_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.id'), primary_key=True)
    criterio_id   = db.Column(db.Integer, db.ForeignKey('criterios.id'),     primary_key=True)
    valor         = db.Column(db.SmallInteger, nullable=False)  # 1 a 5

    evaluacion = db.relationship('Evaluacion', back_populates='calificaciones')
    criterio   = db.relationship('Criterio',   back_populates='calificaciones')
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}

# Comentarios y sentimientos
class Comentario(db.Model):
    __tablename__ = 'comentarios'
    id            = db.Column(db.Integer, primary_key=True, autoincrement=True)
    evaluacion_id = db.Column(db.Integer, db.ForeignKey('evaluaciones.id'), nullable=False)
    tipo          = db.Column(db.Enum('docente', 'curso', name='tipo_enum'), nullable=False)
    texto         = db.Column(db.Text, nullable=False)
    sentimiento   = db.Column(db.String(20))
    fecha         = db.Column(db.DateTime, default=datetime.now)

    evaluacion = db.relationship('Evaluacion', back_populates='comentarios')
    
    # Esto sirve por si ya hay un definicion de la tabla con el mismo nombre este se actualice
    __table_args__ = {'extend_existing': True}