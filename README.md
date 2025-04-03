# 🌓 Moon Path Visualizer

A Streamlit web application that visualizes the Moon's path across the globe and the day/night terminator. The app shows where the Moon is directly overhead and how Earth's day/night regions change over time.

## Features

- Real-time Moon position visualization
- 24-hour Moon path prediction
- Day/night terminator display
- Interactive date and time selection
- Global orthographic projection
- UTC time support

## Installation

1. Clone this repository:
```bash
git clone <your-repository-url>
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run moon_app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar controls to:
   - Select a date
   - Choose a time (in UTC)
   - View the Moon's position and path

## Visualization Guide

- Yellow line: Moon's path over 24 hours
- Large yellow dot: Current Moon position
- Light blue area: Daylight regions
- Dark blue area: Night regions
- Orange line: Day/night terminator (dawn/dusk line)

## Technical Notes

- All calculations are approximations suitable for visualization purposes
- Times are in UTC (Coordinated Universal Time)
- Uses ephem library for astronomical calculations
- Positions show where the Moon is directly overhead

## Requirements

See `requirements.txt` for detailed package requirements.

## License

[Your chosen license]