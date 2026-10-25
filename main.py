"""Gestor de turnos de consola del taller CarUPS. Ejecutar: python main.py."""

from dataclasses import dataclass

from cola import Cola
from lista import Cliente, ListaClientes
from pila import Pila


@dataclass(frozen=True)
class Accion:
    tipo: str
    cliente: Cliente


class GestorTurnos:
    def __init__(self):
        self.clientes = ListaClientes()
        self.turnos = Cola()
        self.historial = Pila()

    # registrar_turno: O(c + t), busca al cliente y evita turnos duplicados.
    def registrar_turno(self, dni):
        cliente = self.clientes.buscar_por_dni(dni.strip())
        if cliente is None:
            raise ValueError("Primero registra al cliente con la opción 1.")
        if self.turnos.contiene_dni(cliente.dni):
            raise ValueError("El cliente ya tiene un turno pendiente.")
        self.turnos.enqueue(cliente)
        self.historial.push(Accion("registrar", cliente))
        return cliente

    # atender: O(1), combina dequeue y push.
    def atender(self):
        cliente = self.turnos.dequeue()
        self.historial.push(Accion("atender", cliente))
        return cliente

    # deshacer: O(t) si revierte un registro de turno y O(1) una atención.
    # LIFO permite revertir primero la acción más reciente, conservando el orden.
    def deshacer(self):
        accion = self.historial.pop()
        if accion.tipo == "registrar":
            self.turnos.quitar_ultimo()
        else:
            self.turnos.agregar_al_inicio(accion.cliente)
        return accion


# mostrar_clientes: O(n), consume y muestra un recorrido completo.
def mostrar_clientes(clientes):
    hay_datos = False
    for cliente in clientes:
        hay_datos = True
        print(f"DNI: {cliente.dni} | Nombre: {cliente.nombre}")
    if not hay_datos:
        print("No hay resultados.")


def main():
    gestor = GestorTurnos()
    menu = """
=== Taller CarUPS ===
1. Agregar cliente
2. Buscar clientes por nombre
3. Mostrar clientes registrados
4. Registrar turno
5. Atender siguiente turno
6. Mostrar turnos pendientes
7. Deshacer última acción de turnos
8. Mostrar historial
0. Salir
"""
    while True:
        try:
            print(menu)
            opcion = input("Opción: ").strip()
            if opcion == "0":
                print("Hasta pronto.")
                break
            if opcion == "1":
                cliente = gestor.clientes.agregar(input("DNI: "), input("Nombre: "))
                print(f"Cliente registrado: {cliente.nombre}.")
            elif opcion == "2":
                mostrar_clientes(gestor.clientes.buscar_por_nombre(input("Nombre completo: ")))
            elif opcion == "3":
                mostrar_clientes(gestor.clientes.recorrer())
            elif opcion == "4":
                cliente = gestor.registrar_turno(input("DNI del cliente: "))
                print(f"Turno registrado para {cliente.nombre}.")
            elif opcion == "5":
                print(f"Cliente atendido: {gestor.atender().nombre}.")
            elif opcion == "6":
                mostrar_clientes(gestor.turnos.recorrer())
            elif opcion == "7":
                accion = gestor.deshacer()
                print(f"Acción deshecha: {accion.tipo} - {accion.cliente.nombre}.")
            elif opcion == "8":
                # Mostrar historial: O(h).
                if gestor.historial.esta_vacia():
                    print("El historial está vacío.")
                for accion in gestor.historial.recorrer():
                    print(f"{accion.tipo}: {accion.cliente.dni} - {accion.cliente.nombre}")
            else:
                print("Opción inválida. Elige un número del menú.")
        except (ValueError, IndexError) as error:
            print(f"Aviso: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break


if __name__ == "__main__":
    main()
