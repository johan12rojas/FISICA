import math
import random
import tkinter as tk
from tkinter import Label, Button, BooleanVar, Scale, Entry, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import cv2
from tkinter import *
import pygame
from tkinter import simpledialog
import csv
import threading
import time


img=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\imagen4.png')
imgLuna=cv2.imread("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\imgLuna.png")
imgGAMEOVER=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\GAMEOVER.png')
imgGAMEOVER2=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\GAMEOVERLUNA.png')
imgWIN=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\youWIN.png')
imgWIN2=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\youWIN2.png')
imgWIN3=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\youWIN4.png')
imgJupiter=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\imgJupiter.png')
imgGAMEOVER3=cv2.imread('C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\gameOVERJUPITER.png')

pygame.init()
detener_parpadeo = False
# Función para registrar el nombre del jugador
def registrar_nombre():
    nombre = simpledialog.askstring("Registro de Nombre", "INGRESA EL NOMBRE DEL PARTICIPANTE")
    if nombre:
        with open('jugadores.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nombre])
        print("Nombre del jugador:", nombre, "registrado y guardado en el archivo CSV")

#registrar nombre del Usuario        
#
        
def Sonido(variable):
    sonido = pygame.mixer.Sound(variable)
    sonido.play()

# Función para calcular el alcance y la altura máxima del proyectil
def calcular_alcance_y_altura_maxima(v0, angulo, gravedad):
    angulo_rad = math.radians(angulo)
    alcance = (v0 ** 2 * math.sin(2 * angulo_rad)) / gravedad
    altura_maxima = (v0 ** 2 * math.sin(angulo_rad) ** 2) / (2 * gravedad)
    return alcance, altura_maxima

# Función para simular el lanzamiento del proyectil y graficar la trayectoria
def simular_lanzamiento(v0, angulo, gravedad):
    angulo_rad = math.radians(angulo)
    tiempo_vuelo = (2 * v0 * math.sin(angulo_rad)) / gravedad
    t = 0
    dt = tiempo_vuelo / 100  # Dividimos el tiempo de vuelo en 100 intervalos
    x, y = [], []

    while t <= tiempo_vuelo:
        x.append(v0 * math.cos(angulo_rad) * t)
        y.append(v0 * math.sin(angulo_rad) * t - 0.5 * gravedad * t ** 2)
        t += dt

    return x, y

# Función para determinar si el proyectil impacta en la diana
def verificar_impacto(x, y, diana_x, diana_y, ancho_diana, alto_diana):
    return (
        diana_x - ancho_diana / 2 <= x[-1] <= diana_x + ancho_diana / 2 and
        diana_y - alto_diana / 2 <= y[-1] <= diana_y + alto_diana / 2
    )

# Función para actualizar la gráfica con los valores ingresados por el usuario
def actualizar_grafica():
            
    global intentos,impact0
    if intentos < 30:
        
        gravedad = 9.81  # Gravedad de la Tierra en m/s^2
        
        usar_gravedad_luna = gravedad_luna_var.get()
        usar_gravedad_Jupiter = gravedad_Jupiter_var.get()
        
        
        if usar_gravedad_Jupiter:
            gravedad_luna_var.set(False)
            gravedad = 24.79  # Gravedad de Jupiter en m/s^2
            ax.imshow(imgJupiter, extent=[0, 150, 0, 70])
            Sonido("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\laser.mp3")
            
        elif usar_gravedad_luna:
            gravedad_Jupiter_var.set(False)
            gravedad = 1.625  # Gravedad de la Luna en m/s^2
            ax.imshow(imgLuna, extent=[0, 150, 0, 70])
            Sonido("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\laser.mp3")
        else:
            ax.imshow(img, extent=[0, 150, 0, 70])
            Sonido("C:\\Users\\Johan\\Downloads\\y2mate.com - Sonido  Explosión de cañón.mp3")
            
        canvas.draw()
        intentos += 1
        intentos_label.config(text=f"INTENTOS--> {intentos}")
        v0 = velocidad_inicial_slider.get()
        angulo = int(angulo_slider.get())
        angulo_label.config(text=f"Ángulo: {angulo} grados")

        # Calcular el alcance y la altura máxima
        alcance, altura_maxima = calcular_alcance_y_altura_maxima(v0, angulo, gravedad)

        # Simular el lanzamiento y graficar la trayectoria
        x, y = simular_lanzamiento(v0, angulo, gravedad)
        proyectil.set_data(x, y)

        # Verificar si el proyectil impacta en la diana
        impacto = verificar_impacto(x, y, diana_x, diana_y, ancho_diana, alto_diana)

        alcance_label.config(text=f"\n\nAlcance: {alcance:.2f} metros")
        altura_maxima_label.config(text=f"\nAltura máxima: {altura_maxima:.2f} metros")

        if impacto:
            
            if impact0==0:
                Sonido("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\y2mate.com - Win sound effect no copyright.mp3")
                resultado_label.config(text="\nEl Proyectil Impacto en \nEl Objetivo de la Tierra \nPUEDES PASAR A LA LUNA",fg="#2BE6EE",font=("ALGERIAN", 25, "bold"))
                impact0+=1
            
            elif impact0==1:
                Sonido("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\y2mate.com - Win sound effect no copyright.mp3")
                resultado_label.config(text="\nEl Proyectil Impacto en \nEl Objetivo de la Luna \nPUEDES PASAR A JUPITER",fg="#2BE6EE",font=("ALGERIAN", 25, "bold"))
                impact0+=1
                
            elif impact0==2:

                Sonido("C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\y2mate.com - Win sound effect no copyright.mp3")
                resultado_label.config(text="\n¡Ganaste! El proyectil\n ha Impactado.\nRECLAMA UN \nDULCE EN EL STAND",fg="#00FF00",font=("ALGERIAN", 34, "bold"))
                parpadeo_thread = threading.Thread(target=parpadear_mensaje)
                parpadeo_thread.daemon = True
                parpadeo_thread.start()
            
            
            usar_gravedad_luna = gravedad_luna_var.get()
            usar_gravedad_Jupiter=gravedad_Jupiter_var.get()
            if usar_gravedad_luna:
                ax.imshow(imgWIN2, extent=[0, 150, 0, 70])
            elif usar_gravedad_Jupiter:
                ax.imshow(imgWIN3, extent=[0, 150, 0, 70])
            else:
                ax.imshow(imgWIN, extent=[0, 150, 0, 70])
            canvas.draw()
        else:
            resultado_label.config(text="\n\nEl proyectil no impactó\n en el Castillo.",fg="red", bg="#1F3A3D", font=("ALGERIAN", 16, "bold"))

        # Actualizar la gráfica
        canvas.draw()
    else:
        resultado_label.config(text="\n\n¡Has alcanzado el límite\nde intentos!",fg="red",font=("ALGERIAN", 32, "bold"))
        Sonido("C:\\Users\\Johan\\Downloads\\y2mate.com - Arcade game over sound effect.mp3")
        
        usar_gravedad_luna = gravedad_luna_var.get()
        usar_gravedad_Jupiter=gravedad_Jupiter_var.get()
        if usar_gravedad_luna:
            ax.imshow(imgGAMEOVER2, extent=[0, 150, 0, 70])
        elif usar_gravedad_Jupiter:
            ax.imshow(imgGAMEOVER3, extent=[0, 150, 0, 70])
        else:
            ax.imshow(imgGAMEOVER, extent=[0, 150, 0, 70])
        
        canvas.draw()

def parpadear_mensaje():
    for _ in range(5):  # Ejecuta el parpadeo durante 5 segundos
        resultado_label.config(fg="#1F3A3D")
        time.sleep(0.8)  # Cambia el mensaje a blanco cada 0.8 segundos
        resultado_label.config(fg="#00FF00")
        time.sleep(0.8)  # Cambia el mensaje a verde cada 0.8 segundos

# Función para reiniciar la simulación
def reiniciar_simulacion():
    global intentos,impact0
    intentos = -1
    impact0=0
    intentos_label.config(text=f"Intentos: {intentos}")
    velocidad_inicial_slider.set(20.0)
    angulo_slider.set(numero_random)
    gravedad_luna_var.set(False)
    gravedad_Jupiter_var.set(False)
    actualizar_grafica()
    
    # Restaurar la imagen original cuando se presiona "Reiniciar"
    
    ax.imshow(img, extent=[0, 150, 0, 70])
    canvas.draw()

# Inicializar el contador de intentos
intentos = 0
impact0=0

# Configurar la ventana
root = tk.Tk()
imgFondo=PhotoImage(file='C:\\Users\\Johan\\Desktop\\Nueva carpeta (2)\\python\\FONDOUNIVERSIDAD3.png')
lblImagen=Label(root,image=imgFondo).place(x=625,y=-20)

# Configurar el tamaño de la ventana
ancho_ventana = root.winfo_screenwidth()  # Aumenta el ancho de la ventana
alto_ventana = root.winfo_screenheight()  # Aumenta la altura de la ventana
root.geometry(f'{ancho_ventana}x{alto_ventana}')

# Obtener el ancho y alto de la pantalla
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (ancho_pantalla - ancho_ventana) 
y = (alto_pantalla - alto_ventana) 

# Centrar la ventana en la pantalla
root.geometry(f'+{x}+{y}')

# Variables para los valores iniciales
velocidad_inicial_slider = tk.DoubleVar()
numero_random = random.randrange(20, 40)  
angulo_slider = tk.IntVar(value=numero_random)  # Valor inicial del ángulo
gravedad_luna_var = BooleanVar()
gravedad_luna_var.trace_add("write", actualizar_grafica)
gravedad_Jupiter_var = BooleanVar()
gravedad_Jupiter_var.trace_add("write", actualizar_grafica)

# Configurar los valores iniciales
velocidad_inicial_slider.set(20.0)

# Crear un marco en la parte izquierda de la ventana para el contador de intentos y la información del juego
marco_informacion = Frame(root, bg="#1F3A3D", padx=10, pady=10)
marco_informacion.pack(side="left", fill="both", expand=True)

# Etiqueta para mostrar el número de intentos

informacion_label = Label(marco_informacion, text="¡LANZA EL PROYECTIL Y TRATA DE \nIMPACTAR EN EL OBJETIVO!\n💥💥💥\n\n-------------------------------------------------",
                          fg="white", bg="#1F3A3D", padx=10, pady=10, font=("ALGERIAN", 15, "bold"))
informacion_label.pack(side="top")
intentos_label = Label(marco_informacion, text=f"INTENTOS--> {intentos}", fg="white", bg="#1F3A3D", padx=10, pady=5,
                       font=("ALGERIAN", 14, "bold"))
intentos_label.pack(side="top")

# Crear la gráfica con más altura
fig = Figure(figsize=(9, 6))  # Aumenta el segundo valor (alto) para dar más altura al gráfico
ax = fig.add_subplot(111)

# Ajusta los valores según el tamaño de tu imagen de fondo


proyectil, = ax.plot(x, y, 'r--')
ax.set_xlabel("Distancia (m)")
ax.set_ylabel("Altura (m)")

# Configurar la diana en posición horizontal en el suelo
diana_x = 112  # Posición x de la diana
diana_y = 1  # Posición y de la diana en el suelo
ancho_diana = 21  # Ancho de la diana
alto_diana = 3  # Altura de la diana (orientación horizontal)

# Crear un rectángulo en lugar de un círculo para la diana
diana = plt.Rectangle((diana_x - ancho_diana / 2, diana_y - alto_diana / 2), ancho_diana, alto_diana,color="#00FF0000")

ax.add_patch(diana)

# Etiqueta para mostrar el ángulo seleccionado
angulo_label = Label(root, text=f"Ángulo: {angulo_slider.get()} grados", font=("Helvetica", 8, "bold"))

# Botones
actualizar_button = Button(root, text="Disparar ⚠", command=actualizar_grafica, bg="#23BAC4",
                          font=("Helvetica", 8, "bold"))  # Establece el color de fondo en verde
reiniciar_button = Button(root, text="Reiniciar 🔙", command=reiniciar_simulacion, bg="orange",
                          font=("Helvetica", 8, "bold"))  # Establece el color de fondo en naranja


# Etiquetas informativas
Label(root, text="Selecciona la Velocidad Inicial (m/s)",background="#02AC66",  font=("Helvetica", 8, "bold")).pack()
velocidad_inicial_slider_widget = Scale(root, from_=1, to=70, resolution=0.1, variable=velocidad_inicial_slider,
                                        orient="horizontal", length=200,background='#CB3234')
velocidad_inicial_slider_widget.pack()
Label(root, text="Selecciona el Ángulo de Lanzamiento °",background="#02AC66",  font=("Helvetica", 8, "bold")).pack()
angulo_slider_widget = Scale(root, from_=1, to=90, variable=angulo_slider, orient="horizontal", length=200,background='blue')
angulo_slider_widget.pack()
angulo_label.pack()

gravedad_luna_checkbox = tk.Checkbutton(root, text="USAR LA GRAVEDAD DE LA LUNA 1.62 m/s²",background="#A0D02F", fg="darkblue", command=actualizar_grafica, font=("Helvetica", 10, "bold"),
                                       variable=gravedad_luna_var)
gravedad_luna_checkbox.pack()

gravedad_Jupiter_checkbox = tk.Checkbutton(root, text="USAR LA GRAVEDAD DE JUPITER 24.79 m/s²",background="#A0D02F", fg="darkblue", command=actualizar_grafica, font=("Helvetica", 10, "bold"),
                                       variable=gravedad_Jupiter_var)
gravedad_Jupiter_checkbox.pack()

actualizar_button.pack()
reiniciar_button.pack()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Etiquetas para mostrar los resultados a la derecha de la gráfica
alcance_label = Label(marco_informacion, text="ALCANCE--> ", fg="orange", bg="#1F3A3D", font=("ALGERIAN", 16, "bold"))
alcance_label.pack()
altura_maxima_label = Label(marco_informacion, text="ALTURA MAX--> ", fg="orange", bg="#1F3A3D", font=("ALGERIAN", 16, "bold"))
altura_maxima_label.pack()
resultado_label = Label(marco_informacion, text="", fg="red", bg="#1F3A3D", font=("ALGERIAN", 16, "bold"))
resultado_label.pack()
NSIMULADOR = Label(marco_informacion, text="\nSIMULADOR  \nLANZAMIENTO DE \nPROYECTILES ", fg="white", bg="#1F3A3D", font=("ALGERIAN", 30, "bold"))
NSIMULADOR.pack()

# Agregar la imagen al fondo
ax.imshow(img, extent=[0, 150, 0, 70])
canvas.draw()



# Lanzar la aplicación
root.mainloop()