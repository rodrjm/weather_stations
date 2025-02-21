from flask import Flask
from flasgger import Swagger
from .routes import routes_bp
from .extensions import db
import config


def create_app():
    """
    Crea y configura la aplicación Flask
    """
    app = Flask(__name__)  # Crea una instancia de la aplicación Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI  # Configura la URI de la base de datos SQLAlchemy desde el archivo config.py.

    db.init_app(app)  # Inicializa la extensión Flask-SQLAlchemy con la aplicación
    app.register_blueprint(routes_bp)  # Registra el blueprint 'routes_bp' para organizar las rutas de la API

    with app.app_context():  # Asegura que la aplicación esté en el contexto correcto para interactuar con la base de datos
        db.create_all()  # Crea las tablas de la base de datos si no existen

    swagger_config = {  # Configura la documentación Swagger (Flasgger)
        "headers": [],
        "specs": [{
            "endpoint": 'apispec',  # Nombre del endpoint para la especificación JSON de Swagger
            "route": '/apispec.json',  # Ruta para acceder a la especificación JSON
            "rule_filter": lambda rule: True,  # Filtro para incluir todas las rutas
            "model_filter": lambda model: True,  # Filtro para incluir todos los modelos
        }],
        "static_url_path": "/flasgger_static",  # Ruta para los archivos estáticos de Swagger UI
        "swagger_ui": True,  # Habilita la interfaz de usuario de Swagger UI
        "security": [],
        "version": "1.0",
        "title": "API de Estaciones Meteorológicas",
        "description": "API RESTful para gestionar estaciones meteorológicas con datos geoespaciales.",
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    }
    Swagger(app, config=swagger_config)  # Inicializa la extensión Flasgger con la aplicación y la configuración


    return app
