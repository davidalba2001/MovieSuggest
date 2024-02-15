import sys
sys.path.append('../code')
import recommendation_engine as re

def mostrar_menu():
    print("Bienvenido al Sistema de Recomendaciones")
    print("1. Iniciar sesión")
    print("2. Registrarse ,Feature not yet implemented")
    print("3. Salir")

def log_in():
    while True:
        usuario = input("Usuario: ")
        if re.exist_userid(usuario):
            print("User accepted")
        else:
            print("Incorrect user. Please try again."
)

def obtener_recomendaciones(user_id):
    # Aquí iría la lógica para obtener las recomendaciones de películas para el usuario
    print(f"Estas son las recomendaciones para {user_id}:")
    re.get_topn_movies(user_id,20)


def ver_detalles_pelicula():
    # Aquí iría la lógica para ver los detalles de una película
    print("Detalles de la película seleccionada:")

def main():
    while True:
        mostrar_menu()
        opcion = input("Por favor, seleccione una opción: ")

        if opcion == "1":
            usuario = log_in
            if usuario:
                while True:
                    print("\nMenú principal:")
                    print("1. Obtener recomendaciones de películas")
                    print("2. Ver detalles de una película,Not Implement")
                    print("3. Cerrar sesión")
                    opcion = input("Por favor, seleccione una opción: ")
                    if opcion == "1":
                        obtener_recomendaciones(usuario)
                    elif opcion == "2":
                        ver_detalles_pelicula()
                    elif opcion == "3":
                        print("Cerrando sesión. ¡Hasta luego!")
                        break
                    else:
                        print("Opción no válida. Por favor, seleccione una opción válida.")
                    
        elif opcion == "2":
            print("Opción de registro no implementada aún.")
        elif opcion == "3":
            print("Gracias por usar nuestro sistema de recomendaciones. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")


if __name__ == "__main__":
    main()