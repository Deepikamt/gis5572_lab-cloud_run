import psycopg2
from flask import Flask
import os

# Set variables equal to connections
dbname = 'gis5572'
user = 'postgres'
password = 'Deepika@98'
host = '35.221.47.162'  # Cloud DB Public IP address
port = '5432'

# create the Flask app
app = Flask(__name__) 

# Connect to the PostgreSQL database

# create the index route
@app.route('/') 
def index(): 
    return "The API is working!"

# create a general DB to GeoJSON function
def database_to_geojson(table_name):
        # create connection to the DB
    conn = psycopg2.connect(
        host = os.environ.get("DB_HOST"),
        database = os.environ.get("DB_NAME"),
        user = os.environ.get("DB_USER"),
        password = os.environ.get("DB_PASS"),
        port = os.environ.get("DB_PORT"),
    )
    # retrieve the data
    with conn.cursor() as cur:
        query =f"""
        SELECT JSON_BUILD_OBJECT(
            'type', 'FeatureCollection',
            'features', JSON_AGG(
                ST_AsGeoJson({table_name}.*)::json
            )
        )
        FROM {table_name};
        """
        
        cur.execute(query)
        
        data = cur.fetchall()
    # close the connection
    conn.close()
    
    # Returning the data
    return data [0][0]

# create the data route

@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    # call our general function
    ele_idw = idwelevationpoints_in_sde 
    return ele_idw


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
