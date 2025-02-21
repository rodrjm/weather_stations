from marshmallow import Schema, fields


class WeatherStationsSchema(Schema):
    """
    Define el esquema para serializar y deserializar los datos de las estaciones meteorológicas.
    """
    id = fields.Integer()  # Define el campo 'id' como un entero
    name = fields.String(required=True)  # Define el campo 'name' como una cadena de texto requerida
    latitude = fields.Float(required=True)  # Define el campo 'latitude' como un número de punto flotante requerido
    longitude = fields.Float(required=True)  # Define el campo 'longitude' como un número de punto flotante requerido


class WeatherDataSchema(Schema):
    """
    Define el esquema para serializar y deserializar los datos registrados por las estaciones meteorológicas.
    """
    id = fields.Integer()  # Define el campo 'id' como un entero
    station_id = fields.Integer()  # Define el campo 'station_id' como un entero
    timestamp = fields.DateTime()  # Define el campo 'timestamp' como una fecha y hora
    temperature = fields.Float()  # Define el campo 'temperature' como un número de punto flotante
    humidity = fields.Float()  # Define el campo 'humidity' como un número de punto flotante
    pressure = fields.Float()  # Define el campo 'pressure' como un número de punto flotante
