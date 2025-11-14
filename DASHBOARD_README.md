# Smart City Dashboard - Visual Interface

## 🚀 Quick Start

### Option 1: Simple Start (Recommended)

1. **Start the API server:**
   ```bash
   cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
   python3 -m app.main
   ```
   Keep this terminal open.

2. **Open the dashboard:**
   - Open `dashboard.html` in your web browser
   - Or double-click the file
   - Or run: `open dashboard.html` (Mac) / `xdg-open dashboard.html` (Linux)

### Option 2: Use Start Script

```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
./start_dashboard.sh
```

This will:
- Start the API server automatically
- Open the dashboard in your browser

## 📊 What You'll See

The dashboard displays:

1. **Current Traffic Segments**
   - Real-time traffic data
   - Speed and congestion levels
   - Risk indicators (Green/Yellow/Red)

2. **Traffic Predictions**
   - 15-30 minute forecasts
   - Predicted speeds
   - Risk levels
   - Reasoning factors

3. **AI Explanation**
   - Natural language summary
   - Current hotspots
   - Future predictions
   - Recommendations

4. **Statistics**
   - Active segments count
   - Total predictions
   - Average congestion

5. **Traffic Zones**
   - Aggregated zone data
   - Air quality (PM2.5)
   - Pollution risk levels

## 🔄 Auto-Refresh

The dashboard automatically refreshes every 30 seconds to show the latest data.

You can also click the "🔄 Refresh" button to manually update.

## 🛠️ Troubleshooting

### Dashboard shows "Error loading..."
- Make sure the API server is running (`python3 -m app.main`)
- Check that the server is on `http://localhost:8000`
- Open browser console (F12) to see detailed errors

### No data showing
- Run the simulation first: `python3 scripts/run_simulation.py`
- Generate predictions: `python3 scripts/test_prediction_cycle.py`
- Wait a few seconds and refresh

### CORS errors
- The dashboard uses `fetch()` to call the API
- Make sure CORS is enabled in the FastAPI app (it should be by default)

## 📱 Features

- **Real-time updates**: Auto-refreshes every 30 seconds
- **Responsive design**: Works on desktop and tablet
- **Color-coded indicators**: Easy to understand risk levels
- **Natural language explanations**: AI-generated summaries
- **Statistics dashboard**: Quick overview of system status

## 🎨 Customization

Edit `dashboard.html` to:
- Change colors and styling
- Add more visualizations
- Modify refresh interval
- Add new data sections

Enjoy your Smart City Dashboard! 🏙️

