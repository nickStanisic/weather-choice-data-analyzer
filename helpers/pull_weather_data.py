import os
from helpers.database import get_db_connection
import sqlalchemy

def pull_weather_data(start_time, end_time, high_temp, low_temp):
    """ 
    Optimized method that does ALL calculations in the database instead of Python loops.
    Returns aggregated results instead of raw data.
    
    Args:
        start_time (int): start time for searching database
        end_time (int): end time for searching database
        high_temp (float): high temperature threshold
        low_temp (float): low temperature threshold

    Returns:
        list: Pre-calculated results for each lat/lon pair
    """
    if start_time > end_time:
        raise ValueError("start time cannot be after end time")
    
    if float(low_temp) > float(high_temp):
        raise ValueError("low can't be bigger than high")
    
    try:
        engine = get_db_connection()
        
        with engine.connect() as conn:
            # This single query replaces ALL your Python loops!
            query = sqlalchemy.text("""
                SELECT 
                    lat,
                    lon,
                    AVG(temperature) as average_temp,
                    MIN(dt) as earliest_time,
                    MAX(dt) as latest_time,
                    COUNT(*) as reading_count,
                    -- Check if ALL temperatures are within range (strict validation)
                    CASE 
                        WHEN MIN(temperature) >= :low_temp AND MAX(temperature) <= :high_temp 
                        THEN true 
                        ELSE false 
                    END as valid,
                    -- Additional useful metrics
                    MIN(temperature) as min_temp,
                    MAX(temperature) as max_temp,
                    STDDEV(temperature) as temp_variance
                FROM weather
                WHERE dt >= :start_time AND dt <= :end_time
                GROUP BY lat, lon
                ORDER BY lat, lon;
            """)
            
            result = conn.execute(query, {
                'start_time': start_time,
                'end_time': end_time,
                'low_temp': float(low_temp),
                'high_temp': float(high_temp)
            })
            
            # Convert to the format your frontend expects
            optimized_results = []
            for row in result:
                optimized_results.append({
                    "date": row.latest_time,  # Use latest time as representative date
                    "average_temp": float(row.average_temp),
                    "lat": float(row.lat),
                    "lon": float(row.lon),
                    "valid": bool(row.valid),
                    # Bonus data for better user experience
                    "min_temp": float(row.min_temp),
                    "max_temp": float(row.max_temp),
                    "reading_count": int(row.reading_count)
                })
            
            return optimized_results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None