from flask import Blueprint, request, jsonify
from geoalchemy2.functions import ST_AsEWKT, ST_Point
from .models import WeatherStations, WeatherData
from .schemas import WeatherStationsSchema, WeatherDataSchema
from marshmallow import ValidationError
from .extensions import db
from .services import create_station, get_nearest_station, update_station, delete_station


routes_bp = Blueprint('routes', __name__)  # Crea un Blueprint para organizar las rutas de la API


@routes_bp.route('/stations', methods=['POST'])
def create_new_station():
    """
    Crea una nueva estación meteorológica.
    ---
    parameters:
      - in: body
        name: station_data
        schema:
          type: object
          properties:
            name:
              type: string
            latitude:
              type: number
            longitude:
              type: number
        required: true
    responses:
      201:
        description: Estación creada exitosamente
      400:
        description: Datos inválidos o faltantes
    """
    schema = WeatherStationsSchema()  # Inicializa el esquema para validar los datos de la solicitud
    try:
        station_data = schema.load(request.get_json())  # Deserializa y valida los datos JSON de la solicitud
    except ValidationError as err:
        return jsonify(err.messages), 400  # Maneja errores de validación y devuelve una respuesta 400

    try:
        new_station = WeatherStations(  # Crea una nueva instancia del modelo WeatherStations con los datos validados
            name=station_data['name'],
            location=ST_Point(station_data['longitude'], station_data['latitude'], srid=4326)
        )
        db.session.add(new_station)  # Agrega la nueva estación a la sesión de la base de datos
        db.session.flush()  # Asegura que el ID de la estación se genere antes de hacer commit
        db.session.commit()  # Confirma los cambios en la base de datos
    except Exception as e:
        db.session.rollback()  # Maneja errores de base de datos, realiza un rollback y devuelve una respuesta 500
        return jsonify({'error': str(e)}), 500

    result = schema.dump(new_station)  # Serializa la nueva estación para la respuesta JSON
    srid = db.session.execute(db.text("SELECT ST_SRID(location) FROM weather_stations WHERE id = :id"), {"id": new_station.id}).scalar()  # Obtiene el SRID de la estación directamente de la base de datos
    result['srid'] = srid  # Agrega el SRID al resultado
    result['location'] = db.session.scalar(ST_AsEWKT(new_station.location))  # Convierte la ubicación a EWKT y la agrega al resultado
    return jsonify(result), 201  # Devuelve la respuesta JSON con la nueva estación y el código de estado 201


@routes_bp.route('/stations/nearest', methods=['GET'])
def get_nearest():
    """
    Obtiene la estación más cercana a una ubicación dada.
    ---
    parameters:
      - in: query
        name: latitude
        type: number
        required: true
      - in: query
        name: longitude
        type: number
        required: true
    responses:
      200:
        description: Estación más cercana encontrada
      400:
        description: Datos de latitud o longitud faltantes o inválidos
      404:
        description: No se encontraron estaciones
    """
    latitude = request.args.get('latitude')  # Obtiene el parámetros de latitud de la consulta
    longitude = request.args.get('longitude')  # Obtiene el parámetros de longitud de la consulta
    if not latitude or not longitude:  # Verifica si los parámetros están presentes
        return jsonify({'error': 'Missing data'}), 400  # Devuelve una respuesta 400 si faltan parámetros

    try:  # Convierte los parámetros a números de punto flotante
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:  # Maneja errores de conversión y devuelve una respuesta 400
        return jsonify({'error': 'Invalid latitude or longitude'}), 400

    nearest_station = get_nearest_station(latitude, longitude)  # Obtiene la estación más cercana utilizando la función de servicio
    if nearest_station:
        result = WeatherStationsSchema().dump(nearest_station)  # Serializa la estación más cercana para la respuesta JSON
        srid = db.session.execute(db.text("SELECT ST_SRID(location) FROM weather_stations WHERE id = :id"), {"id": nearest_station.id}).scalar()  # Obtiene el SRID de la estación directamente de la base de datos
        result['srid'] = srid  # Agrega el SRID al resultado
        result['location'] = db.session.scalar(ST_AsEWKT(nearest_station.location))  # Convierte la ubicación a EWKT y la agrega al resultado
        
        latest_data = WeatherData.query.filter_by(station_id=nearest_station.id).order_by(WeatherData.timestamp.desc()).first()  # Obtiene los datos más recientes de la estación más cercana
        if latest_data:
            result['latest_data'] = WeatherDataSchema().dump(latest_data)  # Serializa los datos más recientes y los agrega al resultado

        return jsonify(result), 200  # Devuelve la respuesta JSON con la estación más cercana y el código de estado 200
    else:
        return jsonify({'message': 'No stations found'}), 404  # Devuelve una respuesta 404 si no se encontraron estaciones


@routes_bp.route('/stations/<int:station_id>', methods=['PUT'])
def update(station_id):
    """
    Actualiza los datos de una estación meteorológica existente.
    ---
    parameters:
      - in: path
        name: station_id
        type: integer
        required: true
      - in: body
        name: station_data
        schema:
          type: object
          properties:
            name:
              type: string
            latitude:
              type: number
            longitude:
              type: number
    responses:
      200:
        description: Estación actualizada exitosamente
      404:
        description: Estación no encontrada
      400:
        description: Datos inválidos o faltantes
    """
    station = WeatherStations.query.get(station_id)  # Obtiene la estación por su ID
    if not station:  # Verifica si la estación existe
        return jsonify({'message': 'Station not found'}), 404  # Devuelve una respuesta 404 si la estación no existe

    # Obtiene los datos de la solicitud JSON
    data = request.get_json()
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if latitude is not None and longitude is not None:  # Verifica si se proporcionan tanto latitud como longitud para actualizar la ubicación
        updated_station = update_station(station_id, name, latitude, longitude)  # Actualiza la estación con la nueva ubicación
    elif name:  # Verifica si solo se proporciona el nombre para actualizarlo
        updated_station = update_station(station_id, name, None, None)  # Actualiza la estación con el nuevo nombre
    else:
        return jsonify({'message': 'Debes enviar tanto latitude como longitude para actualizar la ubicación.'}), 400  # Devuelve una respuesta 400 si faltan datos para la actualización

    if updated_station:
        result = WeatherStationsSchema().dump(updated_station)  # Serializa la estación actualizada para la respuesta JSON
        srid = db.session.execute(db.text("SELECT ST_SRID(location) FROM weather_stations WHERE id = :id"), {"id": updated_station.id}).scalar()  # Obtiene el SRID de la estación directamente de la base de datos
        result['srid'] = srid  # Agrega el SRID al resultado
        result['location'] = db.session.scalar(ST_AsEWKT(updated_station.location))  # Convierte la ubicación a EWKT y la agrega al resultado
        return jsonify(result), 200  # Devuelve la respuesta JSON con la estación actualizada y el código de estado 200
    else:
        return jsonify({'message': 'Station not found'}), 404  # Devuelve una respuesta 404 si la estación no se encontró


@routes_bp.route('/stations/<int:station_id>', methods=['DELETE'])
def delete(station_id):
    """
    Elimina una estación meteorológica existente.
    ---
    parameters:
      - in: path
        name: station_id
        type: integer
        required: true
    responses:
      200:
        description: Estación eliminada exitosamente
      404:
        description: Estación no encontrada
    """
    if delete_station(station_id):  # Elimina la estación utilizando la función de servicio
        return jsonify({'message': 'Station deleted successfully'}), 200  # Devuelve una respuesta 200 si la estación se eliminó correctamente
    else:
        return jsonify({'message': 'Station not found'}), 404  # Devuelve una respuesta 404 si la estación no se encontró