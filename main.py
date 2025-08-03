#!/usr/bin/env python3
"""
Main entry point for the Parking Zones application.
This script generates an interactive map showing parking zones in the specified area.
"""
import logging
import folium

from config import MAP_FILENAME, TARGET_POINT
from parking_zones import ParkingZoneProcessor
from map_utils import add_zone_polylines, add_map_legend, add_center_marker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def create_map(zone_geometries: dict) -> folium.Map:
    """
    Create and configure a Folium map with parking zone data.
    
    Args:
        zone_geometries: Dictionary mapping zone colors to lists of (geometry, name) tuples.
        
    Returns:
        Configured Folium map instance.
    """
    # Create the base map
    m = folium.Map(
        location=TARGET_POINT,
        zoom_start=14,
        tiles='OpenStreetMap'
    )
    
    # Add zone polylines to the map
    add_zone_polylines(m, zone_geometries)
    
    # Add UI elements
    add_map_legend(m)
    add_center_marker(m)
    
    return m


def main():
    """
    Main function to generate the parking zone map.
    """
    try:
        # Initialize and process parking zone data
        processor = ParkingZoneProcessor()
        processor.fetch_map_data()
        processor.process_zones()
        
        # Log processing summary
        processor.log_processing_summary()
        
        # Create and save the map
        m = create_map(processor.zone_geometries)
        m.save(MAP_FILENAME)
        logging.info(f"Map successfully saved to {MAP_FILENAME}")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()