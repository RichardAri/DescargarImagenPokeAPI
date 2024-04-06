import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import filedialog

def obtener_sprite_frontal(nombre_pokemon):
    url_base = "https://pokeapi.co/api/v2/pokemon/"
    url_pokemon = f"{url_base}{nombre_pokemon.lower()}"
    response = requests.get(url_pokemon)
    if response.status_code == 200:
        data = response.json()
        sprite_url = data["sprites"]["front_default"]
        return sprite_url
    else:
        print(f"Error al obtener los datos del Pokémon {nombre_pokemon}: {response.status_code}")
        return None

def cargar_sprite_frontal():
    nombre_pokemon = entrada_nombre.get() or "pikachu" 
    sprite_frontal = obtener_sprite_frontal(nombre_pokemon)
    if sprite_frontal:
        response = requests.get(sprite_frontal)
        imagen_bytes = response.content
        imagen = Image.open(BytesIO(imagen_bytes))

        ancho_original, alto_original = imagen.size
        nuevo_ancho = int(ancho_original * 2 + 300)
        nuevo_alto = int(alto_original * 2 + 300)
        imagen = imagen.resize((nuevo_ancho, nuevo_alto))
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta.config(image=imagen_tk)
        etiqueta.image = imagen_tk 
        ventana.title(nombre_pokemon.capitalize())
        
        #guardar en una ruta con nombre por default
        boton_guardar = tk.Button(ventana, text="Guardar Imagen", command=lambda: guardar_imagen(imagen, nombre_pokemon))
        boton_guardar.pack()

    else:
        print("No se pudo obtener el sprite frontal del Pokémon.")


def guardar_imagen(imagen, nombre_pokemon):
    nombre_archivo = f"{nombre_pokemon}.png"
    ruta_destino = filedialog.asksaveasfilename(defaultextension=".png", initialfile=nombre_archivo, filetypes=[("Archivos PNG", "*.png")])
    if ruta_destino:
        imagen.save(ruta_destino)
        print(f"Imagen guardada en {ruta_destino}")


#GUI
ventana = tk.Tk()
ventana.title("Cargar Sprite Pokémon")

entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack()

#nombre por default para la primera carga
entrada_nombre.insert(tk.END, "pikachu")
boton_cargar = tk.Button(ventana, text="Cargar Imagen", command=cargar_sprite_frontal)
boton_cargar.pack()
etiqueta = tk.Label(ventana)
etiqueta.pack()

cargar_sprite_frontal()

ventana.mainloop()
