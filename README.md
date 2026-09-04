**TP7 - Agenda de Alumnos (Refactorizado)**

- **Resumen:**: Proyecto que gestiona alumnos usando una clase `StudentDB` que asocia un `id` único a cada alumno y ofrece operaciones CRUD, persistencia en JSON y una interfaz de línea de comandos.

**Arquitectura y archivos**
- **`tp7.py`**: Implementación principal con la clase `StudentDB`, funciones de CLI y soporte para guardar/cargar en JSON.
- **`tests/run_tests.py`**: Pequeño runner para comprobar las operaciones básicas (add/update/delete/find).

**Explicación paso a paso del código en `tp7.py`**

- **Encabezado y dependencias:**
  - Se importan `typing` para tipos, `json` para persistencia y `Path` para manejo de rutas.

- **Constantes:**
  - `sep` es una línea separadora usada en la salida por consola.

- **Clase `StudentDB`:**
  - `__init__`: Inicializa `_students` como diccionario vacío y `_next_id` en 1.
  - `_normalize(nombre, apellido)`: Limpia espacios y capitaliza nombre/apellido para normalizar las entradas.
  - `add(nombre, apellido)`: Añade un alumno si no existe duplicado. Devuelve el `id` asignado.
  - `find_by_fullname(nombre, apellido)`: Busca y devuelve el `id` si existe, o `None` si no.
  - `update(id_, nombre, apellido)`: Actualiza un alumno por `id`, con comprobación de existencia y duplicados.
  - `delete(id_)`: Elimina el alumno indicado por `id`.
  - `list()`: Devuelve una representación en texto de todos los alumnos, ordenados por `id`.
  - `to_dict()`: Convierte la estructura interna a un diccionario con claves string para JSON.
  - `save(path)`: Guarda el estado en un archivo JSON (crea directorios si es necesario).
  - `load_from_file(path)`: Método de clase que carga desde JSON, conviernte claves a `int` y fija `_next_id`.

- **Funciones de interacción (CLI):**
  - `prompt_nonempty(prompt)`: Repite la petición hasta recibir una entrada no vacía.
  - `cli_create`, `cli_update`, `cli_delete`, `cli_list`: Envolturas que interactúan con el usuario, manejan excepciones y llaman a los métodos de `StudentDB`.

- **`main()`**
  - Inicia la base de datos en memoria y muestra un menú sencillo.
  - Nuevas opciones: `G` guarda a JSON, `O` carga desde JSON.

**Pruebas**
- Ejecuta `python3 tests/run_tests.py` para validar operaciones básicas.

**Cómo usar**
- Ejecuta el script con `python3 tp7.py`.
- Para guardar: elige `G` y escribe una ruta de archivo (por ejemplo `data/alumnos.json`).
- Para cargar: elige `O` y escribe la ruta al JSON.

**Buenas prácticas aplicadas**
- Encapsulación en una clase con API clara.
- Validaciones de entrada y manejo de errores.
- Separación entre lógica (StudentDB) y presentación/CLI.
- Persistencia simple y portátil (JSON).

---
Overview: `tp7.py` es un ejemplo pequeño pero completo para gestionar entidades simples (alumnos) en memoria, con persistencia opcional y una CLI fácil de usar; está organizado para facilitar pruebas, extensión y reuso.
