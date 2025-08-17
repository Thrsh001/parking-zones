#!/usr/bin/env python3
"""
Parking Zones Visualizer

This script generates an interactive map showing parking zones in a specified area.
It supports various configuration options via command-line arguments.

Example usage:
    python main.py --lat 45.38 --lon 20.39  --output my_map.html --tile-provider "Stamen Terrain"
"""
import argparse
import logging
import sys
from typing import Tuple

from config import DEFAULTS, get_tile_provider, ERROR_MESSAGES
from parking_zones import ParkingZoneProcessor
from map_utils import create_map, add_zone_polylines, add_map_legend

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('parking_zones.log')
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description='Generate an interactive map of parking zones.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Map center coordinates
    parser.add_argument(
        '--lat',
        type=float,
        default=DEFAULTS['target_point'][0],
        help='Latitude of the map center point'
    )
    parser.add_argument(
        '--lon',
        type=float,
        default=DEFAULTS['target_point'][1],
        help='Longitude of the map center point'
    )
    
    # Map configuration
    parser.add_argument(
        '-o', '--output',
        default=DEFAULTS['map_filename'],
        help='Output HTML filename'
    )
    # Get the list of available tile providers with their display names
    available_providers = get_tile_provider('all')
    provider_choices = list(available_providers.keys())
    provider_descriptions = [f"{pid} ({config['name']})" for pid, config in available_providers.items()]
    
    parser.add_argument(
        '-t', '--tile-provider',
        choices=provider_choices,
        default=DEFAULTS['tile_provider'],
        help=f'Map tile provider to use. Available: {", ".join(provider_descriptions)}. Default: %(default)s'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def validate_coordinates(lat: float, lon: float) -> Tuple[float, float]:
    """
    Validate and return latitude and longitude coordinates.
    
    Args:
        lat: Latitude value
        lon: Longitude value
        
    Returns:
        Tuple of (latitude, longitude)

    Raises:
        ValueError: If coordinates are invalid
    """
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude must be between -180 and 180, got {lon}")
    return lat, lon




def generate_map(lat: float, lon: float, tile_provider: str, output_file: str) -> int:
    """
    Generate a parking zone map with the given parameters.
    
    Args:
        lat: Latitude of the center point
        lon: Longitude of the center point
        tile_provider: Name of the tile provider to use
        output_file: Path to save the generated map HTML file
        
    Returns:
        int: 0 on success, non-zero on error
    """
    try:
        # Validate coordinates
        target_point = validate_coordinates(lat, lon)
        
        logger.info(f"Starting parking zone visualization with center at {target_point}")
        logger.info(f"Using tile provider: {tile_provider}")
        
        # Initialize the processor
        processor = ParkingZoneProcessor(
            target_point=target_point,
            tile_provider=tile_provider
        )
        
        # Fetch and process map data
        logger.info("Fetching map data...")
        processor.fetch_map_data()
        logger.info("Processing parking zones...")
        processor.process_zones()
        
        # Log processing summary
        processor.log_processing_summary()
        
        # Create the map with the specified tile provider
        logger.info("Generating the map...")
        m = create_map(
            location=target_point,
            zoom_start=DEFAULTS['zoom_start'],
            tile_provider=tile_provider
        )
        
        # Add parking zone data to the map
        add_zone_polylines(m, processor.zone_geometries)
        add_map_legend(m)
        
        # Save the map to file
        m.save(output_file)
        logger.info(f"Map successfully saved to {output_file}")
        
        return 0
        
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Data error: {e}")
        raise
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        raise

def main():
    """
    Command-line interface for the parking zone map generator.
    """
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Set logging level
        if args.verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("Verbose logging enabled")
        
        # Generate the map
        return generate_map(
            lat=args.lat,
            lon=args.lon,
            tile_provider=args.tile_provider,
            output_file=args.output
        )
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"A fatal error occurred: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)