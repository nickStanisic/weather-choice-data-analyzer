def calculate_temperature(high, low, database_data):
    inside = True
    for row in database_data:
        if row[2] > float(high) or row[2] < float(low):
            inside = False
            break
    if inside:
        data = {
            "date": row[1],
            "temp": row[2],
            "lat": row[3],
            "lon": row[4],
            "valid": True
        }
    else: 
        data = {
            "date": row[1],
            "temp": row[2],
            "lat": row[3],
            "lon": row[4],
            "valid": False
            }
    return data