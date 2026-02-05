# SCAM MESSAGE HONEYPOT API
## Complete Setup & Testing Guide

---

## 📋 INSTALLATION & SETUP

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```

**Expected Output:**
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

---

## 🧪 TESTING WITH POSTMAN

### Setup Postman Collection

1. **Create New Collection**: "Honeypot API"
2. **Set Collection Variable**:
   - Click "Variables" tab
   - Add variable: `api_key` = `TEST_API_KEY`

### Test 1: Health Check (No Auth Required)

**Request:**
```http
GET http://localhost:5000/api/honeypot/health
```

**Expected Response (200):**
```json
{
  "status": "success",
  "message": "Honeypot service is operational",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 2: Authenticate - Valid Credentials

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json
  Authorization: Bearer TEST_API_KEY

Body:
{
  "agent": "endpoint-checker",
  "payload": "Hello, can you help me?"
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "trap": false,
  "scamScore": 0,
  "reply": "Thank you for reaching out. We're reviewing your request and will respond within 24 hours.",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 3: Missing Authentication Header

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json

Body:
{
  "agent": "endpoint-checker",
  "payload": "test"
}
```

**Expected Response (401):**
```json
{
  "status": "error",
  "message": "Missing Authorization header",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 4: Invalid API Key

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json
  Authorization: Bearer WRONG_KEY

Body:
{
  "agent": "endpoint-checker",
  "payload": "test"
}
```

**Expected Response (403):**
```json
{
  "status": "error",
  "message": "Invalid API key",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 5: High Scam Score - OTP + Bank Keywords + Urgency

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json
  Authorization: Bearer TEST_API_KEY

Body:
{
  "agent": "endpoint-checker",
  "payload": "URGENT! Your bank account has been compromised. Please verify your identity immediately by providing your OTP. Click here: http://fakebank.com"
}
```

**Expected Response (200):**
```json
{
  "status": "success",
  "trap": true,
  "scamScore": 85,
  "reply": "We appreciate your patience. Please allow us some time to verify your information.",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

**Note:** `trap: true` indicates scam detected (score > 40)

---

### Test 6: Missing Payload Field

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json
  Authorization: Bearer TEST_API_KEY

Body:
{
  "agent": "endpoint-checker"
}
```

**Expected Response (400):**
```json
{
  "status": "error",
  "message": "Missing 'payload' field",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 7: Invalid JSON

**Request:**
```http
POST http://localhost:5000/api/honeypot/message

Headers:
  Content-Type: application/json
  Authorization: Bearer TEST_API_KEY

Body:
{invalid json}
```

**Expected Response (400):**
```json
{
  "status": "error",
  "message": "Invalid JSON format",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 8: Retrieve All Logs

**Request:**
```http
GET http://localhost:5000/api/honeypot/logs

Headers:
  Authorization: Bearer TEST_API_KEY
```

**Expected Response (200):**
```json
{
  "status": "success",
  "count": 5,
  "logs": [
    {
      "id": "127.0.0.1_1_1707143696789",
      "timestamp": "2026-02-05T12:34:56.789Z",
      "ip_address": "127.0.0.1",
      "user_agent": "PostmanRuntime/7.32.3",
      "message": "Your OTP is 4592 verify now http://fakebank.com",
      "scam_score": 65,
      "trap": true,
      "headers": {...}
    }
  ],
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 9: Filter Logs by IP

**Request:**
```http
GET http://localhost:5000/api/honeypot/logs?ip=127.0.0.1

Headers:
  Authorization: Bearer TEST_API_KEY
```

**Expected Response (200):**
```json
{
  "status": "success",
  "count": 3,
  "logs": [...],
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### Test 10: Non-existent Endpoint

**Request:**
```http
GET http://localhost:5000/api/honeypot/unknown

Headers:
  Authorization: Bearer TEST_API_KEY
```

**Expected Response (404):**
```json
{
  "status": "error",
  "message": "Endpoint not found",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

## 🎯 SCAM DETECTION SCORING

The API analyzes messages for 4 categories of scam indicators:

### Scoring Breakdown:
| Category | Weight | Examples |
|----------|--------|----------|
| **OTP Requests** | 25 pts | "OTP", "verify", "confirmation code", numbers (4-6 digits) |
| **Financial Keywords** | 30 pts | "bank", "payment", "credit card", "cryptocurrency" |
| **Urgency Pressure** | 25 pts | "urgent", "immediately", "verify now", "limited time" |
| **Suspicious Links** | 20 pts | `http://` or `https://` URLs |

### Score Interpretation:
- **0-40**: Legitimate (trap: false)
- **41-100**: Suspicious/Scam (trap: true)

---

## 🔒 AUTHENTICATION BEHAVIOR

### Valid Token:
```bash
Authorization: Bearer TEST_API_KEY
→ 200 (Process request)
```

### Missing Header:
```bash
(No Authorization header)
→ 401 Unauthorized
```

### Wrong Token:
```bash
Authorization: Bearer INVALID_KEY
→ 403 Forbidden
```

### Invalid Format:
```bash
Authorization: InvalidFormat TEST_API_KEY
→ 401 Unauthorized
```

---

## 📊 LOGGING & STORAGE

### Stored Data per Request:
- **ID**: Unique identifier (IP + counter + timestamp)
- **Timestamp**: ISO-8601 format with Z suffix
- **IP Address**: Client source
- **User Agent**: Browser/client information
- **Message**: Original payload
- **Scam Score**: Calculated risk (0-100)
- **Trap**: Boolean indicating if scam detected
- **Headers**: All HTTP headers received

### Log File:
Stored in `honeypot_logs.json` in project directory

---

## ⚙️ AUTOMATED TESTING BEHAVIOR

The API is designed to pass automated endpoint testing tools:

✅ **Connectivity**: Health endpoint accessible without auth
✅ **Authentication**: Proper 401/403 status codes
✅ **Response Format**: Consistent JSON structure with all required fields
✅ **Status Codes**: Correct HTTP status for each scenario
✅ **Error Handling**: Graceful failures with descriptive messages
✅ **Honeypot Function**: Always returns reply, logs interaction
✅ **No Exposure**: Detection logic never revealed to client

---

## 🚀 PRODUCTION DEPLOYMENT

### Environment Variables (if needed):
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export API_KEY=your_secure_key
```

### Run with Gunicorn (Production):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Run with Waitress (Windows-friendly):
```bash
pip install waitress
waitress-serve --port=5000 main:app
```

---

## 🛡️ SECURITY FEATURES

1. **Bearer Token Authentication**: Industry-standard auth header
2. **Input Validation**: JSON structure and field validation
3. **Error Suppression**: No sensitive details in error messages
4. **Rate Limiting Ready**: Can add with Flask-Limiter
5. **CORS Ready**: Can configure with Flask-CORS
6. **Logging**: Full audit trail of all interactions
7. **No SQL**: File-based storage, no injection vulnerabilities

---

## 📝 API CONTRACT

### POST /api/honeypot/message

**Authentication**: Required (Bearer token)

**Request Schema**:
```json
{
  "agent": "string (optional)",
  "payload": "string (required)"
}
```

**Response Schema**:
```json
{
  "status": "string (success|error)",
  "trap": "boolean",
  "scamScore": "number (0-100)",
  "reply": "string",
  "timestamp": "string (ISO-8601)"
}
```

---

## 🧹 CLEANUP

Clear logs:
```bash
rm honeypot_logs.json
```

Stop server:
```bash
Ctrl+C
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Server starts without errors
- [ ] Health check returns 200
- [ ] Valid auth request returns 200 with proper response
- [ ] Missing auth returns 401
- [ ] Wrong auth returns 403
- [ ] Scam detection calculates scores accurately
- [ ] Logs are persisted to file
- [ ] Automated replies are human-like
- [ ] Response format matches specification exactly
- [ ] All status codes are correct

---

**Last Updated**: February 5, 2026
**Version**: 1.0
**Status**: Production Ready ✅
