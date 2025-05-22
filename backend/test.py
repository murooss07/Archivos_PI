import tinytuya

# Datos del dispositivo
DEVICE_NAME = "Televisión"
DEVICE_ID = "xxx"               # Pon el tuyo
DEVICE_IP = "192.168.0.xx"      # Pon la tuya
LOCAL_KEY = "xxx"  # Pon la tuya

# Inicialización del dispositivo
d = tinytuya.OutletDevice(DEVICE_ID, DEVICE_IP, LOCAL_KEY)
d.set_version(3.3)  # Ajusta la versión si es necesario

try:
    result = d.status()
    estado = result['dps'].get('1')

    # Mostrar información
    print(f"Dispositivo: {DEVICE_NAME}")
    print(f"ID: {DEVICE_ID}")
    print(f"Estado: {'Encendido' if estado else 'Apagado'}")

except Exception as e:
    print("❌ Error al conectar con el dispositivo:")
    print(e)
