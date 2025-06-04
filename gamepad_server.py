import vgamepad as vg
import socket
import requests
import json
import os

# Crea dos gamepads
gamepad1 = vg.VX360Gamepad()

# Variable para mantener qué gamepad está activo
active_gamepad = gamepad1

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Esto no necesita estar conectado a Internet, es un "truco" para obtener la IP local
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Ejemplo de uso
print("Mi IP local es:", obtener_ip_local())

def cargar_configuracion():
    try:
        appdata_path = os.getenv('APPDATA')  # e.g., C:\Users\<usuario>\AppData\Roaming
        config_path = os.path.join(appdata_path, 'Gamepad Server', 'config.json')

        with open(config_path, 'r') as archivo:
            config = json.load(archivo)
            return config
    except Exception as e:
        print("Error al leer config.json:", e)
        return {
            "backend_url": "http://localhost",
            "port": 4000
        }
    
config = cargar_configuracion()
backend_ip = config.get("backend_ip")
backend_port = str(config.get("port"))

def enviar_ip_al_backend(ip):
    if not backend_ip:
        print("No se pudo obtener la URL del backend desde config.json")
        return
    
    backend_url = backend_ip + ':' + backend_port + '/registrar_pc'  # Ajusta la URL
    data = { 'ip': ip,
            'id': "PC" }
    try:
        response = requests.post(backend_url, json=data)
        print("Respuesta del backend:", response.status_code, response.text)
    except Exception as e:
        print("Error al enviar IP al backend:", e)

# Al iniciar el servidor:
mi_ip = obtener_ip_local()
enviar_ip_al_backend(mi_ip)

HOST = '0.0.0.0'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Servidor de Gamepad listo en puerto", PORT)

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Conexión establecida con {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode().strip()
                print(f"Comando recibido: {command}")

                if command == "press_a":
                    active_gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    active_gamepad.update()
                    print("Botón A presionado")
                elif command == "release_a":
                    active_gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    active_gamepad.update()
                    print("Botón A liberado")
                elif command == "exit":
                    print("Cerrando servidor")
                    exit()
