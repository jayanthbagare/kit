"""
Visualization utilities for supply chain data.

This module contains functions for creating maps, charts, and other 
visualizations of supply chain data.
"""

import folium
from folium import plugins
from IPython.display import display
import os
from config import PORT_COORDINATES, WAYPOINTS

def plot_shipping_routes_with_waypoints(routes_dict=None):
    """Create a map showing shipping routes with waypoints.
    
    Args:
        routes_dict (dict, optional): Dictionary mapping route names to waypoint lists.
                                     If None, uses default WAYPOINTS from config.
    
    Returns:
        folium.Map: The created map object
    """
    # Create map centered around Europe
    europe_coords = (30.0, 10.0)  # Central coordinates for world view
    m = folium.Map(
        location=europe_coords,
        zoom_start=2,
        tiles='CartoDB positron'
    )
    
    # Use default waypoints if none provided
    routes_to_plot = routes_dict or WAYPOINTS
    
    # Define colors for each route
    route_colors = {
        'San Antonio': 'red',
        'Auckland': 'blue',
        'Mumbai': 'green',
        'Cape Town': 'purple'
    }
    
    # Add routes to map
    for route_name, waypoints in routes_to_plot.items():
        color = route_colors.get(route_name, 'gray')
        
        # Add markers for origin and destination
        if waypoints:
            # Origin
            folium.Marker(
                location=waypoints[0],
                popup=f"{route_name} (Origin)",
                icon=folium.Icon(color=color)
            ).add_to(m)
            
            # Destination
            folium.Marker(
                location=waypoints[-1],
                popup="Rotterdam (Destination)",
                icon=folium.Icon(color=color)
            ).add_to(m)
            
            # Add route line
            folium.PolyLine(
                waypoints, 
                color=color, 
                weight=2.5, 
                opacity=0.8,
                popup=f"{route_name} to Rotterdam"
            ).add_to(m)
            
            # Add waypoint markers (smaller)
            for i, waypoint in enumerate(waypoints[1:-1], 1):
                folium.CircleMarker(
                    location=waypoint,
                    radius=3,
                    color=color,
                    fill=True,
                    fill_color=color,
                    popup=f"{route_name} Waypoint {i}"
                ).add_to(m)
    
    # Add fullscreen control
    plugins.Fullscreen().add_to(m)
    
    return m

def save_and_display_map(map_obj, filename="shipping_routes.html"):
    """Save the map to an HTML file and display it if in a notebook.
    
    Args:
        map_obj (folium.Map): The map to save and display
        filename (str): The filename to save the map as
        
    Returns:
        None
    """
    try:
        map_obj.save(filename)
        print(f"Map saved to {filename}")
        
        # Try to display the map (will work in notebooks)
        try:
            display(map_obj)
        except:
            pass
    except Exception as e:
        print(f"Error saving map: {e}")
