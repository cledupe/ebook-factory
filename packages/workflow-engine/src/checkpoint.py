from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver


def create_sqlite_checkpointer(db_path: str = "checkpoints.db") -> SqliteSaver:
    return SqliteSaver.from_conn_string(db_path)


def create_postgres_checkpointer(connection_string: str) -> PostgresSaver:
    return PostgresSaver.from_conn_string(connection_string)
