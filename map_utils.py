"""Utility functions for map processing and visualization."""
from typing import Dict, List, Tuple, Any, Set

import folium
from folium import Element
import osmnx as ox

from config import ZONE_COLORS, MARKER_SETTINGS


def add_map_legend(folium_map: folium.Map) -> None:
    """
    Adds a color legend to the Folium map.
    
    Args:
        folium_map: The Folium map instance to add the legend to.
    """
    legend_html = """
    <div style="position: fixed;
                top: 50px; right: 50px; width: 180px; height: 100px;
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity: 0.9;
                ">  <b>Легенда (Зоне)</b> <br>
        <i class="fa fa-square" style="color:red"></i>  Црвена зона<br>
        <i class="fa fa-square" style="color:yellow"></i>  Жута зона<br>
        <i class="fa fa-square" style="color:green"></i>  Зелена зона
    </div>
    """
    folium_map.get_root().html.add_child(Element(legend_html))


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
    """
    zone_geometries = {color: [] for color in ZONE_COLORS}
    found_streets = set()
    
    for u, v, data in graph.edges(data=True):
        street_name = data.get('name')
        if not street_name:
            continue

        street_names = [street_name] if isinstance(street_name, str) else street_name

        for name in street_names:
            zone_color = streets_to_zone.get(name.lower())
            if zone_color:
                line_points = [
                    (graph.nodes[u]['y'], graph.nodes[u]['x']),
                    (graph.nodes[v]['y'], graph.nodes[v]['x'])
                ]
                zone_geometries[zone_color].append((line_points, name))
                found_streets.add(name.lower())
                break
                
    return zone_geometries, found_streets


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
