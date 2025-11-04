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

# Eliminamos acentos y convierte el texto a minusculas para facilitar comparaciones
def normalizar_texto(t):
    if not t:
        return ""
    texto_normal = unicodedata.normalize('NFKD', t)
    texto_sin_acentos = ''.join(c for c in texto_normal if not unicodedata.combining(c))
    return texto_sin_acentos.strip().lower()

# Funciones clave
def clave_nombre(pais):
    return pais['nombre'].lower()

def clave_poblacion(pais):
    return pais['poblacion']

def clave_superficie(pais):
    return pais['superficie']

# Leemos y validamos los datos del archivo CSV cargandolos en la lista paises
def cargar_datos():
    if not os.path.exists("paises.csv"):
        print("Error: El archivo 'paises.csv' no existe. Coloque el CSV en la misma carpeta y vuelva a ejecutar.")
        return False

    with open("paises.csv", encoding="utf-8") as archivo:
        lineas = [linea.strip() for linea in archivo.readlines() if linea.strip()]

        if not lineas:
            print("Error: El archivo CSV esta vacio.")
            return False

        # Leer encabezado manualmente
        encabezado = lineas[0].split(',')
        columnas_requeridas = ['nombre', 'poblacion', 'superficie', 'continente']

        if not all(col in encabezado for col in columnas_requeridas):
            print("Error: El archivo CSV no tiene las columnas requeridas.")
            return False

        # Indices de las columnas
        indice_nombre = encabezado.index('nombre')
        indice_poblacion = encabezado.index('poblacion')
        indice_superficie = encabezado.index('superficie')
        indice_continente = encabezado.index('continente')

        # Procesar las filas, desde la segunda linea
        for num_linea, linea in enumerate(lineas[1:], 2):
            valores = [v.strip() for v in linea.split(',')]

            # Verificar cantidad de columnas
            if len(valores) < len(columnas_requeridas):
                print(f"Error en linea {num_linea}: numero de columnas insuficiente.")
                return False

            nombre = valores[indice_nombre]
            poblacion_raw = valores[indice_poblacion]
            superficie_raw = valores[indice_superficie]
            continente = valores[indice_continente]

            # Validaciones
            if not nombre:
                print(f"Error en linea {num_linea}: 'nombre' vacio.")
                return False
            if not continente:
                print(f"Error en linea {num_linea}: 'continente' vacio.")
                return False
            if not es_entero(poblacion_raw):
                print(f"Error en linea {num_linea}: 'poblacion' invalida ('{poblacion_raw}'). Debe ser entero.")
                return False
            if not es_float(superficie_raw):
                print(f"Error en linea {num_linea}: 'superficie' invalida ('{superficie_raw}'). Debe ser numerico.")
                return False

            pais = {
                'nombre': nombre,
                'poblacion': int(poblacion_raw),
                'superficie': float(superficie_raw),
                'continente': continente
            }
            paises.append(pais)

        print(f"Datos cargados correctamente. {len(paises)} paises procesados.")
        globals()['paises'] = paises
        return True
    
def buscar_pais_por_nombre(nombre, exacta):
    # Buscamos paises por nombre (coincidencia parcial o exacta)
    if not paises:
        return []
 
    nombre = normalizar_texto(nombre)
    resultados = []
 
    for pais in paises:
        nombre_pais = normalizar_texto(pais['nombre'])
        if exacta:
            if nombre_pais == nombre:
                resultados.append(pais)
        else:
            if nombre in nombre_pais:
                resultados.append(pais)
 
    return resultados
 
def filtrar_por_continente(continente):
    # Filtra paises por continente
    if not paises:
        return []
    continente = normalizar_texto(continente)
    return [pais for pais in paises if normalizar_texto(pais['continente']) == continente]
 
def filtrar_por_rango_poblacion(min_poblacion, max_poblacion):
    # Filtra paises por rango de poblacion
    if not paises:
        return []
 
    min_val = int(min_poblacion) if min_poblacion is not None else 0
    max_val = int(max_poblacion) if max_poblacion is not None else float('inf')
 
    return [pais for pais in paises if min_val <= pais['poblacion'] <= max_val]
 
def filtrar_por_rango_superficie(min_superficie, max_superficie):
    # Filtra paises por rango de superficie
    if not paises:
        return []
 
    min_val = float(min_superficie) if min_superficie is not None else 0.0
    max_val = float(max_superficie) if max_superficie is not None else float('inf')
 
    return [pais for pais in paises if min_val <= pais['superficie'] <= max_val]
 
def ordenar_paises(criterio, tipo):
    # Ordena paises por nombre, poblacion o superficie
    if not paises:
        return []
 
    funciones_clave = {
        'nombre': clave_nombre,
        'poblacion': clave_poblacion,
        'superficie': clave_superficie
    }
    if criterio not in funciones_clave:
        print(f"Error: Criterio '{criterio}' no valido.")
        return paises.copy()
 
    clave_func = funciones_clave[criterio]
    paises_ordenados = sorted(paises, key=clave_func, reverse=not tipo)
    return paises_ordenados
 
def mostrar_estadisticas():
    # Calcula y retorna estadisticas de los paises
    if not paises:
        return {}
 
    pais_max_poblacion = max(paises, key=clave_poblacion)
    pais_min_poblacion = min(paises, key=clave_poblacion)
 
    total_poblacion = sum(p['poblacion'] for p in paises)
    total_superficie = sum(p['superficie'] for p in paises)
    promedio_poblacion = total_poblacion / len(paises)
    promedio_superficie = total_superficie / len(paises)
 
    paises_por_continente = {}
    for p in paises:
        cont = p['continente']
        paises_por_continente[cont] = paises_por_continente.get(cont, 0) + 1
 
    estadisticas = {
        'pais_mayor_poblacion': pais_max_poblacion,
        'pais_menor_poblacion': pais_min_poblacion,
        'promedio_poblacion': promedio_poblacion,
        'promedio_superficie': promedio_superficie,
        'paises_por_continente': paises_por_continente,
        'total_paises': len(paises)
    }
    return estadisticas
 
def mostrar_paises(lista_paises, titulo):
    # Muestra una lista de paises formateada
    if not lista_paises:
        print("No se encontraron paises que coincidan con los criterios.")
        return
 
    print(f"\nResultados ({len(lista_paises)} paises encontrados):")
    linea_separadora
    print(f"{'Nombre':<20} {'Población':<15} {'Superficie':<15} {'Continente':<15}")
    linea_separadora
    for pais in lista_paises:
        print(f"{pais['nombre']:<20} {pais['poblacion']:<15,} {pais['superficie']:<15,.2f} {pais['continente']:<15}")
    linea_separadora()

def mostrar_menu():
    linea_separadora()
    print("        SISTEMA DE GESTION DE PAISES")
    linea_separadora()
    print("1. Buscar pais por nombre\n2. Filtrar paises\n3. Ordenar paises\n4. Mostrar estadisticas\n5. Recargar datos\n6. Salir")
    linea_separadora()

def menu_buscar():
    print("\n--- BUSCAR PAIS POR NOMBRE ---")
    
    # Validar que el nombre no este vacio
    while True:
        nombre = input("Ingrese el nombre del pais a buscar: ").strip()
        if not nombre:
            print("Error: Debe ingresar un nombre.")
            continue
        break

    # Mostrar tipo de busqueda y validar que no se deje vacio ni sea invalido
    print("\nTipo de búsqueda:\n1. Coincidencia parcial\n2. Coincidencia exacta")
    
    while True:
        opcion = input("Seleccione una opcion (1-2): ").strip()
        if not opcion:
            print("Error: Debe ingresar una opcion.")
            continue
        if opcion not in ["1", "2"]:
            print("Opcion no valida. Intente nuevamente.")
            continue
        break

    # Ejecutar la busqueda segun la opcion
    if opcion == "1":
        resultados = buscar_pais_por_nombre(nombre, exacta=False)
        mostrar_paises(resultados, f"Paises que contienen '{nombre}'")
    elif opcion == "2":
        resultados = buscar_pais_por_nombre(nombre, exacta=True)
        mostrar_paises(resultados, f"Paises con nombre exacto '{nombre}'")

def menu_filtrar():
    print("\n--- FILTRAR PAISES ---")
    print("1. Por continente\n2. Por rango de poblacion\n3. Por rango de superficie")

    # Validar opcion vacia o invalida
    while True:
        opcion = input("Seleccione una opcion (1-3): ").strip()
        if not opcion:
            print("Error: Debe ingresar una opcion.")
            continue
        if opcion not in ["1", "2", "3"]:
            print("Opcion no valida. Intente nuevamente.")
            continue
        break
    
    if opcion == "1":
        while True:
            continente = input("Ingrese el continente: ").strip()
            if not continente:
                print("Error: Debe ingresar un continente.")
                continue
            break
        resultados = filtrar_por_continente(continente)
        mostrar_paises(resultados, f"Paises del continente '{continente}'")

    elif opcion == "2":
        while True:
            min_pob = input("Poblacion minima (dejar vacio para 0): ").strip()
            if min_pob and not es_entero(min_pob):
                print("Error: Debe ingresar un numero entero o dejar vacio.")
                continue
            break

        while True:
            max_pob = input("Poblacion maxima (dejar vacio para sin limite): ").strip()
            if max_pob and not es_entero(max_pob):
                print("Error: Debe ingresar un numero entero o dejar vacio.")
                continue
            break

        min_val = int(min_pob) if min_pob else None
        max_val = int(max_pob) if max_pob else None
        resultados = filtrar_por_rango_poblacion(min_val, max_val)
        mostrar_paises(resultados, "Paises filtrados por poblacion")

    elif opcion == "3":
        while True:
            min_sup = input("Superficie minima (dejar vacio para 0): ").strip()
            if min_sup and not es_float(min_sup):
                print("Error: Debe ingresar un numero o dejar vacio.")
                continue
            break

        while True:
            max_sup = input("Superficie maxima (dejar vacio para sin limite): ").strip()
            if max_sup and not es_float(max_sup):
                print("Error: Debe ingresar un numero o dejar vacio.")
                continue
            break

        min_val = float(min_sup) if min_sup else None
        max_val = float(max_sup) if max_sup else None
        resultados = filtrar_por_rango_superficie(min_val, max_val)
        mostrar_paises(resultados, "Paises filtrados por superficie")

def menu_ordenar():
    print("\n--- ORDENAR PAISES ---\n1. Por nombre ascendente (A-Z)\n2. Por nombre descendente (Z-A)\n3. Por poblacion ascendente (menor a mayor)\n4. Por poblacion descendente (mayor a menor)\n5. Por superficie ascendente (menor a mayor)\n6. Por superficie descendente (mayor a menor)")

    # Validar opcion vacia o invalida
    while True:
        opcion = input("Seleccione una opcion (1-6): ").strip()
        if not opcion:
            print("Error: Debe ingresar una opcion.")
            continue
        if opcion not in ["1", "2", "3", "4", "5", "6"]:
            print("Opcion no valida. Intente nuevamente.")
            continue
        break

    opciones_ordenamiento = {
        '1': ('nombre', True),
        '2': ('nombre', False),
        '3': ('poblacion', True),
        '4': ('poblacion', False),
        '5': ('superficie', True),
        '6': ('superficie', False)
    }

    criterio, ascendente = opciones_ordenamiento[opcion]
    resultados = ordenar_paises(criterio, ascendente)
    direccion = "ascendente" if ascendente else "descendente"
    mostrar_paises(resultados, f"Paises ordenados por {criterio} {direccion}")

def menu_estadisticas():
    print("\n--- ESTADISTICAS ---")
    estadisticas = mostrar_estadisticas()
    if not estadisticas:
        print("No hay datos para mostrar estadisticas.")
        return
    print(f"Total de paises: {estadisticas['total_paises']:,}")
    print(f"\nPais con mayor poblacion:")
    print(f"  # {estadisticas['pais_mayor_poblacion']['nombre']}: {estadisticas['pais_mayor_poblacion']['poblacion']:,} habitantes")
    print(f"\nPais con menor poblacion:")
    print(f"  # {estadisticas['pais_menor_poblacion']['nombre']}: {estadisticas['pais_menor_poblacion']['poblacion']:,} habitantes")
    print(f"\nPromedio de poblacion: {estadisticas['promedio_poblacion']:,.2f} habitantes")
    print(f"Promedio de superficie: {estadisticas['promedio_superficie']:,.2f} km2")
    print(f"\nCantidad de paises por continente:")
    for continente, cantidad in estadisticas['paises_por_continente'].items():
        print(f"  # {continente}: {cantidad} paises")

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