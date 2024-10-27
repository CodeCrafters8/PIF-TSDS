import logging

def configurar_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Cambia el nivel a INFO para registrar mensajes de info y superiores

    # Crear un manejador para la consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Muestra mensajes de info y superiores en la consola

    # Crear un manejador para el archivo
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)  # También se registran mensajes de info y superiores en el archivo

    # Formato de los mensajes
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Añadir los manejadores al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

