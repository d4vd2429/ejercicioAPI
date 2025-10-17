# Proyecto de Gestión de Videojuegos

Este proyecto es una base para la gestión de videojuegos y consolas, implementado siguiendo el patrón arquitectónico por capas. Utiliza Python, Flask como framework web y SQLAlchemy como ORM para la interacción con bases de datos relacionales.

## Descripción General
El sistema permite registrar, consultar, actualizar y eliminar videojuegos, así como gestionar las consolas asociadas a cada videojuego. La arquitectura por capas facilita la separación de responsabilidades, mejorando la mantenibilidad, escalabilidad y flexibilidad del código. El uso de un ORM como SQLAlchemy permite desacoplar la lógica de negocio de la base de datos, facilitando la portabilidad y la seguridad.

## Características principales
- API RESTful para la gestión de videojuegos y consolas.
- Modelos bien definidos y documentados.
- Repositorios para el acceso a datos desacoplados de la lógica de negocio.
- Documentación detallada para facilitar la comprensión y extensión del sistema.

## Estructura del Proyecto
- `models/`: Definición de los modelos de datos (`Game`, `Console`) y documentación asociada.
- `repositories/`: Implementación de la capa de acceso a datos (repositorios) y su documentación.
- `controllers/`: Lógica de los endpoints y controladores de la API.
- `services/`: Lógica de negocio y conexión entre controladores y repositorios.
- `config/`: Configuración de la base de datos y utilidades.
- `juegos.py`: Archivo principal para iniciar la aplicación Flask.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Cómo crear un entorno virtual en Python
El uso de un entorno virtual es fundamental para aislar las dependencias del proyecto y evitar conflictos con otras aplicaciones o proyectos en tu sistema. Un entorno virtual te permite instalar paquetes específicos para este proyecto sin afectar el entorno global de Python.

### Pasos para crear y activar un entorno virtual:
1. Instala virtualenv si no lo tienes:
	```
	pip install virtualenv
	```
2. Crea el entorno virtual:
	```
	python -m venv venv
	```
	Esto creará una carpeta llamada `venv` en el directorio del proyecto.
3. Activa el entorno virtual:
	- En Linux/Mac:
	  ```
	  source venv/bin/activate
	  ```
	- En Windows:
	  ```
	  venv\Scripts\activate
	  ```
4. Instala las dependencias del proyecto:
	```
	pip install -r requirements.txt
	```

## Importancia de usar un entorno virtual
- **Aislamiento:** Evita conflictos entre dependencias de diferentes proyectos.
- **Reproducibilidad:** Permite que otros desarrolladores instalen exactamente las mismas versiones de las librerías.
- **Facilidad de despliegue:** Simplifica la migración y despliegue en diferentes entornos (desarrollo, pruebas, producción).
- **Limpieza:** Mantiene tu instalación global de Python libre de paquetes innecesarios.

## Contribuciones
Si deseas contribuir, por favor sigue las buenas prácticas de documentación y arquitectura ya establecidas en el proyecto. ¡Toda mejora es bienvenida!

## Licencia
Este proyecto es de uso libre para fines educativos y de aprendizaje.

## Actualizaciones 
Se implementó un sistema de autenticación y autorización completo basado en JWT.
Se añadió soporte para roles de usuario (campo role).
Se añadió revocación de refresh tokens (blocklist).
Se creó la estructura completa para usuarios: modelo, repositorio, servicio y controlador.
Se hicieron commits en la rama develop
