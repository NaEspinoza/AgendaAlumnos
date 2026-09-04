"""
Trabajo Practico N7 - Refactorizado

Mejoras aplicadas:
- Uso de un diccionario para asociar un `id` único a cada alumno.
- Encapsulado en una clase `StudentDB` con type hints y validaciones.
- Interfaz de línea de comandos más robusta y mensajes claros.
"""

from typing import Dict, Optional
import json
from pathlib import Path

sep = "=" * 20


class StudentDB:
    def __init__(self) -> None:
        self._students: Dict[int, Dict[str, str]] = {}
        self._next_id: int = 1

    def _normalize(self, nombre: str, apellido: str) -> Dict[str, str]:
        return {"nombre": nombre.strip().capitalize(), "apellido": apellido.strip().capitalize()}

    def add(self, nombre: str, apellido: str) -> int:
        student = self._normalize(nombre, apellido)
        if any(s["nombre"] == student["nombre"] and s["apellido"] == student["apellido"] for s in self._students.values()):
            raise ValueError("El alumno ya existe")
        id_ = self._next_id
        self._students[id_] = student
        self._next_id += 1
        return id_

    def find_by_fullname(self, nombre: str, apellido: str) -> Optional[int]:
        target = self._normalize(nombre, apellido)
        for id_, s in self._students.items():
            if s == target:
                return id_
        return None

    def update(self, id_: int, nombre: str, apellido: str) -> None:
        if id_ not in self._students:
            raise KeyError("ID no encontrado")
        student = self._normalize(nombre, apellido)
        if any(i != id_ and s == student for i, s in self._students.items()):
            raise ValueError("Otro alumno con ese nombre ya existe")
        self._students[id_] = student

    def delete(self, id_: int) -> None:
        if id_ not in self._students:
            raise KeyError("ID no encontrado")
        del self._students[id_]

    def list(self) -> str:
        if not self._students:
            return "No hay alumnos registrados."
        lines = [f"{sep}"]
        for id_, s in sorted(self._students.items()):
            lines.append(f"{id_:>3}: {s['nombre']}, {s['apellido']}")
        lines.append(sep)
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        # Convertir keys a str para serializar a JSON
        return {str(k): v for k, v in self._students.items()}

    def save(self, path: str) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", encoding="utf-8") as f:
            json.dump({
                "students": self.to_dict(),
                "next_id": self._next_id,
            }, f, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> "StudentDB":
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(path)
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        inst = cls()
        students_raw = data.get("students", {})
        inst._students = {int(k): v for k, v in students_raw.items()}
        inst._next_id = int(data.get("next_id", max(inst._students.keys(), default=0) + 1))
        return inst


def prompt_nonempty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Entrada vacía. Intente de nuevo.")


def cli_create(db: StudentDB) -> None:
    nombre = prompt_nonempty("Ingresa Nombre: ")
    apellido = prompt_nonempty("Ingresa Apellido: ")
    try:
        id_ = db.add(nombre, apellido)
        print(f"\nAlumno agregado con ID: {id_}\n")
    except ValueError as e:
        print(f"Error: {e}")


def cli_update(db: StudentDB) -> None:
    raw = prompt_nonempty("Ingrese ID del alumno a modificar: ")
    try:
        id_ = int(raw)
    except ValueError:
        print("ID inválido. Debe ser un número.")
        return
    nombre = prompt_nonempty("Nuevo Nombre: ")
    apellido = prompt_nonempty("Nuevo Apellido: ")
    try:
        db.update(id_, nombre, apellido)
        print(f"\nAlumno {id_} actualizado correctamente.\n")
    except (KeyError, ValueError) as e:
        print(f"Error: {e}")


def cli_delete(db: StudentDB) -> None:
    raw = prompt_nonempty("Ingrese ID del alumno a eliminar: ")
    try:
        id_ = int(raw)
    except ValueError:
        print("ID inválido. Debe ser un número.")
        return
    try:
        db.delete(id_)
        print(f"\nAlumno {id_} eliminado correctamente.\n")
    except KeyError as e:
        print(f"Error: {e}")


def cli_list(db: StudentDB) -> None:
    print("\n" + db.list() + "\n")


def main() -> None:
    db = StudentDB()
    print(f"{sep * 2}\n\tAgenda de Alumnos\n{sep * 2}")
    menu = (
        "\n[C]rear alumno",
        "[M]odificar alumno",
        "[E]liminar alumno",
        "[L]istar alumnos",
        "[G]uardar/Exportar a JSON",
        "[O]PEN Cargar desde JSON",
        "[S]alir",
    )
    while True:
        for line in menu:
            print(line)
        op = input("\nSelecciona una opción: ").strip().upper()
        if op == "C":
            cli_create(db)
        elif op == "M":
            cli_update(db)
        elif op == "E":
            cli_delete(db)
        elif op == "L":
            cli_list(db)
        elif op == "G":
            path = prompt_nonempty("Ruta archivo para guardar (ej: data/alumnos.json): ")
            try:
                db.save(path)
                print(f"\nGuardado en: {path}\n")
            except Exception as e:
                print(f"Error guardando: {e}")
        elif op == "O":
            path = prompt_nonempty("Ruta archivo para cargar (ej: data/alumnos.json): ")
            try:
                db = StudentDB.load_from_file(path)
                print(f"\nCargado desde: {path}\n")
            except Exception as e:
                print(f"Error cargando: {e}")
        elif op == "S":
            print("\nSaliendo del programa...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    main()