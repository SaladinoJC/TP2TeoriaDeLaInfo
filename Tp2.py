import sys
import os
from collections import Counter

# Función para verificar la inecuación de Kraft-McMillan
def verificar_kraft_mcmillan(longitudes):
    sumatoria = sum(2 ** (-l) for l in longitudes)
    return sumatoria <= 1

# Función para verificar la propiedad de prefijo
def verificar_prefijo(palabras):
    palabras_ordenadas = sorted(palabras, key=len)  # Ordenamos las palabras por longitud
    for i in range(len(palabras_ordenadas)):
        for j in range(i + 1, len(palabras_ordenadas)):
            if palabras_ordenadas[j].startswith(palabras_ordenadas[i]):
                return False
    return True

def procesar_archivo(input_file, output_file=None, N=None):
    # Leer el archivo de entrada
    try:
        with open(input_file, 'r') as f:
            contenido = f.read()
            print(f"Se leyó el archivo {input_file}.")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {input_file}.")
        sys.exit(1)

    # Obtener las palabras separadas por espacios
    palabras = contenido.split()
    
    # Identificar el alfabeto código (caracteres únicos)
    alfabeto_codigo = set(''.join(palabras))  # Unimos todas las palabras y tomamos los caracteres únicos
    print(f"Alfabeto código: {sorted(alfabeto_codigo)}")

    # Obtener las longitudes de las palabras (representan las longitudes de los códigos)
    longitudes = [len(palabra) for palabra in palabras]
    print(f"Longitudes de las palabras: {longitudes}")

    # Verificar si cumple la inecuación de Kraft-McMillan
    cumple_kraft = verificar_kraft_mcmillan(longitudes)
    
    # Verificar la propiedad de prefijo
    cumple_prefijo = verificar_prefijo(palabras)

    if cumple_kraft and cumple_prefijo:
        print("El código cumple con la inecuación de Kraft-McMillan y es instantáneo (no tiene prefijos).")
    elif not cumple_kraft:
        print("El código NO cumple con la inecuación de Kraft-McMillan.")
    elif not cumple_prefijo:
        print("El código NO es instantáneo: una palabra es prefijo de otra.")

    # Si se proporciona un archivo de salida, escribir el resultado en ese archivo
    if output_file:
        with open(output_file, 'w') as f:
            f.write(f"Alfabeto código: {sorted(alfabeto_codigo)}\n")
            f.write(f"Longitudes de las palabras: {longitudes}\n")
            if cumple_kraft and cumple_prefijo:
                f.write("El código cumple con la inecuación de Kraft-McMillan y es instantáneo (no tiene prefijos).\n")
            elif not cumple_kraft:
                f.write("El código NO cumple con la inecuación de Kraft-McMillan.\n")
            elif not cumple_prefijo:
                f.write("El código NO es instantáneo: una palabra es prefijo de otra.\n")
        print(f"Resultado guardado en '{output_file}'.")

def main():
    os.system("cls" if os.name == "nt" else "clear")
     # Verificar los argumentos de la línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python Tp2.py input.txt [output.txt N]")
        sys.exit(1)

    # Asignar los argumentos de entrada
    input_file = sys.argv[1]
    output_file = None
    N = None

    # Verificar si se proporcionaron argumentos opcionales
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]

    if len(sys.argv) == 4:
        try:
            N = int(sys.argv[3])
        except ValueError:
            print("Error: N debe ser un número entero.")
            sys.exit(1)

    # Llamar a la función para procesar el archivo
    procesar_archivo(input_file, output_file, N)

if __name__ == "__main__":
    main()
