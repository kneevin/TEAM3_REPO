from typing import Any, Dict, List, NamedTuple, Callable, Optional
import sqlite3
from fastapi import HTTPException
from pydantic import BaseModel, model_validator

class DashboardGraphParams(BaseModel):
    graph_ids: List[int]
    xy_coords: List[List[int]]
    width_height: List[List[int]]

    @model_validator(mode='before')
    def check_values(cls, data: Any) -> Any:
        graph_ids = data.get('graph_ids')
        xy_coords = data.get('xy_coords')
        width_height = data.get('width_height')
        
        # Ensure all lists are present
        if any(x is None for x in [graph_ids, xy_coords, width_height]):
            raise HTTPException(status_code=400, detail="Missing required fields.")
        
        # Check if all lists have the same length
        if not (len(graph_ids) == len(xy_coords) == len(width_height)):
            raise HTTPException(status_code=400, detail="Arrays are not of the same length.")
        
        # Check if each xy_coords element has exactly two integers
        if not all(len(xy) == 2 for xy in xy_coords):
            raise HTTPException(
                status_code=400,
                detail="Each element in xy_coords must be a list of two integers [x,y]."
            )
        
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
    xy_coords: Optional[List[List[int]]] = []

    @model_validator(mode='before')
    def check_lengths(cls, data: Any) -> Any:
        graph_ids, xy_coords = data.get('graph_ids'), data.get('xy_coords')
        if (graph_ids or xy_coords) and not(len(graph_ids) == len(xy_coords)):
            raise HTTPException(status_code=400, detail="Arrays are not of the same length.")
        return data

class DashboardGraphMetadata(BaseModel):
    graph_id: int
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

class DashboardLayoutUpdateParams(BaseModel):
    dashboard_id: int
    graph_ids: List[int]
    xy_coords: List[List[int]]
    width_height: List[List[int]]

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
            if not self.__dashboard_exists(dashboard_id=dashboard_id, db_conn=conn):
                raise HTTPException(status_code=404, detail=f"Dashboard with id {dashboard_id} not found.")

            # Delete the entire dashboard if no graph_ids or xy_coords are provided
            if not query.graph_ids and not query.xy_coords:
                self.__delete_entire_dashboard(dashboard_id, db_conn=conn)
            else: # Otherwise, delete specified graphs
                GRAPH_IDS = query.graph_ids
                XY_COORDS = query.xy_coords
                DASHBOARD_IDS = [dashboard_id for _ in range(len(GRAPH_IDS))]
                DELETE_QUERY = """
                    DELETE FROM master_dashboard 
                    WHERE 1=1
                        AND dashboard_id = ? 
                        AND graph_id = ?

                """
                values = list(zip(DASHBOARD_IDS, GRAPH_IDS))
                conn.executemany(DELETE_QUERY, values)
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
                SELECT graph_id, width, height, x_coord, y_coord
                FROM master_dashboard
                WHERE dashboard_id = ?
            """, (dashboard_id,))

            rows = cursor.fetchall()

            # Create a list of DashboardGraphMetadata instances using dictionary access
            metadata_graphs = [
                DashboardGraphMetadata(
                    graph_id=row['graph_id'],
                    width=row['width'],
                    height=row['height'],
                    x_coord=row['x_coord'],
                    y_coord=row['y_coord']
                ) for row in rows
            ]

            # Construct the DashboardMetadata instance - always return this even if no graphs
            dashboard_metadata = DashboardMetadata(
                dashboard_id=dashboard_id,
                dashboard_title=dashboard_title,
                metadata_graphs=metadata_graphs  # This will be empty list if no graphs found
            )

            return dashboard_metadata

    def get_dashboard_id_mp(self) -> DashboardMapResponse:
        with self.get_sql_db_connection() as conn:
            # Set row factory to get dictionary-like row objects
            conn.row_factory = sqlite3.Row

            # Retrieve all dashboards with their metadata
            dashboards = conn.execute("""
                SELECT dt.dashboard_id, dt.dashboard_title, 
                    md.graph_id, md.width, md.height, md.x_coord, md.y_coord
                FROM dashboard_title_mp AS dt
                LEFT JOIN master_dashboard AS md ON dt.dashboard_id = md.dashboard_id
                ORDER BY dt.dashboard_id
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
            cursor = conn.execute(
                "INSERT INTO dashboard_title_mp (dashboard_title) VALUES (?)",
                (query.dashboard_title,)
            )
            dashboard_id = cursor.lastrowid

            # Updated data preparation to use paired xy coordinates
            data_to_insert = [
                (dashboard_id, graph_id, xy[0], xy[1], width, height)
                for graph_id, xy, (width, height) in zip(query.graph_ids, query.xy_coords, query.width_height)
                ]

            # Insert the data into the master_dashboard table
            conn.executemany(
                """
                INSERT INTO master_dashboard (dashboard_id, graph_id, x_coord, y_coord, width, height)
                VALUES (?, ?, ?, ?, ?, ?)
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
            # existing_entries = conn.execute(
            #     "SELECT graph_id, idx FROM master_dashboard WHERE dashboard_id = ?",
            #     (dashboard_id,)
            # ).fetchall()

            # existing_idxs = {row['idx'] for row in existing_entries}

            # Check for idx values that are already used
            # conflicting_xy_coords = set(query.xy_coords) & {row['xy_coords'] for row in existing_entries}
            # if conflicting_xy_coords:
            #     raise HTTPException(
            #         status_code=400, 
            #         detail=f"XY coordinates {conflicting_xy_coords} are already used in the dashboard."
            #     )

            # Prepare the data for bulk insertion
            data_to_insert = [
                (dashboard_id, graph_id, xy[0], xy[1], width, height)
                for graph_id, xy, (width, height) in zip(query.graph_ids, query.xy_coords, query.width_height)
                ]

            # Insert the data into the master_dashboard table
            conn.executemany(
                """
                INSERT INTO master_dashboard (dashboard_id, graph_id, x_coord, y_coord, width, height)
                VALUES (?, ?, ?, ?, ?, ?)
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
            db_conn: sqlite3.Connection = None
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
                    width INTEGER NOT NULL,
                    height INTEGER NOT NULL,
                    x_coord INTEGER NOT NULL,
                    y_coord INTEGER NOT NULL,
                    PRIMARY KEY (dashboard_id, graph_id),
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

    def update_dashboard_layout(self, query: DashboardLayoutUpdateParams) -> None:
        with self.get_sql_db_connection() as conn:
            # Update each graph's layout information
            for graph_id, xy, (width, height) in zip(query.graph_ids, query.xy_coords, query.width_height):
                conn.execute("""
                    UPDATE master_dashboard 
                    SET x_coord = ?, y_coord = ?, width = ?, height = ?
                    WHERE dashboard_id = ? AND graph_id = ?
                """, (xy[0], xy[1], width, height, query.dashboard_id, graph_id))
            conn.commit()

    