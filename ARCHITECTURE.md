# Smart City Dashboard - System Architecture

## 🎯 Understanding & Requirements

### Problem Statement
NYC DOT needs a unified dashboard to:
- Reduce congestion and improve commute times
- Coordinate traffic with transit and waste routes
- Monitor environmental impact of traffic

### Key Pain Points
- Incomplete real-time data
- No predictive congestion insights
- Siloed data across departments
- Unclear link between traffic and pollution

---

## 🏗️ System Architecture

### Three-Agent System + Validation

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCES                              │
├─────────────────────────────────────────────────────────────┤
│  511NY API  │  NYC DOT OpenData  │  MTA GTFS-RT  │  DOHMH   │
└──────┬──────┴──────────┬──────────┴──────┬────────┴────┬────┘
       │                 │                  │             │
       └─────────────────┼──────────────────┼─────────────┘
                         │                  │
              ┌──────────▼──────────────────▼──────────┐
              │   AGENT 1: DATA INGESTION             │
              │   - Polls APIs (30s-15min)            │
              │   - Stores RAW data in MongoDB        │
              └──────────┬────────────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │   AGENT 2: CLEANING + CORRELATION    │
              │   - Cleans invalid values            │
              │   - Imputes gaps                     │
              │   - Fuses data → segments_state      │
              │   - Aggregates → zones_state         │
              └──────────┬────────────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │   AGENT 3: PREDICTIVE CONGESTION      │
              │   - Predicts 15-30 min ahead          │
              │   - Stores in predicted_segments     │
              └──────────┬────────────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │   VALIDATION SCRIPT                   │
              │   - MAE tracking                     │
              │   - Sensor reliability checks         │
              └───────────────────────────────────────┘
                         │
              ┌──────────▼────────────────────────────┐
              │   FASTAPI REST ENDPOINTS              │
              │   - /api/segments/current            │
              │   - /api/zones/current               │
              │   - /api/predictions                 │
              │   - /api/health/validation           │
              └───────────────────────────────────────┘
```

---

## 📊 MongoDB Schema Design

### RAW Collections (Agent 1 Output)

#### `raw_traffic_511`
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "source": "511ny",
  "segment_id": String,
  "segment_name": String,
  "speed_mph": Number,
  "incident_type": String | null,
  "incident_description": String | null,
  "roadwork_flag": Boolean,
  "camera_id": String | null,
  "latitude": Number,
  "longitude": Number,
  "raw_data": Object  // Full API response
}
```

#### `raw_traffic_dot`
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "source": "nyc_dot_opendata",
  "segment_id": String,
  "speed_mph": Number,
  "latitude": Number,
  "longitude": Number,
  "raw_data": Object
}
```

#### `raw_transit_mta`
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "source": "mta_gtfs_rt",
  "trip_id": String,
  "route_id": String,
  "vehicle_id": String,
  "stop_id": String,
  "delay_seconds": Number,
  "arrival_time": ISODate,
  "departure_time": ISODate,
  "latitude": Number,
  "longitude": Number,
  "raw_data": Object
}
```

#### `raw_air_quality`
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "source": "dohmn" | "airnow",
  "sensor_id": String,
  "pm25": Number,
  "pm10": Number | null,
  "aqi": Number | null,
  "latitude": Number,
  "longitude": Number,
  "raw_data": Object
}
```

---

### PROCESSED Collections (Agent 2 Output)

#### `segments_state`
```json
{
  "_id": ObjectId,
  "segment_id": String,
  "timestamp_bucket": ISODate,  // 5-min bucket
  "speed_mph": Number,
  "congestion_index": Number,  // 0-1 normalized
  "incident_flag": Boolean,
  "transit_delay_flag": Boolean,
  "pm25_nearby": Number | null,
  "data_confidence_score": Number,  // 0-1
  "latitude": Number,
  "longitude": Number,
  "segment_name": String,
  "sources": [String]  // ["511ny", "nyc_dot"]
}
```

**Indexes:**
- `{segment_id: 1, timestamp_bucket: -1}` (compound)
- `{timestamp_bucket: -1}`

#### `zones_state`
```json
{
  "_id": ObjectId,
  "zone_id": String,  // e.g., "manhattan_cbd", "brooklyn_downtown"
  "timestamp_bucket": ISODate,  // 5-min bucket
  "avg_speed_mph": Number,
  "avg_congestion_index": Number,
  "avg_pm25": Number | null,
  "traffic_pollution_risk": String,  // "Low" | "Medium" | "High"
  "segment_count": Number,
  "incident_count": Number,
  "transit_delay_count": Number,
  "bounding_box": {
    "min_lat": Number,
    "max_lat": Number,
    "min_lon": Number,
    "max_lon": Number
  }
}
```

**Indexes:**
- `{zone_id: 1, timestamp_bucket: -1}` (compound)
- `{timestamp_bucket: -1}`

---

### PREDICTIONS Collection (Agent 3 Output)

#### `predicted_segments`
```json
{
  "_id": ObjectId,
  "segment_id": String,
  "forecast_timestamp": ISODate,  // When prediction is made
  "target_timestamp": ISODate,  // 15 or 30 min ahead
  "forecast_window_minutes": Number,  // 15 or 30
  "predicted_speed_mph": Number,
  "predicted_congestion_index": Number,
  "risk_level": String,  // "green" | "yellow" | "red"
  "reasoning_tags": [String],  // ["time_of_day", "transit_delay", "historical_pattern"]
  "confidence_score": Number,  // 0-1
  "model_type": String  // "moving_avg" | "exponential_smoothing" | "gradient_boosting"
}
```

**Indexes:**
- `{segment_id: 1, target_timestamp: -1}` (compound)
- `{target_timestamp: 1}`

---

### VALIDATION Collection

#### `validation_metrics`
```json
{
  "_id": ObjectId,
  "timestamp": ISODate,
  "metric_type": String,  // "mae_speed" | "sensor_reliability" | "prediction_accuracy"
  "segment_id": String | null,
  "value": Number,
  "threshold": Number,
  "status": String,  // "pass" | "warning" | "fail"
  "details": Object
}
```

---

## 🔄 Data Flow

1. **Ingestion (Agent 1)**
   - Polls APIs every 30s-15min
   - Stores raw data with timestamps
   - No processing, just storage

2. **Cleaning & Fusion (Agent 2)**
   - Reads raw collections
   - Cleans invalid values
   - Imputes missing data
   - Correlates traffic + transit + air quality
   - Creates 5-min buckets
   - Writes to `segments_state` and `zones_state`

3. **Prediction (Agent 3)**
   - Reads `segments_state` history
   - Applies prediction model
   - Writes to `predicted_segments`

4. **Validation**
   - Compares predictions vs actuals
   - Checks sensor reliability
   - Updates `validation_metrics`

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+
- **API Framework:** FastAPI
- **Database:** MongoDB (Motor for async)
- **Scheduling:** APScheduler
- **ML/Stats:** scikit-learn, statsmodels
- **HTTP Client:** httpx (async)

---

## 📁 Proposed Project Structure

```
smartcity_dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Config & env vars
│   ├── database.py             # MongoDB connection
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent1_ingestion.py
│   │   ├── agent2_cleaning.py
│   │   └── agent3_prediction.py
│   │
│   ├── clients/
│   │   ├── __init__.py
│   │   ├── traffic_511.py
│   │   ├── traffic_dot.py
│   │   ├── transit_mta.py
│   │   └── air_quality.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   └── mongodb_models.py    # Document structures
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── correlation.py      # Traffic-pollution correlation
│   │   ├── imputation.py       # Gap filling logic
│   │   └── validation.py       # Validation logic
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── segments.py
│       │   ├── zones.py
│       │   ├── predictions.py
│       │   └── health.py
│       └── dependencies.py
│
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_clients.py
│   └── test_api.py
│
├── scripts/
│   ├── run_simulation.py       # Full cycle test
│   └── seed_test_data.py
│
├── .env.example
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

---

## 🔑 Environment Variables

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=smartcity_dashboard

# API Keys
API_KEY_511NY=your_511ny_key
API_KEY_MTA=your_mta_key
AIRNOW_API_KEY=your_airnow_key  # Optional

# Scheduling
INGESTION_INTERVAL_TRAFFIC=30  # seconds
INGESTION_INTERVAL_TRANSIT=60  # seconds
INGESTION_INTERVAL_AIR_QUALITY=900  # 15 minutes

# Prediction
PREDICTION_WINDOW_15MIN=true
PREDICTION_WINDOW_30MIN=true
```

---

## ✅ Implementation Plan

1. ✅ Scaffold project structure
2. ✅ Set up MongoDB connection & schemas
3. ✅ Build API clients with mock responses
4. ✅ Implement Agent 1 (Ingestion)
5. ✅ Implement Agent 2 (Cleaning + Correlation)
6. ✅ Implement Agent 3 (Prediction)
7. ✅ Build REST API endpoints
8. ✅ Create validation script
9. ✅ Write test simulation script

---

**Status:** Ready to implement! 🚀

