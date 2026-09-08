import os
import sqlite3
import tempfile
import unittest

from db_safety import guarded_connection, make_backup


class DatabaseSafetyTests(unittest.TestCase):
    def make_db(self, path):
        conn = sqlite3.connect(path)
        conn.execute("CREATE TABLE scholarships (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

    def test_zero_byte_database_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "empty.db")
            open(path, "wb").close()
            with self.assertRaises(RuntimeError):
                make_backup(path)

    def test_backup_is_integrity_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "source.db")
            self.make_db(path)
            backup = make_backup(path)
            self.assertGreater(os.path.getsize(backup), 0)
            with sqlite3.connect(backup) as conn:
                self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def test_transaction_rolls_back_on_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "source.db")
            self.make_db(path)
            with self.assertRaises(RuntimeError):
                with guarded_connection(path) as conn:
                    conn.execute("INSERT INTO scholarships (name) VALUES ('not saved')")
                    raise RuntimeError("abort")
            with sqlite3.connect(path) as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
