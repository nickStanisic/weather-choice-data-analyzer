import os
from helpers.database import get_db_connection
import sqlalchemy

def pull_weather_data(start_time, end_time):
    """ 
    This method uses SQLAlchemy to pull data from the weather table in the postgres database 
    based on specified start and end times passed to the function. All lat and lon pairs for those times 
    in the database are returned

    Args:
        start_time (int): start time for searching database
        end_time (int): end time for searching database

    Raises:
        ValueError: This error is raised if times passed are incorrect

    Returns:
        rows: this is a list of tuples that are sorted by lat and lon in the form [(id,dt,temp,lat,lon),...,...]
    """
    if start_time > end_time:
        raise ValueError("start time cannot be after end time")
    
    try:
        engine = get_db_connection()
        
        with engine.connect() as conn:
            query = sqlalchemy.text("""
                SELECT id, dt, temperature, lat, lon
                FROM weather
                WHERE dt >= :start_time
                  AND dt <= :end_time
                ORDER BY lat ASC, lon ASC;
            """)
            
            result = conn.execute(query, {
                'start_time': start_time,
                'end_time': end_time
            })
            
            rows = result.fetchall()
            return rows
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None