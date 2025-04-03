# 🌓 Moon Path Visualizer

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.24+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An interactive web application that visualizes the Moon's path across the globe and Earth's day/night terminator in real-time. Watch where the Moon is directly overhead and how Earth's day/night regions change throughout the day.

[Live Demo](https://moonpath.streamlit.app) <!-- Visit the deployed app here -->

![App Screenshot](#) <!-- Add a screenshot of your app here -->

## ✨ Features

- 🌍 Real-time Moon position visualization on an interactive 3D globe
- 🛣️ 24-hour Moon path prediction
- 🌓 Dynamic day/night terminator display
- 📅 Interactive date and time selection
- 🌐 Global orthographic projection with zoom and pan
- 🕒 UTC time support
- 🗺️ Country borders and coastlines

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/kongpop10/moon-path-visualizer.git
cd moon-path-visualizer
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

### Running the App

1. Start the Streamlit server:
```bash
streamlit run moon_app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

## 🎯 How to Use

1. **Date Selection**: Use the sidebar date picker to choose any date
2. **Time Selection**: Select the time in UTC using the time picker
3. **Visualization**:
   - Yellow line shows the Moon's 24-hour path
   - Large yellow dot indicates current Moon position
   - Light blue areas represent daylight regions
   - Dark blue areas show night regions
   - Orange line represents the dawn/dusk terminator

## 🔧 Technical Details

### Visualization Components
- **Moon Position**: Shows where the Moon is directly overhead
- **Path Tracking**: 24-hour prediction with hourly points
- **Day/Night Display**: Real-time calculation of Earth's illumination
- **Terminator Line**: Accurate dawn/dusk boundary visualization

### Technologies Used
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualization
- **ephem**: Astronomical calculations
- **NumPy/Pandas**: Data processing
- **pytz**: Timezone handling

## 📝 Notes

- All astronomical calculations are approximations suitable for visualization
- Times are displayed in UTC (Coordinated Universal Time)
- Position calculations show where the Moon is directly overhead
- Visualization accuracy is optimized for general use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [ephem](https://rhodesmill.org/pyephem/) for astronomical calculations
- [Plotly](https://plotly.com/) for interactive visualizations

## 📧 Contact

kongpop10 - kongpopu@outlook.com

Project Link: [https://github.com/kongpop10/moon-path-visualizer](https://github.com/kongpop10/moon-path-visualizer)
