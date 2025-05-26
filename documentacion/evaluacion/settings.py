from datetime import timedelta
from environs import Env

env = Env()
env.read_env()

class Settings:
    # Configuración general
    ENV = env.str("FLASK_ENV", default="production")
    DEBUG = ENV == "development"
    SECRET_KEY = env.str("SECRET_KEY", default="dev")
    SEND_FILE_MAX_AGE_DEFAULT = env.int("SEND_FILE_MAX_AGE_DEFAULT", default=0)
    BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
    DEBUG_TB_ENABLED = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "flask_caching.backends.SimpleCache"
    WTF_CSRF_ENABLED = False

    # Configurracion para la conexion de Base de datos MySQL
    SQLALCHEMY_DATABASE_URI = env.str(
        "DATABASE_URL",
        default="mysql+pymysql://root:Bicho777#@localhost/nlp_comentarios_actual"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración correo
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'david.urrutia.c@uniautonoma.edu.co'
    MAIL_PASSWORD = 'Jdurrutia777&'  # Usa contraseña de aplicación si es Gmail
    MAIL_DEFAULT_SENDER = ('Evaluación Docente', 'david.urrutia.c@uniautonoma.edu.co')

    # Configuración JWT
    JWT_SECRET_KEY = "HCqacbibdaja64kQ07y8hyj_Ra55ugXQgpz4bCodOpE"  # Clave secreta para generar tokens JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=40)  # El token expira en 30 minutos

# Crear una instancia de la clase Settings
settings = Settings()