# Gestor de turnos del taller CarUPS

Actividad de desarrollo de la Unidad 1 de Algoritmos y Estructuras de Datos.
Programa de consola en Python con pila, cola y lista simplemente enlazada
implementadas desde nodos propios. Las estructuras no usan listas de Python,
`deque` ni colecciones externas como almacenamiento.

## Ejecutar

Requiere Python 3.10 o posterior. No necesita instalar paquetes.
Abre una terminal dentro de esta carpeta y ejecuta:

```console
python main.py
```

En Windows también puedes usar `py main.py` si Python está instalado con ese lanzador.
Para comprobar la versión: `python --version`.

## Archivos

- `pila.py`: nodos de historial, `push`, `pop` y recorrido desde la cima.
- `cola.py`: nodos de turnos con `head` y `tail`; `enqueue` y `dequeue`.
- `lista.py`: cliente con DNI y nombre, nodos y registro enlazado de clientes.
- `main.py`: integración y menú de consola.
- `test_estructuras.py`: ocho pruebas automatizadas de estructuras e integración.

## Uso del menú

1. Agrega un cliente con DNI y nombre. El DNI se guarda como texto para conservar
   ceros iniciales; se aceptan dígitos y no se impone una longitud nacional específica.
2. Agrega otro cliente si deseas observar el orden de atención.
3. Registra los turnos mediante la opción 4, ingresando cada DNI.
4. Consulta los pendientes con la opción 6 y atiende con la opción 5.
5. Usa la opción 7 para deshacer la última acción de turnos.
6. Busca por nombre completo con la opción 2 o muestra todos los clientes con la 3.
7. Consulta el historial con la opción 8 y finaliza con la 0.

Ejemplo: agrega `001 / Ana` y `002 / Luis`; registra los turnos en ese orden.
La primera atención corresponde a Ana. Deshacer esa atención devuelve a Ana al
inicio, antes de Luis. Deshacer ahora el registro más reciente retira el turno de Luis.

La búsqueda por nombre es exacta, ignora mayúsculas y muestra todas las coincidencias.
El registro rechaza DNI repetidos y la cola evita dos turnos pendientes del mismo DNI.
Los clientes se muestran desde la cabeza, del agregado más reciente al más antiguo.
Los datos permanecen en memoria y se pierden al cerrar el programa.

## Estructuras y deshacer

**Pila:** el historial registra únicamente las operaciones exitosas de registrar turno
y atender. LIFO es adecuado porque se debe revertir primero la acción más reciente.
Deshacer realiza `pop` y aplica la operación inversa; no crea otra acción de historial.

**Cola:** FIFO conserva el orden de llegada. `tail` permite agregar al final en O(1)
y `head` permite atender al primero en O(1). Al quedar vacía ambas referencias son `None`.
Deshacer una atención inserta al inicio; deshacer un registro de turno retira el último.
El orden LIFO garantiza que el turno registrado que se deshace vuelve a estar al final.

**Lista enlazada:** conserva los clientes de forma independiente de sus turnos. Agregar
inserta en la cabeza tras comprobar el DNI; buscar y mostrar recorren los nodos.
Deshacer un turno no elimina al cliente registrado. Agregar clientes no es una acción
reversible del historial, cuyo alcance son los turnos y las atenciones.

## Complejidades

Sean c los clientes registrados, t los turnos pendientes y h las acciones del historial.
Se expresa el peor caso; se considera acotada la longitud de DNI y nombre.
Los recorridos con `yield` cuestan O(n) al consumirse por completo.

| Estructura o integración | Operación | Tiempo | Justificación |
| --- | --- | --- | --- |
| Pila | `push`, `pop`, `esta_vacia` | O(1) | Solo consulta o cambia la cima. |
| Pila | `recorrer` | O(h) | Visita las h acciones. |
| Cola | `enqueue`, `dequeue`, `esta_vacia` | O(1) | Usa head y tail sin recorrido. |
| Cola | `agregar_al_inicio` | O(1) | Actualiza head y, si estaba vacía, tail. |
| Cola | `quitar_ultimo` | O(t) | Busca el predecesor del último nodo. |
| Cola | `contiene_dni`, `recorrer` | O(t) | Puede visitar todos los turnos. |
| Lista | `agregar` | O(c) | Busca duplicados O(c) y enlaza en O(1). |
| Lista | `buscar_por_dni`, `buscar_por_nombre`, `recorrer` | O(c) | Recorre hasta c clientes. |
| Gestor | `registrar_turno` | O(c + t) | Busca cliente y turno duplicado; enqueue y push son O(1). |
| Gestor | `atender` | O(1) | Ejecuta dequeue y push. |
| Gestor | `deshacer` atención | O(1) | Pop y reinserción al inicio. |
| Gestor | `deshacer` registro de turno | O(t) | Pop O(1) y retiro del último O(t). |

El espacio total es O(c + t + h): se crea un nodo por cliente, turno y acción vigente.
La cola sigue siendo simplemente enlazada: disponer de tail no permite conocer su
predecesor en O(1), por eso quitar el último requiere recorrido.

## Pruebas

```console
python -m unittest -v
```

Se comprueban LIFO y pila vacía; FIFO, vaciado y reutilización de la cola; operaciones
inversas; registro, búsqueda y recorrido de clientes; validación de datos; reversión
completa de acciones; y que una operación fallida no contamine el historial.

## Repositorio y entrega

Repositorio público del proyecto:
https://github.com/PaulG250/Garcia_Paul_AlgEstDatos_U1

Para descargar y ejecutar el programa:

```console
git clone https://github.com/PaulG250/Garcia_Paul_AlgEstDatos_U1.git
cd Garcia_Paul_AlgEstDatos_U1
python main.py
```
