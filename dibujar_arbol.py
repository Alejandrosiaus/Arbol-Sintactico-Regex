import networkx as nx
import matplotlib.pyplot as plt


def _construir_grafo(nodo, grafo=None, id_padre=None):
    if grafo is None:
        grafo = nx.DiGraph()

    grafo.add_node(nodo.id, label=nodo.valor)
    if id_padre is not None:
        grafo.add_edge(id_padre, nodo.id)

    if nodo.izq is not None:
        _construir_grafo(nodo.izq, grafo, nodo.id)
    if nodo.der is not None:
        _construir_grafo(nodo.der, grafo, nodo.id)

    return grafo


def _calcular_posiciones(nodo, profundidad=0, contador_x=None, posiciones=None):
    if contador_x is None:
        contador_x = [0]
    if posiciones is None:
        posiciones = {}

    hijos = [h for h in (nodo.izq, nodo.der) if h is not None]

    if not hijos:
        x = contador_x[0]
        contador_x[0] += 1
    else:
        for hijo in hijos:
            _calcular_posiciones(hijo, profundidad + 1, contador_x, posiciones)
        x = sum(posiciones[h.id][0] for h in hijos) / len(hijos)

    posiciones[nodo.id] = (x, -profundidad)
    return posiciones


def dibujar_arbol(raiz, titulo, ruta_salida):
    grafo = _construir_grafo(raiz)
    posiciones = _calcular_posiciones(raiz)
    etiquetas = nx.get_node_attributes(grafo, 'label')

    num_hojas = sum(1 for n in grafo.nodes if grafo.out_degree(n) == 0)
    ancho = max(6, num_hojas * 1.1)

    plt.figure(figsize=(ancho, 5))
    nx.draw(
        grafo,
        posiciones,
        labels=etiquetas,
        with_labels=True,
        node_color="#AED6F1",
        edgecolors="#2E4053",
        node_size=1400,
        font_size=11,
        font_weight="bold",
        arrows=False,
        linewidths=1.5,
    )
    plt.title(titulo, fontsize=13)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(ruta_salida, dpi=150)
    plt.close()
