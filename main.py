"""
SCAM MESSAGE HONEYPOT API
Senior Backend Engineering Implementation
Author: Cybersecurity Team
"""

from flask import Flask, request, jsonify
from datetime import datetime, timezone
from functools import wraps
from typing import Dict, Tuple, List
import re
import json
import os
from dataclasses import dataclass, asdict
from collections import defaultdict

# =====================
# CONFIGURATION
# =====================

TEST_API_KEY = "hpy_prod_5f8e3a1b9c7d4e2f6a8c3b1e5d7f9a2c8e3f1b5d7e9a2c4f6b8d1f3e5a7c"
LOG_FILE = "honeypot_logs.json"

# Scam detection patterns
SCAM_INDICATORS = {
    "otp_keywords": [
        r'\botp\b', r'verify', r'confirmation.*code', r'security.*code',
        r'one.*time.*password', r'\d{4,6}', r'verify.*now', r'confirm.*identity'
    ],
    "bank_keywords": [
        r'bank', r'payment', r'credit.*card', r'debit.*card', r'account',
        r'transaction', r'wire.*transfer', r'atm', r'cryptocurrency',
        r'bitcoin', r'ethereum', r'paypal', r'amazon', r'apple'
    ],
    "urgency_keywords": [
        r'urgent', r'immediately', r'right.*now', r'limited.*time',
        r'act.*now', r'confirm.*immediately', r'verify.*now',
        r'expire', r'suspended', r'locked', r'compromised'
    ],
    "suspicious_links": [
        r'https?://(?!$)',  # http/https protocols
    ]
}

# =====================
# DATA MODELS
# =====================

@dataclass
class ScamLog:
    """Model for storing interaction logs"""
    id: str
    timestamp: str
    ip_address: str
    user_agent: str
    message: str
    scam_score: int
    trap: bool
    headers: Dict

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ApiResponse:
    """Standard API response format"""
    status: str
    trap: bool
    scamScore: int
    reply: str
    timestamp: str

    def to_dict(self) -> Dict:
        return asdict(self)


# =====================
# LOGGER SERVICE
# =====================

class HoneypotLogger:
    """Handles logging of interactions"""
    
    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file
        self.logs: List[ScamLog] = []
        self._load_logs()
    
    def _load_logs(self):
        """Load logs from file if exists"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    # Reconstruct ScamLog objects
                    self.logs = [ScamLog(**log) for log in data]
            except (json.JSONDecodeError, TypeError):
                self.logs = []
    
    def _save_logs(self):
        """Persist logs to file"""
        with open(self.log_file, 'w') as f:
            json.dump([log.to_dict() for log in self.logs], f, indent=2)
    
    def add_log(self, log: ScamLog) -> None:
        """Add new log entry"""
        self.logs.append(log)
        self._save_logs()
    
    def get_all_logs(self) -> List[Dict]:
        """Retrieve all logs"""
        return [log.to_dict() for log in self.logs]
    
    def get_logs_by_ip(self, ip: str) -> List[Dict]:
        """Get logs for specific IP address"""
        return [log.to_dict() for log in self.logs if log.ip_address == ip]


# =====================
# SCAM DETECTION SERVICE
# =====================

class ScamDetector:
    """Analyzes messages for scam indicators"""
    
    def __init__(self):
        self.compiled_patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, List]:
        """Pre-compile regex patterns for performance"""
        compiled = {}
        for category, patterns in SCAM_INDICATORS.items():
            compiled[category] = [re.compile(p, re.IGNORECASE) for p in patterns]
        return compiled
    
    def calculate_scam_score(self, message: str) -> Tuple[int, List[str]]:
        """
        Calculate scam score (0-100) based on detected indicators.
        Returns: (score, detected_indicators)
        """
        if not message or not isinstance(message, str):
            return 0, []
        
        message_lower = message.lower()
        detected = []
        score = 0
        
        # Check OTP keywords (weight: 25)
        otp_matches = sum(1 for pattern in self.compiled_patterns['otp_keywords'] 
                         if pattern.search(message_lower))
        if otp_matches > 0:
            detected.append("otp_request")
            score += min(25, otp_matches * 10)
        
        # Check bank/payment keywords (weight: 30)
        bank_matches = sum(1 for pattern in self.compiled_patterns['bank_keywords'] 
                          if pattern.search(message_lower))
        if bank_matches > 0:
            detected.append("financial_keywords")
            score += min(30, bank_matches * 8)
        
        # Check urgency keywords (weight: 25)
        urgency_matches = sum(1 for pattern in self.compiled_patterns['urgency_keywords'] 
                             if pattern.search(message_lower))
        if urgency_matches > 0:
            detected.append("urgency_pressure")
            score += min(25, urgency_matches * 8)
        
        # Check suspicious links (weight: 20)
        link_matches = sum(1 for pattern in self.compiled_patterns['suspicious_links'] 
                          if pattern.search(message_lower))
        if link_matches > 0:
            detected.append("suspicious_links")
            score += min(20, link_matches * 10)
        
        return min(100, score), detected
    
    def is_scam(self, message: str) -> bool:
        """Determine if message is likely scam (score > 40)"""
        score, _ = self.calculate_scam_score(message)
        return score > 40


# =====================
# AUTOMATED REPLY GENERATOR
# =====================

class ReplyGenerator:
    """Generates believable automated replies"""
    
    REPLY_TEMPLATES = [
        "Thank you for reaching out. We're reviewing your request and will respond within 24 hours.",
        "Your message has been received. A support agent will contact you shortly with further instructions.",
        "We appreciate your patience. Please allow us some time to verify your information.",
        "Your inquiry is important to us. Please check your email for a confirmation and next steps.",
        "Thank you for contacting us. You should receive a follow-up message within the next 2-3 business days.",
        "We've received your submission and will review it promptly. Stay tuned for updates.",
        "Your request has been logged. Please maintain this conversation for reference.",
    ]
    
    @staticmethod
    def generate_reply(scam_score: int, detected_indicators: List[str]) -> str:
        """Generate appropriate reply based on scam score"""
        # Always appear friendly and functional - never reveal detection
        if scam_score < 30:
            base_reply = ReplyGenerator.REPLY_TEMPLATES[0]
        elif scam_score < 60:
            base_reply = ReplyGenerator.REPLY_TEMPLATES[2]
        else:
            base_reply = ReplyGenerator.REPLY_TEMPLATES[4]
        
        return base_reply


# =====================
# FLASK APP SETUP
# =====================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize services
logger = HoneypotLogger()
detector = ScamDetector()
reply_gen = ReplyGenerator()

# Request counter for ID generation
request_counter = defaultdict(int)


# =====================
# AUTHENTICATION MIDDLEWARE
# =====================

def require_auth(f):
    """Decorator for API key authentication - supports both Bearer token and x-opi-key header"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Try x-opi-key header first (for hackathon/external tools)
        api_key = request.headers.get('x-opi-key')
        
        if api_key:
            # Validate x-opi-key
            if api_key != TEST_API_KEY:
                return jsonify({
                    "status": "error",
                    "message": "Invalid API key",
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                }), 403
            return f(*args, **kwargs)
        
        # Fallback to Authorization Bearer token
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "status": "error",
                "message": "Missing Authorization header or x-opi-key",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 401
        
        # Validate Bearer token format
        try:
            scheme, credentials = auth_header.split(' ')
            if scheme.lower() != 'bearer':
                raise ValueError("Invalid scheme")
        except (ValueError, IndexError):
            return jsonify({
                "status": "error",
                "message": "Invalid Authorization header format",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 401
        
        # Check if key is valid
        if credentials != TEST_API_KEY:
            return jsonify({
                "status": "error",
                "message": "Invalid API key",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


# =====================
# ENDPOINTS
# =====================

@app.route('/api/honeypot/health', methods=['GET'])
def health_check():
    """Health check endpoint - no auth required"""
    return jsonify({
        "status": "success",
        "message": "Honeypot service is operational",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }), 200


@app.route('/api/honeypot/message', methods=['POST'])
@require_auth
def honeypot_message():
    """
    Main honeypot message endpoint
    Accepts messages, analyzes for scams, logs, and returns reply
    """
    try:
        # Validate Content-Type
        if request.content_type and 'application/json' not in request.content_type:
            return jsonify({
                "status": "error",
                "message": "Content-Type must be application/json",
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 400
        
        # Parse JSON
        try:
            data = request.get_json(force=True) if not request.is_json else request.get_json()
            if data is None:
                raise ValueError("Empty body")
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON format",
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 400
        
        # Validate required fields
        if 'payload' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'payload' field",
                "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }), 400
        
        message = data.get('payload', '')
        agent = data.get('agent', 'unknown')
        
        # Calculate scam score
        scam_score, detected_indicators = detector.calculate_scam_score(message)
        is_scam = detector.is_scam(message)
        
        # Generate reply
        reply = reply_gen.generate_reply(scam_score, detected_indicators)
        
        # Extract client info
        client_ip = request.remote_addr or "unknown"
        user_agent = request.headers.get('User-Agent', 'unknown')
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        # Generate unique log ID
        request_counter[client_ip] += 1
        log_id = f"{client_ip}_{request_counter[client_ip]}_{int(datetime.now(timezone.utc).timestamp() * 1000)}"
        
        # Create and store log
        log_entry = ScamLog(
            id=log_id,
            timestamp=timestamp,
            ip_address=client_ip,
            user_agent=user_agent,
            message=message,
            scam_score=scam_score,
            trap=is_scam,
            headers=dict(request.headers)
        )
        logger.add_log(log_entry)
        
        # Build response - EXACT FORMAT REQUIRED
        response = ApiResponse(
            status="success",
            trap=is_scam,
            scamScore=scam_score,
            reply=reply,
            timestamp=timestamp
        )
        
        return jsonify(response.to_dict()), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }), 500


@app.route('/api/honeypot/logs', methods=['GET'])
@require_auth
def get_logs():
    """
    Retrieve stored interaction logs
    Query parameters:
    - ip: Filter by IP address (optional)
    """
    try:
        filter_ip = request.args.get('ip')
        
        if filter_ip:
            logs = logger.get_logs_by_ip(filter_ip)
        else:
            logs = logger.get_all_logs()
        
        return jsonify({
            "status": "success",
            "count": len(logs),
            "logs": logs,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        }), 500


# =====================
# ERROR HANDLERS
# =====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "status": "error",
        "message": "Method not allowed",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }), 500


# =====================
# APPLICATION ENTRY
# =====================

if __name__ == '__main__':
    print("=" * 60)
    print("SCAM MESSAGE HONEYPOT API - Starting Server")
    print("=" * 60)
    print(f"API Key: {TEST_API_KEY}")
    print("Server running on: http://localhost:5000")
    print("=" * 60)
    print("\nEndpoints:")
    print("  GET  /api/honeypot/health")
    print("  POST /api/honeypot/message (Requires Auth)")
    print("  GET  /api/honeypot/logs (Requires Auth)")
    print("=" * 60)
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False,  # Production mode
        threaded=True
    )
