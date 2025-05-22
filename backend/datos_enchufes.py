import tinytuya  # Librería para comunicarse con la nube de Tuya y dispositivos locales

ACCESS_ID = "xxx"   # Access ID del proyecto creado en la Tuya IoT Platform (Pon el de tu proyecto)
ACCESS_KEY = "xxx"  # Access Key del mismo proyecto (Pon el de tu proyecto)
API_REGION = "eu"   # Región del centro de datos (puede ser 'us', 'eu', 'cn', 'in', etc.)
# Función principal del script
def main():
    print("Autenticando con Tuya Cloud...")

    # Creamos una instancia del cliente Cloud de tinytuya con tus credenciales
    c = tinytuya.Cloud(
        apiRegion=API_REGION,    # Región de Tuya
        apiKey=ACCESS_ID,        # ID del proyecto
        apiSecret=ACCESS_KEY     # Clave secreta del proyecto
    )

    print("Obteniendo lista de dispositivos...")

    # Obtenemos la lista de dispositivos registrados en Tuya Cloud
    response = c.getdevices()

    if isinstance(response, list):
        devices = response
    elif isinstance(response, dict) and "result" in response:
        devices = response["result"]
    else:
        print("Error inesperado al obtener dispositivos:", response)
        return

    # Verificamos si se encontraron dispositivos
    if not devices:
        print("No se encontraron dispositivos.")
        return

    # Mostramos cuántos dispositivos se encontraron
    print(f"Se encontraron {len(devices)} dispositivo(s):\n")

    # Recorremos la lista de dispositivos y mostramos su información
    for dev in devices:
        name = dev.get("name")               # Nombre del dispositivo
        dev_id = dev.get("id")               # ID único del dispositivo (para controlarlo desde la nube)
        local_key = dev.get("key", "N/A")    # Clave local (para controlarlo desde tu red local con TinyTuya)

        print(f"- {name} (ID: {dev_id}, LocalKey: {local_key})")
