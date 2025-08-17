# 🚗 Parking Zones Visualizer

A Python application for visualizing parking zones on an interactive map using OpenStreetMap data. The application provides both a web interface and a command-line interface for generating parking zone visualizations.

## Features

- 🌍 Web-based interface with Streamlit
- 🗺️ Interactive map with zoom and pan functionality
- 🎨 Multiple map styles (OpenStreetMap, CyclOSM, CartoDB Positron)
- 📍 Predefined locations with easy selection
- 📊 Visual representation of different parking zones
- 📱 Responsive design that works on desktop and mobile
- 🚀 Fast map generation with caching
- 🔄 Real-time coordinate display
- 🖥️ Command-line interface for advanced usage

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Thrsh001/parking-zones.git
   cd parking-zones
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🖥️ Web App Usage

### Running the Web App

```bash
streamlit run app.py
```

This will start a local web server and open the app in your default web browser at `http://localhost:8501`.

### Using the Web Interface

1. **Set Location**:
   - Select the location from the dropdown (more locations coming soon)

2. **Adjust Settings**:
   - Choose your preferred map style

3. **Generate Map**:
   - Click the "Generate Map" button
   - The map will appear below the controls

## ⌨️ Command Line Usage

You can also use the command-line interface:

```bash
python main.py --lat 45.38 --lon 20.39 --output my_map.html --tile-provider "cyclosm"
```

### Command-line Options

```
usage: main.py [-h] [--lat LATITUDE] [--lon LONGITUDE]  [-o OUTPUT] [-t TILE_PROVIDER] [-v]

Generate an interactive map of parking zones.

options:
  -h, --help            show this help message and exit
  --lat LATITUDE        Latitude of the center point (default: 45.38096)
  --lon LONGITUDE       Longitude of the center point (default: 20.39373)
  -o OUTPUT, --output OUTPUT
                        Output HTML filename (default: parking_map.html)
  -t TILE_PROVIDER, --tile-provider TILE_PROVIDER
                        Map tile provider to use (default: openstreetmap)
  -v, --verbose         Enable verbose logging
```

## 🏗️ Project Structure

- `app.py`: Streamlit web application
- `main.py`: Command-line interface
- `parking_zones.py`: Core functionality for processing parking zone data
- `map_utils.py`: Utility functions for map creation and visualization
- `config.py`: Configuration settings and constants
- `requirements.txt`: Python dependencies

## 🌐 Deployment

### Local Deployment

For personal use, running the Streamlit app locally is sufficient.

## 👥 Authors
Thrsh001

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
