import sqlite3
import pandas as pd
from typing import List, Dict


class TableManager:
    DB_FNAME = "./table_manager.db"

    def __init__(self):
        self.__create_master_table()

    def __create_master_table(self):
        create_master_table_query = """
        CREATE TABLE IF NOT EXISTS master_tables (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT UNIQUE
        )
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            cursor.execute(create_master_table_query)
            conn.commit()

    def add_table(self, table_name: str, dataframe: pd.DataFrame):
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO master_tables (table_name)
            VALUES (?)
            """
            cursor.execute(insert_query, (table_name,))

            column_definitions = []
            for column_name, dtype in dataframe.dtypes.items():
                if pd.api.types.is_integer_dtype(dtype):
                    column_type = "INTEGER"
                elif pd.api.types.is_float_dtype(dtype):
                    column_type = "REAL"
                elif pd.api.types.is_bool_dtype(dtype):
                    column_type = "BOOLEAN"
                else:
                    column_type = "TEXT"
                column_definitions.append(f"{column_name} {column_type}")

            columns = ", ".join(column_definitions)
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns}
            )
            """
            cursor.execute(create_table_query)

            placeholders = ", ".join(["?" for _ in dataframe.columns])
            insert_query = f"""
            INSERT INTO {table_name} ({', '.join(dataframe.columns)})
            VALUES ({placeholders})
            """
            cursor.executemany(insert_query, dataframe.values.tolist())
            conn.commit()

    def get_all_table_names(self) -> List[str]:
        select_query = """
        SELECT table_name FROM master_tables
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.execute(select_query)
            table_names = [row[0] for row in cursor.fetchall()]
        return table_names

    def get_table_id_mp(self) -> Dict[str, str]:
        select_query = """SELECT table_id, table_name from master_tables"""
        with sqlite3.connect(self.DB_FNAME) as conn:
            df = pd.read_sql_query(select_query, conn)
        return dict(zip(df['table_id'], df['table_name']))

    def get_table_data(self, table_name: str) -> pd.DataFrame:
        select_query = f"""
        SELECT * FROM {table_name}
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.execute(select_query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)

    def get_all_table_columns(self) -> Dict[str, List[str]]:
        tables_columns = {}
        table_names = self.get_all_table_names()
        with sqlite3.connect(self.DB_FNAME) as conn:
            for table_name in table_names:
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                tables_columns[table_name] = columns
        return tables_columns

    def table_exists(self, table_name: str) -> bool:
        check_query = """
        SELECT 1 FROM master_tables WHERE table_name=? LIMIT 1
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.execute(check_query, (table_name,))
            return cursor.fetchone() is not None

    def column_exists(self, table_name: str, column_name: str) -> bool:
        return self.columns_exist(table_name, column_names=[column_name])

    def columns_exist(self, table_name: str, column_names: List[str]) -> bool:
        check_query = f"""
        PRAGMA table_info({table_name})
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.execute(check_query)
            columns = [row[1] for row in cursor.fetchall()]
        return all(column in columns for column in column_names)

    def get_table_name(self, table_id: int) -> str:
        SELECT_QUERY = """SELECT table_name FROM master_tables WHERE table_id = ? LIMIT 1"""
        with sqlite3.connect(self.DB_FNAME) as conn:
            df = pd.read_sql_query(SELECT_QUERY, conn, params=(table_id, ))
        return df.iloc[0]['table_name']

    def get_table_id_graph(self, table_id: str, ax0: str, ax1: str) -> pd.DataFrame:
        table_name = self.get_table_name(table_id=table_id)
        return self.get_table_graph(table_name, ax0, ax1)

    def get_table_graph(self, table_name: str, ax0: str, ax1: str) -> pd.DataFrame:
        select_query = f"""
        SELECT {ax0}, {ax1} FROM {table_name}
        """
        with sqlite3.connect(self.DB_FNAME) as conn:
            cursor = conn.execute(select_query)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=columns)