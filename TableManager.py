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
            "Bar Graph": "bar", 
            "Line Graph": "line", 
            "Scatterplot": "scatter"
        }

    def add_table(self, fname: str, table_df: pd.DataFrame):
        table_name = os.path.splitext(fname)[0]
        self.tables[table_name] = table_df
    
    def get_tables(self):
        return list(self.tables.keys())
    
    def get_table_columns(self, table_name: str) -> list[str]:
        if table_name not in self.tables:
            return []
        else:
            return self.tables[table_name].columns.to_list()
        
    def get_graph_types(self) -> Dict[str, str]:
        return self.graph_types
    