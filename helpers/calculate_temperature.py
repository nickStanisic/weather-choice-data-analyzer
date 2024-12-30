def calculate_temperature(high, low, database_data):
    inside = True
    temperature_average = 0
    count = 0
    for row in database_data:
        if row[2] > float(high) or row[2] < float(low):
            inside = False
        temperature_average += row[2]
        count += 1
    if inside:
        data = {
            "date": row[1],
            "average temp": temperature_average/count,
            "lat": row[3],
            "lon": row[4],
            "valid": True
        }
    else: 
        data = {
            "date": row[1],
            "average temp": temperature_average/count,
            "lat": row[3],
            "lon": row[4],
            "valid": False
            }
    return data