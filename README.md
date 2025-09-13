# Proyecto de Gestión de Videojuegos

Este proyecto es una base para la gestión de videojuegos y consolas, implementado siguiendo el patrón arquitectónico por capas. Utiliza Python, Flask como framework web y SQLAlchemy como ORM para la interacción con bases de datos relacionales.

## Descripción General
El sistema permite registrar, consultar, actualizar y eliminar videojuegos, la arquitectura por capas facilita la separación de responsabilidades, mejorando la mantenibilidad, escalabilidad y flexibilidad del código. El uso de un ORM como SQLAlchemy permite desacoplar la lógica de negocio de la base de datos, facilitando la portabilidad y la seguridad.

## Características principales
- API RESTful para la gestión de videojuegos.
- Modelos bien definidos y documentados.
- Repositorios para el acceso a datos desacoplados de la lógica de negocio.
- Documentación detallada para facilitar la comprensión y extensión del sistema.

## Estructura del Proyecto
- `models/`: Definición de los modelos de datos (`Game`) y documentación asociada.
- `repositories/`: Implementación de la capa de acceso a datos (repositorios) y su documentación.
- `controllers/`: Lógica de los endpoints y controladores de la API.
- `services/`: Lógica de negocio y conexión entre controladores y repositorios.
- `config/`: Configuración de la base de datos y utilidades.
- `juegos.py`: Archivo principal para iniciar la aplicación Flask.



## Licencia
Este proyecto es de uso libre para fines educativos y de aprendizaje.
