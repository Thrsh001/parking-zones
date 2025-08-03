"""Utility functions for map processing and visualization."""
import logging
from typing import Dict, List, Tuple, Any, Set, Optional

import folium
from folium import Element, TileLayer, LayerControl
import osmnx as ox

from config import ZONE_COLORS, MARKER_SETTINGS, DEFAULTS, get_tile_provider, ERROR_MESSAGES

# Configure logging
logger = logging.getLogger(__name__)


def create_map(
    location: Tuple[float, float] = DEFAULTS['target_point'],
    zoom_start: int = DEFAULTS['zoom_start'],
    tile_provider: str = DEFAULTS['tile_provider']
) -> folium.Map:
    """
    Create a Folium map with the specified settings.
    
    Args:
        location: Tuple of (latitude, longitude) for the map center
        zoom_start: Initial zoom level
        tile_provider: ID of the tile provider to use (e.g., 'openstreetmap', 'stamen_terrain')
        
    Returns:
        Configured Folium map instance
        
    Raises:
        ValueError: If the tile provider is not found
    """
    try:
        # Get all available providers
        all_providers = get_tile_provider('all')
        
        # Get the default provider config
        default_provider = all_providers.get(tile_provider)
        if not default_provider:
            raise ValueError(f"Tile provider '{tile_provider}' not found")
        
        # Create the base map without any tiles
        folium_map = folium.Map(
            location=location,
            zoom_start=zoom_start,
            tiles=None,
            control_scale=True
        )
        
        # Add all tile providers as base layers
        for provider_id, provider_config in all_providers.items():
            is_default = (provider_id == tile_provider)
            TileLayer(
                tiles=provider_config['tiles'],
                attr=provider_config['attr'],
                name=provider_config['name'],
                min_zoom=provider_config.get('min_zoom', 1),
                max_zoom=provider_config.get('max_zoom', 19),
                overlay=False,
                control=True,
                show=is_default  # Only show the default provider initially
            ).add_to(folium_map)
        
        # Add layer control to switch between tile providers
        LayerControl(
            position='topright',
            collapsed=False
        ).add_to(folium_map)
        
        return folium_map
        
    except Exception as e:
        logger.error(f"Error creating map: {e}")
        raise


def add_map_legend(folium_map: folium.Map) -> None:
    """
    Adds a color legend to the Folium map.
    
    Args:
        folium_map: The Folium map instance to add the legend to.
    """
    try:
        legend_html = """
        <div style="position: fixed;
                    top: 50px; left: 50px; width: 180px; height: 100px; padding: 12px;
                    border:2px solid grey; z-index:9999; font-size:14px;
                    background-color:white; opacity: 0.9;
                    ">  <b>Легенда (Зоне)</b> <br>
            <i class="fa fa-square" style="color:red"></i>  Црвена зона<br>
            <i class="fa fa-square" style="color:yellow"></i>  Жута зона<br>
            <i class="fa fa-square" style="color:green"></i>  Зелена зона
        </div>
        """
        folium_map.get_root().html.add_child(Element(legend_html))
    except Exception as e:
        logger.error(f"Failed to add map legend: {str(e)}")
        raise


def process_street_geometries(
    graph: ox.graph,
    streets_to_zone: Dict[str, str]
) -> Tuple[Dict[str, List[Tuple[List[Tuple[float, float]], str]]], Set[str]]:
    """
    Process street geometries and group them by their parking zones.
    
    Args:
        graph: The OSMnx graph containing street data.
        streets_to_zone: Dictionary mapping street names to their zone colors.
        
    Returns:
        A tuple containing:
        - Dictionary mapping zone colors to lists of (geometry, street_name) tuples
        - Set of found street names
        
    Raises:
        ValueError: If the graph is empty or no streets are found
    """
    if not graph or len(graph) == 0:
        raise ValueError("Empty graph provided. Cannot process street geometries.")
    
    zone_geometries = {color: [] for color in ZONE_COLORS}
    found_streets = set()
    
    try:
        for u, v, data in graph.edges(data=True):
            street_name = data.get('name')
            if not street_name:
                continue

            street_names = [street_name] if isinstance(street_name, str) else street_name

            for name in street_names:
                zone_color = streets_to_zone.get(name.lower())
                if zone_color:
                    try:
                        line_points = [
                            (graph.nodes[u]['y'], graph.nodes[u]['x']),
                            (graph.nodes[v]['y'], graph.nodes[v]['x'])
                        ]
                        zone_geometries[zone_color].append((line_points, name))
                        found_streets.add(name.lower())
                        break  # Found a match, no need to check other names
                    except KeyError as e:
                        logger.warning(f"Missing coordinate data for street segment: {name}. Error: {e}")
                        continue
        
        # Check if any streets were found
        if not any(zone_geometries.values()):
            logger.warning("No streets matching the parking zones were found in the area.")
            
        return zone_geometries, found_streets
        
    except Exception as e:
        logger.error(f"Error processing street geometries: {str(e)}")
        raise ValueError("Failed to process street geometries. Please check the input data and try again.") from e


def add_zone_polylines(
    folium_map: folium.Map,
    zone_geometries: Dict[str, List[Tuple[List[Tuple[float, float]], str]]]
) -> None:
    """
    Add zone polylines to the Folium map.
    
    Args:
        folium_map: The Folium map to add the polylines to.
        zone_geometries: Dictionary mapping zone colors to lists of (geometry, name) tuples.
    """
    for color, geometries in zone_geometries.items():
        for points, name in geometries:
            folium.PolyLine(
                locations=points,
                color=color,
                weight=5,
                opacity=0.8,
                popup=folium.Popup(f'Улица: {name}<br>Зона: {color.capitalize()}', 
                                 max_width=300)
            ).add_to(folium_map)


def add_center_marker(folium_map: folium.Map) -> None:
    """
    Add a marker at the center point of the map.
    
    Args:
        folium_map: The Folium map to add the marker to.
    """
    folium.Marker(
        location=MARKER_SETTINGS["location"],
        popup=MARKER_SETTINGS["popup"],
        icon=folium.Icon(color=MARKER_SETTINGS["color"], 
                        icon=MARKER_SETTINGS["icon"])
    ).add_to(folium_map)
