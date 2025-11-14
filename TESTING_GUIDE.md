# Complete Testing Guide with Checkpoints

## ✅ CHECKPOINT 0: Prerequisites Setup

### Step 0.1: Verify Dependencies Installed
```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
pip list | grep -E "fastapi|motor|pandas|scikit-learn"
```
**✅ Checkpoint 0.1:** All packages should be listed (already done!)

---

### Step 0.2: MongoDB Setup

**Option A: Local MongoDB**
```bash
# Check if MongoDB is installed
brew services list | grep mongodb
# OR
which mongod

# If not installed, install it:
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Option B: MongoDB Atlas (Cloud - Recommended for Testing)**
1. Go to https://www.mongodb.com/cloud/atlas
2. Create free account
3. Create free cluster
4. Get connection string (looks like: `mongodb+srv://user:pass@cluster.mongodb.net/`)
5. Update `.env`:
   ```env
   MONGODB_URI=mongodb+srv://your_connection_string
   ```

**✅ Checkpoint 0.2:** MongoDB connection works
```bash
# Test connection
python3 -c "from app.database import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"
```
Should show: `Connected to MongoDB: smartcity_dashboard`

---

## ✅ CHECKPOINT 1: Environment Configuration

### Step 1.1: Verify .env File
```bash
cat .env
```

**Expected:**
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=smartcity_dashboard
ENVIRONMENT=development
USE_MOCKS=true
LOG_LEVEL=INFO
```

**✅ Checkpoint 1.1:** `.env` file exists and has correct values

---

## ✅ CHECKPOINT 2: Full Simulation Test (Mock Mode)

### Step 2.1: Run Simulation
```bash
python3 scripts/run_simulation.py
```

**Expected Output:**
```
================================================================================
SMART CITY DASHBOARD - SIMULATION CYCLE
================================================================================
Step 1: Connecting to MongoDB...
✓ Connected to MongoDB

Step 2: Running Agent 1 - Data Ingestion...
✓ Ingestion complete:
  - 511NY Traffic: 5 records
  - NYC DOT Traffic: 3 records
  - MTA Transit: 15 records
  - Air Quality: 5 records

Step 3: Running Agent 2 - Cleaning + Correlation...
✓ Processing complete:
  - Segments created: X
  - Zones created: Y

Step 4: Running Agent 3 - Predictive Congestion...
✓ Predictions generated: Z

Step 5: Running Validation...
✓ Validation complete
```

**✅ Checkpoint 2.1: Ingestion**
- [ ] All 4 sources show records > 0
- [ ] No critical errors

**✅ Checkpoint 2.2: Cleaning**
- [ ] Segments created > 0
- [ ] Zones created > 0

**✅ Checkpoint 2.3: Prediction**
- [ ] Predictions generated (may be 0 if no models trained - that's OK)

**✅ Checkpoint 2.4: Validation**
- [ ] Validation completes without errors

---

## ✅ CHECKPOINT 3: MongoDB Data Verification

### Step 3.1: Check Raw Data Collections
```bash
# Using mongosh (MongoDB shell)
mongosh smartcity_dashboard

# In mongosh, run:
db.raw_traffic_511.countDocuments({})
db.raw_traffic_dot.countDocuments({})
db.raw_transit_mta.countDocuments({})
db.raw_air_quality.countDocuments({})
```

**✅ Checkpoint 3.1:** All collections have documents > 0

### Step 3.2: Check Processed Data
```bash
# In mongosh:
db.segments_state.countDocuments({})
db.zones_state.countDocuments({})
db.segments_state.findOne()
db.zones_state.findOne()
```

**✅ Checkpoint 3.2:**
- [ ] `segments_state` has documents
- [ ] `zones_state` has documents
- [ ] Documents have: speed_mph, congestion_index, timestamp_bucket

---

## ✅ CHECKPOINT 4: API Server Test

### Step 4.1: Start API Server
```bash
# In a NEW terminal window
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
python3 -m app.main
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Connected to MongoDB: smartcity_dashboard
INFO:     Scheduler started
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**✅ Checkpoint 4.1:** Server starts without errors

### Step 4.2: Test Root Endpoint
```bash
# In another terminal
curl http://localhost:8000/
```

**Expected:** JSON with service info

**✅ Checkpoint 4.2:** Returns 200 OK with endpoints list

### Step 4.3: Test Segments Endpoint
```bash
curl http://localhost:8000/api/segments/current | python3 -m json.tool
```

**Expected:** JSON with segments array

**✅ Checkpoint 4.3:**
- [ ] Returns 200 OK
- [ ] Has "segments" array
- [ ] Each segment has: segment_id, speed_mph, congestion_index

### Step 4.4: Test Zones Endpoint
```bash
curl http://localhost:8000/api/zones/current | python3 -m json.tool
```

**✅ Checkpoint 4.4:**
- [ ] Returns 200 OK
- [ ] Has "zones" array
- [ ] Each zone has: zone_id, avg_speed_mph, traffic_pollution_risk

### Step 4.5: Test Predictions Endpoint
```bash
curl http://localhost:8000/api/predictions | python3 -m json.tool
```

**✅ Checkpoint 4.5:**
- [ ] Returns 200 OK
- [ ] Has "predictions" array (may be empty if no models trained)

### Step 4.6: Test Explanation Endpoint
```bash
curl http://localhost:8000/api/explain/hotspots | python3 -m json.tool
```

**✅ Checkpoint 4.6:**
- [ ] Returns 200 OK
- [ ] Has "explanation" field with readable text
- [ ] Explanation mentions hotspots, predictions, recommendations

### Step 4.7: Test Health/Validation
```bash
curl http://localhost:8000/api/health/validation | python3 -m json.tool
```

**✅ Checkpoint 4.7:**
- [ ] Returns 200 OK
- [ ] Has validation metrics

---

## ✅ CHECKPOINT 5: ML Model Training

### Step 5.1: Train Models
```bash
# Stop API server first (Ctrl+C), then:
python3 scripts/train_models.py
```

**Expected Output:**
```
TRAINING CONGESTION PREDICTION MODELS
Training global model (all segments)...
✓ Global model trained:
  - MAE: X.XX mph
  - RMSE: X.XX mph
  - R²: 0.XXX
  - Samples: XXX
```

**✅ Checkpoint 5.1:**
- [ ] Training completes without errors
- [ ] MAE < 15 mph (reasonable)
- [ ] R² > 0.2 (some predictive power)
- [ ] Model file created in `models/congestion_models/`

### Step 5.2: Verify Model File
```bash
ls -la models/congestion_models/
```

**✅ Checkpoint 5.2:** Model file exists (e.g., `gradient_boosting_global.joblib`)

---

## ✅ CHECKPOINT 6: Prediction with Trained Models

### Step 6.1: Test Prediction Cycle
```bash
python3 scripts/test_prediction_cycle.py
```

**Expected Output:**
```
Step 5: Generating predictions...
✓ Generated X predictions

Step 6: Sample predictions:
  1. Segment: xxx
     Predicted Speed: XX.X mph
     Risk Level: GREEN/YELLOW/RED
```

**✅ Checkpoint 6.1:**
- [ ] Predictions generated > 0
- [ ] Each prediction has: speed, congestion, risk_level, reasoning_tags

---

## ✅ CHECKPOINT 7: Real Data Test (Optional)

### Step 7.1: Switch to Real Mode
```bash
# Edit .env: Change USE_MOCKS=false
# Then test:
python3 scripts/test_live_ingestion.py
```

**✅ Checkpoint 7.1:**
- [ ] Fetches data from NYC OpenData
- [ ] Records stored in MongoDB
- [ ] No critical errors

---

## 🎯 Final Verification Checklist

### System Health
- [ ] MongoDB connection works
- [ ] All 4 data sources ingest data
- [ ] Cleaning agent creates segments/zones
- [ ] API server starts without errors
- [ ] All API endpoints return 200 OK

### Data Quality
- [ ] Raw data has timestamps
- [ ] Segments have speed and congestion_index
- [ ] Zones have aggregated data
- [ ] Predictions have risk_level

### ML Models
- [ ] Models train successfully
- [ ] Training metrics reasonable
- [ ] Predictions use trained models

### API Functionality
- [ ] All endpoints accessible
- [ ] Data returned in correct format
- [ ] Explanation endpoint returns readable text

---

## 🚨 Common Issues & Solutions

### Issue: MongoDB Connection Refused
**Solution:**
```bash
# Start MongoDB locally
brew services start mongodb-community

# OR use MongoDB Atlas (cloud) - update MONGODB_URI in .env
```

### Issue: No Data Ingested
**Check:**
- `USE_MOCKS=true` in .env (for mock mode)
- MongoDB is running
- Check logs for specific errors

### Issue: Model Training Fails
**Check:**
- At least 50 segments in `segments_state`
- Run ingestion and cleaning first
- Check MongoDB has historical data

### Issue: API Endpoints Return Empty
**Check:**
- Data exists in MongoDB
- Timestamps are recent
- Cleaning agent has run

---

## 📊 Success Criteria

**System is working correctly if:**
1. ✅ All 4 data sources ingest data
2. ✅ Segments and zones are created
3. ✅ API server runs without errors
4. ✅ All endpoints return valid JSON
5. ✅ Models can be trained
6. ✅ Predictions are generated
7. ✅ Explanation endpoint returns readable text

---

**Ready to test!** Start from Checkpoint 0 and work through each step.

