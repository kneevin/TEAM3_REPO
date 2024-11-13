import sqlite3
import pandas as pd
from typing import List, Any, Callable, Optional
from pydantic import BaseModel

class TableResponse(BaseModel):
    table_id: int
    table_name: str
    column_names: List[str]
    rows: List[List]

class TableMapResponse(BaseModel):
    table_ids: List[int]
    table_names: List[str]

class TableManager:
    def __init__(self, get_connection_callback: Callable[[], sqlite3.Connection]):
        self.get_sql_db_connection = get_connection_callback
        self.__create_tables()

    def __create_tables(self):
        with self.get_sql_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_tables (
                table_id INTEGER PRIMARY KEY AUTOINCREMENT,
                db_name TEXT GENERATED ALWAYS AS ('tbl_' || table_id) VIRTUAL,
                table_name TEXT NOT NULL
            )
            ''')
            conn.commit()

    def get_table_id_mp(self) -> TableMapResponse:
        TABLE_IDS = []
        TABLE_NAMES = []
        with self.get_sql_db_connection() as conn:
            SELECT_QUERY = '''SELECT table_id, table_name FROM master_tables'''
            curs = conn.cursor()
            curs.execute(SELECT_QUERY)
            for table_id, table_name in curs.fetchall():
                TABLE_IDS.append(table_id)
                TABLE_NAMES.append(table_name)

        return TableMapResponse(
            table_ids=TABLE_IDS,
            table_names=TABLE_NAMES
        )

    def insert_master_table(self, table_name: str):
        with self.get_sql_db_connection() as conn:
            cursor = conn.cursor()
            INSERTION_QUERY = '''
                INSERT INTO master_tables (table_name) VALUES (?)
                RETURNING db_name
            '''
            cursor.execute(INSERTION_QUERY, (table_name,))
            row = cursor.fetchone()
            (db_name, ) = row if row else None
            conn.commit()
        return db_name

    def get_table_columns(self):
        tables_columns = {}
        ALL_DB_QUERIES = """
        SELECT db_name, table_name FROM master_tables
        """
        with self.get_sql_db_connection() as conn:
            cursor = conn.execute(ALL_DB_QUERIES)
            DB_NAMES = [(row[0], row[1]) for row in cursor.fetchall()]

            for db_name, table_name in DB_NAMES:
                cursor = conn.execute(f"PRAGMA table_info({db_name})")
                columns = [row[1] for row in cursor.fetchall()]
                tables_columns[table_name] = columns
        return tables_columns

    def add_table(self, table_name: str, dataframe: pd.DataFrame, tbl_response) -> Optional[TableResponse]:
        with self.get_sql_db_connection() as conn:
            cursor = conn.cursor()
            db_name = self.insert_master_table(table_name)

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
            CREATE TABLE IF NOT EXISTS {db_name} (
                {columns}
            )
            """
            cursor.execute(create_table_query)

            placeholders = ", ".join(["?" for _ in dataframe.columns])
            insert_query = f"""
            INSERT INTO {db_name} ({', '.join(dataframe.columns)})
            VALUES ({placeholders})
            """
            cursor.executemany(insert_query, dataframe.values.tolist())
            conn.commit()
        if tbl_response:
            return self.get_table_response(db_name)

    def get_table_respone_by_id(self, table_id: int):
        with self.get_sql_db_connection() as conn:
            SELECT_TABLE_METADATA = """SELECT * FROM master_tables WHERE table_id = ? LIMIT 1"""
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(SELECT_TABLE_METADATA, (table_id, ))
            row = cursor.fetchone()
            tbl_mp = dict(row)

            DB_NAME = tbl_mp['db_name']
            SELECT_TABLE_DATA = f"""SELECT * FROM {DB_NAME}"""
            df = pd.read_sql_query(SELECT_TABLE_DATA, con=conn)
        
        return TableResponse(
            table_id=tbl_mp['table_id'],
            table_name=tbl_mp['table_name'],
            column_names=list(df.columns),
            rows=df.values.tolist()
        )

    def get_table_response(self, db_name: str) -> TableResponse:
        with self.get_sql_db_connection() as conn:
            SELECT_TABLE_DATA = f"""SELECT * FROM {db_name}"""
            df = pd.read_sql_query(SELECT_TABLE_DATA, con=conn)

            SELECT_TABLE_METADATA = """SELECT * FROM master_tables WHERE db_name = ? LIMIT 1"""
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(SELECT_TABLE_METADATA, (db_name, ))
            row = cursor.fetchone()
            tbl_mp = dict(row)

        return TableResponse(
            table_id=tbl_mp['table_id'],
            table_name=tbl_mp['table_name'],
            column_names=list(df.columns),
            rows=df.values.tolist()
        )



    # def get_all_table_names(self) -> List[str]:
    #     select_query = """
    #     SELECT table_name FROM master_tables
    #     """
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         cursor = conn.execute(select_query)
    #         table_names = [row[0] for row in cursor.fetchall()]
    #     return table_names

    # def get_table_id_mp(self) -> Dict[str, str]:
    #     select_query = """SELECT table_id, table_name from master_tables"""
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         df = pd.read_sql_query(select_query, conn)
    #     return dict(zip(df['table_id'], df['table_name']))

    # def get_table_data(self, table_name: str) -> pd.DataFrame:
    #     select_query = f"""
    #     SELECT * FROM {table_name}
    #     """
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         cursor = conn.execute(select_query)
    #         columns = [description[0] for description in cursor.description]
    #         rows = cursor.fetchall()
    #     return pd.DataFrame(rows, columns=columns)

    # def get_all_table_columns(self) -> Dict[str, List[str]]:
    #     tables_columns = {}
    #     table_names = self.get_all_table_names()
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         for table_name in table_names:
    #             cursor = conn.execute(f"PRAGMA table_info({table_name})")
    #             columns = [row[1] for row in cursor.fetchall()]
    #             tables_columns[table_name] = columns
    #     return tables_columns

    # def table_exists(self, table_name: str) -> bool:
    #     check_query = """
    #     SELECT 1 FROM master_tables WHERE table_name=? LIMIT 1
    #     """
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         cursor = conn.execute(check_query, (table_name,))
    #         return cursor.fetchone() is not None

    # def column_exists(self, table_name: str, column_name: str) -> bool:
    #     return self.columns_exist(table_name, column_names=[column_name])

    # def columns_exist(self, table_name: str, column_names: List[str]) -> bool:
    #     check_query = f"""
    #     PRAGMA table_info({table_name})
    #     """
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         cursor = conn.execute(check_query)
    #         columns = [row[1] for row in cursor.fetchall()]
    #     return all(column in columns for column in column_names)

    # def get_table_name(self, table_id: int) -> str:
    #     SELECT_QUERY = """SELECT table_name FROM master_tables WHERE table_id = ? LIMIT 1"""
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         df = pd.read_sql_query(SELECT_QUERY, conn, params=(table_id, ))
    #     return df.iloc[0]['table_name']

    # def get_table_id_graph(self, table_id: str, ax0: str, ax1: str) -> pd.DataFrame:
    #     table_name = self.get_table_name(table_id=table_id)
    #     return self.get_table_graph(table_name, ax0, ax1)

    # def get_table_graph(self, table_name: str, ax0: str, ax1: str) -> pd.DataFrame:
    #     select_query = f"""
    #     SELECT {ax0}, {ax1} FROM {table_name}
    #     """
    #     with sqlite3.connect(self.DB_FNAME) as conn:
    #         cursor = conn.execute(select_query)
    #         columns = [description[0] for description in cursor.description]
    #         rows = cursor.fetchall()
    #     return pd.DataFrame(rows, columns=columns)