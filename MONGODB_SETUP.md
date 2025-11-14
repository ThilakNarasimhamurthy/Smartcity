# MongoDB Atlas Setup Guide

## 🔧 Fixing Connection Issues

### Common Issue: SSL Handshake Failed

This usually means your IP address is not whitelisted in MongoDB Atlas.

### Solution Steps:

1. **Go to MongoDB Atlas Dashboard:**
   - Visit: https://cloud.mongodb.com
   - Login to your account

2. **Navigate to Network Access:**
   - Click on your cluster
   - Go to "Network Access" (left sidebar)
   - Or go directly: https://cloud.mongodb.com/v2#/security/network/whitelist

3. **Add IP Address:**
   - Click "Add IP Address"
   - For testing: Add `0.0.0.0/0` (allows all IPs - **use only for testing**)
   - OR add your current IP address
   - Click "Confirm"

4. **Wait 1-2 minutes** for changes to propagate

5. **Test Connection:**
   ```bash
   python3 -c "import asyncio; from app.database import connect_to_mongo, close_mongo_connection; asyncio.run(connect_to_mongo()); asyncio.run(close_mongo_connection()); print('✅ Connected!')"
   ```

### Alternative: Check Connection String

Make sure your connection string in `.env` is:
```
MONGODB_URI=mongodb+srv://nthilak799:DPtE9WlRAMZMWdLZ@smartcity.dc4uwnq.mongodb.net/
```

**Note:** The password might need URL encoding if it has special characters.

### Test Connection String Directly

You can test the connection string with mongosh:
```bash
mongosh "mongodb+srv://nthilak799:DPtE9WlRAMZMWdLZ@smartcity.dc4uwnq.mongodb.net/"
```

If this works, the issue is in the Python code. If it doesn't, the issue is with Atlas configuration.

---

## ✅ Quick Checklist

- [ ] MongoDB Atlas account created
- [ ] Cluster is running (not paused)
- [ ] IP address whitelisted in Network Access
- [ ] Connection string is correct in `.env`
- [ ] Database user has proper permissions

---

## 🚀 Once Connected

After connection works, you can proceed with testing:
```bash
python3 scripts/run_simulation.py
```

