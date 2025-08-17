"""
Streamlit app for Parking Zones Visualization
"""
import streamlit as st
import tempfile
import os
from streamlit.components.v1 import html as components_html

from main import generate_map
from config import LOCATIONS, get_tile_provider

# Page configuration
st.set_page_config(
    page_title="Parking Zones Visualizer",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .stSelectbox, .stNumberInput, .stSlider {
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def _get_tile_provider_options():   # noqa C901
    """Get available tile provider options."""
    tile_providers = get_tile_provider('all')
    return {config['name']: pid for pid, config in tile_providers.items()}

def _render_location_settings():
    """Render location selection UI and return selected location."""
    st.subheader("Location")
    selected = st.selectbox(
        "Select Location",
        options=list(LOCATIONS.keys()),
        index=0
    )
    display_coordinates(selected)
    return selected

def _render_map_style_settings():
    """Render map style selection and return selected provider ID."""
    st.subheader("Map Settings")
    provider_names = _get_tile_provider_options()
    selected_name = st.selectbox(
        "Map Style",
        options=list(provider_names.keys()),
        index=0
    )
    return provider_names[selected_name]

def get_map_settings():
    """Render and return the map settings from the sidebar."""
    st.header("🔧 Settings")
    selected_location = _render_location_settings()
    tile_provider_id = _render_map_style_settings()
    
    return {
        'lat': LOCATIONS[selected_location]['lat'],
        'lon': LOCATIONS[selected_location]['lon'],
        'tile_provider': tile_provider_id
    }


def display_coordinates(selected_location):
    # Get coordinates based on selection
    location = LOCATIONS[selected_location]
    lat, lon = location['lat'], location['lon']

    # Display coordinates as read-only for reference
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Latitude", value=f"{lat:.5f}", disabled=True)
    with col2:
        st.text_input("Longitude", value=f"{lon:.5f}", disabled=True)


def show_instructions():
    """Display application instructions."""
    st.markdown("""
        ### How to use:
        1. Adjust the location using the latitude and longitude inputs
        2. Choose your preferred map style
        3. Click "Generate Map" to create your parking zone visualization
        
        The map will show different parking zones in different colors.
        """)


def handle_map_generation(lat, lon, tile_provider):
    """Handle the map generation process with proper error handling."""
    with st.spinner("Generating map... This might take a moment..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                output_file = tmpfile.name

            result = generate_map(
                lat=lat,
                lon=lon,
                tile_provider=tile_provider,
                output_file=output_file
            )

            if result == 0:
                st.success("Map generated successfully!")
                # Read the generated HTML file
                with open(output_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Display the map in the app
                st.components.v1.html(html_content, height=600)
            else:
                st.error("Failed to generate the map. Please check the console for details.")

            return result

        except ValueError as e:
            st.error(f"Invalid input: {str(e)}")
            st.error(f"Input validation error: {str(e)}", exc_info=True)
        except ConnectionError as e:
            st.error("Failed to fetch map data. Please check your internet connection and try again.")
            st.error(f"Connection error: {str(e)}", exc_info=True)
        except Exception as e:
            st.error("An unexpected error occurred while generating the map.")
            st.error(f"Error: {str(e)}")
            st.error("Unexpected error:", exc_info=True)
        finally:
            # Clean up the temporary file if it exists
            if 'output_file' in locals() and os.path.exists(output_file):
                try:
                    os.unlink(output_file)
                except Exception as e:
                    st.error(f"Error cleaning up temporary file: {e}")
        return None


def main():
    """Main application entry point."""
    st.title("🚗 Parking Zones Visualizer")
    st.markdown("Visualize parking zones on an interactive map. Customize the location and style below.")

    # Sidebar for inputs
    with st.sidebar:
        settings = get_map_settings()
        generate_btn = st.button("Generate Map", type="primary")

    # Main content area
    if generate_btn:
        handle_map_generation(settings['lat'], settings['lon'], settings['tile_provider'])
    else:
        show_instructions()


if __name__ == "__main__":
    main()
