import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime
import ephem
import pytz
from math import degrees, radians, sin, cos, asin, acos, pi

st.set_page_config(
    page_title="Moon Path Visualizer",
    page_icon="🌓",
    layout="wide",
    initial_sidebar_state="expanded"  # Start with sidebar expanded
)

# Title and description
st.title("🌓 Moon Path Visualizer")
st.markdown("""
This application shows the Moon's path across the globe and the day/night terminator.
Adjust the date and time to see how the Moon's position and Earth's illumination change.
""")

# Function to calculate Moon's position for a given time
def get_moon_position(dt):
    # Create an observer at the center of the Earth
    observer = ephem.Observer()
    observer.date = dt

    # Compute the Moon's position
    moon = ephem.Moon(observer)
    moon.compute(dt)

    # Get Moon's latitude (declination)
    moon_lat = degrees(float(moon.dec))

    # Convert right ascension to longitude
    # First convert RA from hours to degrees (RA is in radians in ephem)
    ra_deg = degrees(float(moon.ra))

    # Convert RA to longitude (need to account for Earth's rotation)
    # Get the Greenwich sidereal time in degrees
    gst = degrees(observer.sidereal_time())

    # Calculate longitude (RA - GST, adjusted to -180 to 180 range)
    moon_lon = (ra_deg - gst) % 360
    if moon_lon > 180:
        moon_lon -= 360

    return moon_lat, moon_lon

# Function to calculate positions for the Moon's path over 24 hours
def calculate_moon_path(base_dt):
    path_data = []

    # Calculate positions for 24 hours (1 hour intervals)
    for hour_offset in range(25):  # 25 points for a smooth path (0-24 hours)
        dt = base_dt + datetime.timedelta(hours=hour_offset)
        lat, lon = get_moon_position(dt)

        # Format time for hover text
        time_str = dt.strftime('%Y-%m-%d %H:%M UTC')

        path_data.append({
            'lat': lat,
            'lon': lon,
            'time': time_str,
            'hour': hour_offset
        })

    return pd.DataFrame(path_data)

# Function to calculate day/night terminator
def calculate_terminator(dt):
    # Get the Sun's position
    observer = ephem.Observer()
    observer.date = dt
    sun = ephem.Sun(observer)
    sun.compute(dt)

    # Get Sun's declination (latitude)
    sun_dec = degrees(float(sun.dec))

    # Convert right ascension to longitude
    ra_deg = degrees(float(sun.ra))
    gst = degrees(observer.sidereal_time())
    sun_ra = (ra_deg - gst) % 360
    if sun_ra > 180:
        sun_ra -= 360

    # Create terminator points
    terminator_lats = []
    terminator_lons = []

    # Create a more efficient grid for day/night visualization
    day_lats = []
    day_lons = []
    night_lats = []
    night_lons = []

    # Convert sun position to radians for calculations
    sun_lat_rad = radians(sun_dec)
    sun_lon_rad = radians(sun_ra)

    # Create a grid of points (reduced density for performance)
    lat_step = 5
    lon_step = 5

    for lat in np.arange(-90, 91, lat_step):
        for lon in np.arange(-180, 181, lon_step):
            lat_rad = radians(lat)
            lon_rad = radians(lon)

            # Calculate the angle between the sun and the point
            angle = acos(sin(sun_lat_rad) * sin(lat_rad) +
                         cos(sun_lat_rad) * cos(lat_rad) * cos(lon_rad - sun_lon_rad))

            # Determine if the point is in day or night
            # The terminator is approximately at 90 degrees from the sun
            if abs(degrees(angle) - 90) < 2:  # Points near the terminator
                terminator_lats.append(lat)
                terminator_lons.append(lon)
            elif degrees(angle) < 90:  # Day side
                day_lats.append(lat)
                day_lons.append(lon)
            else:  # Night side
                night_lats.append(lat)
                night_lons.append(lon)

    return {
        'terminator': (terminator_lats, terminator_lons),
        'day': (day_lats, day_lons),
        'night': (night_lats, night_lons)
    }

# Sidebar for date and time selection
st.sidebar.header("Date and Time Settings")

# Get current UTC time as default
initial_default_time = datetime.datetime.now(pytz.UTC)

# Initialize session state for date and time if they don't exist
if 'selected_date' not in st.session_state:
    st.session_state.selected_date = initial_default_time.date()
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = initial_default_time.time()

# Define time navigation callback functions
def fast_backward():
    # Create a datetime object from the current date and time
    current_dt = datetime.datetime.combine(
        st.session_state.selected_date,
        st.session_state.selected_time,
        tzinfo=pytz.UTC
    )
    # Calculate new datetime (1 hour back)
    new_dt = current_dt - datetime.timedelta(hours=1)
    # Update session state for the next render
    st.session_state.selected_date = new_dt.date()
    st.session_state.selected_time = new_dt.time()

def backward():
    # Create a datetime object from the current date and time
    current_dt = datetime.datetime.combine(
        st.session_state.selected_date,
        st.session_state.selected_time,
        tzinfo=pytz.UTC
    )
    # Calculate new datetime (15 minutes back)
    new_dt = current_dt - datetime.timedelta(minutes=15)
    # Update session state for the next render
    st.session_state.selected_date = new_dt.date()
    st.session_state.selected_time = new_dt.time()

def forward():
    # Create a datetime object from the current date and time
    current_dt = datetime.datetime.combine(
        st.session_state.selected_date,
        st.session_state.selected_time,
        tzinfo=pytz.UTC
    )
    # Calculate new datetime (15 minutes forward)
    new_dt = current_dt + datetime.timedelta(minutes=15)
    # Update session state for the next render
    st.session_state.selected_date = new_dt.date()
    st.session_state.selected_time = new_dt.time()

def fast_forward():
    # Create a datetime object from the current date and time
    current_dt = datetime.datetime.combine(
        st.session_state.selected_date,
        st.session_state.selected_time,
        tzinfo=pytz.UTC
    )
    # Calculate new datetime (1 hour forward)
    new_dt = current_dt + datetime.timedelta(hours=1)
    # Update session state for the next render
    st.session_state.selected_date = new_dt.date()
    st.session_state.selected_time = new_dt.time()

# Date picker
selected_date = st.sidebar.date_input(
    "Select Date",
    key='selected_date' # Use key to automatically update session state
)

# Time picker
selected_time = st.sidebar.time_input(
    "Select Time (UTC)",
    key='selected_time' # Use key to automatically update session state
)

# Combine date and time
selected_datetime = datetime.datetime.combine(
    st.session_state.selected_date, # Use session state values
    st.session_state.selected_time, # Use session state values
    tzinfo=pytz.UTC
)

# Display selected date and time
st.sidebar.write(f"Selected: {selected_datetime.strftime('%Y-%m-%d %H:%M UTC')}")

# Add custom CSS for button styling
st.markdown("""
<style>
    /* Custom button style for navigation buttons */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button {
        background-color: #00A6ED !important;
        color: white !important;
        border-color: #00A6ED !important;
    }
</style>
""", unsafe_allow_html=True)

# Time navigation buttons
st.sidebar.markdown("### Time Navigation")

# Create a container for the buttons
button_container = st.sidebar.container()

# Create columns for the buttons
col1, col2, col3, col4 = button_container.columns(4)

# Fast backward button (-1 hour)
col1.button("⏪", help="Go back 1 hour", key="fast_backward", on_click=fast_backward)

# Backward button (-15 minutes)
col2.button("◀️", help="Go back 15 minutes", key="backward", on_click=backward)

# Forward button (+15 minutes)
col3.button("▶️", help="Go forward 15 minutes", key="forward", on_click=forward)

# Fast forward button (+1 hour)
col4.button("⏩", help="Go forward 1 hour", key="fast_forward", on_click=fast_forward)

# Calculate Moon's position and path
current_moon_lat, current_moon_lon = get_moon_position(selected_datetime)
moon_path_df = calculate_moon_path(selected_datetime)

# Calculate day/night terminator
terminator_data = calculate_terminator(selected_datetime)

# Create the map visualization
st.subheader("Moon Path and Day/Night Visualization")

# Create a figure without using a container to maximize space
fig = go.Figure()

# Add night side as a scatter plot with dark blue color
fig.add_trace(go.Scattergeo(
    lon=terminator_data['night'][1],
    lat=terminator_data['night'][0],
    mode='markers',
    marker=dict(
        size=4,
        color='rgba(25, 25, 112, 0.7)',  # Dark blue with transparency
        opacity=0.7
    ),
    name='Night',
    showlegend=True
))

# Add day side as a scatter plot with light blue color
fig.add_trace(go.Scattergeo(
    lon=terminator_data['day'][1],
    lat=terminator_data['day'][0],
    mode='markers',
    marker=dict(
        size=4,
        color='rgba(135, 206, 250, 0.7)',  # Light blue with transparency
        opacity=0.7
    ),
    name='Day',
    showlegend=True
))

# Add terminator line
fig.add_trace(go.Scattergeo(
    lon=terminator_data['terminator'][1],
    lat=terminator_data['terminator'][0],
    mode='markers',
    marker=dict(
        size=3,
        color='rgba(255, 165, 0, 0.8)',  # Orange with transparency
        opacity=0.8
    ),
    name='Terminator',
    showlegend=True
))

# Add Moon's path
fig.add_trace(go.Scattergeo(
    lon=moon_path_df['lon'],
    lat=moon_path_df['lat'],
    mode='lines+markers',
    line=dict(
        width=2,
        color='yellow'
    ),
    marker=dict(
        size=4,
        color='yellow'
    ),
    text=moon_path_df['time'],
    hoverinfo='text+lon+lat',
    name='Moon Path'
))

# Add current Moon position with a larger marker
fig.add_trace(go.Scattergeo(
    lon=[current_moon_lon],
    lat=[current_moon_lat],
    mode='markers',
    marker=dict(
        size=12,
        color='yellow',
        line=dict(
            width=2,
            color='black'
        ),
        symbol='circle'
    ),
    name='Current Moon Position',
    text=[f"Moon at {selected_datetime.strftime('%Y-%m-%d %H:%M UTC')}"],
    hoverinfo='text+lon+lat'
))

# Configure the map to maximize the globe view
fig.update_geos(
    projection_type="orthographic",
    projection_rotation=dict(lon=current_moon_lon, lat=current_moon_lat, roll=0), # Rotate view to center on Moon
    landcolor='rgb(217, 217, 217)',
    oceancolor='rgb(55, 97, 164)',
    showland=True,
    showocean=True,
    showcoastlines=True,
    showcountries=True,
    countrycolor='white',
    coastlinecolor='white',
    coastlinewidth=0.5,
    countrywidth=0.5,
    bgcolor='rgba(0,0,0,0)',
    # projection_scale=1.1, # Removed to allow auto-scaling
    fitbounds=False,  # Don't auto-fit bounds
    visible=True  # Ensure the map is visible
)

# Update layout to maximize space and remove blank areas
fig.update_layout(
    title=f"Moon's Path and Day/Night Cycle",
    height=700,  # Set a larger default height for the visualization
    autosize=True,  # Allow auto-sizing based on container
    margin=dict(l=0, r=0, t=30, b=0, pad=0),  # Remove all margins and padding
    legend=dict(
        x=0,
        y=1,
        bgcolor='rgba(255, 255, 255, 0.7)',
        orientation='h'  # Horizontal legend to save space
    ),
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# Display the map with full width
# Create columns to force full width usage
col1, col2, col3 = st.columns([0.05, 99.9, 0.05])  # Adjusted to give more space to the map
with col2:
    st.plotly_chart(fig, use_container_width=True, config={
        'responsive': True,
        'displayModeBar': False,
        'scrollZoom': True,  # Enable scroll zoom for better interaction
        'modeBarButtonsToRemove': ['select2d', 'lasso2d']  # Remove unnecessary buttons
    })

# How to Use and About section moved to sidebar

# Add a note about the calculations
st.sidebar.markdown("""
### Note on Calculations
This visualization provides an approximation of:
- The Moon's position (where it appears directly overhead)
- The day/night terminator
- The Moon's path over 24 hours

For precise astronomical calculations, specialized tools should be used.
""")

# Add the How to Use and About section to the sidebar
st.sidebar.markdown("---") # Add a separator

# Create a collapsible section for How to Use
with st.sidebar.expander("How to Use", expanded=False):
    st.markdown("""
    - Use the date and time selectors in the sidebar to choose when to view the Moon's position.
    - The yellow line shows the Moon's path over 24 hours from the selected time.
    - The large yellow dot shows the Moon's position at the selected time.
    - Blue areas are in daylight, while dark blue areas are in night.
    - The orange line represents the day/night terminator (dawn/dusk line).
    """)

# Create a collapsible section for About
with st.sidebar.expander("About", expanded=False):
    st.markdown("""
    This visualization uses astronomical calculations to determine:
    - The Moon's position relative to Earth (where the Moon is directly overhead)
    - The day/night terminator based on the Sun's position
    - The projected path of the Moon over a 24-hour period
    """)
