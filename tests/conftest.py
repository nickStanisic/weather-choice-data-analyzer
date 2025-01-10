import subprocess
import time
import psycopg2
import pytest
import os
from dotenv import load_dotenv
from datetime import datetime
from app import create_app
from flask import Flask

load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def ensure_database_is_running(): 
    """
    This method runs the docker-compose file to spin up the test database. It then connects to the database
    for the duration of the testing session. Afterward, it shuts down the database.
    """            
    env = os.environ.copy()

    #run docker-compose up to get database container running
    subprocess.run(["docker-compose", "-f", "docker/docker-compose.yml", "up", "-d"], check=True, env=env)
    
    #try to connect to DB
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
        pytest.fail("Database is not available")

    #wait while other tests are run
    yield

    #shut down the database container
    subprocess.run(["docker-compose", "-f", "docker/docker-compose.yml", "down"], check=True, env=env)


@pytest.fixture()
def db_connection():
    """
    This method connects to the database created in ensure_database_is_running and creates a weather table 
    for the database. It closes the connection after session is done. 

    Yields:
        conn: connection to database
    """    

    #connect to test database
    conn = psycopg2.connect(os.getenv("DB_URL_TEST"))
    conn.autocommit = True
    
    #drop table and create new table for testing
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
    Connects to the database and inserts data to the weather table for testing. After the session is done,
    it deletes the table.

    Args:
        db_connection (cursor): cursor object to interact with database
    """    

    #use cursor to execute multiple inserts. Use parameters to avoid SQL injection.
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
    
@pytest.fixture
def mock_db_url(monkeypatch):
    """
    Fixture to mock the DB_URL environment variable. 
    I need it here since DB_URL is directly set in app.
    """
    DB_TEST = os.getenv("DB_URL_TEST")
    monkeypatch.setenv("DB_URL", DB_TEST)

@pytest.fixture
def app(mock_db_url):
    """
    Create and configure a new Flask application for each test.
    """
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """
    Provides a test client for the Flask app.
    """
    return app.test_client()

