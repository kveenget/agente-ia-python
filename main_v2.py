import anthropic
import gspread
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

# Google Sheets setup
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
gc = gspread.authorize(creds)
sheet = gc.open("Calificacion").sheet1

# Anthropic setup
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

historial = []

tools = [
    {
        "name": "guardar_lead",           # nombre de la función
        "description": "Guarda un lead calificado cuando ya tienes nombre, empresa, mensaje y calificación",
        "input_schema": {                  # le dices qué parámetros esperas
            "type": "object",
            "properties": {
                "nombre":       {"type": "string", "description": "Nombre del contacto"},
                "empresa":      {"type": "string", "description": "Nombre de la empresa"},
                "mensaje":      {"type": "string", "description": "Qué quiere importar"},
                "calificacion": {"type": "string", "description": "caliente, tibio o frío"}
            },
            "required": ["nombre", "empresa", "mensaje", "calificacion"]
        }
    }
]


print("Agente listo. Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú: ")

    if user_input.lower() == "salir":
        break

    historial.append({"role": "user", "content": user_input})

    response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    system="""Eres un agente que califica leads para una empresa de importación
    pregunta nomre, empresa y que quieren importar.
    Cuando tengas los 3 datos, usa la tool guardar_lead.""",
    messages=historial,
    tools=tools

)