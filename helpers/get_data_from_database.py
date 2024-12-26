import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def pull_weather_data(startTime, endTime, lat, lon):
    try:

        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = conn.cursor()

        query = """
            SELECT id, dt, temperature, lat, lon
            FROM weather
            WHERE dt >= %s
              AND dt <= %s
              AND lat = %s
              AND lon = %s
            ORDER BY date_time;
        """

        # Execute the query with parameters
        cursor.execute(query, (startTime, endTime, float(lat), float(lon)))
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
