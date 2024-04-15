import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='gis5572',
            user='postgres',
            password='Deepika@98',
            host='35.221.47.162',  # Cloud DB Public IP address
            port='5432'
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to the database: {e}")
        return None

def database_to_geojson(table_name):
    conn = connect_to_db()
    if conn is None:
        return {"error": "Failed to connect to the database"}

    try:
        with conn.cursor() as cur:
            query = f"""
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
            return data[0][0]
    except psycopg2.Error as e:
        print(f"Error executing query: {e}")
        return {"error": "Failed to execute query"}
    finally:
        conn.close()

@app.route('/')
def index():
    return "The API is working!"

@app.route('/get_elevation_idw_geojson', methods=['GET'])
def get_elevation_idw_geojson():
    ele_idw = database_to_geojson("idwelevationpoints_in_sde")
    return jsonify(ele_idw)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)











