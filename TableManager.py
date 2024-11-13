from typing import Dict, List
import matplotlib.pyplot as pl
import seaborn as sns
import pandas as pd
import numpy as np
import os

class TableManager:
    def __init__(self):
        self.tables: Dict[str, pd.DataFrame] = {}
        self.graph_types: Dict[str, str] = {
            "bar": "Bar Graph", 
            "line": "Line Graph", 
            "scatter": "Scatterplot"
        }

    def add_table(self, fname: str, table_df: pd.DataFrame):
        table_name = os.path.splitext(fname)[0]
        self.tables[table_name] = table_df
    
    def get_tables(self):
        return list(self.tables.keys())
    
    def table_exists(self, table_name: str) -> bool:
        return table_name in self.tables

    def graph_exists(self, graph_type: str):
        return graph_type in self.graph_types

    def graph_table(self, graph_type: str, table_id: str, x_column: str, y_column: str):
        SS = [x_column, y_column]
        df = self.tables[table_id][SS]
        return df.plot(kind=graph_type, x=x_column, y=y_column).get_figure()
        
    def get_graph_types(self) -> Dict[str, str]:
        return self.graph_types
    
    def get_all_table_columns(self) -> Dict[str, List[str]]:
        return {
            table_name: df.columns.to_list() 
                for table_name, df in self.tables.items()
        }
    
    def get_table_data(self, table_name: str) -> dict:
        if not self.table_exists(table_name):
            raise ValueError(f"Table {table_name} does not exist.")

        # Get the table as a DataFrame
        df = self.tables[table_name]
        df = df.fillna('')
        # Convert DataFrame to a list of lists
        data = df.values.tolist()

        # Extract the first row as columns and the rest as data rows
        columns = df.columns.tolist()
        rows = data


        return {
            "headers": columns,
            "rows": rows
        }