import psycopg2


def pull_weather_data(DBURL, startTime, endTime):
    if startTime > endTime:
        raise ValueError("start time cannot be after end time")
    
    try:
        DB_URL = DBURL
        conn = psycopg2.connect(DB_URL)
        
        cursor = conn.cursor()
        query = """
            SELECT id, dt, temperature, lat, lon
            FROM weather
            WHERE dt >= %s
              AND dt <= %s
            ORDER BY lat ASC, lon ASC;
        """

        # Execute the query with parameters
        cursor.execute(query, (startTime, endTime))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
