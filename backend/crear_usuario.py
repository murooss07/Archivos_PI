# Importaciones necesarias para SQLAlchemy y bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import bcrypt

# URL de conexión a la base de datos PostgreSQL (usuario: ruben, password: ruben, host: db, puerto: 5432, base de datos: enchufes)
DATABASE_URL = "postgresql://usuario:contraseña@db:5432/enchufes"

# Crea una instancia del motor de la base de datos
engine = create_engine(DATABASE_URL)

# Crea una clase para sesiones de base de datos
SessionLocal = sessionmaker(bind=engine)

# Clase base para declarar modelos
Base = declarative_base()

# Modelo de usuario (corresponde a la tabla 'usuarios' en la base de datos)
class Usuario(Base):
    __tablename__ = "usuarios"   # Nombre de la tabla
    id = Column(Integer, primary_key=True)  # ID autoincremental
    nombre_usuario = Column(String, unique=True, index=True)  # Nombre de usuario único y con índice
    contrasena = Column(String)  # Contraseña encriptada

# Función para crear un nuevo usuario
def crear_usuario(nombre_usuario: str, contrasena: str):
    # Crea una nueva sesión de base de datos
    db = SessionLocal()

    # Verifica si el usuario ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
    if usuario_existente:
        print(f"⚠️ El usuario '{nombre_usuario}' ya existe.")
        db.close()
        return

    # Encripta la contraseña usando bcrypt
    hashed_password = bcrypt.hashpw(contrasena.encode(), bcrypt.gensalt()).decode()

    # Crea el nuevo objeto usuario
    usuario = Usuario(nombre_usuario=nombre_usuario, contrasena=hashed_password)

    # Agrega el nuevo usuario a la base de datos
    db.add(usuario)
    db.commit()
    db.close()
    print(f"✅ Usuario '{nombre_usuario}' creado con éxito.")
