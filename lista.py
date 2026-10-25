"""Registro de clientes mediante una lista simplemente enlazada."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    dni: str
    nombre: str


class NodoCliente:
    def __init__(self, cliente, siguiente=None):
        self.cliente = cliente
        self.siguiente = siguiente


class ListaClientes:
    def __init__(self):
        self.cabeza = None

    # agregar: O(c), incluye búsqueda de DNI duplicado; enlazar cuesta O(1).
    def agregar(self, dni, nombre):
        dni, nombre = dni.strip(), nombre.strip()
        if not dni or not dni.isascii() or not dni.isdigit():
            raise ValueError("El DNI debe contener solo dígitos del 0 al 9.")
        if not nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if self.buscar_por_dni(dni) is not None:
            raise ValueError("Ya existe un cliente con ese DNI.")
        cliente = Cliente(dni, nombre)
        self.cabeza = NodoCliente(cliente, self.cabeza)
        return cliente

    # buscar_por_dni: O(c), puede visitar los c clientes.
    def buscar_por_dni(self, dni):
        actual = self.cabeza
        while actual is not None:
            if actual.cliente.dni == dni:
                return actual.cliente
            actual = actual.siguiente
        return None

    # buscar_por_nombre: O(c), comparación exacta sin distinguir mayúsculas.
    def buscar_por_nombre(self, nombre):
        nombre = nombre.strip().casefold()
        actual = self.cabeza
        while actual is not None:
            if actual.cliente.nombre.casefold() == nombre:
                yield actual.cliente
            actual = actual.siguiente

    # recorrer: O(c), visita los nodos desde la cabeza.
    def recorrer(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.cliente
            actual = actual.siguiente
