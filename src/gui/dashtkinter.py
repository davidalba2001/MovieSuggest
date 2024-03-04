import sys
sys.path.append('./src/code')
import tkinter as tk
from tkinter import messagebox
import recommendation_engine as re

class SistemaPeliculas:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Sistema de Clasificación y Recomendación de Películas")

        # Configurar tamaño de la ventana principal
        self.ventana.geometry("1000x800")  # Ancho x Alto

        # Centrar la ventana en la pantalla
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f"+{x}+{y}")

        # Etiqueta y entrada para buscar películas
        self.etiqueta_busqueda = tk.Label(ventana, text="Buscar Película:")
        self.etiqueta_busqueda.grid(row=0, column=0, padx=10, pady=5)
        self.entrada_busqueda = tk.Entry(ventana, width=60)
        self.entrada_busqueda.grid(row=0, column=1, padx=10, pady=5)
        self.boton_buscar = tk.Button(ventana, text="Buscar", command=self.buscar_pelicula)
        self.boton_buscar.grid(row=0, column=2, padx=10, pady=5)

        # Lista para mostrar los resultados de la búsqueda
        self.lista_resultados = tk.Listbox(ventana, height=15, width=80)
        self.lista_resultados.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Botón para clasificar la película seleccionada
        self.boton_clasificar = tk.Button(ventana, text="Clasificar Película", command=self.clasificar_pelicula)
        self.boton_clasificar.grid(row=2, column=0, columnspan=3, padx=10, pady=5)
        
        # Botón para recomendar películas
        self.boton_recomendar = tk.Button(ventana, text="Recomendar", command=self.recomendar_peliculas)
        self.boton_recomendar.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        
        # Diccionario para almacenar las clasificaciones de películas
        self.clasificaciones = {}

        # Obtener la lista de películas de la recomendation engine
        self.lista_peliculas = re.get_movies()

        # Mostrar la lista de películas al iniciar la aplicación
        self.mostrar_lista_peliculas()

    def mostrar_lista_peliculas(self):
        for pelicula in self.lista_peliculas:
            self.lista_resultados.insert(tk.END, pelicula)

    def buscar_pelicula(self):
        # Obtener el término de búsqueda ingresado por el usuario
        termino_busqueda = self.entrada_busqueda.get().lower()

        # Limpiar la lista de resultados antes de mostrar los nuevos resultados
        self.lista_resultados.delete(0, tk.END)

        # Buscar películas que coincidan con el término de búsqueda
        for pelicula in self.lista_peliculas:
            if termino_busqueda in pelicula.lower():
                self.lista_resultados.insert(tk.END, pelicula)

    def clasificar_pelicula(self):
        # Obtenemos la película seleccionada
        seleccion = self.lista_resultados.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Por favor, seleccione una película.")
            return
        pelicula_seleccionada = self.lista_resultados.get(seleccion)
        
        # Creamos una ventana para la clasificación
        ventana_clasificacion = tk.Toplevel(self.ventana)
        ventana_clasificacion.title("Clasificar Película")
        ventana_clasificacion.geometry("400x300")  # Ancho x Alto

        # Centrar la ventana de clasificación en la pantalla
        ventana_clasificacion.update_idletasks()
        width = ventana_clasificacion.winfo_width()
        height = ventana_clasificacion.winfo_height()
        x = (ventana_clasificacion.winfo_screenwidth() // 2) - (width // 2)
        y = (ventana_clasificacion.winfo_screenheight() // 2) - (height // 2)
        ventana_clasificacion.geometry(f"+{x}+{y}")

        # Etiqueta y escala para la clasificación
        etiqueta_clasificacion = tk.Label(ventana_clasificacion, text="Clasificación:")
        etiqueta_clasificacion.grid(row=0, column=0, padx=10, pady=5)
        escala_clasificacion = tk.Scale(ventana_clasificacion, from_=1, to=5, orient=tk.HORIZONTAL, length=200)
        escala_clasificacion.grid(row=0, column=1, padx=10, pady=5)
        
        # Botón para guardar la clasificación
        boton_guardar = tk.Button(ventana_clasificacion, text="Guardar", command=lambda: self.guardar_clasificacion(pelicula_seleccionada, escala_clasificacion.get(), ventana_clasificacion))
        boton_guardar.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

    def guardar_clasificacion(self, pelicula, clasificacion, ventana):
        # Guardamos la clasificación en el diccionario
        self.clasificaciones[pelicula] = clasificacion
        messagebox.showinfo("Éxito", f"Clasificación de '{pelicula}' guardada con éxito: {clasificacion} estrellas.")
        
        # Cerramos la ventana de clasificación
        ventana.destroy()
    
    def recomendar_peliculas(self):
    # Añadir vector o diccionario de clasificaciones al sistema de recomendación
        re.add_vector_to_matrix(self.clasificaciones,self.lista_peliculas)
    
    # Calcular los coeficientes de correlación
        re.calculate_correlation_matrix()
    
    # Obtener las recomendaciones de películas para el usuario actual
        recomendaciones = re.get_topn_movies(re.n_users, 20)
    
        # Encode the movie titles using UTF-8 to handle special characters 
        print(recomendaciones)
        formatted_recommendations = "\n".join([f"{movie}" for movie in recomendaciones])

# Show the recommendations in a messagebox with a more descriptive title
        messagebox.showinfo("Películas Recomendadas", f"Aquí están algunas películas recomendadas:\n\n{formatted_recommendations}")

        self.clasificaciones = {}

def show_larger_info_message(title, message):
    # Create a Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Set the size of the message box
    root.geometry("400x300")  # Adjust the size as needed

    # Show the larger message box
    messagebox.showinfo(title, message)

    # Close the Tkinter window
    root.destroy()

# Crear la ventana principal de la aplicación
ventana_principal = tk.Tk()
app = SistemaPeliculas(ventana_principal)
ventana_principal.mainloop()
