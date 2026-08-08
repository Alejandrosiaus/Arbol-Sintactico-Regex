import os
import sys

from shunting_yard import procesar_expresion, ExpresionInvalida
from arbol_sintactico import postfix_a_arbol, imprimir_arbol, ArbolInvalido
from dibujar_arbol import dibujar_arbol


def procesar_archivo(ruta_archivo, carpeta_imagenes="arboles_generados"):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            lineas = [linea.rstrip("\n") for linea in f if linea.strip() != ""]
    except FileNotFoundError:
        print(f"ERROR: no se encontró el archivo '{ruta_archivo}'.")
        return

    os.makedirs(carpeta_imagenes, exist_ok=True)

    for num, expresion in enumerate(lineas, start=1):
        print("=" * 90)
        print(f"EXPRESIÓN {num}: {expresion}")
        print("=" * 90)

        print("\n--- Paso 1: Shunting Yard (infix -> postfix) ---")
        try:
            postfix, pasos_shunting_yard = procesar_expresion(expresion)
        except ExpresionInvalida as e:
            print(f"  ERROR en la expresión: {e}")
            continue

        for paso in pasos_shunting_yard:
            print("  " + paso)
        print(f"\n  >> Postfix resultante: {postfix}")

        print("\n--- Paso 2: Construcción del árbol sintáctico ---")
        try:
            raiz, pasos_arbol = postfix_a_arbol(postfix)
        except ArbolInvalido as e:
            print(f"  ERROR construyendo el árbol: {e}")
            continue

        for paso in pasos_arbol:
            print("  " + paso)

        print("\n  >> Árbol sintáctico (texto):")
        imprimir_arbol(raiz)

        nombre_archivo = f"arbol_{num:02d}.png"
        ruta_imagen = os.path.join(carpeta_imagenes, nombre_archivo)
        dibujar_arbol(raiz, titulo=expresion, ruta_salida=ruta_imagen)
        print(f"\n  >> Imagen del árbol guardada en: {ruta_imagen}")
        print()

    print("=" * 90)
    print("Fin del procesamiento.")
    print("=" * 90)


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "expresiones.txt"
    procesar_archivo(ruta)
