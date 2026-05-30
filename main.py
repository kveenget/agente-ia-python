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
datos_lead = {"nombre": "", "empresa": "", "mensaje": "", "calificacion": ""}

print("Agente listo. Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú: ")

    if user_input.lower() == "salir":
        break

    historial.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="""Eres un agente que califica leads para una empresa de importación.
Pregunta nombre, empresa y qué quieren importar.
Cuando tengas los 3 datos, responde EXACTAMENTE en este formato y nada más:
LEAD|nombre|empresa|mensaje|calificacion
Donde calificacion es: caliente, tibio o frío.""",
        messages=historial
    )

    respuesta = response.content[0].text
    historial.append({"role": "assistant", "content": respuesta})

    if respuesta.startswith("LEAD|"):
        partes = respuesta.split("|")
        sheet.append_row([partes[1], partes[2], partes[3], partes[4]])
        print(f"\nAgente: Lead guardado en Google Sheets ✅\n")
    else:
        print(f"\nAgente: {respuesta}\n")