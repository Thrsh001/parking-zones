"""Configuration settings for the parking zones application."""
from typing import Dict, List, Tuple, Optional, Any
import logging, sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr),
        logging.FileHandler('parking_zones.log')
    ]
)

# Default settings
DEFAULTS = {
    'target_point': (45.38096, 20.39373),  # Default center point (lat, lon)
    'zoom_start': 17,                       # Default zoom level
    'map_filename': 'parking_map.html',     # Default output filename
    'tile_provider': 'openstreetmap',       # Default tile provider
    'radius': 10000,                         # Default radius in meters
}

# Predefined locations with their coordinates
LOCATIONS = {
    "Zrenjanin": {
        'lat': 45.3836,
        'lon': 20.3819
    }
}

# Available tile providers and their configurations
TILE_PROVIDERS = {
    'openstreetmap': {
        'name': 'OpenStreetMap',
        'tiles': 'OpenStreetMap',
        'attr': 'OpenStreetMap contributors',
        'min_zoom': 1,
        'max_zoom': 19,
    },
    'cyclosm': {
        'name': 'CyclOSM',
        'tiles': 'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
        'attr': 'OpenStreetMap contributors CyclOSM',
        'min_zoom': 1,
        'max_zoom': 18,
    },
    'cartodb_positron': {
        'name': 'CartoDB Positron',
        'tiles': 'CartoDB Positron',
        'attr': ' OpenStreetMap contributors CartoDB',
        'min_zoom': 1,
        'max_zoom': 20,
    },
}

# Parking zone definitions
PARKING_ZONES: Dict[str, List[str]] = {
    "red": [
        "Пупинова", "Светосавска", "Јеврејска", "Гимназијска", "Краља Александра I Карађорђевића",
        "Краља Петра Првог", "Сарајлијина", "Немањина", "Др Славка Жупанског"
    ],
    "yellow": [
        "Слободана Бурсаћа", "Савезничка", "Цара Душана", "Мирослава Тирша"
    ],
    "green": [
        "Кеј другог октобра", "Обала Соње Маринковић", "Обилићева",
        "Петефијева", "Даничићева", "Марка Орешковића", "Иве Лоле Рибара",
        "Косте Абрашевића", "20. октобра", "Југ Богдана", "Саве Текелије"
    ]
}

# Map visualization settings
ZONE_COLORS = {
    "red": "#FF0000",
    "yellow": "#FFFF00",
    "green": "#00FF00"
}

# Map marker settings
MARKER_SETTINGS = {
    "location": DEFAULTS['target_point'],
    "popup": "Центар",
    "color": "blue",
    "icon": "info-sign"
}

# Error messages
ERROR_MESSAGES = {
    'invalid_coordinates': 'Invalid coordinates. Please provide latitude and longitude as numbers.',
    'tile_provider_not_found': 'Tile provider not found. Available providers are: {}'.format(', '.join(TILE_PROVIDERS.keys())),
    'map_data_fetch_failed': 'Failed to fetch map data. Please check your internet connection and try again.',
    'no_streets_found': 'No streets found in the specified area. Try increasing the search radius or check the coordinates.',
}

def get_tile_provider(provider_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the configuration for a tile provider.
    
    Args:
        provider_name: Name of the tile provider. If None or 'all', returns all providers.
                     If not specified, returns the default provider.
        
    Returns:
        Dictionary with tile provider configuration, or dict of all providers if provider_name is 'all'
        
    Raises:
        ValueError: If the specified provider is not found and provider_name is not None or 'all'
    """
    if provider_name is None:
        # Return default provider if no specific provider requested
        return TILE_PROVIDERS[DEFAULTS['tile_provider']]
    elif provider_name.lower() == 'all':
        # Return all providers
        return TILE_PROVIDERS

    # Return the requested provider or raise an error if not found
    provider = TILE_PROVIDERS.get(provider_name)

    if not provider:
        raise ValueError(ERROR_MESSAGES['tile_provider_not_found'])
    return provider
