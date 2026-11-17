import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
from unicodedata import normalize, combining

ARCHIVO = Path(__file__).with_name("paises.csv")
CAMPOS = ("nombre", "poblacion", "superficie", "continente", "capital", "moneda", "gentilicio")
CONTINENTES = ("América", "Europa", "Asia", "África", "Oceanía")


def clave(texto):
    return "".join(letra for letra in normalize("NFD", texto.strip().casefold())
                   if not combining(letra))


def entero(texto):
    valor = int(texto)
    if valor <= 0:
        raise ValueError("Ingresá un entero mayor que cero.")
    return valor


def validar(pais):
    if any(not pais[campo] or not pais[campo].strip() for campo in CAMPOS):
        raise ValueError("Todos los campos deben estar completos.")
    if pais["continente"] not in CONTINENTES:
        raise ValueError("Continente inválido.")
    for campo in ("poblacion", "superficie"):
        pais[campo] = entero(pais[campo])
    return pais


def cargar(archivo):
    paises = []
    nombres = set()
    with archivo.open(encoding="utf-8-sig", newline="") as entrada:
        lector = csv.DictReader(entrada, strict=True)
        if lector.fieldnames != list(CAMPOS):
            raise ValueError("Encabezado del CSV inválido.")
        for fila in lector:
            try:
                if None in fila:
                    raise ValueError("Hay columnas adicionales.")
                pais = validar(fila)
                nombre = clave(pais["nombre"])
                if nombre in nombres:
                    raise ValueError("El país está duplicado.")
            except ValueError as error:
                raise ValueError(f"Fila {lector.line_num}: {error}") from error
            nombres.add(nombre)
            paises.append(pais)
    return paises


def guardar(paises, archivo):
    # Se escribe primero un archivo temporal para preservar el CSV si falla la escritura.
    temporal = None
    try:
        with NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                dir=archivo.parent, delete=False) as salida:
            temporal = Path(salida.name)
            escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
            escritor.writeheader()
            escritor.writerows(paises)
        temporal.replace(archivo)
    finally:
        if temporal is not None:
            temporal.unlink(missing_ok=True)


def formatear_numero(valor, decimales=0):
    formato = f"{valor:,.{decimales}f}" if decimales else f"{valor:,d}"
    return formato.translate(str.maketrans(",.", ".,"))


def mostrar(paises):
    if not paises:
        print("No se encontraron países.")
    for pais in paises:
        print(f'{pais["nombre"]} | {pais["continente"]} | Capital: {pais["capital"]} | '
              f'Población: {formatear_numero(pais["poblacion"])} | Superficie: {formatear_numero(pais["superficie"])} km² | '
              f'Moneda: {pais["moneda"]} | Gentilicio: {pais["gentilicio"]}')


def buscar(paises, nombre, exacta):
    consulta = clave(nombre)
    if not consulta:
        raise ValueError("Ingresá un nombre para buscar.")
    if exacta:
        return [pais for pais in paises if clave(pais["nombre"]) == consulta]
    return [pais for pais in paises if consulta in clave(pais["nombre"])]


def alta(paises):
    datos = {campo: input(f"{campo.capitalize()}: ").strip() for campo in CAMPOS}
    pais = validar(datos)
    if buscar(paises, pais["nombre"], True):
        raise ValueError("Ya existe un país con ese nombre.")
    return paises + [pais]


def actualizar(paises):
    coincidencias = buscar(paises, input("Nombre exacto: "), True)
    if not coincidencias:
        raise ValueError("No se encontró el país.")
    original = coincidencias[0]
    nuevo = dict(original, poblacion=entero(input("Población: ")),
                 superficie=entero(input("Superficie en km²: ")))
    return [nuevo if pais is original else pais for pais in paises]


def elegir(opciones, mensaje):
    for numero, opcion in enumerate(opciones, 1):
        print(f"{numero}. {opcion.capitalize()}")
    numero = entero(input(mensaje))
    if numero > len(opciones):
        raise ValueError("Opción inválida.")
    return opciones[numero - 1]


def filtrar(paises):
    campo = elegir(("continente", "poblacion", "superficie"), "Filtro: ")
    if campo == "continente":
        continente = elegir(CONTINENTES, "Continente: ")
        return [pais for pais in paises if pais[campo] == continente]
    minimo = entero(input("Mínimo: "))
    maximo = entero(input("Máximo: "))
    if minimo > maximo:
        raise ValueError("El mínimo debe ser menor o igual al máximo.")
    return [pais for pais in paises if minimo <= pais[campo] <= maximo]


def ordenar(paises):
    campo = elegir(("nombre", "poblacion", "superficie"), "Campo: ")
    sentido = elegir(("ascendente", "descendente"), "Sentido: ")
    return sorted(paises, key=lambda pais: clave(pais[campo]) if campo == "nombre"
                  else pais[campo], reverse=sentido == "descendente")


def estadisticas(paises):
    if not paises:
        print("No hay países para calcular estadísticas.")
        return
    menor = min(pais["poblacion"] for pais in paises)
    mayor = max(pais["poblacion"] for pais in paises)
    for etiqueta, valor in (("Menor población", menor), ("Mayor población", mayor)):
        nombres = ", ".join(pais["nombre"] for pais in paises if pais["poblacion"] == valor)
        print(f"{etiqueta}: {nombres} ({formatear_numero(valor)} habitantes)")
    for campo, etiqueta in (("poblacion", "población"), ("superficie", "superficie en km²")):
        promedio = sum(pais[campo] for pais in paises) / len(paises)
        print(f"Promedio de {etiqueta}: {formatear_numero(promedio, 2)}")
    print(f"Total de países: {len(paises)}")
    for continente in CONTINENTES:
        cantidad = sum(pais["continente"] == continente for pais in paises)
        print(f"{continente}: {cantidad}")


def main():
    try:
        paises = cargar(ARCHIVO)
    except (OSError, ValueError, csv.Error) as error:
        print(f"No se pudo cargar el CSV: {error}")
        return

    opciones = ("agregar país", "actualizar país", "buscar país", "filtrar países",
                "ordenar países", "ver estadísticas", "salir")
    while True:
        print("\nGestión de países")
        try:
            opcion = elegir(opciones, "Opción: ")
            if opcion == "salir":
                break
            if opcion in ("agregar país", "actualizar país"):
                nueva_lista = alta(paises) if opcion == "agregar país" else actualizar(paises)
                guardar(nueva_lista, ARCHIVO)
                paises = nueva_lista
                print("Cambios guardados.")
            elif opcion == "buscar país":
                modo = elegir(("exacta", "parcial"), "Tipo de búsqueda: ")
                mostrar(buscar(paises, input("Nombre: "), modo == "exacta"))
            elif opcion == "filtrar países":
                mostrar(filtrar(paises))
            elif opcion == "ordenar países":
                mostrar(ordenar(paises))
            else:
                estadisticas(paises)
        except (ValueError, OSError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nFin del programa.")
            break


if __name__ == "__main__":
    main()
