import psycopg2


def pull_weather_data(DBURL, start_time, end_time):
    """ 
    This method uses psycopg2 library to pull data from the weather table in the postgres database 
    based on specified DBURL, start, and end times passed to the function.  All lat and lon pairs for those times 
    in the database are returned

    Args:
        DBURL (string): This is the URL that specifies the database to access
        startTime (int): start time for searching database
        endTime (int): end time for searching database

    Raises:
        ValueError: This error is raised if times passed are incorrect

    Returns:
        rows: this is a list of tuples that are sorted by lat and lon in the form [(id,dt,temp,lat,lon),...,...]
    """
    if start_time > end_time:
        raise ValueError("start time cannot be after end time")
    
    #try to connect to DB
    try:
        DB_URL = DBURL
        conn = psycopg2.connect(DB_URL)
        
        #select rows between start and end date
        cursor = conn.cursor()
        query = """
            SELECT id, dt, temperature, lat, lon
            FROM weather
            WHERE dt >= %s
              AND dt <= %s
            ORDER BY lat ASC, lon ASC;
        """

        # Execute the query with parameters
        cursor.execute(query, (start_time, end_time))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    
    #if it can't connect to the database, print an error.
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
