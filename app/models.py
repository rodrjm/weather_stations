from .extensions import db
from geoalchemy2 import Geography


class WeatherStations(db.Model):
    """
    Define el modelo de datos para las estaciones meteorológicas.
    """
    id = db.Column(db.Integer, primary_key=True)  # Define la clave primaria 'id' como un entero autoincremental
    name = db.Column(db.String(100), nullable=False)  # Define el campo 'name' como una cadena de texto de hasta 100 caracteres, que no puede ser nulo
    location = db.Column(Geography(geometry_type='POINT'), nullable=False)  # Define el campo 'location' como un punto geográfico utilizando el tipo Geography de GeoAlchemy2, que no puede ser nulo. El parámetro 'geometry_type='POINT'' especifica que el campo almacenará puntos geográficos


class WeatherData(db.Model):
    """
    Define el modelo de datos para los datos registrados por las estaciones meteorológicas.
    """
    id = db.Column(db.Integer, primary_key=True)  # Define la clave primaria 'id' como un entero autoincremental
    station_id = db.Column(db.Integer, db.ForeignKey('weather_stations.id'))  # Define la clave foránea 'station_id' que referencia la tabla 'weather_stations'
    timestamp = db.Column(db.DateTime, nullable=False)  # Define el campo 'timestamp' como una fecha y hora, que no puede ser nulo
    temperature = db.Column(db.Float)  # Define el campo 'temperature' como un número de punto flotante
    humidity = db.Column(db.Float)  # Define el campo 'humidity' como un número de punto flotante
    pressure = db.Column(db.Float)  # Define el campo 'pressure' como un número de punto flotante
    station = db.relationship('WeatherStations', backref=db.backref('data', lazy=True))  # Define la relación con la tabla 'weather_stations'
