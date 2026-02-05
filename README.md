# 🍯 SCAM MESSAGE HONEYPOT API

**A Production-Ready Cybersecurity Backend Service**

A sophisticated REST API that simulates a vulnerable service to detect, analyze, and log phishing and scam message attempts. Designed for security research, threat intelligence, and automated endpoint testing.

---

## 📚 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Authentication](#-authentication)
- [Scam Detection](#-scam-detection)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Security](#-security)

---

## ✨ Features

### Core Capabilities
✅ **Scam Detection Engine** - Analyzes messages for OTP requests, financial keywords, urgency pressure, and suspicious links  
✅ **Bearer Token Authentication** - Industry-standard API key authentication  
✅ **Automated Human-like Replies** - Generated responses that never reveal honeypot status  
✅ **Complete Request Logging** - Stores IP, timestamp, headers, and scam scores  
✅ **Persistent Storage** - JSON-based log persistence  
✅ **Production-Ready** - Error handling, validation, and status codes  
✅ **Automated Testing Ready** - Designed to pass endpoint testing tools  

### API Endpoints
- `GET /api/honeypot/health` - Service health check (public)
- `POST /api/honeypot/message` - Submit messages for analysis (authenticated)
- `GET /api/honeypot/logs` - Retrieve interaction logs (authenticated)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Application                      │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐  ┌──────────────────┐              │
│  │   Authentication │  │   Route Handlers │              │
│  │    Middleware    │  │   (3 Endpoints)  │              │
│  └────────┬─────────┘  └────────┬─────────┘              │
│           │                     │                        │
│  ┌────────▼──────────────────────▼─────────────────┐    │
│  │      ScamDetector Service                       │    │
│  │  - Pattern Matching (OTP, Bank, Urgency, Links)│    │
│  │  - Score Calculation (0-100)                    │    │
│  │  - Threat Classification                        │    │
│  └────────┬─────────────────────────────────────────┘   │
│           │                                              │
│  ┌────────▼─────────────────┐  ┌──────────────────┐    │
│  │  ReplyGenerator Service   │  │ HoneypotLogger   │    │
│  │  - Believable Responses   │  │ - File Storage   │    │
│  │  - Zero Exposure          │  │ - IP Filtering   │    │
│  └──────────────────────────┘  └──────────┬───────┘    │
│                                            │             │
│                              ┌─────────────▼───────┐   │
│                              │ honeypot_logs.json  │   │
│                              └─────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation
```bash
# 1. Navigate to project directory
cd Homey_pot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python main.py
```

### First Request
```bash
curl -X POST http://localhost:5000/api/honeypot/message \
  -H "Authorization: Bearer TEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent": "endpoint-checker",
    "payload": "Your OTP is 1234. Verify now: http://bank.com"
  }'
```

### Expected Response
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

## 📖 API Documentation

### 1. Health Check

**Endpoint**: `GET /api/honeypot/health`  
**Authentication**: Not required  
**Purpose**: Verify service availability

**Response** (200):
```json
{
  "status": "success",
  "message": "Honeypot service is operational",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

### 2. Submit Message

**Endpoint**: `POST /api/honeypot/message`  
**Authentication**: Required (Bearer token)  
**Purpose**: Analyze message for scam indicators

**Request**:
```json
{
  "agent": "endpoint-checker",
  "payload": "Your message to analyze"
}
```

**Response** (200):
```json
{
  "status": "success",
  "trap": false,
  "scamScore": 35,
  "reply": "Thank you for reaching out. We're reviewing your request and will respond within 24 hours.",
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

**Status Codes**:
- `200` - Success
- `400` - Bad JSON / Missing payload field
- `401` - Missing Authorization header
- `403` - Invalid API key
- `500` - Internal error

---

### 3. Retrieve Logs

**Endpoint**: `GET /api/honeypot/logs`  
**Authentication**: Required (Bearer token)  
**Query Parameters**:
- `ip` (optional) - Filter by source IP

**Response** (200):
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
      "message": "Your OTP is 1234 verify now http://bank.com",
      "scam_score": 75,
      "trap": true,
      "headers": {
        "Authorization": "Bearer TEST_API_KEY",
        "Content-Type": "application/json",
        "User-Agent": "PostmanRuntime/7.32.3"
      }
    }
  ],
  "timestamp": "2026-02-05T12:34:56.789Z"
}
```

---

## 🔐 Authentication

### Bearer Token Format
```
Authorization: Bearer TEST_API_KEY
```

### Behavior

| Scenario | Status Code | Action |
|----------|------------|--------|
| Valid key | 200 | Process request |
| Missing header | 401 | Reject - no auth provided |
| Invalid key | 403 | Reject - unauthorized |
| Invalid format | 401 | Reject - malformed header |

### Example

**Valid Request**:
```bash
curl -H "Authorization: Bearer TEST_API_KEY" \
     http://localhost:5000/api/honeypot/logs
```

**Missing Auth** (401):
```bash
curl http://localhost:5000/api/honeypot/message
```

**Wrong Key** (403):
```bash
curl -H "Authorization: Bearer WRONG_KEY" \
     http://localhost:5000/api/honeypot/message
```

---

## 🎯 Scam Detection

### Scoring System

The API calculates a scam score (0-100) based on four categories:

#### 1. OTP Requests (Weight: 25 points)
Detects messages requesting one-time passwords or verification codes.

**Keywords**:
- "OTP", "verify", "confirmation code", "security code"
- "one-time password", "confirm identity"
- 4-6 digit numbers

**Example**:
```
"Your OTP is 4592 verify now"  → +25 points
```

#### 2. Financial Keywords (Weight: 30 points)
Identifies banking and payment-related terms.

**Keywords**:
- "bank", "payment", "credit card", "debit card"
- "account", "transaction", "wire transfer"
- "bitcoin", "cryptocurrency", "paypal", "amazon"

**Example**:
```
"Update your bank account details"  → +30 points
```

#### 3. Urgency Pressure (Weight: 25 points)
Detects high-pressure language tactics.

**Keywords**:
- "urgent", "immediately", "right now"
- "limited time", "act now", "verify immediately"
- "expire", "suspended", "locked", "compromised"

**Example**:
```
"Verify immediately or account will be suspended"  → +25 points
```

#### 4. Suspicious Links (Weight: 20 points)
Identifies HTTP/HTTPS URLs (commonly used in phishing).

**Pattern**: `http://` or `https://`

**Example**:
```
"Click here: http://fakebank.com"  → +20 points
```

### Score Interpretation

| Score | Classification | trap Value |
|-------|-----------------|-----------|
| 0-40 | Legitimate | false |
| 41-100 | Suspicious/Scam | true |

### Example Analysis

**High Score Message**:
```
"URGENT! Your bank account has been compromised. 
Verify your identity immediately with your OTP. 
Visit: http://fakebank.com"
```

**Detected Indicators**:
- "URGENT", "immediately" → 20 pts (urgency)
- "bank account" → 15 pts (financial)
- "OTP" → 15 pts (OTP request)
- "http://fakebank.com" → 20 pts (link)
- **Total: 70 points** → `trap: true`

---

## 🧪 Testing

### With Postman

1. **Import Collection**:
   - Open Postman
   - Click "Import"
   - Select `Honeypot_API_Postman_Collection.json`
   - All 12 test cases are ready to run

2. **Or Create Manually**:
   - Base URL: `http://localhost:5000`
   - Authorization: Bearer Token (Value: `TEST_API_KEY`)

### Sample Test Cases

**Test 1: Legitimate Message**
```json
{
  "agent": "endpoint-checker",
  "payload": "Hello, can you help me with my account?"
}
```
**Expected**: `scamScore: 0`, `trap: false`

**Test 2: High Scam Score**
```json
{
  "agent": "endpoint-checker",
  "payload": "Your OTP is 4592 verify now http://fakebank.com"
}
```
**Expected**: `scamScore: 65`, `trap: true`

**Test 3: Missing Authentication**
```
POST /api/honeypot/message (no Authorization header)
```
**Expected**: 401 Unauthorized

**Test 4: Invalid API Key**
```
Authorization: Bearer WRONG_KEY
```
**Expected**: 403 Forbidden

See `TESTING_GUIDE.md` for 12 complete test scenarios.

---

## 🚢 Deployment

### Development
```bash
python main.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

### Production with Waitress (Windows-friendly)
```bash
pip install waitress
waitress-serve --port=5000 main:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
```

---

## 🛡️ Security

### Built-in Protections

1. **Input Validation**
   - JSON schema validation
   - Required field checking
   - Type validation

2. **Authentication**
   - Bearer token scheme
   - Credential validation
   - No credentials in error messages

3. **Error Handling**
   - No sensitive details exposed
   - Graceful failure modes
   - Proper status codes

4. **Logging**
   - Complete audit trail
   - No sensitive data exposure
   - File-based persistence

5. **No Exposure**
   - Detection logic never revealed
   - Human-like automated replies
   - Service appears normal even under attack

### Additional Hardening

Add rate limiting:
```bash
pip install Flask-Limiter
```

Add CORS (if needed):
```bash
pip install Flask-CORS
```

Add HTTPS:
```python
app.run(ssl_context='adhoc')  # Development
# Use reverse proxy (nginx) in production
```

---

## 📊 Logging

### Stored per Request
- **ID**: Unique identifier
- **Timestamp**: ISO-8601 format
- **IP Address**: Source IP
- **User Agent**: Client information
- **Message**: Original payload
- **Scam Score**: Calculated risk (0-100)
- **Trap**: Boolean indicator
- **Headers**: All HTTP headers

### Log File
`honeypot_logs.json` - Created automatically on first request

### Example Log Entry
```json
{
  "id": "192.168.1.100_1_1707143696789",
  "timestamp": "2026-02-05T12:34:56.789Z",
  "ip_address": "192.168.1.100",
  "user_agent": "PostmanRuntime/7.32.3",
  "message": "Your OTP is 4592 verify now http://fakebank.com",
  "scam_score": 65,
  "trap": true,
  "headers": {...}
}
```

---

## 📁 Project Structure

```
Homey_pot/
├── main.py                              # Main application
├── requirements.txt                     # Dependencies
├── honeypot_logs.json                   # Generated logs
├── QUICK_START.md                       # 60-second setup
├── TESTING_GUIDE.md                     # Detailed test cases
├── README.md                            # This file
└── Honeypot_API_Postman_Collection.json # Postman tests
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'flask'`
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
Edit `main.py`, change port:
```python
app.run(host='0.0.0.0', port=8000)
```

### Issue: Logs not saving
- Verify write permissions in project directory
- Check `honeypot_logs.json` is not read-only
- Ensure Flask is running with proper permissions

### Issue: Authentication failing
- Verify header format: `Authorization: Bearer TEST_API_KEY`
- Check for trailing/leading spaces
- Ensure `Content-Type: application/json` is set

---

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server starts without errors (`python main.py`)
- [ ] Health check returns 200 (GET /health)
- [ ] Valid auth request returns 200
- [ ] Missing auth returns 401
- [ ] Wrong key returns 403
- [ ] Scam detection calculates scores
- [ ] Logs persist to file
- [ ] Responses match specification
- [ ] All status codes are correct

---

## 📝 API Contract Summary

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET | /api/honeypot/health | No | Service status |
| POST | /api/honeypot/message | Yes | Analyze message |
| GET | /api/honeypot/logs | Yes | Retrieve logs |

---

## 🎓 Learning Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **REST API Best Practices**: https://restfulapi.net/
- **OWASP Security**: https://owasp.org/
- **Phishing Detection**: https://www.ncsc.gov.uk/guidance

---

## 📄 License

This project is provided as-is for educational and security research purposes.

---

## 👨‍💼 Author

**Senior Cybersecurity Backend Engineer**  
Specialized in threat detection, honeypot systems, and API security.

---

## 📅 Version History

- **v1.0** (Feb 5, 2026) - Production release
  - Full API implementation
  - Scam detection engine
  - Complete logging system
  - Postman collection
  - Testing guides

---

**Status**: ✅ Production Ready  
**Last Updated**: February 5, 2026  
**Support**: Refer to TESTING_GUIDE.md and QUICK_START.md
