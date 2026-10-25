"""Cola simplemente enlazada con referencias head y tail."""


class NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        self.head = None
        self.tail = None

    # esta_vacia: O(1).
    def esta_vacia(self):
        return self.head is None

    # enqueue: O(1), usa tail sin recorrer la cola.
    def enqueue(self, dato):
        nuevo = NodoCola(dato)
        if self.tail is None:
            self.head = nuevo
        else:
            self.tail.siguiente = nuevo
        self.tail = nuevo

    # dequeue: O(1), mueve head al siguiente nodo.
    def dequeue(self):
        if self.esta_vacia():
            raise IndexError("No hay turnos pendientes.")
        dato = self.head.dato
        self.head = self.head.siguiente
        if self.head is None:
            self.tail = None
        return dato

    # agregar_al_inicio: O(1), restaura una atención deshecha.
    def agregar_al_inicio(self, dato):
        nuevo = NodoCola(dato)
        nuevo.siguiente = self.head
        self.head = nuevo
        if self.tail is None:
            self.tail = nuevo

    # quitar_ultimo: O(t), busca el predecesor de tail en una cola simple.
    def quitar_ultimo(self):
        if self.esta_vacia():
            raise IndexError("No hay turnos pendientes.")
        if self.head is self.tail:
            return self.dequeue()
        anterior = self.head
        while anterior.siguiente is not self.tail:
            anterior = anterior.siguiente
        dato = self.tail.dato
        anterior.siguiente = None
        self.tail = anterior
        return dato

    # contiene_dni: O(t), busca entre los t turnos pendientes.
    def contiene_dni(self, dni):
        actual = self.head
        while actual is not None:
            if actual.dato.dni == dni:
                return True
            actual = actual.siguiente
        return False

    # recorrer: O(t), recorre en orden FIFO.
    def recorrer(self):
        actual = self.head
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
