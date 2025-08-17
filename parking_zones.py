"""Core functionality for managing and processing parking zones."""
import logging
import osmnx as ox

from config import (
    DEFAULTS, 
    PARKING_ZONES, 
    ERROR_MESSAGES,
    get_tile_provider
)
from map_utils import process_street_geometries
from typing import Dict, Set, Tuple, Optional

# Configure logging
logger = logging.getLogger(__name__)


class ParkingZoneProcessor:
    """Handles processing and managing parking zone data."""
    
    def __init__(
        self,
        target_point: Optional[Tuple[float, float]] = None,
        tile_provider: Optional[str] = None
    ):
        """
        Initialize the ParkingZoneProcessor with configuration.
        
        Args:
            target_point: Tuple of (latitude, longitude) for the map center.
                         If None, uses the default from config.
            tile_provider: Name of the tile provider to use for the map.
                          If None, uses the default from config.
        """
        self.target_point = target_point or DEFAULTS['target_point']
        self.tile_provider = tile_provider or DEFAULTS['tile_provider']
        
        # Validate inputs
        self._validate_config()
        
        # Initialize instance variables
        self.street_to_zone = self._prepare_street_to_zone_lookup()
        self.graph = None
        self.zone_geometries = {}
        self.found_streets = set()
        logger.info(f"Initialized ParkingZoneProcessor with center at {self.target_point}, "
                    f"tile provider: {self.tile_provider}")
    
    def _validate_config(self) -> None:
        """Validate the configuration parameters."""
        try:
            # Validate target point
            if (not isinstance(self.target_point, (tuple, list)) or 
                len(self.target_point) != 2 or 
                not all(isinstance(coord, (int, float)) for coord in self.target_point)):
                raise ValueError(ERROR_MESSAGES['invalid_coordinates'])
                
            # Validate tile provider
            if self.tile_provider not in get_tile_provider('all'):
                raise ValueError(ERROR_MESSAGES['tile_provider_not_found'])
                
        except Exception as e:
            logger.error(f"Configuration validation failed: {str(e)}")
            raise
    
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
    
    def fetch_map_data(self, max_retries: int = 3) -> None:
        """
        Fetch OpenStreetMap data for the target area.
        
        Args:
            max_retries: Maximum number of retry attempts for fetching data
            
        Raises:
            ConnectionError: If unable to fetch map data after retries
            ValueError: If the fetched graph is empty or invalid
        """
        logger.info(f"Retrieving map data for point {self.target_point}...")
        
        for attempt in range(1, max_retries + 1):
            try:
                # Try to fetch the graph data
                self.graph = ox.graph_from_point(
                    center_point=self.target_point,
                    network_type='all',
                    dist=DEFAULTS['radius'],
                    simplify=True
                )
                
                # Validate the graph
                if not self.graph or len(self.graph) == 0:
                    error_msg = "Received empty graph from OpenStreetMap"
                    logger.warning(f"Attempt {attempt}/{max_retries}: {error_msg}")
                    if attempt == max_retries:
                        raise ValueError(ERROR_MESSAGES['no_streets_found'])
                    continue
                    
                logger.info(f"Successfully fetched map data with {len(self.graph)} nodes")
                return
                
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"Failed to fetch map data after {max_retries} attempts: {str(e)}")
                    if "connection" in str(e).lower():
                        raise ConnectionError(ERROR_MESSAGES['map_data_fetch_failed']) from e
                    raise ValueError(ERROR_MESSAGES['no_streets_found']) from e
                
                logger.warning(f"Attempt {attempt}/{max_retries} failed: {str(e)}")
    
    def process_zones(self) -> None:
        """
        Process the map data to identify parking zones.
        
        Raises:
            ValueError: If no map data is available or no streets are found
        """
        if not self.graph:
            raise ValueError("No map data available. Call fetch_map_data() first.")
            
        logger.info("Processing graph edges to find parking zones...")
        
        try:
            self.zone_geometries, self.found_streets = process_street_geometries(
                self.graph, self.street_to_zone
            )
            
            # Log summary of found zones
            for color, geometries in self.zone_geometries.items():
                logger.info(f"Found {len(geometries)} street segments in {color} zone")
                
            if not any(self.zone_geometries.values()):
                logger.warning("No parking zones were found in the specified area.")
                
        except Exception as e:
            logger.error(f"Error processing zones: {str(e)}")
            raise ValueError("Failed to process parking zones. Please check the input data and try again.") from e
    
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
