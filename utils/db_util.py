import psycopg
import pandas as pd


class DbUtil:
    conn = None

    def __init__(self, **conn_params) -> None:
        self.conn = psycopg.connect(**conn_params)

    def get_results(self, query: str, params: list[any] = []):
        if self.conn:
            df = pd.read_sql_query(query, self.conn, params=params)
            return df
        else:
            return None

    def insert(self, query: str, params: tuple = None):
        """
        Executes an INSERT query and commits the transaction.
        """
        if self.conn:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                self.conn.commit()
