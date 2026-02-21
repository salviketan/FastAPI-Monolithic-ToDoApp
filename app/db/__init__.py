import sys

from api.deps import db_session
from db.init_db import init_db
from prestart import (
    db_connection,
    db_creation,
    run_migrations,
    user_creation,
)
from psycopg2._psycopg import connection

try:
    con: connection = db_connection()
    db, db_exists = db_creation(con)
    miles_con: connection = db_connection(dbname=True)
    user_creation(con=miles_con, db_name=db)
    print("Running migrations...")
    run_migrations()
    print("Application pre-startup setup complete.")

    init_db(db=db_session)
except Exception as e:
    con.rollback()
    miles_con.rollback()
    db_session.rollback()
    exception_template: str = f"Traceback {type(e).__name__}: {e}, File {__file__}, Error on line {sys.exc_info()[-1].tb_lineno}\n"
    print(exception_template)
    raise
finally:
    con.close()
    miles_con.close()
    db_session.close()
