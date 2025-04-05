from flask import Flask, request, jsonify, render_template
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# Load the GeoJSON file when the app starts
try:
    zoning_data = gpd.read_file('BucksCountyMunicipalZoning202312.geojson.txt')
    print("Successfully loaded zoning data")
except Exception as e:
    print(f"Error loading zoning data: {e}")
    zoning_data = None

def geocode_address(address):
    """Convert address to coordinates using Nominatim"""
    geolocator = Nominatim(user_agent="bucks_county_zoning_app")
    try:
        location = geolocator.geocode(f"{address}, Bucks County, PA")
        if location:
            return {
                'point': Point(location.longitude, location.latitude),
                'full_address': location.address
            }
        return None
    except GeocoderTimedOut:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_zoning', methods=['POST'])
def check_zoning():
    if zoning_data is None:
        return jsonify({'error': 'Zoning data not available'}), 500

    data = request.get_json()
    address = data.get('address')
    
    if not address:
        return jsonify({'error': 'Address is required'}), 400

    # Convert address to coordinates
    location_data = geocode_address(address)
    if not location_data:
        return jsonify({'error': 'Could not geocode address'}), 400

    point = location_data['point']
    
    # Create a GeoDataFrame with the point
    point_gdf = gpd.GeoDataFrame(geometry=[point], crs=zoning_data.crs)

    # Check if point is within any zoning district
    for idx, zone in zoning_data.iterrows():
        if zone.geometry.contains(point):
            return jsonify({
                'success': True,
                'in_bucks_county': True,
                'full_address': location_data['full_address'],
                'coordinates': {
                    'lat': point.y,
                    'lng': point.x
                },
                'zoning_info': {
                    'district': zone['Zoning'],
                    'municipality': zone['Municipali'],
                    'code': zone['ZoningAbbr'],
                    'general_zoning': zone['GenZoning'],
                    'website': zone['Website']
                }
            })

    return jsonify({
        'success': True,
        'in_bucks_county': False,
        'full_address': location_data['full_address'],
        'coordinates': {
            'lat': point.y,
            'lng': point.x
        },
        'message': 'Address is not within Bucks County zoning districts'
    })

if __name__ == '__main__':
    app.run(debug=True) 