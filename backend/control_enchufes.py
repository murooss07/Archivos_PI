import tinytuya  # Librería para controlar dispositivos Tuya localmente
from enchufes import enchufes  # Diccionario con la configuración de los enchufes

# Enciende o apaga un enchufe inteligente Tuya según el nombre del dispositivo y la acción deseada.
def switch_device(device_name: str, turn_on: bool):
    print(f"Llamando a switch_device para {device_name}, encender={turn_on}")

# Verificar si el dispositivo existe en la configuración
    if device_name not in enchufes:
        return {"status": "error", "detail": "Dispositivo no encontrado"}

    # Obtener configuración del enchufe desde el diccionario
    config = enchufes[device_name]

    # Crear una instancia del dispositivo Tuya con los datos necesarios
    d = tinytuya.OutletDevice(config["id_enchufe"], config["ip"], config["clave_local"])
    d.set_version(3.3)  # Establecer la versión del protocolo Tuya
  
    try:
        # Cambiar el estado del enchufe (DP 1 es el que controla encendido/apagado)
        d.set_status(turn_on, 1)
        return {"status": "ok", "device": device_name, "action": "on" if turn_on else "off"}
    except Exception as e:
        # Capturar y devolver cualquier error que ocurra
        return {"status": "error", "detail": str(e)}
