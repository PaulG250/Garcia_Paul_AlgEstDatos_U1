"""Pila enlazada para el historial de acciones del operador."""


class NodoPila:
    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Pila:
    def __init__(self):
        self.cima = None

    # esta_vacia: O(1), consulta una referencia.
    def esta_vacia(self):
        return self.cima is None

    # push: O(1), enlaza un nodo en la cima.
    def push(self, dato):
        self.cima = NodoPila(dato, self.cima)

    # pop: O(1), retira el nodo de la cima.
    def pop(self):
        if self.esta_vacia():
            raise IndexError("El historial está vacío.")
        dato = self.cima.dato
        self.cima = self.cima.siguiente
        return dato

    # recorrer: O(h), visita las h acciones de la más reciente a la antigua.
    def recorrer(self):
        actual = self.cima
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
