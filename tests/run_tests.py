from tp7 import StudentDB


def run():
    db = StudentDB()

    # Add
    id1 = db.add("ana", "perez")
    assert id1 == 1
    assert db.find_by_fullname("ana", "perez") == 1

    # Prevent duplicate
    try:
        db.add("ana", "perez")
        raise SystemExit("Expected ValueError for duplicate")
    except ValueError:
        pass

    # Add second
    id2 = db.add("juan", "lopez")
    assert id2 == 2

    # Update
    db.update(id1, "ana maria", "perez")
    assert db.find_by_fullname("ana maria", "perez") == id1

    # Delete
    db.delete(id2)
    assert db.find_by_fullname("juan", "lopez") is None

    # Save and load
    path = "data/test_alumnos.json"
    db.save(path)
    db2 = StudentDB.load_from_file(path)
    assert db2.find_by_fullname("ana maria", "perez") == id1

    print("All tests passed!")


if __name__ == "__main__":
    run()
