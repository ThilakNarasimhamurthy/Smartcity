# Quick Testing Guide - Step by Step

## 🚨 CRITICAL: Fix MongoDB Connection First

### The Error You're Seeing:
```
SSL handshake failed... Your IP address may not be whitelisted in MongoDB Atlas
```

### Fix This First (2 minutes):

1. **Open MongoDB Atlas:**
   - Go to: https://cloud.mongodb.com
   - Login with your account

2. **Whitelist Your IP:**
   - Click on your cluster: `smartcity`
   - Click **"Network Access"** (left sidebar, under Security)
   - Click **"Add IP Address"** button
   - Click **"Allow Access from Anywhere"** (adds `0.0.0.0/0`)
   - OR click **"Add Current IP Address"** to add just your IP
   - Click **"Confirm"**
   - **Wait 1-2 minutes** for changes to take effect

3. **Verify Connection:**
   ```bash
   cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
   python3 -c "import asyncio; from app.database import connect_to_mongo, close_mongo_connection; asyncio.run(connect_to_mongo()); asyncio.run(close_mongo_connection()); print('✅ Connected!')"
   ```

**✅ Checkpoint:** Should print "✅ Connected!" without errors

---

## 📋 Complete Testing Checklist

### ✅ CHECKPOINT 1: Dependencies Installed
```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
pip list | grep -E "fastapi|motor|pandas|scikit-learn"
```
**Status:** ✅ Already done!

---

### ✅ CHECKPOINT 2: MongoDB Connection
```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
python3 -c "import asyncio; from app.database import connect_to_mongo, close_mongo_connection; asyncio.run(connect_to_mongo()); asyncio.run(close_mongo_connection()); print('✅ Connected!')"
```
**Expected:** `✅ Connected!` (no errors)

**If fails:** Whitelist IP in MongoDB Atlas (see above)

---

### ✅ CHECKPOINT 3: Run Full Simulation
```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
python3 scripts/run_simulation.py
```

**Expected Output:**
```
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
```

**Checkpoints:**
- [ ] All 4 sources show records > 0
- [ ] Segments created > 0
- [ ] Zones created > 0
- [ ] No critical errors

---

### ✅ CHECKPOINT 4: Start API Server
```bash
# In a NEW terminal window
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
python3 -m app.main
```

**Expected:**
```
INFO: Connected to MongoDB: smartcity_dashboard
INFO: Scheduler started
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Checkpoint:** Server starts, no errors

---

### ✅ CHECKPOINT 5: Test API Endpoints

**Open a THIRD terminal window:**

```bash
# Test 1: Root endpoint
curl http://localhost:8000/

# Test 2: Segments (current traffic)
curl http://localhost:8000/api/segments/current | python3 -m json.tool

# Test 3: Zones (aggregated)
curl http://localhost:8000/api/zones/current | python3 -m json.tool

# Test 4: Predictions
curl http://localhost:8000/api/predictions | python3 -m json.tool

# Test 5: Explanation (natural language)
curl http://localhost:8000/api/explain/hotspots | python3 -m json.tool

# Test 6: Health/Validation
curl http://localhost:8000/api/health/validation | python3 -m json.tool
```

**Checkpoints:**
- [ ] All endpoints return 200 OK
- [ ] Segments endpoint has "segments" array
- [ ] Zones endpoint has "zones" array
- [ ] Explanation endpoint has readable "explanation" text
- [ ] All responses are valid JSON

---

### ✅ CHECKPOINT 6: Train ML Models
```bash
# Stop API server first (Ctrl+C in that terminal)
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
python3 scripts/train_models.py
```

**Expected:**
```
✓ Global model trained:
  - MAE: X.XX mph
  - RMSE: X.XX mph
  - R²: 0.XXX
  - Samples: XXX
```

**Checkpoints:**
- [ ] Training completes without errors
- [ ] MAE < 15 mph (reasonable)
- [ ] Model file created in `models/congestion_models/`

---

### ✅ CHECKPOINT 7: Test Predictions with Models
```bash
python3 scripts/test_prediction_cycle.py
```

**Expected:**
```
Step 5: Generating predictions...
✓ Generated X predictions

Step 6: Sample predictions:
  1. Segment: xxx
     Predicted Speed: XX.X mph
     Risk Level: GREEN/YELLOW/RED
```

**Checkpoints:**
- [ ] Predictions generated > 0
- [ ] Each prediction has risk_level, reasoning_tags

---

## 🎯 Success Criteria

**System is working correctly if:**

1. ✅ MongoDB connection successful
2. ✅ All 4 data sources ingest data
3. ✅ Segments and zones created
4. ✅ API server runs without errors
5. ✅ All 6 API endpoints return valid JSON
6. ✅ Explanation endpoint returns readable text
7. ✅ Models can be trained
8. ✅ Predictions generated with risk levels

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution:** Make sure you're in the `Smartcity` directory:
```bash
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"
```

### Issue: MongoDB SSL handshake failed
**Solution:** Whitelist your IP in MongoDB Atlas (see top of this guide)

### Issue: No data ingested
**Check:**
- `USE_MOCKS=true` in `.env` (for mock mode)
- MongoDB connection works
- Check logs for specific errors

### Issue: API endpoints return empty
**Check:**
- Run simulation first to create data
- Check MongoDB has documents
- Ensure cleaning agent has run

---

## 📝 Quick Command Reference

```bash
# Always start from this directory:
cd "/Users/karandavda/Desktop/Smart City Dashboard/Smartcity"

# Test MongoDB connection:
python3 -c "import asyncio; from app.database import connect_to_mongo, close_mongo_connection; asyncio.run(connect_to_mongo()); asyncio.run(close_mongo_connection()); print('✅ Connected!')"

# Run full simulation:
python3 scripts/run_simulation.py

# Start API server:
python3 -m app.main

# Train models:
python3 scripts/train_models.py

# Test predictions:
python3 scripts/test_prediction_cycle.py
```

---

**Next Step:** Whitelist your IP in MongoDB Atlas, then start from Checkpoint 2!

