"""Pruebas: python -m unittest -v. No requiere paquetes externos."""

import unittest

from cola import Cola
from lista import Cliente, ListaClientes
from main import GestorTurnos
from pila import Pila


class PruebasPila(unittest.TestCase):
    def test_lifo_y_vacia(self):
        pila = Pila()
        pila.push("registrar")
        pila.push("atender")
        self.assertEqual(list(pila.recorrer()), ["atender", "registrar"])
        self.assertEqual(pila.pop(), "atender")
        self.assertEqual(pila.pop(), "registrar")
        self.assertTrue(pila.esta_vacia())
        with self.assertRaises(IndexError):
            pila.pop()


class PruebasCola(unittest.TestCase):
    def test_fifo_y_reutilizacion(self):
        cola = Cola()
        cola.enqueue("Ana")
        cola.enqueue("Luis")
        self.assertEqual(cola.dequeue(), "Ana")
        self.assertEqual(cola.dequeue(), "Luis")
        self.assertIsNone(cola.head)
        self.assertIsNone(cola.tail)
        with self.assertRaises(IndexError):
            cola.dequeue()
        cola.enqueue("Eva")
        self.assertIs(cola.head, cola.tail)
        self.assertEqual(cola.dequeue(), "Eva")

    def test_operaciones_para_deshacer(self):
        cola = Cola()
        cola.agregar_al_inicio("Ana")
        self.assertIs(cola.head, cola.tail)
        cola.enqueue("Luis")
        cola.enqueue("Eva")
        self.assertEqual(cola.quitar_ultimo(), "Eva")
        self.assertEqual(list(cola.recorrer()), ["Ana", "Luis"])
        self.assertIsNone(cola.tail.siguiente)
        self.assertEqual(cola.quitar_ultimo(), "Luis")
        self.assertEqual(cola.quitar_ultimo(), "Ana")
        self.assertIsNone(cola.head)
        self.assertIsNone(cola.tail)


class PruebasLista(unittest.TestCase):
    def test_agregar_buscar_y_recorrer(self):
        clientes = ListaClientes()
        ana = clientes.agregar("001", "Ana Pérez")
        otra_ana = clientes.agregar("002", "Ana Pérez")
        self.assertEqual(ana.dni, "001")
        self.assertEqual(list(clientes.recorrer()), [otra_ana, ana])
        self.assertEqual(list(clientes.buscar_por_nombre(" ANA PÉREZ ")), [otra_ana, ana])
        self.assertEqual(clientes.buscar_por_dni("001"), ana)
        self.assertIsNone(clientes.buscar_por_dni("999"))
        self.assertEqual(list(clientes.buscar_por_nombre("Luis")), [])

    def test_validaciones(self):
        clientes = ListaClientes()
        clientes.agregar("001", "Ana")
        for dni, nombre in [("001", "Luis"), ("abc", "Ana"), ("", "Ana"), ("002", " ")]:
            with self.assertRaises(ValueError):
                clientes.agregar(dni, nombre)


class PruebasGestor(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorTurnos()
        self.ana = self.gestor.clientes.agregar("001", "Ana")
        self.luis = self.gestor.clientes.agregar("002", "Luis")

    def test_deshacer_secuencia_completa(self):
        g = self.gestor
        g.registrar_turno("001")
        g.registrar_turno("002")
        self.assertEqual(g.atender(), self.ana)
        g.deshacer()
        self.assertEqual(list(g.turnos.recorrer()), [self.ana, self.luis])
        g.deshacer()
        self.assertEqual(list(g.turnos.recorrer()), [self.ana])
        g.deshacer()
        self.assertTrue(g.turnos.esta_vacia())
        self.assertEqual(list(g.clientes.recorrer()), [self.luis, self.ana])
        with self.assertRaises(IndexError):
            g.deshacer()

    def test_deshacer_atencion_de_cola_vacia(self):
        g = self.gestor
        g.registrar_turno("001")
        g.atender()
        g.deshacer()
        self.assertIs(g.turnos.head, g.turnos.tail)
        self.assertEqual(g.atender(), self.ana)

    def test_errores_no_modifican_historial(self):
        g = self.gestor
        with self.assertRaises(IndexError):
            g.atender()
        with self.assertRaises(ValueError):
            g.registrar_turno("999")
        self.assertTrue(g.historial.esta_vacia())
        g.registrar_turno("001")
        with self.assertRaises(ValueError):
            g.registrar_turno("001")
        self.assertEqual(len(list(g.historial.recorrer())), 1)


if __name__ == "__main__":
    unittest.main()
