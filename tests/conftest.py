import subprocess
import time
import psycopg2
import pytest
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def ensure_database_is_running(): 
     """
     Method to make sure test database is running before running test suite
     """        
     env = os.environ.copy()

     subprocess.run(["docker-compose", "-f", "docker/docker-compose.yml", "up", "-d"], check=True, env=env)

     for _ in range(30):
         try:
             conn = psycopg2.connect(
                 os.getenv("DB_URL_TEST")
             )
             conn.close()
             break
         except psycopg2.OperationalError:
             time.sleep(2)
     else:
        print("== Printing Postgres container logs for debugging... ==")
        subprocess.run(["docker-compose", "-f", "docker/docker-compose.yml", "logs", "db"],
                       check=False, env=env)
        pytest.fail("Database is not available")

     yield

     subprocess.run(["docker-compose", "-f", "docker/docker-compose.yml", "down"], check=True, env=env)


@pytest.fixture()
def db_connection():
    "connect to test database"
    conn = psycopg2.connect(os.getenv("DB_URL_TEST"))
    conn.autocommit = True
    
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS weather;")
        cursor.execute("""
            CREATE TABLE weather (
                id SERIAL PRIMARY KEY,
                dt INT,
                temperature FLOAT,
                lat FLOAT,
                lon FLOAT,
                date_time TIMESTAMP
            );
        """)

    yield conn

    conn.close()

@pytest.fixture
def populate_test_data(db_connection):
    """
    Fill test database with different test data
    """
    with db_connection.cursor() as cursor:
        cursor.executemany(
            "INSERT INTO weather (dt, temperature, lat, lon, date_time) VALUES (%s, %s, %s, %s, %s)",
            [
                (1735270874, -10, 41, 110, datetime.now()),
                (1735270874, 23, 41, 110, datetime.now()),
                (1735270874, 76, 41, 109, datetime.now()),
                (1735270874, 87, 40, 109, datetime.now()),
                (1735270894, 76, 41, 109, datetime.now()),
                (1735270895, 87, 42, 108, datetime.now())
            ]
        )
    
    yield

    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM weather;")