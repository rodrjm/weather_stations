# API de Estaciones Meteorológicas

Este proyecto es una API RESTful desarrollada con Flask, Flask-SQLAlchemy y PostGIS para gestionar estaciones meteorológicas con datos geoespaciales.

## Características

* Creación, lectura, actualización y eliminación (CRUD) de estaciones meteorológicas.
* Búsqueda de la estación meteorológica más cercana a una ubicación dada.
* Almacenamiento y recuperación de datos meteorológicos registrados por cada estación.
* Documentación interactiva de la API con Swagger (Flasgger).

## Requisitos

* Python 3.7+
* PostgreSQL con extensión PostGIS
* pip (gestor de paquetes de Python)
* git (opcional, para clonar el repositorio)

## Instalación

1.  **Clonar el repositorio (opcional):**

    ```bash
    git clone https://github.com/rodrjm/weather_stations
    cd weather_stations
    ```

2.  **Crear un entorno virtual (recomendado):**

    ```bash
    python -m venv .venv
    ```

3.  **Activar el entorno virtual:**

    * En Windows:

        ```bash
        .venv\Scripts\activate
        ```

    * En macOS y Linux:

        ```bash
        source .venv/bin/activate
        ```

4.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar la base de datos:**

    * Como se mencionó anteriormente, es un requisito tener PostgreSQL instalado y PostGIS habilitado.
    * Crea una base de datos llamada `weather_stations`.
    * Configura la variable de entorno `DATABASE_URL` con la URI de conexión a tu base de datos. Por ejemplo:

        * En Windows (PowerShell):

            ```powershell
            [Environment]::SetEnvironmentVariable('DATABASE_URL', 'postgresql://usuario:contraseña@localhost/weather_stations', 'User')
            ```

        * O crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

            ```
            DATABASE_URL=postgresql://usuario:contraseña@localhost/weather_stations
            ```

            Y luego instala `python-dotenv`:

            ```bash
            pip install python-dotenv
            ```

            Y modifica `config.py` para que lea el archivo `.env`:

            ```python
            from dotenv import load_dotenv
            import os

            load_dotenv()

            SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
            ```

6.  **Ejecutar la aplicación:**

    ```bash
    python run.py
    ```

7.  **Acceder a la documentación de Swagger:**

    * Abre tu navegador y ve a `http://127.0.0.1:5000/apidocs/`.

## Uso de la API

La API proporciona los siguientes endpoints:

* `POST /stations`: Crea una nueva estación meteorológica.
* `GET /stations/nearest`: Obtiene la estación más cercana a una ubicación dada y sus datos más recientes.
* `PUT /stations/<station_id>`: Actualiza una estación existente.
* `DELETE /stations/<station_id>`: Elimina una estación existente.

Consulta la documentación de Swagger para obtener detalles sobre los parámetros y las respuestas de cada endpoint.
