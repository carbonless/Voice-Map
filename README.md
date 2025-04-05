# Voice-Map: Bucks County Zoning Checker

A web application that allows users to check zoning information for any address in Bucks County, Pennsylvania. Part of the Voice-Map project.

## Features

- Interactive map interface
- Address geocoding
- Zoning district lookup
- Detailed zoning information display
- Links to zoning regulations

## Setup

1. Clone the repository:
```bash
git clone https://github.com/carbonless/Voice-Map.git
cd Voice-Map
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask geopandas shapely geopy
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Data Source

The zoning data is sourced from the [Bucks County GIS Open Data Portal](https://dataportal-bucksgis.opendata.arcgis.com/).

## Technologies Used

- Flask (Python web framework)
- GeoPandas (Geospatial data handling)
- Shapely (Geometric operations)
- Geopy (Address geocoding)
- Leaflet.js (Interactive maps)

## License

MIT License 