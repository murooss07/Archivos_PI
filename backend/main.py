# Importación de librerías necesarias
import bcrypt
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
import pytz
from control_enchufes import switch_device

# Configuración del token JWT
SECRET_KEY = "xxx"  # Reemplazar por una clave segura
ALGORITHM = "HS256"

# URL de conexión a la base de datos PostgreSQL
DATABASE_URL = "postgresql://usuario:contraseña@db:5432/enchufes"

# Inicialización del motor de SQLAlchemy y la sesión de base de datos
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Creación de la aplicación FastAPI
app = FastAPI(root_path="/api")

# Configuración de CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sistema de autenticación con OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Definición del modelo de tabla 'usuarios'
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, unique=True, index=True)
    contrasena = Column(String)

# Definición del modelo de tabla 'registros_acceso'
class AccessLog(Base):
    __tablename__ = "registros_acceso"
    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, nullable=False)
    ip_contenedor = Column(String, nullable=False)
    ip_publica_usuario = Column(String, nullable=True)
    accion = Column(String, nullable=False)
    fecha_hora = Column(DateTime, nullable=False)

# Creación de las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de base de datos en cada solicitud
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generación de un token JWT válido durante 1 hora
def create_token(nombre_usuario):
    expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode = {"sub": nombre_usuario, "exp": expiration}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verifica el token y devuelve el usuario autenticado
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nombre_usuario = payload.get("sub")
        if nombre_usuario is None:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.nombre_usuario == nombre_usuario).first()
    if user is None:
        raise HTTPException(status_code=401)
    return user

# Esquema para los datos de inicio de sesión
class LoginData(BaseModel):
    nombre_usuario: str
    contrasena: str

# Función para encriptar contraseñas con bcrypt
def hash_password(contrasena: str):
    return bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Función para verificar contraseñas comparando texto plano y hash
def verify_password(contrasena_plana: str, contrasena_hash: str):
    return bcrypt.checkpw(contrasena_plana.encode('utf-8'), contrasena_hash.encode('utf-8'))

# Crea un registro de acceso en la base de datos con IP e información del usuario
def create_access_log(db, nombre_usuario, request, accion):
    container_ip = request.client.host.strip()
    x_forwarded_for = request.headers.get("X-Forwarded-For", container_ip)
    real_ip = x_forwarded_for.split(",")[0].strip()
    ip_publica_usuario = real_ip if real_ip != container_ip else None

# Obtener la hora local Europe/Madrid sin tzinfo y sin microsegundos
    utc_now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    madrid_tz = pytz.timezone("Europe/Madrid")
    madrid_now = utc_now.astimezone(madrid_tz)
    now = madrid_now.replace(tzinfo=None, microsecond=0)

    log = AccessLog(
        nombre_usuario=nombre_usuario,
        ip_contenedor=container_ip,
        ip_publica_usuario=ip_publica_usuario,
        accion=accion,
        fecha_hora=now
    )
    db.add(log)
    db.commit()

# Endpoint para iniciar sesión y devolver un token JWT
@app.post("/login")
def login(data: LoginData, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.nombre_usuario == data.nombre_usuario).first()
    if user is None or not verify_password(data.contrasena, user.contrasena):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    create_access_log(db, user.nombre_usuario, request, "login")
    return {"access_token": create_token(user.nombre_usuario), "token_type": "bearer"}

# Endpoint para encender un dispositivo (enchufe)
@app.post("/device/{name}/on")
def turn_on_device(name: str, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = switch_device(name, True)
    create_access_log(db, user.nombre_usuario, request, f"{name}_on")
    return result

# Endpoint para apagar un dispositivo (enchufe)
@app.post("/device/{name}/off")
def turn_off_device(name: str, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = switch_device(name, False)
    create_access_log(db, user.nombre_usuario, request, f"{name}_off")
    return result

# Endpoint de prueba para verificar autenticación y conexión
@app.get("/ping")
def ping(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    create_access_log(db, user.nombre_usuario, request, "ping")
    return {"message": f"pong, {user.nombre_usuario}"}
