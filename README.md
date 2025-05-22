Proyecto: Control de Enchufes Inteligentes
Este proyecto consiste en una aplicación web que permite encender y apagar enchufes inteligentes Gosund de forma remota, a través de una interfaz sencilla, protegida por contraseña, desplegada en contenedores Docker y accesible desde el navegador web mediante un dominio personalizado. El objetivo es desarrollar un sistema funcional, económico y realista para el control de dispositivos del hogar, integrando una aplicación web, una API, una base de datos y enchufes inteligentes, todo ello ejecutado en contenedores Docker.

Tecnologías utilizadas:
Python + FastAPI
HTML + CSS + JavaScript (sin frameworks)
PostgreSQL
Docker y Docker Compose
Apache (como proxy inverso)
TinyTuya (control local de enchufes Tuya/Gosund)
Let's Encrypt (certificado SSL)
IONOS (gestión del dominio)

Estructura del proyecto
backend/ → API REST desarrollada en FastAPI para gestionar usuarios y controlar los enchufes.
frontend/ → Interfaz web desarrollada en HTML, CSS y JavaScript.
frontend/src/ → Archivos HTML, JS y CSS principales.
enchufes/ → docker-compose.yml y configuración para levantar todos los servicios con Docker.
README.md → Este archivo.

Cómo desplegar el sistema
Asegúrate de tener instalado Docker y Docker Compose.
Clona este repositorio en tu servidor.
Ajusta los códigos a tu configuración
Ejecuta el siguiente comando desde la raíz del proyecto:
docker-compose up --build -d
Accede a la interfaz web desde tu navegador en el dominio configurado o en localhost: (según cómo esté desplegado).

Seguridad
Acceso mediante login con usuario y contraseña encriptada (SHA-256).
Base de datos aislada en su contenedor.
Tráfico cifrado con HTTPS (Let’s Encrypt).
Control de acceso mediante autenticación básica en Apache.

Funcionalidades
Iniciar sesión en la interfaz web.
Encender o apagar enchufes inteligentes Gosund desde la interfaz.
Registro de cada acción en la base de datos (usuario, IP, acción y fecha).
Arquitectura desplegada en contenedores para facilitar mantenimiento y portabilidad.
