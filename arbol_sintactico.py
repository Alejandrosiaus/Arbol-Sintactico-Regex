import copy
from nodo import Nodo
from shunting_yard import SIMBOLO_CONCAT

OPERADORES_BINARIOS = {'|', SIMBOLO_CONCAT}
OPERADORES_UNARIOS_DIRECTOS = {'*'}
OPERADORES_UNARIOS_SIMPLIFICABLES = {'+', '?'}


class ArbolInvalido(Exception):
    pass


def _clonar(nodo):
    if nodo is None:
        return None
    return Nodo(nodo.valor, _clonar(nodo.izq), _clonar(nodo.der))


def postfix_a_arbol(postfix_str, pasos=None):
    if pasos is None:
        pasos = []

    tokens = postfix_str.split()
    pila = []

    def estado():
        return f"Pila: {[n.valor for n in pila]}"

    for tok in tokens:
        if tok in OPERADORES_UNARIOS_DIRECTOS:
            if not pila:
                raise ArbolInvalido(f"'{tok}' sin operando en la pila.")
            hijo = pila.pop()
            nuevo = Nodo('*', hijo)
            pila.append(nuevo)
            pasos.append(f"'*' -> Nodo(*) con hijo {hijo.valor!r}. {estado()}")

        elif tok == '+':
            if not pila:
                raise ArbolInvalido("'+' sin operando en la pila.")
            x = pila.pop()
            x_estrella = Nodo('*', _clonar(x))
            nuevo = Nodo(SIMBOLO_CONCAT, x, x_estrella)
            pila.append(nuevo)
            pasos.append(
                f"'+' -> simplificado como (X · X*) sobre {x.valor!r}. {estado()}"
            )

        elif tok == '?':
            if not pila:
                raise ArbolInvalido("'?' sin operando en la pila.")
            x = pila.pop()
            epsilon = Nodo('ε')
            nuevo = Nodo('|', x, epsilon)
            pila.append(nuevo)
            pasos.append(
                f"'?' -> simplificado como (X | ε) sobre {x.valor!r}. {estado()}"
            )

        elif tok in OPERADORES_BINARIOS:
            if len(pila) < 2:
                raise ArbolInvalido(f"'{tok}' necesita 2 operandos en la pila.")
            der = pila.pop()
            izq = pila.pop()
            nuevo = Nodo(tok, izq, der)
            pila.append(nuevo)
            pasos.append(
                f"'{tok}' -> Nodo({tok}) con hijos {izq.valor!r} y {der.valor!r}. {estado()}"
            )

        else:
            nuevo = Nodo(tok)
            pila.append(nuevo)
            pasos.append(f"'{tok}' -> Nodo hoja. {estado()}")

    if len(pila) != 1:
        raise ArbolInvalido(
            f"Postfix inválido: quedaron {len(pila)} nodos en la pila (se esperaba 1)."
        )

    return pila[0], pasos


def imprimir_arbol(nodo, prefijo="", es_ultimo=True):
    conector = "└── " if es_ultimo else "├── "
    print(prefijo + conector + str(nodo.valor))

    hijos = [h for h in (nodo.izq, nodo.der) if h is not None]
    nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
    for i, hijo in enumerate(hijos):
        imprimir_arbol(hijo, nuevo_prefijo, i == len(hijos) - 1)
