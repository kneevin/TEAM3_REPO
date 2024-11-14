from typing import Any, Dict, List, NamedTuple, Callable, Optional
import sqlite3
from fastapi import HTTPException
from pydantic import BaseModel, model_validator

class DashboardGraphParams(BaseModel):
    graph_ids: List[int]
    indices: List[int]
    width_height: List[List[int]]

    @model_validator(mode='before')
    def check_values(cls, data: Any) -> Any:
        graph_ids = data.get('graph_ids')
        indices = data.get('indices')
        width_height = data.get('width_height')
        
        # Ensure all lists are present
        if graph_ids is None or indices is None or width_height is None:
            raise HTTPException(status_code=400, detail="Missing required fields.")
        
        # Check if all lists have the same length
        if not (len(graph_ids) == len(indices) == len(width_height)):
            raise HTTPException(status_code=400, detail="Arrays are not of the same length.")
        
        # Check if each width_height element has exactly two integers
        if not all(len(wh) == 2 for wh in width_height):
            raise HTTPException(
                status_code=400,
                detail="Each element in width_height must be a list of two integers."
            )
        return data

class DashboardCreateQueryParams(DashboardGraphParams):
    dashboard_title: str

class DashboardPutQueryParams(DashboardGraphParams):
    dashboard_id: int

class DashboardDeleteQueryParams(BaseModel):
    dashboard_id: int
    graph_ids: Optional[List[int]] = []
    indices: Optional[List[int]] = []

    @model_validator(mode='before')
    def check_lengths(cls, data: Any) -> Any:
        graph_ids, indices = data.get('graph_ids'), data.get('indices')
        if (graph_ids or indices) and not(len(graph_ids) == len(indices)):
            raise HTTPException(status_code=400, detail="Arrays are not of the same length.")
        return data

class DashboardGraphMetadata(BaseModel):
    graph_id: int
    idx: int
    width: int
    height: int
    x_coord: int
    y_coord: int

class DashboardMetadata(BaseModel):
    dashboard_id: int
    dashboard_title: str
    metadata_graphs: List[DashboardGraphMetadata]

class DashboardMapResponse(BaseModel):
    dashboard_metadatas: List[DashboardMetadata]

class DashboardManager:
    def __init__(self, get_connection_callback: Callable[[], sqlite3.Connection]):
        self.get_sql_db_connection = get_connection_callback
        self.__create_tables()

    def delete_dashboard(self, query: DashboardDeleteQueryParams):
        with self.get_sql_db_connection() as conn:
            # Set the row factory to sqlite3.Row to get dictionary-like row objects
            conn.row_factory = sqlite3.Row

            dashboard_id = query.dashboard_id

            # Check if the dashboard_id exists
            if self.__dashboard_exists(dashboard_id=dashboard_id, db_conn=conn):
                raise HTTPException(status_code=404, detail=f"Dashboard with id {dashboard_id} not found.")

            # Delete the entire dashboard if no graph_ids or indices are provided
            if not query.graph_ids and not query.indices:
                self.__delete_entire_dashboard(dashboard_id, db_conn=conn)
            else: # Otherwise, delete specified graphs
                GRAPH_IDS = query.graph_ids
                INDICES = query.indices
                DASHBOARD_IDS = [dashboard_id for _ in range(len(GRAPH_IDS))]
                DELETE_QUERY = """
                    DELETE FROM master_dashboard 
                    WHERE 1=1
                        AND dashboard_id = ? 
                        AND graph_id = ?
                        AND idx = ?
                """
                conn.executemany(DELETE_QUERY, (DASHBOARD_IDS, GRAPH_IDS, INDICES))
            conn.commit()

    def get_dashboard(self, dashboard_id: int) -> DashboardMetadata:
        with self.get_sql_db_connection() as conn:
            # Set the row factory to sqlite3.Row to get dictionary-like row objects
            conn.row_factory = sqlite3.Row

            # Retrieve the dashboard title
            result = conn.execute(
                "SELECT dashboard_title FROM dashboard_title_mp WHERE dashboard_id = ?",
                (dashboard_id,)
            ).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail=f"Dashboard with id {dashboard_id} not found.")

            dashboard_title = result['dashboard_title']

            # Retrieve the graph metadata associated with the dashboard
            cursor = conn.execute("""
                SELECT graph_id, idx, width, height, x_coord, y_coord
                FROM master_dashboard
                WHERE dashboard_id = ?
                ORDER BY idx
            """, (dashboard_id,))

            rows = cursor.fetchall()

            if not rows:
                return None
            #     raise HTTPException(status_code=404, detail=f"No graphs found for dashboard id {dashboard_id}.")

            # Create a list of DashboardGraphMetadata instances using dictionary access
            metadata_graphs = [
                DashboardGraphMetadata(
                    graph_id=row['graph_id'],
                    idx=row['idx'],
                    width=row['width'],
                    height=row['height'],
                    x_coord=row['x_coord'],
                    y_coord=row['y_coord']
                ) for row in rows
            ]

            # Construct the DashboardMetadata instance
            dashboard_metadata = DashboardMetadata(
                dashboard_id=dashboard_id,
                dashboard_title=dashboard_title,
                metadata_graphs=metadata_graphs
            )

            return dashboard_metadata

    def get_dashboard_id_mp(self) -> DashboardMapResponse:
        with self.get_sql_db_connection() as conn:
            # Set row factory to get dictionary-like row objects
            conn.row_factory = sqlite3.Row

            # Retrieve all dashboards with their metadata
            dashboards = conn.execute("""
                SELECT dt.dashboard_id, dt.dashboard_title, 
                    md.graph_id, md.idx, md.width, md.height, md.x_coord, md.y_coord
                FROM dashboard_title_mp AS dt
                LEFT JOIN master_dashboard AS md ON dt.dashboard_id = md.dashboard_id
                ORDER BY dt.dashboard_id, md.idx
            """).fetchall()

            # Group metadata by dashboard_id
            dashboard_map = {}
            for row in dashboards:
                dashboard_id = row['dashboard_id']
                if dashboard_id not in dashboard_map:
                    dashboard_map[dashboard_id] = {
                        "dashboard_id": dashboard_id,
                        "dashboard_title": row['dashboard_title'],
                        "metadata_graphs": []
                    }
                
                # Append graph metadata if exists
                if row['graph_id'] is not None:
                    dashboard_map[dashboard_id]["metadata_graphs"].append(
                        DashboardGraphMetadata(
                            graph_id=row['graph_id'],
                            idx=row['idx'],
                            width=row['width'],
                            height=row['height'],
                            x_coord=row['x_coord'],
                            y_coord=row['y_coord']
                        )
                    )

            # Convert dictionary to list of DashboardMetadata objects
            dashboard_metadatas = [
                DashboardMetadata(
                    dashboard_id=meta["dashboard_id"],
                    dashboard_title=meta["dashboard_title"],
                    metadata_graphs=meta["metadata_graphs"]
                ) for meta in dashboard_map.values()
            ]

            return DashboardMapResponse(dashboard_metadatas=dashboard_metadatas)

    def create_new_dashboard(self, query: DashboardCreateQueryParams) -> int:
        with self.get_sql_db_connection() as conn:
            # Insert the dashboard title and get the new dashboard_id
            cursor = conn.execute(
                "INSERT INTO dashboard_title_mp (dashboard_title) VALUES (?)",
                (query.dashboard_title,)
            )
            dashboard_id = cursor.lastrowid

            # Prepare the data for bulk insertion
            data_to_insert = [
                (dashboard_id, graph_id, idx, width, height)
                for graph_id, idx, (width, height) in zip(query.graph_ids, query.indices, query.width_height)
            ]

            # Insert the data into the master_dashboard table
            conn.executemany(
                """
                INSERT INTO master_dashboard (dashboard_id, graph_id, idx, width, height)
                VALUES (?, ?, ?, ?, ?)
                """,
                data_to_insert
            )

            # Commit the transaction
            conn.commit()

        # Optionally, return the dashboard_id
        return dashboard_id

    def add_to_dashboard(self, query: DashboardPutQueryParams) -> int:
        dashboard_id = query.dashboard_id
        with self.get_sql_db_connection() as conn:
            # Set row factory to get dictionary-like row objects
            conn.row_factory = sqlite3.Row

            # Check if the dashboard_id exists
            result = conn.execute(
                "SELECT dashboard_title FROM dashboard_title_mp WHERE dashboard_id = ?",
                (dashboard_id,)
            ).fetchone()

            if result is None:
                raise HTTPException(status_code=404, detail=f"Dashboard with id {dashboard_id} not found.")

            # Retrieve existing graph_ids and idxs in the dashboard
            existing_entries = conn.execute(
                "SELECT graph_id, idx FROM master_dashboard WHERE dashboard_id = ?",
                (dashboard_id,)
            ).fetchall()

            existing_idxs = {row['idx'] for row in existing_entries}

            # Check for idx values that are already used
            conflicting_idxs = set(query.indices) & existing_idxs
            if conflicting_idxs:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Idx values {conflicting_idxs} are already used in the dashboard."
                )

            # Prepare the data for bulk insertion
            data_to_insert = [
                (dashboard_id, graph_id, idx, width, height)
                for graph_id, idx, (width, height) in zip(query.graph_ids, query.indices, query.width_height)
            ]

            # Insert the data into the master_dashboard table
            conn.executemany(
                """
                INSERT INTO master_dashboard (dashboard_id, graph_id, idx, width, height)
                VALUES (?, ?, ?, ?, ?)
                """,
                data_to_insert
            )

            # Commit the transaction
            conn.commit()

        # Return the dashboard_id
        return dashboard_id

    def __delete_entire_dashboard(
            self, 
            dashboard_id: int, *, 
            db_conn: sqlite3.Connect = None
        ):
        DELETE_QUERY = "DELETE FROM dashboard_title_mp WHERE dashboard_id = ?"
        if not db_conn:
            with self.get_sql_db_connection() as conn:
                conn.execute(DELETE_QUERY, (dashboard_id, ))
                conn.commit()
        else:
            db_conn.execute(DELETE_QUERY, (dashboard_id, ))
            db_conn.commit()

    def __dashboard_exists(self, dashboard_id: int, *, db_conn: sqlite3.Connection = None):
        SELECT_QUERY = "SELECT dashboard_title FROM dashboard_title_mp WHERE dashboard_id = ?"
        if not db_conn:
            with self.get_sql_db_connection() as conn:
                res = conn.execute(SELECT_QUERY, (dashboard_id,)).fetchone()
        else:
            res = db_conn.execute(SELECT_QUERY, (dashboard_id,)).fetchone()
        return res is not None

    def __create_tables(self):
        with self.get_sql_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS master_dashboard (
                    dashboard_id INTEGER NOT NULL,
                    graph_id INTEGER NOT NULL,
                    idx INTEGER NOT NULL,
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    x_coord INTEGER GENERATED ALWAYS AS ((idx * 4) % 12) STORED,
                    y_coord INTEGER GENERATED ALWAYS AS (idx / 3) STORED,
                    PRIMARY KEY (dashboard_id, graph_id, idx),
                    FOREIGN KEY (graph_id) REFERENCES graphs(graph_id) ON DELETE CASCADE,
                    FOREIGN KEY (dashboard_id) REFERENCES dashboard_title_mp(dashboard_id) ON DELETE CASCADE
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dashboard_title_mp (
                    dashboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dashboard_title TEXT NOT NULL
                )
            """)
            conn.commit() # is called automatically afterwards

    