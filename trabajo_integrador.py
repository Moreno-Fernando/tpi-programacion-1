import os
import unicodedata

paises = []

def linea_separadora():
    return print("-" * 80)

# funciones de validacion
def es_entero(a):
    a = a.strip()
    return a.isdigit()

def es_float(a):
    a = a.strip()
    float(a)
    return True

def normalizar_texto(t):
    if not t:
        return ""
    texto_normal = unicodedata.normalize('NFKD', t)
    texto_sin_acentos = ''.join(c for c in texto_normal if not unicodedata.combining(c))
    return texto_sin_acentos.strip().lower()

def cargar_datos():
    pass

def mostrar_menu():
    pass

def menu_buscar():
    pass

def menu_filtrar():
    pass

def menu_ordenar():
    pass

def menu_estadisticas():
    pass


def principal():
    if not os.path.exists("paises.csv"):
        print(f"Archivo requerido no encontrado: 'paises.csv'. Debe proporcionarlo antes de ejecutar.")
        return

    if not cargar_datos():
        print("No se pudieron cargar los datos. Saliendo del programa.")
        return

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        if opcion == "1":
            menu_buscar()
        elif opcion == "2":
            menu_filtrar()
        elif opcion == "3":
            menu_ordenar()
        elif opcion == "4":
            menu_estadisticas()
        elif opcion == "5":
            if cargar_datos():
                print("Datos recargados correctamente.")
            else:
                print("Error al recargar los datos.")
        elif opcion == "6":
            print("¡Gracias por usar el sistema de gestion de paises!")
            break
        else:
            print("Opcion no valida. Por favor, seleccione una opcion del 1 al 6.")
        input("\nPresione Enter para continuar...")

# programa principal
principal()