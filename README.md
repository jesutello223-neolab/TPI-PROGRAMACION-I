# Gestión de datos de países

Trabajo Práctico Integrador de Programación 1. El programa usa una lista de diccionarios, uno por país, y guarda los registros en un archivo CSV.

## Ejecución

Abrí una terminal en esta carpeta y ejecutá `python gestion_paises.py`. Se requiere Python 3.8 o posterior. El programa utiliza la biblioteca estándar de Python y lee `paises.csv` desde la misma carpeta que el código.

## Opciones y ejemplos

- **Agregar país**. Ingresá los siete campos. Para la demostración, Uruguay se carga con población 3384688, superficie 181034 km², continente América, capital Montevideo, moneda Peso uruguayo (UYU) y gentilicio uruguayo/a.
- **Actualizar país**. Buscá por el nombre exacto e ingresá la nueva población y superficie.
- **Buscar país**. Una búsqueda parcial por `Arg` devuelve Argentina y Argelia. La búsqueda exacta por `argentina` devuelve solo Argentina. Se admiten consultas con o sin tildes.
- **Filtrar países**. Elegí un continente o un rango inclusivo de población o superficie.
- **Ordenar países**. Elegí nombre, población o superficie y el sentido del orden.
- **Ver estadísticas**. El CSV inicial contiene 85 países. Los recuentos son 20 en América, 20 en Europa, 20 en Asia, 20 en África y 5 en Oceanía.

El programa rechaza nombres duplicados, campos vacíos, enteros inválidos y rangos invertidos. Las altas y actualizaciones se guardan en el CSV. La consola muestra población y superficie con puntos de miles (por ejemplo, 1.000 y 10.000.000) y usa coma para los decimales de los promedios. Para ingresar valores, escribí los enteros sin separadores.

## Datos

La población corresponde a 2025 y se obtuvo del [Banco Mundial](https://data.worldbank.org/indicator/SP.POP.TOTL). La superficie en km² y las fichas de referencia provienen del [conjunto de datos Countries](https://github.com/mledoze/countries). Para las formas en español se consultó el [Diccionario panhispánico de dudas](https://www.rae.es/dpd/ayuda/paises-y-capitales-con-sus-gentilicios). *Geo Atlas 360* (Editorial Visor, 2011) se incluye como referencia bibliográfica para superficie, capital y moneda. El detalle de las consultas figura en el [registro de fuentes](Registro%20de%20fuentes.md).

## Entrega

Trabajo individual de **Tello Arce Jesús Alberto**. El proyecto abarca la preparación del conjunto de datos, el programa de gestión y la demostración de sus funciones.

- [Informe del TPI con capturas](Informe%20TPI.pdf)
- [Video de demostración en Google Drive](https://drive.google.com/file/d/1XWfya2svviumwyDCG9mEnswiM2OSLHcH/view?usp=drive_link)
