import socket
import tkinter as tk
from tkinter import font

# Configura el cliente
HOST = '192.168.34.78'  # Dirección IP del servidor
PORT = 54321        # Psssuerto en el que escuchará el servidor


# Crea un socket del cliente
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta al servidor
client_socket.connect((HOST, PORT))

# Crear la ventana de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Cuestionario")
ventana.geometry("800x600")  # Aumenta el tamaño de la ventana
ventana.configure(bg="lightgray")

# Variable de control para la etiqueta de la pregunta
pregunta_var = tk.StringVar()
pregunta_var.set("Pregunta del servidor:")

# Etiqueta para mostrar las preguntas
pregunta_label = tk.Label(ventana, textvariable=pregunta_var, bg="lightgray", fg="blue", font=font.Font(family="Arial", size=30))
pregunta_label.pack()

# Lista de radio buttons
radio_buttons = []

# Índice de la respuesta seleccionada
respuesta_seleccionada = tk.IntVar()

# Función para recibir y mostrar preguntas y opciones
def recibir_y_mostrar_pregunta():
    pregunta = client_socket.recv(1024).decode()
    if pregunta == "FIN":
        pregunta_var.set("Acabaron las preguntas.\nPuede cerrar su pantalla.")
        responder_button.config(state="disabled")
        responder_button.pack_forget()

        
        # Elimina botones de opción anteriores
        for radio_button in radio_buttons:
            radio_button.destroy()
        radio_buttons.clear()

    else:
        pregunta_var.set(f"{pregunta}")

        opciones = obtener_opciones_pregunta(pregunta)

        # Elimina botones de opción anteriores
        for radio_button in radio_buttons:
            radio_button.destroy()
        radio_buttons.clear()

        respuesta_seleccionada.set(-1)  # Reinicia la respuesta seleccionada

        # Muestra nuevas opciones
        for i, opcion in enumerate(opciones):
            opcion_button = tk.Radiobutton(ventana, text=opcion, value=i, bg="lightgray", variable=respuesta_seleccionada, font=("Arial", 16),anchor="w")
            opcion_button.pack()
            radio_buttons.append(opcion_button)


# Función para obtener opciones de respuesta a partir de la pregunta
def obtener_opciones_pregunta(pregunta):
    # Puedes implementar lógica para obtener opciones de respuesta según la pregunta.
    # Aquí, devolvemos opciones fijas para ejemplificar.
    if pregunta == "¿A qué crees que sabría el color azul?":
        return ["A menta fresca", "A arándanos", "A algodón de azúcar", " A agua de mar"]
    elif pregunta == "Si los animales pudieran hablar, \n¿cuál crees que sería el más sabio?":
        return ["El búho", "El delfín", "El elefante", "El perro"]
    elif pregunta =="Si pudieras viajar a cualquier planeta, \n¿cuál elegirías?":
        return ["Marte, para explorar sus desiertos", "Júpiter, para ver sus tormentas gigantescas", "Saturno, para admirar sus anillos", "Un exoplaneta desconocido"]
    elif pregunta =="¿Cuál es tú lenguage de programación favorito?":
        return ["Java" , "Python" , "C#", "C++"]
    elif pregunta =="¿Cuál es tú profesor de programación favorito?":
        return ["Juan Sola" , "Omar Díaz" , "Nelliud Torres", "Antonio Huertas", "Rene Rodríguez", "Miguel Veléz"]
    elif pregunta =="¿Cuál es tú lugar de almuerzo preferido en la Universidad?":
        return ["Cafetería(cuando estaba)" , "Las guaguitas" , "Las pastas", "Doordash o Uber Eat", "Prefiero salir" ]
    elif pregunta =="¿Cuál es tú lugar de comida rápida preferido?":
        return ["McDonald's" , "Burger King" , "Wendy's", "Chick-fill-A", "Church's" ]
    elif pregunta =="¿En que año se fundo la UPR de Bayamón?":
        return ["1970" , "1972" , "1971", "1961", "1960" ]
    else:
        return []

# Función para responder la pregunta seleccionada
def responder_pregunta():
    respuesta_index = respuesta_seleccionada.get()
    if respuesta_index != -1:
        opciones = obtener_opciones_pregunta(pregunta_var.get().replace("Pregunta del servidor: ", ""))
        respuesta = opciones[respuesta_index]
        client_socket.send(respuesta.encode())
    recibir_y_mostrar_pregunta()  # Recibe la siguiente pregunta


# Botón para responder preguntas
responder_button = tk.Button(ventana, text="Responder", command=responder_pregunta, bg="green", fg="white", font=("Arial", 14))
responder_button.pack()

# Función para cerrar la ventana y la conexión cuando se cierre la ventana
def cerrar_ventana():
    client_socket.close()
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Recibe la primera pregunta al iniciar la aplicación
recibir_y_mostrar_pregunta()

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()