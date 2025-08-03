# Parking Zones Visualizer

A Python application that visualizes parking zones on an interactive map using OpenStreetMap data.

## Features

- Visualizes different parking zones (red, yellow, green) on an interactive map
- Shows street names and zone information in popups
- Includes a legend for zone identification
- Marks the center point of the map area
- Logs processing information and any missing streets

## Project Structure

```
parking-zones/
├── config.py           # Configuration settings and constants
├── main.py            # Main script to run the application
├── map_utils.py       # Utility functions for map processing
├── parking_zones.py   # Core parking zone processing logic
├── README.md          # This file
└── requirements.txt   # Project dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd parking-zones
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. Open the generated `parking_map.html` file in a web browser to view the parking zones.

## Configuration

You can modify the following settings in `config.py`:

- `TARGET_POINT`: Center point of the map (latitude, longitude)
- `MAP_RADIUS_METERS`: Radius in meters to search for streets
- `MAP_FILENAME`: Name of the output HTML file
- `PARKING_ZONES`: Definition of streets in each parking zone

## Dependencies

- Python 3.7+
- folium
- osmnx

## License

This project is open source and available under the [MIT License](LICENSE).
