import pywhatkit as kit
import time
import datetime

numero_destino = "+573225500380"  # Reemplaza con el número al que deseas enviar el mensaje

# Supongamos que 'mensajes' es tu array con los mensajes a enviar
mensajes = [
    "Pendejo",
    "Sapo",
    "Mujeriego",
    # Añade aquí los mensajes adicionales que desees enviar
]

# Obtener la hora actual
hora_actual = datetime.datetime.now()

# Hora a la que quieres enviar el mensaje
hora_envio = hora_actual.replace(hour=21, minute=35, second=0)

# Enviar cada mensaje del array a las 9:20 PM con un minuto de diferencia
for i, mensaje in enumerate(mensajes):
    tiempo_envio = hora_envio + datetime.timedelta(minutes=i)
    kit.sendwhatmsg(numero_destino, mensaje, tiempo_envio.hour, tiempo_envio.minute)
