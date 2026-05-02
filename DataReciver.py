import serial
import time
import json
import requests

arduino_port = 'COM3' 
baud_rate = 115200 
api_url = "http://localhost:8000/actualizar_datos"

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=2)
    time.sleep(2)
    print(f"Conectado a {arduino_port}")
except Exception as e:
    print(f"Error: {e}")
    exit()

def leer_y_enviar_datos():
    try:
        while True:
            raw_line = ser.readline()
            try:
                # 1. Decodificamos ignorando errores de caracteres extraños
                line = raw_line.decode('utf-8', errors='ignore').strip()
                
                if line:
                    # 2. Buscamos dónde empieza el JSON por si hay basura antes
                    start_index = line.find('{')
                    if start_index != -1:
                        json_str = line[start_index:]
                        datos_dict = json.loads(json_str)
                        
                        print(f"Datos procesados: {datos_dict}")
                        
                        # 3. Enviar a la API
                        response = requests.post(api_url, json=datos_dict)
                        print(f"Respuesta API: {response.status_code}")
                    else:
                        print(f"Línea omitida (no es JSON): {line}")
                        
            except json.JSONDecodeError:
                print(f"Error decodificando JSON en esta línea: {raw_line}")
            except Exception as e:
                print(f"Error inesperado: {e}")

            time.sleep(1)
    except KeyboardInterrupt:
        ser.close()

leer_y_enviar_datos()