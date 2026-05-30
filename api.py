from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Lead(BaseModel):
    nombre: str
    empresa: str
    mensaje: str

@app.post("/lead")
def recibir_lead(data: Lead):
    print(data)
    return {"status": "recibido"}