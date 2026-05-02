from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel
import json
import os

app = FastAPI()

# Definimos el modelo una sola vez con los campos de TU ESP32
class DatosSensor(BaseModel):
    temperature: float
    pressure: float
    altitude: float

# Para servir archivos HTML usando templates de Jinja2
templates = Jinja2Templates(directory="templates")

# Definimos la ruta del archivo donde guardaremos los datos
DATA_FILE = "datos.json"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/welcome")
async def welcome():
    return {"message": "Welcome to my FastAPI application!"}

# --- EJERCICIO 4: Endpoint POST para guardar datos ---
@app.post("/actualizar_datos")
async def guardar_datos(datos: DatosSensor):
    # Leemos lo que ya hay en el archivo
    lista_datos = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                lista_datos = json.load(f)
            except json.JSONDecodeError:
                lista_datos = []

    # Añadimos el nuevo registro usando los campos correctos
    nuevo_registro = {
        "temperature": datos.temperature, 
        "pressure": datos.pressure, 
        "altitude": datos.altitude
    }
    lista_datos.append(nuevo_registro)

    # Guardamos de nuevo en el JSON
    with open(DATA_FILE, "w") as f:
        json.dump(lista_datos, f, indent=4)
    
    return {"status": "ok", "mensaje": "Datos guardados correctamente"}

# --- EJERCICIO 5: Endpoint GET para leer datos ---
@app.get("/obtener_valores")
async def obtener_valores():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        datos = json.load(f)
        return datos