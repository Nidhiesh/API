# ⚡ QUICK START GUIDE

## 1️⃣ Install & Run (60 seconds)

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

Server will be available at: **http://localhost:5000**

---

## 2️⃣ Test in Postman (30 seconds)

### Option A: Import Collection
1. Open Postman
2. Click "Import" → Select `Honeypot_API_Postman_Collection.json`
3. Run any test request

### Option B: Manual Test
1. **Method**: POST
2. **URL**: `http://localhost:5000/api/honeypot/message`
3. **Headers**:
   ```
   Authorization: Bearer TEST_API_KEY
   Content-Type: application/json
   ```
4. **Body**:
   ```json
   {
     "agent": "endpoint-checker",
     "payload": "Your OTP is 1234 verify now http://bank.com"
   }
   ```

---

## 3️⃣ Expected Response

```json
{
  "status": "success",
  "trap": true,
  "scamScore": 75,
  "reply": "We appreciate your patience. Please allow us some time to verify your information.",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

## 🎯 Key Features

| Feature | Status |
|---------|--------|
| Bearer Token Authentication | ✅ |
| Scam Detection (0-100 scoring) | ✅ |
| Automated Human-like Replies | ✅ |
| Request Logging & Persistence | ✅ |
| 3 Core Endpoints | ✅ |
| Error Handling | ✅ |
| Automated Testing Ready | ✅ |

---

## 📍 Endpoints Summary

```
GET  /api/honeypot/health           → Check service (no auth)
POST /api/honeypot/message          → Send message (auth required)
GET  /api/honeypot/logs             → View logs (auth required)
```

---

## 🔒 Authentication

All endpoints except `/health` require:
```
Authorization: Bearer TEST_API_KEY
```

---

## 📊 Scam Score Indicators

Messages are scored 0-100 based on:
- **OTP requests** (25 pts)
- **Bank keywords** (30 pts)
- **Urgency words** (25 pts)
- **Suspicious links** (20 pts)

Score > 40 = Marked as `trap: true`

---

## 📁 Project Files

- **main.py** - Complete API implementation
- **requirements.txt** - Dependencies
- **TESTING_GUIDE.md** - Detailed test cases
- **Honeypot_API_Postman_Collection.json** - Postman tests
- **honeypot_logs.json** - Generated on first request

---

## ❌ Troubleshooting

**Port 5000 already in use?**
```bash
# Change port in main.py, line ~350
app.run(host='0.0.0.0', port=8000)  # Change to 8000
```

**Dependencies not found?**
```bash
# Ensure you're in the project directory
pip install --upgrade pip
pip install -r requirements.txt
```

**Logs not saving?**
- Check file permissions
- honeypot_logs.json will be created automatically in the project directory

---

## 🧪 Quick Test Commands

```bash
# Test health
curl http://localhost:5000/api/honeypot/health

# Test with auth
curl -X POST http://localhost:5000/api/honeypot/message \
  -H "Authorization: Bearer TEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent":"test","payload":"Your OTP is 1234"}'

# View logs
curl -H "Authorization: Bearer TEST_API_KEY" \
  http://localhost:5000/api/honeypot/logs
```

---

**Status**: ✅ Production Ready
**Last Updated**: February 5, 2026
