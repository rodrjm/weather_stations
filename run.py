from app import create_app


app = create_app()  # Crea una instancia de la aplicación Flask llamando a la función create_app()


if __name__ == '__main__':  # Verifica si el script se está ejecutando directamente (no como un módulo importado)
    app.run(debug=True)  # Inicia el servidor de desarrollo de Flask. La opción debug=True habilita el modo de depuración, que proporciona información de error detallada y recarga automática del servidor
