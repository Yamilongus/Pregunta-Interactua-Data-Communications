import socket
import tkinter as tk

# Configura el servidor
HOST = '25.62.255.165'  # Dirección IP del servidor
PORT = 54321        # Puerto en el que escuchará el servidor

# Lista de preguntas predefinidas
preguntas = [
    "¿A qué crees que sabría el color azul?",
    "Si los animales pudieran hablar, \n¿cuál crees que sería el más sabio?",
    "Si pudieras viajar a cualquier planeta, \n¿cuál elegirías?",
    "¿Cuál es tú lenguage de programación favorito?",
    "¿Cuál es tú profesor de programación favorito?",
    "¿Cuál es tú lugar de almuerzo preferido en la Universidad?",
    "¿Cuál es tú lugar de comida rápida preferido?",
    "¿En que año se fundo la UPR de Bayamón?",
    "FIN"
]

# Crea un socket del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlaza el socket al host y puerto
server_socket.bind((HOST, PORT))

# Escucha conexiones entrantes
server_socket.listen()

print(f"Servidor escuchando en {HOST}:{PORT}")

# Acepta una conexión entrante
client_socket, client_address = server_socket.accept()
print(f"Conexión entrante de {client_address}")

# Función para enviar preguntas automáticamente
def enviar_preguntas_automaticamente():
    for pregunta in preguntas:
        client_socket.send(pregunta.encode())
        respuesta = client_socket.recv(1024).decode()
        mostrar_respuesta(pregunta, respuesta)

# Función para mostrar las respuestas en la GUI
def mostrar_respuesta(pregunta, respuesta):
    respuesta_text.config(state=tk.NORMAL)
    respuesta_text.insert(tk.END, f"{pregunta}\n {respuesta}\n\n")

    respuesta_text.config(state=tk.DISABLED)

# Crea una ventana de la GUI
ventana = tk.Tk()
ventana.title("Respuestas del Usuario")

# Crea un área de texto para mostrar las respuestas
respuesta_text = tk.Text(ventana, wrap=tk.WORD, state=tk.DISABLED)
respuesta_text.pack()

# Iniciar el envío automático de preguntas
enviar_preguntas_automaticamente()

# Función para cerrar la ventana y la conexión cuando se cierre la ventana
def cerrar_ventana():
    client_socket.close()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()

# Cierra el socket del servidor
server_socket.close()
