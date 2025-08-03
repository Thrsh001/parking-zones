"""Core functionality for managing and processing parking zones."""
from typing import Dict, List, Tuple, Set
import logging

import osmnx as ox

from config import TARGET_POINT, MAP_RADIUS_METERS, PARKING_ZONES
from map_utils import process_street_geometries


class ParkingZoneProcessor:
    """Handles processing and managing parking zone data."""
    
    def __init__(self):
        """Initialize the ParkingZoneProcessor with configuration."""
        self.street_to_zone = self._prepare_street_to_zone_lookup()
        self.graph = None
        self.zone_geometries = {}
        self.found_streets = set()
    
    @staticmethod
    def _prepare_street_to_zone_lookup() -> Dict[str, str]:
        """
        Create a lookup dictionary mapping street names to their zone colors.
        
        Returns:
            Dictionary mapping street names (lowercase) to zone colors.
        """
        street_map = {}
        for color, streets in PARKING_ZONES.items():
            for street in streets:
                street_map[street.lower()] = color
        return street_map
    
    def fetch_map_data(self) -> None:
        """Fetch OpenStreetMap data for the target area."""
        logging.info(f"Retrieving map data for point {TARGET_POINT} within {MAP_RADIUS_METERS}m...")
        self.graph = ox.graph_from_point(
            center_point=TARGET_POINT,
            network_type='all',
            dist=MAP_RADIUS_METERS
        )
    
    def process_zones(self) -> None:
        """Process the map data to identify parking zones."""
        if not self.graph:
            raise ValueError("No map data available. Call fetch_map_data() first.")
            
        logging.info("Processing graph edges to find parking zones...")
        self.zone_geometries, self.found_streets = process_street_geometries(
            self.graph, self.street_to_zone
        )
    
    def get_missing_streets(self) -> Set[str]:
        """
        Get a set of street names that were not found in the map data.
        
        Returns:
            Set of street names that were not found.
        """
        all_streets = set(self.street_to_zone.keys())
        return all_streets - self.found_streets
    
    def log_processing_summary(self) -> None:
        """Log a summary of the processing results."""
        for color, geometries in self.zone_geometries.items():
            logging.info(f"Found {len(geometries)} street segments for the {color} zone.")
        
        missing = self.get_missing_streets()
        if missing:
            logging.warning(f"Could not find map data for {len(missing)} streets:")
            for street in sorted(missing):
                logging.warning(f" - {street.capitalize()}")
