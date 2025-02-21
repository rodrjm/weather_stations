import os


SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Obtiene la URI de la base de datos de la variable de entorno 'DATABASE_URL'
