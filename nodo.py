class Nodo:
    _contador_global = 0

    def __init__(self, valor, izq=None, der=None):
        self.valor = valor
        self.izq = izq
        self.der = der

        self.id = Nodo._contador_global
        Nodo._contador_global += 1

    def es_hoja(self):
        return self.izq is None and self.der is None

    def es_unario(self):
        return self.izq is not None and self.der is None

    def es_binario(self):
        return self.izq is not None and self.der is not None

    def __repr__(self):
        return f"Nodo({self.valor!r})"
