import os
import sys

from dotenv import load_dotenv

sys.path.append("..\\profit")
from conn.database_connector import DatabaseConnector
from conn.mysql_connector import MySQLConnector

load_dotenv(override=True)

try:
    mysql_connector = MySQLConnector(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER_ADMIN"],
        password=os.environ["DB_PASSWORD"],
    )
    mysql_connector.connect()
    db = DatabaseConnector(mysql_connector)
    cursor = db.get_cursor()
    cursor.execute("SELECT * FROM users;")
    print(cursor.fetchone())
except Exception as e:
    print(f"Ocurrió un error en la conexión o consulta: {e}")
finally:
    try:
        db.close_connection()
    except Exception:
        pass
