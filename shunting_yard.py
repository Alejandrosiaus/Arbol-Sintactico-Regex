import sys

PRECEDENCIA = {'|': 1, '·': 2, '*': 3, '+': 3, '?': 3}
POSTFIJOS_UNARIOS = {'*', '+', '?'}
SIMBOLO_CONCAT = '·'


class ExpresionInvalida(Exception):
    pass


def tokenizar(expresion):
    tokens = []
    i = 0
    n = len(expresion)

    while i < n:
        c = expresion[i]

        if c == '\\':
            if i + 1 >= n:
                raise ExpresionInvalida(
                    f"Carácter de escape '\\' sin par al final (posición {i + 1})"
                )
            tokens.append(('LIT', expresion[i:i + 2]))
            i += 2

        elif c == '[':
            cierre = expresion.find(']', i + 1)
            if cierre == -1:
                raise ExpresionInvalida(
                    f"Clase de caracteres '[' sin cerrar (posición {i + 1})"
                )
            tokens.append(('LIT', expresion[i:cierre + 1]))
            i = cierre + 1

        elif c == '(':
            tokens.append(('LPAREN', '('))
            i += 1

        elif c == ')':
            tokens.append(('RPAREN', ')'))
            i += 1

        elif c in ('|', '*', '+', '?'):
            tokens.append(('OP', c))
            i += 1

        else:
            tokens.append(('LIT', c))
            i += 1

    return tokens


def validar_operadores(tokens):
    anterior = None
    for idx, (tipo, val) in enumerate(tokens):
        if tipo == 'OP' and val in POSTFIJOS_UNARIOS:
            operando_valido = anterior is not None and (
                anterior[0] in ('LIT', 'RPAREN')
                or (anterior[0] == 'OP' and anterior[1] in POSTFIJOS_UNARIOS)
            )
            if not operando_valido:
                raise ExpresionInvalida(
                    f"El operador '{val}' (posición {idx + 1}) no tiene un "
                    f"operando válido antes de él."
                )
        if tipo == 'OP' and val == '|':
            operando_valido = anterior is not None and (
                anterior[0] in ('LIT', 'RPAREN')
                or (anterior[0] == 'OP' and anterior[1] in POSTFIJOS_UNARIOS)
            )
            if not operando_valido:
                raise ExpresionInvalida(
                    f"El operador '|' (posición {idx + 1}) no tiene un "
                    f"operando válido antes de él."
                )
        anterior = (tipo, val)

    if anterior is not None and anterior[0] == 'OP' and anterior[1] == '|':
        raise ExpresionInvalida("La expresión termina en '|' sin operando después.")


def insertar_concatenacion(tokens):
    resultado = []
    for tok in tokens:
        if resultado:
            anterior = resultado[-1]
            fin_de_operando = anterior[0] in ('LIT', 'RPAREN') or (
                anterior[0] == 'OP' and anterior[1] in POSTFIJOS_UNARIOS
            )
            inicio_de_operando = tok[0] in ('LIT', 'LPAREN')
            if fin_de_operando and inicio_de_operando:
                resultado.append(('OP', SIMBOLO_CONCAT))
        resultado.append(tok)
    return resultado


def a_postfix(tokens):
    pila = []
    salida = []
    pasos = []

    def estado():
        return f"Salida: {' '.join(salida) if salida else '(vacía)'} | Pila: {list(reversed(pila))}"

    for tipo, val in tokens:
        if tipo == 'LIT':
            salida.append(val)
            pasos.append(f"Token '{val}' (literal) -> se agrega a la salida. {estado()}")

        elif tipo == 'LPAREN':
            pila.append('(')
            pasos.append(f"Token '(' -> se apila. {estado()}")

        elif tipo == 'RPAREN':
            while pila and pila[-1] != '(':
                op = pila.pop()
                salida.append(op)
                pasos.append(f"Token ')' -> se desapila '{op}' hacia la salida. {estado()}")
            if not pila:
                raise ExpresionInvalida("Paréntesis desbalanceados: falta '(' correspondiente.")
            pila.pop()
            pasos.append(f"Token ')' -> se descarta el '(' que hace pareja. {estado()}")

        elif tipo == 'OP':
            while (pila and pila[-1] != '('
                   and PRECEDENCIA.get(pila[-1], 0) >= PRECEDENCIA[val]):
                op = pila.pop()
                salida.append(op)
                pasos.append(
                    f"Token '{val}' -> se desapila '{op}' "
                    f"(precedencia >= '{val}'). {estado()}"
                )
            pila.append(val)
            pasos.append(f"Token '{val}' -> se apila. {estado()}")

    while pila:
        op = pila.pop()
        if op == '(':
            raise ExpresionInvalida("Paréntesis desbalanceados: sobra un '('.")
        salida.append(op)
        pasos.append(f"Fin de expresión -> se desapila '{op}' hacia la salida. {estado()}")

    return ' '.join(salida), pasos


def procesar_expresion(expresion):
    tokens = tokenizar(expresion)
    validar_operadores(tokens)
    tokens_concat = insertar_concatenacion(tokens)
    postfix, pasos = a_postfix(tokens_concat)
    return postfix, pasos


def procesar_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            lineas = [linea.rstrip("\n") for linea in f if linea.strip() != ""]
    except FileNotFoundError:
        print(f"ERROR: no se encontró el archivo '{ruta_archivo}'.")
        return

    print("=" * 78)
    print(f"Procesando archivo: {ruta_archivo}")
    print("=" * 78)

    for num, expr in enumerate(lineas, start=1):
        print(f"\nLínea {num} (infix): {expr}")
        print("-" * 78)
        try:
            postfix, pasos = procesar_expresion(expr)
            for paso in pasos:
                print("  " + paso)
            print(f"\n  >> Resultado postfix: {postfix}")
        except ExpresionInvalida as e:
            print(f"  ERROR: {e}")

    print("\n" + "=" * 78)
    print("Fin del procesamiento.")
    print("=" * 78)


if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "problema1_expresiones.txt"
    procesar_archivo(ruta)
