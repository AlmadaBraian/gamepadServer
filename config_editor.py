import os
import json
import tkinter as tk
from tkinter import messagebox

def obtener_ruta_config():
    appdata_path = os.getenv('APPDATA')
    config_dir = os.path.join(appdata_path, 'Gamepad Server')
    config_path = os.path.join(config_dir, 'config.json')
    return config_dir, config_path

def cargar_config():
    _, config_path = obtener_ruta_config()
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        return {
            "backend_ip": "",
            "port": 4000
        }

def guardar_config():
    config_dir, config_path = obtener_ruta_config()
    os.makedirs(config_dir, exist_ok=True)

    try:
        new_config = {
            "backend_ip": entry_backend_url.get().strip(),
            "port": int(entry_port.get().strip())
        }
        with open(config_path, 'w') as f:
            json.dump(new_config, f, indent=4)
        messagebox.showinfo("Guardado", "Configuración guardada correctamente.")
    except ValueError:
        messagebox.showerror("Error", "El puerto debe ser un número entero.")

# Crear interfaz
ventana = tk.Tk()
ventana.title("Editor de Configuración - Gamepad Server")
ventana.geometry("450x220")

config = cargar_config()

tk.Label(ventana, text="Backend URL:").pack(pady=5)
entry_backend_url = tk.Entry(ventana, width=60)
entry_backend_url.insert(0, config.get("backend_ip", ""))
entry_backend_url.pack()

tk.Label(ventana, text="Puerto:").pack(pady=5)
entry_port = tk.Entry(ventana, width=60)
entry_port.insert(0, str(config.get("port", 4000)))
entry_port.pack()

tk.Button(ventana, text="Guardar", command=guardar_config).pack(pady=10)

ventana.mainloop()
