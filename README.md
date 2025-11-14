# Smart City Dashboard - NYC DOT

A comprehensive Smart City Dashboard prototype for NYC DOT that integrates real-time traffic, transit, and air quality data with predictive congestion insights.

## 🎯 Overview

This system addresses NYC DOT's key challenges:
- **Reduce congestion** and improve commute times
- **Coordinate traffic** with transit and waste routes
- **Monitor environmental impact** of traffic

## 🏗️ Architecture

The system consists of three core agents:

1. **Agent 1: Data Ingestion** - Pulls live feeds from multiple sources
2. **Agent 2: Cleaning + Correlation** - Fuses and cleans data into usable structures
3. **Agent 3: Predictive Congestion** - Predicts congestion 15-30 minutes ahead

Plus a validation system for monitoring prediction accuracy and sensor reliability.

## 📊 Data Sources

- **Traffic:** 511NY REST API, NYC DOT OpenData
- **Transit:** MTA GTFS-Realtime Feeds
- **Environment:** NYC DOHMH Real-time PM2.5, AirNow API (fallback)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- MongoDB (local or cloud)
- API keys for 511NY and MTA (optional - uses mock data without keys)

### Installation

1. **Clone and navigate to project:**
```bash
cd Smartcity
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your MongoDB URI and API keys
```

4. **Run simulation test:**
```bash
python scripts/run_simulation.py
```

5. **Start the API server:**
```bash
python -m app.main
# Or: uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Segments
- `GET /api/segments/current` - Get current segment states
- `GET /api/segments/{segment_id}` - Get specific segment

### Zones
- `GET /api/zones/current` - Get current zone states
- `GET /api/zones/{zone_id}` - Get specific zone

### Predictions
- `GET /api/predictions` - Get congestion predictions
- `GET /api/predictions/{segment_id}` - Get predictions for segment

### Health & Validation
- `GET /api/health` - Health check
- `GET /api/health/validation` - Validation metrics

### Explanation
- `GET /api/explain/hotspots?limit=5` - Natural language explanation of current hotspots

## 📁 Project Structure

```
smartcity_dashboard/
├── app/
│   ├── agents/          # Three core agents
│   ├── clients/         # API clients (with mock fallbacks)
│   ├── models/          # Pydantic schemas & MongoDB models
│   ├── services/        # Imputation, correlation, validation
│   ├── api/             # FastAPI routes
│   ├── config.py        # Configuration
│   ├── database.py      # MongoDB connection
│   └── main.py          # FastAPI app
├── scripts/
│   └── run_simulation.py # Full cycle test script
├── tests/               # Test suite (to be added)
└── requirements.txt
```

## 🔧 Configuration

### Environment Setup

1. **Copy environment template:**
```bash
cp .env.example .env
```

2. **Edit `.env` file:**

**Core Settings:**
```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=smartcity_dashboard
ENVIRONMENT=development
USE_MOCKS=true  # Set to false for real APIs
```

**NYC OpenData (No API keys needed - Public datasets):**
```env
# These are already configured with public endpoints
# No changes needed unless you want different datasets
```

**MTA API (Optional - for real-time transit):**
```env
MTA_API_KEY=your_mta_key_here  # Optional - we have bus breakdowns data
```

**ML Model Configuration:**
```env
ML_MODEL_TYPE=gradient_boosting  # or random_forest
ML_MODEL_PATH=models/congestion_models
ML_TRAINING_HISTORY_DAYS=7
```

**Scheduling:**
```env
INGESTION_INTERVAL_TRAFFIC=30
INGESTION_INTERVAL_TRANSIT=60
INGESTION_INTERVAL_AIR_QUALITY=900
```

### Mock vs Real Mode

**Mock Mode (Default - `USE_MOCKS=true`):**
- Uses generated mock data
- No API keys needed
- Perfect for development/testing
- All features work

**Real Mode (`USE_MOCKS=false`):**
- Uses real NYC OpenData endpoints
- No API keys needed for most sources
- MTA API key optional (we have bus breakdowns data)
- Requires some historical data for ML training

## 📊 MongoDB Collections

### Raw Data
- `raw_traffic_511` - 511NY traffic data
- `raw_traffic_dot` - NYC DOT traffic data
- `raw_transit_mta` - MTA transit data
- `raw_air_quality` - Air quality readings

### Processed Data
- `segments_state` - Cleaned, fused segment states (5-min buckets)
- `zones_state` - Aggregated zone states

### Predictions
- `predicted_segments` - Future congestion predictions

### Validation
- `validation_metrics` - Prediction accuracy and sensor reliability

## 🔄 Data Flow

1. **Ingestion** (every 30s-15min) → Stores raw data
2. **Cleaning** (every 2min) → Creates segments_state and zones_state
3. **Prediction** (every 5min) → Generates future predictions
4. **Validation** (on-demand) → Checks accuracy and reliability

## 🧪 Testing

### Mock Mode Testing (Default)

Run the full simulation cycle with mock data:

```bash
python scripts/run_simulation.py
```

This will:
1. Ingest mock data from all sources
2. Clean and fuse the data
3. Generate predictions
4. Run validation checks

### Live Data Testing

**Step 1: Test Live Ingestion**

Test real API endpoints (set `USE_MOCKS=false` in `.env` first):

```bash
python scripts/test_live_ingestion.py
```

This will:
- Fetch data from real NYC OpenData endpoints
- Store in MongoDB
- Show ingestion statistics
- Verify data storage

**Step 2: Test Prediction Cycle**

After collecting some data, test the complete prediction pipeline:

```bash
python scripts/test_prediction_cycle.py
```

This will:
- Run cleaning/correlation agent
- Train ML models (if not already trained)
- Generate predictions
- Show sample predictions

**Step 3: Train Models**

Train ML models from historical data:

```bash
python scripts/train_models.py
```

This will:
- Load historical data from MongoDB
- Train gradient boosting or random forest model
- Save model to `models/congestion_models/`
- Show training metrics (MAE, RMSE, R²)

## 📋 API Requirements

See `API_REQUIREMENTS.md` for detailed API information.

### Quick Summary:
- ✅ **NYC DOT OpenData** - Public (no key needed)
- ✅ **NYC Air Quality (DOHMH)** - Public (no key needed)  
- ⚠️ **511NY API Key** - **NEED TO OBTAIN**
- ⚠️ **MTA API Key** - **NEED TO OBTAIN**
- ⚠️ **AirNow API Key** - Optional fallback

**All clients work in mock mode for development without API keys.**

## 📝 TODO / Next Steps

- [x] Replace mock API clients with real implementations
- [x] Implement ML models for prediction (gradient boosting)
- [x] Add explanation agent (template-based, no Hugging Face)
- [x] Add test scripts for live data verification
- [ ] Add proper zone boundary definitions
- [ ] Add frontend dashboard (React + Mapbox)
- [ ] Add comprehensive test suite
- [ ] Add Docker deployment configuration

## 📄 License

MIT License

## 👥 Contributors

Built for NYC DOT Smart City Hackathon

---

**Status:** ✅ Core system implemented - API clients ready for real data
