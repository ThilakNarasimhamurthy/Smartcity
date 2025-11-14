# Data Sources Configuration Guide

## 📍 Where URLs Are Configured

All data source URLs are configured in **`app/config.py`** (lines 17-42)

---

## 🚦 Traffic Data Sources

### 1. **511NY Traffic API** (Optional - Currently using mocks)
- **Config File**: `app/config.py` (lines 18-19)
- **URL Variable**: `ny511_base_url`
- **Default Value**: `https://api.511.org/traffic/v2`
- **Used By**: `app/clients/traffic_511.py`
- **What It Pulls**: Traffic speeds, incidents, roadwork
- **Status**: ⚠️ Requires API key (currently using mocks)

---

### 2. **NYC DOT Traffic Speeds** ✅ PRIMARY SOURCE
- **Config File**: `app/config.py` (line 22)
- **URL Variable**: `nyc_dot_traffic_speeds_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/i4gi-tjb9.json`
- **Used By**: `app/clients/traffic_dot.py` (line 18)
- **What It Pulls**: Real-time traffic speeds by segment
- **Public Website**: https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9
- **Status**: ✅ **PUBLIC - No API key needed**

---

### 3. **NYC DOT Traffic Volume**
- **Config File**: `app/config.py` (line 23)
- **URL Variable**: `nyc_dot_traffic_volume_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/7ym2-wayt.json`
- **Used By**: `app/clients/traffic_dot.py` (line 19)
- **What It Pulls**: Automated traffic volume counts
- **Public Website**: https://data.cityofnewyork.us/Transportation/Automated-Traffic-Volume-Counts/7ym2-wayt
- **Status**: ✅ **PUBLIC - No API key needed**

---

### 4. **NYC DOT Collisions** (For Incidents)
- **Config File**: `app/config.py` (line 24)
- **URL Variable**: `nyc_dot_collisions_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/h9gi-nx95.json`
- **Used By**: `app/clients/traffic_dot.py` (line 20)
- **What It Pulls**: Motor vehicle collision data (used for incident detection)
- **Public Website**: https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
- **Status**: ✅ **PUBLIC - No API key needed**

---

### 5. **NYC DOT Traffic Calming**
- **Config File**: `app/config.py` (line 25)
- **URL Variable**: `nyc_dot_traffic_calming_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/hz4p-9f7s.json`
- **Used By**: `app/clients/traffic_dot.py` (not actively used yet)
- **What It Pulls**: Turn-traffic-calming data
- **Public Website**: https://data.cityofnewyork.us/Transportation/VZV_Turn-Traffic-Calming/hz4p-9f7s
- **Status**: ✅ **PUBLIC - No API key needed**

---

## 🚌 Transit Data Sources

### 6. **MTA GTFS-Realtime - Vehicle Positions**
- **Config File**: `app/config.py` (line 29)
- **URL Variable**: `mta_gtfs_vehicle_url`
- **Default Value**: `https://gtfsrt.prod.obanyc.com/vehiclePositions`
- **Used By**: `app/clients/transit_mta.py` (line 27)
- **What It Pulls**: Real-time bus/subway vehicle positions
- **Status**: ⚠️ **Requires MTA API key**

---

### 7. **MTA GTFS-Realtime - Trip Updates**
- **Config File**: `app/config.py` (line 30)
- **URL Variable**: `mta_gtfs_tripupdates_url`
- **Default Value**: `https://gtfsrt.prod.obanyc.com/tripUpdates`
- **Used By**: `app/clients/transit_mta.py` (line 28)
- **What It Pulls**: Real-time trip delays and updates
- **Status**: ⚠️ **Requires MTA API key**

---

### 8. **MTA GTFS-Realtime - Alerts**
- **Config File**: `app/config.py` (line 31)
- **URL Variable**: `mta_gtfs_alerts_url`
- **Default Value**: `https://gtfsrt.prod.obanyc.com/alerts`
- **Used By**: `app/clients/transit_mta.py` (line 29)
- **What It Pulls**: Service alerts and disruptions
- **Status**: ⚠️ **Requires MTA API key**

---

### 9. **NYC Bus Breakdowns/Delays** ✅ FALLBACK
- **Config File**: `app/config.py` (line 34)
- **URL Variable**: `nyc_bus_breakdowns_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/ez4e-fazm.json`
- **Used By**: `app/clients/transit_mta.py` (can be used as supplement)
- **What It Pulls**: Bus breakdown and delay incidents
- **Public Website**: https://data.cityofnewyork.us/Transportation/Bus-Breakdown-and-Delays/ez4e-fazm
- **Status**: ✅ **PUBLIC - No API key needed**

---

## 🌍 Air Quality Data Sources

### 10. **NYC Air Quality (NYCCAS)** ✅ PRIMARY
- **Config File**: `app/config.py` (line 37)
- **URL Variable**: `nyc_air_quality_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/q68s-8qxv.json`
- **Used By**: `app/clients/air_quality.py` (line 19)
- **What It Pulls**: PM2.5 and air pollution readings
- **Public Website**: https://data.cityofnewyork.us/Environment/NYCCAS-Air-Pollution-Rasters/q68s-8qxv
- **Status**: ✅ **PUBLIC - No API key needed**

---

### 11. **AirNow API** (Fallback)
- **Config File**: `app/config.py` (line 39)
- **URL Variable**: `airnow_base_url`
- **Default Value**: `https://www.airnowapi.org/aq/observation/zipCode/current`
- **Used By**: `app/clients/air_quality.py` (line 20)
- **What It Pulls**: EPA air quality data (fallback if NYC data fails)
- **Status**: ⚠️ **Requires API key** (optional fallback)

---

## 📋 Additional Data Sources

### 12. **NYC 311 Service Requests**
- **Config File**: `app/config.py` (line 42)
- **URL Variable**: `nyc_311_requests_url`
- **Default Value**: `https://data.cityofnewyork.us/resource/erm2-nwe9.json`
- **Used By**: Not actively used yet (available for future use)
- **What It Pulls**: Service requests (can include traffic-related issues)
- **Public Website**: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
- **Status**: ✅ **PUBLIC - No API key needed**

---

## 🔧 How to Change URLs

### Option 1: Edit Config File Directly
Edit `app/config.py` and change the default values:
```python
nyc_dot_traffic_speeds_url: str = "YOUR_NEW_URL_HERE"
```

### Option 2: Use Environment Variables (Recommended)
Add to your `.env` file:
```bash
NYC_DOT_TRAFFIC_SPEEDS_URL=https://data.cityofnewyork.us/resource/i4gi-tjb9.json
NYC_DOT_TRAFFIC_VOLUME_URL=https://data.cityofnewyork.us/resource/7ym2-wayt.json
# etc...
```

Environment variables override the defaults in `config.py`.

---

## 📊 Data Flow Summary

```
app/config.py (URLs defined)
    ↓
app/clients/traffic_dot.py (uses URLs)
    ↓
app/agents/agent1_ingestion.py (calls clients)
    ↓
MongoDB (stores raw data)
    ↓
app/agents/agent2_cleaning.py (processes)
    ↓
Dashboard (displays)
```

---

## 🎯 Quick Reference: Which URL Pulls What

| **Dashboard Shows** | **Pulled From** | **URL Config** | **File** |
|-------------------|-----------------|----------------|---------|
| Current Traffic Conditions | NYC DOT Traffic Speeds | `nyc_dot_traffic_speeds_url` | `app/config.py:22` |
| Traffic Volume | NYC DOT Traffic Volume | `nyc_dot_traffic_volume_url` | `app/config.py:23` |
| Active Incidents | NYC DOT Collisions | `nyc_dot_collisions_url` | `app/config.py:24` |
| Transit Delays | MTA GTFS-RT / Bus Breakdowns | `mta_gtfs_*_url` / `nyc_bus_breakdowns_url` | `app/config.py:29-34` |
| Air Quality | NYC Air Quality | `nyc_air_quality_url` | `app/config.py:37` |

---

## 🔍 How to Verify URLs Are Working

1. **Check Config**: `app/config.py` lines 17-42
2. **Check Client Usage**: Each client file shows which URLs it uses
3. **Test Directly**: Open URLs in browser to see raw data
4. **Check Logs**: When running, logs show which URLs are being called

---

## 📝 Notes

- All NYC OpenData URLs are **public** (no API keys needed)
- URLs can be overridden via `.env` file
- MTA URLs require API keys (currently using mocks)
- 511NY URL requires API key (currently using mocks)

