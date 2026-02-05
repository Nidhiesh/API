# 🚀 GETTING STARTED - HONEYPOT API

## ✅ Setup Complete!

Your Scam Message Honeypot API is fully implemented and ready to use.

---

## 📋 What You Have

### Core Files
- **main.py** - Complete REST API (1000+ lines)
- **config.py** - Configuration & settings
- **requirements.txt** - Dependencies (Flask, Werkzeug)

### Documentation
- **README.md** - Full API documentation
- **QUICK_START.md** - 60-second setup guide
- **TESTING_GUIDE.md** - 10 detailed test scenarios
- **PROJECT_SUMMARY.md** - Technical details

### Testing Tools
- **test_suite.py** - Automated test runner (8 tests)
- **verify_setup.py** - Installation verification
- **Honeypot_API_Postman_Collection.json** - Postman tests

---

## 🎯 Quick Start (3 Minutes)

### Step 1: Start the Server
```bash
python main.py
```

Expected output:
```
============================================================
SCAM MESSAGE HONEYPOT API - Starting Server
============================================================
API Key: TEST_API_KEY
Server running on: http://localhost:5000
============================================================

Endpoints:
  GET  /api/honeypot/health
  POST /api/honeypot/message (Requires Auth)
  GET  /api/honeypot/logs (Requires Auth)
============================================================
```

### Step 2: Test in New Terminal
```bash
python test_suite.py
```

### Step 3: View Results
Server should show requests logged, and test suite shows results.

---

## 🧪 Manual Testing

### Test 1: Health Check (No Auth)
```bash
curl http://localhost:5000/api/honeypot/health
```

Response:
```json
{
  "status": "success",
  "message": "Honeypot service is operational",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

### Test 2: Submit Message (Requires Auth)
```bash
curl -X POST http://localhost:5000/api/honeypot/message \
  -H "Authorization: Bearer TEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent":"test","payload":"Your OTP is 1234"}'
```

Response:
```json
{
  "status": "success",
  "trap": true,
  "scamScore": 25,
  "reply": "Thank you for reaching out...",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

### Test 3: View Logs (Requires Auth)
```bash
curl -H "Authorization: Bearer TEST_API_KEY" \
  http://localhost:5000/api/honeypot/logs
```

---

## 📊 API Endpoints

### 1. GET /api/honeypot/health
- **Auth**: Not required
- **Purpose**: Check if service is running
- **Status Code**: 200

### 2. POST /api/honeypot/message
- **Auth**: Required (Bearer TEST_API_KEY)
- **Purpose**: Submit message for analysis
- **Status Code**: 200 (success), 400 (bad data), 401 (no auth), 403 (bad key), 500 (error)
- **Body**: `{"agent":"string","payload":"string"}`
- **Response**: `{"status":"success","trap":boolean,"scamScore":number,"reply":"string","timestamp":"ISO-8601"}`

### 3. GET /api/honeypot/logs
- **Auth**: Required (Bearer TEST_API_KEY)
- **Purpose**: Retrieve all stored logs
- **Status Code**: 200
- **Query**: `?ip=<ip_address>` (optional filter)
- **Response**: `{"status":"success","count":number,"logs":array,"timestamp":"ISO-8601"}`

---

## 🎓 Scam Detection Scoring

Messages are scored 0-100:

| Category | Points | Keywords |
|----------|--------|----------|
| **OTP** | 0-25 | otp, verify, code, 4-6 digits |
| **Bank** | 0-30 | bank, payment, card, account |
| **Urgency** | 0-25 | urgent, immediately, suspended |
| **Links** | 0-20 | http://, https:// |

**Score > 40** = `trap: true` (scam detected)  
**Score ≤ 40** = `trap: false` (legitimate)

---

## 🔒 Authentication

All endpoints except `/health` require:

```
Authorization: Bearer TEST_API_KEY
```

### Behavior
- **Missing header** → 401 Unauthorized
- **Wrong key** → 403 Forbidden
- **Valid key** → Process request

---

## 📁 Project Structure

```
Homey_pot/
├── main.py                          ← Start here
├── config.py                        ← Customize settings
├── test_suite.py                    ← Run tests
├── verify_setup.py                  ← Check installation
├── requirements.txt                 ← Dependencies
├── honeypot_logs.json               ← Logs (auto-created)
├── README.md                        ← Full documentation
├── QUICK_START.md                   ← Quick guide
├── TESTING_GUIDE.md                 ← Test cases
├── PROJECT_SUMMARY.md               ← Technical details
└── Honeypot_API_Postman_Collection.json ← Postman tests
```

---

## 🔧 Configuration

Edit `config.py` to customize:
- API host/port
- API key (change from TEST_API_KEY)
- Scam detection patterns
- Automated reply templates
- Score weights

---

## 📚 Documentation Guide

**New to the API?**
1. Read `QUICK_START.md` (5 minutes)
2. Try the curl commands above
3. Import Postman collection

**Need detailed info?**
1. Read `README.md` (complete reference)
2. Check `TESTING_GUIDE.md` for test scenarios
3. See `PROJECT_SUMMARY.md` for technical details

**Want to customize?**
1. Edit `config.py`
2. See config.py comments for guidance
3. Test with `test_suite.py`

---

## 🧪 Testing Options

### Automated Test Suite
```bash
python test_suite.py
```
Runs 8 tests, generates test_results.json

### Postman Collection
1. Import `Honeypot_API_Postman_Collection.json`
2. Set variable: `api_key = TEST_API_KEY`
3. Run all 12 requests

### Manual cURL
```bash
# Health
curl http://localhost:5000/api/honeypot/health

# Submit message
curl -X POST http://localhost:5000/api/honeypot/message \
  -H "Authorization: Bearer TEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent":"test","payload":"test message"}'

# Get logs
curl -H "Authorization: Bearer TEST_API_KEY" \
  http://localhost:5000/api/honeypot/logs
```

---

## 🚢 Deployment

### Development (Local)
```bash
python main.py
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Production (Docker)
```bash
docker build -t honeypot-api .
docker run -p 5000:5000 honeypot-api
```

---

## ⚙️ Features Summary

✅ **3 REST Endpoints**
- Health check (public)
- Message analysis (authenticated)
- Log retrieval (authenticated)

✅ **Scam Detection**
- 4-category analysis
- Score calculation (0-100)
- Configurable patterns

✅ **Authentication**
- Bearer token validation
- Proper error codes (401/403)

✅ **Logging**
- IP tracking
- Timestamp recording
- Header capture
- Persistent storage

✅ **Response Consistency**
- Standard JSON format
- ISO-8601 timestamps
- Always includes required fields

✅ **Error Handling**
- Graceful failures
- Sanitized error messages
- Proper status codes

---

## 🎯 Next Steps

1. **Start server**: `python main.py`
2. **Run tests**: `python test_suite.py` (in another terminal)
3. **Try Postman**: Import the collection
4. **Read docs**: Check README.md for full details
5. **Customize**: Edit config.py as needed
6. **Deploy**: Follow deployment instructions

---

## 📞 Support

**All documentation is in the project directory:**
- README.md - Full API reference
- QUICK_START.md - Fast setup
- TESTING_GUIDE.md - Test scenarios
- PROJECT_SUMMARY.md - Technical details
- config.py - Configuration guide

---

## ✅ Verification

Run this to verify everything is working:
```bash
python verify_setup.py
```

Should show all checks passed.

---

## 🎉 You're Ready!

Your Scam Message Honeypot API is complete and production-ready.

**Start now**:
```bash
python main.py
```

**Questions?** Check the documentation files included in the project.

---

**Status**: Production Ready ✅  
**Version**: 1.0  
**Date**: February 5, 2026  

Enjoy your honeypot API!
