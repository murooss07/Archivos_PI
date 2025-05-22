# Diccionario que contiene la configuración de los enchufes inteligentes controlados por TinyTuya
enchufes = {
    "tele": {                  # Identificador lógico para el enchufe de la televisión
        "ip": "192.168.0.xx",  # Dirección IP local del enchufe en la red (Pon la tuya)
        "id_enchufe": "xxx",   # ID único del dispositivo proporcionado por Tuya (Pon el tuyo)
        "clave_local": "xxx",  # Clave local del dispositivo, necesaria para autenticar el control local (Pon la tuya)
    },
    "luz": {                   # Identificador lógico para el enchufe de la luz
        "ip": "192.168.0.xx",  # Dirección IP local del enchufe (Pon la tuya)
        "id_enchufe": "xxx",   # ID único del enchufe de la luz (Pon el tuyo)
        "clave_local": "xxx",  # Clave local correspondiente a este dispositivo (Pon la tuya)
    },
}
