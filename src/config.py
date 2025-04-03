"""
Configuration module for Supply Chain simulation.

This module contains configuration settings and constants used throughout the application.
"""

# Apple varieties available in the system
APPLE_VARIETIES = [
    "Royal Gala",
    "Fuji",
    "Granny Smith",
    "Golden Delicious",
    "Pink Lady"
]

# Potential shelf lives for apples (in days)
SHELF_LIVES = [5, 10, 15]

# Apple grades
GRADES = ["Small", "Medium", "Large"]

# Units of measure for quantities
UNITS_OF_MEASURE = ["metrictons"]

# Month mapping (name to number)
MONTH_MAP = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4, 
    'May': 5, 'June': 6, 'July': 7, 'August': 8, 
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# Month mapping (number to name)
INV_MONTH_MAP = {v: k for k, v in MONTH_MAP.items()}

# Planning lead time in months
PLANNING_LEAD_TIME = 3

# Supplier port mapping
COUNTRY_PORT_MAP = {
    'India': 'Jawaharlal Nehru Port Sheva Navi Mumbai',
    'South Africa': 'Port of Cape Town',
    'Chile': 'Port of San Antonio',
    'New Zealand': 'Ports of Auckland'
}

# Shipping port coordinates (latitude, longitude)
PORT_COORDINATES = {
    'Jawaharlal Nehru Port Sheva Navi Mumbai': (18.9397, 72.9153),
    'Port of Cape Town': (-33.9072, 18.4227),
    'Port of San Antonio': (-33.5983, -71.6133),
    'Ports of Auckland': (-36.8485, 174.7633),
    'Albert Plesmanweg 240 Rotterdam': (51.9225, 4.4689)
}

# Apple variety mapping for demand data
VARIETY_MAP = {
    'royal_gala': 'Royal Gala',
    'fuji': 'Fuji',
    'granny_smith': 'Granny Smith',
    'golden_delicious': 'Golden Delicious',
    'pink_lady': 'Pink Lady'
}

# Waypoints for shipping routes visualization
WAYPOINTS = {
    'San Antonio': [
        (-33.6, -71.6),  # San Antonio, Chile
        (10.0, -79.5),  # Panama Canal
        (35.0, -5.0),   # Strait of Gibraltar
        (51.9225, 4.4792) # Rotterdam, Netherlands
    ],
    'Auckland': [
        (-36.8485, 174.7633),  # Auckland, New Zealand
        (-12.0, 160.0),        # Pacific Ocean waypoint
        (0.0, -20.0),          # Atlantic Ocean waypoint
        (35.0, -5.0),          # Strait of Gibraltar
        (51.9225, 4.4792)      # Rotterdam, Netherlands
    ],
    'Mumbai': [
        (18.9750, 72.8258),    # Mumbai, India
        (20.0, 80.0),          # Arabian Sea, East of India
        (22.0, 50.0),          # Near Oman
        (35.0, -5.0),          # Strait of Gibraltar
        (51.9225, 4.4792)      # Rotterdam, Netherlands
    ],
    'Cape Town': [
        (-33.918861, 18.423300),  # Cape Town, South Africa
        (-15.387526, 12.479099),  # Near Angola (West Africa)
        (0.0, -20.0),             # Equatorial Atlantic
        (14.599512, -17.439150),  # Near Senegal
        (35.179554, -6.144410),   # Strait of Gibraltar
        (45.0, 0.0),              # Bay of Biscay (near France)
        (51.9225, 4.4792)         # Rotterdam, Netherlands
    ]
}

# Default data paths
DATA_DIR = "data"

# Output file paths
def get_output_path(filename):
    """Get the absolute path for an output file.
    
    Args:
        filename (str): The name of the output file
        
    Returns:
        str: The absolute path to the output file
    """
    import os
    return os.path.abspath(os.path.join(DATA_DIR, filename))
