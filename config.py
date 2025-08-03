"""Configuration settings for the parking zones application."""
from typing import Dict, List, Tuple, Optional, Any

# Default settings
DEFAULTS = {
    # Map center point (latitude, longitude)
    'target_point': (45.38096, 20.39373),
    'map_radius_meters': 10000,
    'map_filename': 'parking_map.html',
    'tile_provider': 'openstreetmap',  # Default tile provider
    'zoom_start': 14,
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
    'invalid_radius': 'Invalid radius. Please provide a positive number for the map radius in meters.',
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
    print('\n\nprovider_name:', provider_name)
    if provider_name is None:
        # Return default provider if no specific provider requested
        return TILE_PROVIDERS[DEFAULTS['tile_provider']]
    elif provider_name.lower() == 'all':
        # Return all providers
        return TILE_PROVIDERS

    # Return the requested provider or raise an error if not found
    provider = TILE_PROVIDERS.get(provider_name)
    print('\n\nprovider :', provider)
    if not provider:
        raise ValueError(ERROR_MESSAGES['tile_provider_not_found'])
    return provider
