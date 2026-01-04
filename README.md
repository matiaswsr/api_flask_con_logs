# Desarrollo de API RESTful en Flask con sistema para logs

## Separación de responsabilidades:
- Se utilizan servicios para encapsular la lógica de negocio, lo que facilita la escalabilidad y el mantenimiento.
- Las funciones de validación están en un archivo separado (`utils.py`), lo que permite que el código sea más modular.

## Validación de datos:
- Se implementan validaciones de datos tanto para los JSON entrantes como para formatos específicos como fecha y correo electrónico. Esto asegura que la API reciba solo datos válidos y previene errores en el procesamiento de solicitudes.

## Manejo de errores:
- Manejo de excepciones con los `errorhandlers` de Flask, lo que asegura que los usuarios obtengan respuestas claras cuando algo sale mal (por ejemplo, error 404 si no se encuentra la ruta, error 422 si los datos no son válidos, etc.).

## Logging:
- Utiliza un sistema de logging con rotación de archivos y diferentes niveles de detalle según el entorno (desarrollo o producción).
- Además, el logging también está integrado con la funcionalidad de los endpoints, lo que permite un buen seguimiento de las solicitudes y posibles errores.

## Middleware:
- Se implementó el middleware `before_request` para registrar la información de las solicitudes antes de que se procesen, lo que es muy útil para monitorear y auditar el uso de la API.

**Middleware**: Un middleware es una pieza de software que actúa como un intermediario, interceptando las solicitudes HTTP entrantes y las respuestas salientes para ejecutar código adicional, permitiendo tareas transversales como autenticación, registro o modificación de datos antes o después de que la lógica de la ruta se procese, promoviendo la separación de responsabilidades y reduciendo la duplicación de código.

## Modularización:
- La lógica está organizada en servicios (`services.py`), validaciones (`utils.py`), y el controlador principal (`app.py`), lo que facilita la extensión y el mantenimiento a largo plazo.

---

# Diagrama de la arquitectura

### API Gateway (Flask):
- Este es el punto de entrada de las solicitudes HTTP.
- Se encarga de gestionar las rutas, recibir las solicitudes y llamar a los servicios correspondientes.

### Servicios:
- Los servicios (`services.py`) contienen la lógica de negocio, como la creación, actualización, y eliminación de personas.
- Los servicios interactúan con la base de datos para manipular los datos.

### Base de Datos:
- Usa SQLAlchemy para interactuar con una base de datos (por ejemplo, PostgreSQL, MySQL, SQLite, etc.).
- La base de datos contiene la tabla `persona` que almacena la información de las personas.

### Utilidades (`utils.py`):
- Las funciones de validación (como la validación de fechas, correos electrónicos, etc.) están separadas en `utils.py` para mantener la modularidad.
- Estas funciones son invocadas por los controladores antes de ejecutar cualquier lógica de negocio.

### Logging:
- Todas las interacciones de la API son registradas mediante `logger` (en `app.py`).
- El log contiene información de las solicitudes, errores, y excepciones, y está configurado para rotar diariamente.

![Diagrama](https://github.com/user-attachments/assets/9c0126ca-61c9-4c1c-96b3-9a626a59a90b)

## Descripción del flujo:

1. **API Gateway (Flask)**: El cliente realiza una solicitud HTTP (GET, POST, PUT, DELETE). Flask recibe esta solicitud, la registra utilizando logging y pasa los datos a través de los controladores.
2. **Controlador (app.py)**: El controlador verifica que los datos estén bien formateados y llama a los servicios correspondientes.
3. **Servicios**: Los servicios realizan la lógica de negocio y manipulan los datos, ya sea creando, actualizando, buscando o eliminando registros.
4. **Base de Datos**: Los servicios interactúan con la base de datos a través de SQLAlchemy.
5. **Utilidades**: Se validan los datos como los correos electrónicos o fechas antes de procesar cualquier solicitud.
6. **Logging**: Todo el proceso se registra en los archivos de log, lo que permite monitorear las solicitudes, respuestas, errores y excepciones.

Este diagrama proporciona una visión clara de cómo los diferentes componentes de la API interactúan entre sí y facilita la documentación.









