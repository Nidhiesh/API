"""
Configuration file for Scam Message Honeypot API
Edit this file to customize API behavior
"""

# =====================
# API CONFIGURATION
# =====================

# API Server Settings
API_HOST = '0.0.0.0'
API_PORT = 5000
API_DEBUG = False  # Set to True for development only

# =====================
# AUTHENTICATION
# =====================

# Bearer Token for API authentication
API_KEY = "hpy_prod_5f8e3a1b9c7d4e2f6a8c3b1e5d7f9a2c8e3f1b5d7e9a2c4f6b8d1f3e5a7c"

# =====================
# LOGGING
# =====================

# Log storage file
LOG_FILE = "honeypot_logs.json"

# Maximum number of logs to keep in memory
# (Note: all logs are persisted to file)
MAX_MEMORY_LOGS = 10000

# =====================
# SCAM DETECTION
# =====================

# Scam score threshold for marking as trap
SCAM_SCORE_THRESHOLD = 40  # Score > 40 = trap: true

# Scam Detection Patterns (regex)
SCAM_INDICATORS = {
    "otp_keywords": [
        r'\botp\b', 
        r'verify', 
        r'confirmation.*code', 
        r'security.*code',
        r'one.*time.*password', 
        r'\d{4,6}', 
        r'verify.*now', 
        r'confirm.*identity'
    ],
    "bank_keywords": [
        r'bank', 
        r'payment', 
        r'credit.*card', 
        r'debit.*card', 
        r'account',
        r'transaction', 
        r'wire.*transfer', 
        r'atm', 
        r'cryptocurrency',
        r'bitcoin', 
        r'ethereum', 
        r'paypal', 
        r'amazon', 
        r'apple'
    ],
    "urgency_keywords": [
        r'urgent', 
        r'immediately', 
        r'right.*now', 
        r'limited.*time',
        r'act.*now', 
        r'confirm.*immediately', 
        r'verify.*now',
        r'expire', 
        r'suspended', 
        r'locked', 
        r'compromised'
    ],
    "suspicious_links": [
        r'https?://(?!$)'  # http/https protocols
    ]
}

# Scam Score Weights
SCAM_WEIGHTS = {
    "otp_keywords": 25,        # Maximum 25 points
    "bank_keywords": 30,       # Maximum 30 points
    "urgency_keywords": 25,    # Maximum 25 points
    "suspicious_links": 20     # Maximum 20 points
}

# =====================
# AUTOMATED REPLIES
# =====================

# Human-like automated response templates
REPLY_TEMPLATES = [
    "Thank you for reaching out. We're reviewing your request and will respond within 24 hours.",
    "Your message has been received. A support agent will contact you shortly with further instructions.",
    "We appreciate your patience. Please allow us some time to verify your information.",
    "Your inquiry is important to us. Please check your email for a confirmation and next steps.",
    "Thank you for contacting us. You should receive a follow-up message within the next 2-3 business days.",
    "We've received your submission and will review it promptly. Stay tuned for updates.",
    "Your request has been logged. Please maintain this conversation for reference.",
]

# =====================
# SECURITY
# =====================

# Enable CORS (Cross-Origin Resource Sharing)
ENABLE_CORS = False

# Enable rate limiting
ENABLE_RATE_LIMITING = False

# Rate limit: requests per minute per IP
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

# =====================
# DEPLOYMENT
# =====================

# Environment: 'development' or 'production'
ENVIRONMENT = 'production'

# Number of worker threads
WORKER_THREADS = 4

# =====================
# NOTES
# =====================

"""
CUSTOMIZATION GUIDE:

1. Changing API Key:
   - Update API_KEY variable
   - Communicate new key to clients

2. Adding Detection Patterns:
   - Add regex patterns to SCAM_INDICATORS
   - Patterns are case-insensitive
   - Test patterns thoroughly

3. Adjusting Score Weights:
   - Modify SCAM_WEIGHTS dictionary
   - Must total ≤ 100
   - Higher weight = more impact on score

4. Custom Replies:
   - Add strings to REPLY_TEMPLATES
   - Replies should appear human-written
   - Should never reveal detection logic

5. Production Deployment:
   - Set API_DEBUG = False
   - Change API_KEY to secure value
   - Use HTTPS (nginx reverse proxy)
   - Monitor logs regularly
   - Set up log rotation

6. Rate Limiting:
   - Install Flask-Limiter: pip install Flask-Limiter
   - Set ENABLE_RATE_LIMITING = True
   - Adjust limits as needed

7. CORS:
   - Install Flask-CORS: pip install Flask-CORS
   - Set ENABLE_CORS = True
   - Configure allowed origins
"""

if __name__ == '__main__':
    print("Configuration loaded successfully")
    print(f"API running on {API_HOST}:{API_PORT}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Scam threshold: {SCAM_SCORE_THRESHOLD}")
