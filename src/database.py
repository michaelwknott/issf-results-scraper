import sqlite3

DB_FILENAME: str = "issf.db"
TABLE_NAME: str = "competitions"
TABLE_COLUMNS: dict[str, str] = {
    "championship": "TEXT NOT NULL",
    "year": "TEXT NOT NULL",
    "city": "TEXT NOT NULL",
    "event": "TEXT NOT NULL",
    "category": "TEXT NOT NULL",
    "id": "TEXT PRIMARY KEY",
}


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self.database_filename = database_filename
        self.connection = sqlite3.connect(self.database_filename)

    def __del__(self) -> None:
        self.connection.close()

    def _execute(
        self, sql_statement: str, values: tuple[str, ...] | None = None
    ) -> sqlite3.Cursor:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(sql_statement, values or [])
            return cursor

    def _execute_many(
        self, sql_statement: str, values: tuple[str, ...] | None = None
    ) -> sqlite3.Cursor:
        with self.connection:
            cursor = self.connection.cursor()
            cursor.executemany(sql_statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: dict[str, str]) -> None:
        columns_with_types = [
            f"{column_name} {column_type}"
            for column_name, column_type in columns.items()
        ]

        self._execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            """
        )

    def add(self, table_name: str, data: dict[str, str]) -> None:
        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        self._execute(
            f"""
            INSERT OR IGNORE INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """,
            column_values,
        )

    def add_many(self, table_name: str, data: dict[str, str]) -> None:
        placeholders = ", ".join("?" * len(data))
        column_names = ", ".join(data.keys())
        column_values = tuple(data.values())
        self._execute_many(
            f"""
            INSERT OR IGNORE INTO {table_name}
            ({column_names})
            VALUES ({placeholders});
            """,
            column_values,
        )


if __name__ == "__main__":
    db = DatabaseManager(database_filename=DB_FILENAME)
    db.create_table(table_name=TABLE_NAME, columns=TABLE_COLUMNS)
