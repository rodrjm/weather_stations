from geoalchemy2.functions import ST_Point, ST_Distance
from .models import WeatherStations
from .extensions import db


def create_station(name, latitude, longitude):
    """Crea una nueva estación meteorológica."""
    location = ST_Point(longitude, latitude, srid=4326)  # Crea un punto geográfico con el SRID 4326
    new_station = WeatherStations(name=name, location=location)  # Crea una nueva instancia del modelo WeatherStations
    try:
        db.session.add(new_station)  # Agrega la nueva estación a la sesión de la base de datos
        db.session.commit()  # Confirma los cambios en la base de datos
    except Exception as e:
        db.session.rollback()  # Maneja errores de base de datos y realiza un rollback
        raise e  # Re-lanza la excepción para que se maneje en la ruta
    return new_station  # Devuelve la nueva estación creada


def get_nearest_station(latitude, longitude):
    """Obtiene la estación más cercana a una ubicación dada."""
    point = ST_Point(longitude, latitude, srid=4326)  # Crea un punto geográfico de referencia con el SRID 4326
    return WeatherStations.query.order_by(ST_Distance(WeatherStations.location, point)).first()  # Realiza una consulta para obtener la estación más cercana, ordenando por distancia


def update_station(station_id, name, latitude, longitude):
    """Actualiza los datos de una estación meteorológica existente."""
    station = WeatherStations.query.get(station_id)  # Obtiene la estación por su ID
    if station:  # Verifica si la estación existe
        if name:  # Actualiza el nombre si se proporciona
            station.name = name
        if latitude is not None and longitude is not None:  # Actualiza la ubicación si se proporcionan latitud y longitud
            station.location = ST_Point(longitude, latitude, srid=4326)
        try:
            db.session.commit()  # Confirma los cambios en la base de datos
        except Exception as e:
            db.session.rollback()  # Maneja errores de base de datos y realiza un rollback
            raise e  # Re-lanza la excepción para que se maneje en la ruta
        return station  # Devuelve la estación actualizada
    return None  # Devuelve None si la estación no se encontró


def delete_station(station_id):
    """Elimina una estación meteorológica existente."""
    station = WeatherStations.query.get(station_id)  # Obtiene la estación por su ID
    if station:  # Verifica si la estación existe
        try:
            db.session.delete(station)  # Elimina la estación de la sesión de la base de datos
            db.session.commit()  # Confirma los cambios en la base de datos
        except Exception as e:
            db.session.rollback()  # Maneja errores de base de datos y realiza un rollback
            raise e  # Re-lanza la excepción para que se maneje en la ruta
        return True  # Devuelve True si la estación se eliminó correctamente
    return False  # Devuelve False si la estación no se encontró