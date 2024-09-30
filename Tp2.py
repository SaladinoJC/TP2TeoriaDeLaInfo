import sys
import os
import math
import random



def generar_mensaje_aleatorio(palabras, probabilidades, N):
    # Calcula la distribución acumulada
    distribucion_acumulada = []
    suma = 0
    for probabilidad in probabilidades:
        suma += probabilidad
        distribucion_acumulada.append(suma)

    mensaje = []

    for _ in range(N):
        # Genera un número aleatorio entre 0 y 1
        numero_aleatorio = random.random()

        # Selecciona la palabra correspondiente usando la distribución acumulada
        for i, umbral in enumerate(distribucion_acumulada):
            if numero_aleatorio <= umbral:
                mensaje.append(palabras[i])
                break

    return " ".join(mensaje)


# Función para calcular la entropía de la fuente
def calcular_entropia(probabilidades, base):
    entropia = -sum(p * math.log(p, base) for p in probabilidades)
    return entropia


# Función para calcular la longitud media del código
def calcular_longitud_media(probabilidades, longitudes):
    longitud_media = sum(p * l for p, l in zip(probabilidades, longitudes))
    return longitud_media


# Función para calcular las probabilidades de un código compacto
def calcular_probabilidades_compacto(longitudes, r):
    probabilidades = [r**-l for l in longitudes]
    sum_probabilidades = sum(probabilidades)
    return probabilidades, sum_probabilidades


# Función para verificar la inecuación de Kraft-McMillan
def verificar_kraft_mcmillan(longitudes):
    sumatoria = sum(2 ** (-l) for l in longitudes)
    return sumatoria <= 1


# Función para verificar la propiedad de prefijo
def verificar_prefijo(palabras):
    palabras_ordenadas = sorted(palabras, key=len)  # Ordena las palabras por longitud
    for i in range(len(palabras_ordenadas)):
        for j in range(i + 1, len(palabras_ordenadas)):
            if palabras_ordenadas[j].startswith(palabras_ordenadas[i]):
                return False
    return True


def procesar_archivo(input_file, output_file=None, N=None):
    # Lee el archivo de entrada
    try:
        with open(input_file, "r") as f:
            contenido = f.read()
            print(f"Se leyó el archivo {input_file}.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {input_file}.")
        sys.exit(1)

    # Obtiene las palabras separadas por espacios
    palabras = contenido.split()

    # Identifica el alfabeto código (caracteres únicos)
    alfabeto_codigo = set("".join(palabras))
    print(f"Alfabeto código: {sorted(alfabeto_codigo)}")

    # Obtiene las longitudes de las palabras
    longitudes = [len(palabra) for palabra in palabras]
    print(f"Longitudes de las palabras: {longitudes}")

    # Verifica si cumple la inecuación de Kraft-McMillan
    cumple_kraft = verificar_kraft_mcmillan(longitudes)

    # Verifica la propiedad de prefijo
    cumple_prefijo = verificar_prefijo(palabras)

    # Determina si puede conformar un código compacto
    r = len(alfabeto_codigo)
    probabilidades, suma_probabilidades = calcular_probabilidades_compacto(
        longitudes, r
    )

    if math.isclose(suma_probabilidades, 1, rel_tol=1e-9):
        print("El código puede ser compacto.")
        print(f"Probabilidades: {probabilidades}")

        # Calcula la entropía de la fuente
        entropia = calcular_entropia(probabilidades, r)
        print(f"Entropía de la fuente: {entropia}")

        # Calcula la longitud media del código
        longitud_media = calcular_longitud_media(probabilidades, longitudes)
        print(f"Longitud media del código: {longitud_media}")

        # Genera un mensaje de N símbolos codificados si N
        if N:
            mensaje_aleatorio = generar_mensaje_aleatorio(palabras, probabilidades, N)
            print(f"Mensaje generado aleatoriamente: {mensaje_aleatorio}")

        # Si se proporciona un archivo de salida y se ha generado un mensaje aleatorio, escribe el mensaje en el archivo
        if output_file and N:
            try:
                with open(output_file, "w") as f:
                    f.write(mensaje_aleatorio)
                print(f"Mensaje generado y guardado en '{output_file}'.")
            except IOError:
                print(f"Error: No se pudo escribir en el archivo {output_file}.")
                sys.exit(1)

    else:
        print("El código NO puede ser compacto.")
        print(f"Suma de las probabilidades: {suma_probabilidades}")

    if cumple_kraft and cumple_prefijo:
        print(
            "El código cumple con la inecuación de Kraft-McMillan y es instantáneo (no tiene prefijos)."
        )
    elif not cumple_kraft:
        print("El código NO cumple con la inecuación de Kraft-McMillan.")
    elif not cumple_prefijo:
        print("El código NO es instantáneo: una palabra es prefijo de otra.")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    # Verificar los argumentos de la línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python Tp2.py input.txt [output.txt N]")
        sys.exit(1)

    # Asigna los argumentos de entrada
    input_file = sys.argv[1]
    output_file = None
    N = None

    # Verifica si se proporcionaron argumentos opcionales
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]

    if len(sys.argv) == 4:
        try:
            N = int(sys.argv[3])
        except ValueError:
            print("Error: N debe ser un número entero.")
            sys.exit(1)

    # Llama a la función para procesar el archivo
    procesar_archivo(input_file, output_file, N)


if __name__ == "__main__":
    main()
