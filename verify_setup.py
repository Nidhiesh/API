#!/usr/bin/env python3
"""
Setup Verification Script - Validates Honeypot API Installation
Run this to verify all components are properly set up
"""

import os
import sys
import json
from pathlib import Path

def check_file(filepath, description):
    """Check if file exists and report status"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    size = f" ({os.path.getsize(filepath)} bytes)" if exists else ""
    print(f"{status} {description}{size}")
    return exists

def check_python():
    """Check Python version"""
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = sys.version_info >= (3, 7)
    status = "✅" if ok else "❌"
    print(f"{status} Python {version} (required: 3.7+)")
    return ok

def check_imports():
    """Check if required modules are installed"""
    modules = {
        "flask": "Flask",
        "werkzeug": "Werkzeug"
    }
    
    print("\n📦 Checking Dependencies:")
    all_ok = True
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} NOT installed (pip install {module})")
            all_ok = False
    
    return all_ok

def check_config():
    """Check configuration values"""
    print("\n⚙️  Checking Configuration:")
    
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Check for API key
        if 'API_KEY' in content:
            print("✅ API key configured")
        else:
            print("❌ API key missing")
            return False
        
        # Check for patterns
        if 'SCAM_INDICATORS' in content:
            print("✅ Scam detection patterns configured")
        else:
            print("❌ Scam patterns missing")
            return False
        
        # Check for replies
        if 'REPLY_TEMPLATES' in content:
            print("✅ Automated reply templates configured")
        else:
            print("❌ Reply templates missing")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

def check_code():
    """Check main code file"""
    print("\n🔍 Checking Main Code:")
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        checks = {
            "Flask app": "app = Flask(__name__)" in content,
            "Health endpoint": "/api/honeypot/health" in content,
            "Message endpoint": "/api/honeypot/message" in content,
            "Logs endpoint": "/api/honeypot/logs" in content,
            "Authentication": "@require_auth" in content,
            "ScamDetector": "class ScamDetector" in content,
            "HoneypotLogger": "class HoneypotLogger" in content,
            "ReplyGenerator": "class ReplyGenerator" in content,
        }
        
        all_ok = True
        for check, result in checks.items():
            status = "✅" if result else "❌"
            print(f"{status} {check}")
            all_ok = all_ok and result
        
        return all_ok
    
    except Exception as e:
        print(f"❌ Code check failed: {e}")
        return False

def check_documentation():
    """Check if all documentation is present"""
    print("\n📚 Checking Documentation:")
    
    docs = {
        "README.md": "Main documentation",
        "QUICK_START.md": "Quick start guide",
        "TESTING_GUIDE.md": "Testing guide",
        "PROJECT_SUMMARY.md": "Project summary"
    }
    
    all_ok = True
    for file, desc in docs.items():
        exists = os.path.exists(file)
        status = "✅" if exists else "❌"
        print(f"{status} {desc} ({file})")
        all_ok = all_ok and exists
    
    return all_ok

def check_test_suite():
    """Check test suite"""
    print("\n🧪 Checking Test Suite:")
    
    try:
        with open('test_suite.py', 'r') as f:
            content = f.read()
        
        required = {
            "Health check": "test_health_check()" in content,
            "Legitimate message": "test_legitimate_message()" in content,
            "High scam score": "test_high_scam_score()" in content,
            "Missing auth": "test_missing_auth()" in content,
            "Invalid key": "test_invalid_api_key()" in content,
            "Missing payload": "test_missing_payload()" in content,
            "Get logs": "test_get_logs()" in content,
            "Unknown endpoint": "test_unknown_endpoint()" in content,
        }
        
        all_ok = True
        for test, result in required.items():
            status = "✅" if result else "❌"
            print(f"{status} {test}")
            all_ok = all_ok and result
        
        return all_ok
    
    except Exception as e:
        print(f"❌ Test suite check failed: {e}")
        return False

def print_summary(checks):
    """Print final summary"""
    print("\n" + "=" * 70)
    passed = sum(1 for c in checks.values() if c)
    total = len(checks)
    
    print(f"✅ Passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED - API IS READY TO RUN")
        print("\nNext steps:")
        print("  1. python main.py          (start server)")
        print("  2. python test_suite.py    (run tests in another terminal)")
        print("  3. Review QUICK_START.md for detailed instructions")
    else:
        print(f"\n⚠️  {total - passed} ISSUE(S) FOUND")
        print("Review errors above and fix them")
    
    print("=" * 70)

def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 10 + "SCAM MESSAGE HONEYPOT API - SETUP VERIFICATION" + " " * 12 + "║")
    print("╚" + "=" * 68 + "╝\n")
    
    checks = {}
    
    # File checks
    print("📁 Checking Project Files:")
    files = {
        "main.py": "Main API implementation",
        "config.py": "Configuration file",
        "test_suite.py": "Test suite",
        "requirements.txt": "Dependencies",
        "README.md": "Documentation",
        "QUICK_START.md": "Quick start guide",
        "TESTING_GUIDE.md": "Testing guide",
        "Honeypot_API_Postman_Collection.json": "Postman collection"
    }
    
    for filename, desc in files.items():
        checks[f"File: {desc}"] = check_file(filename, desc)
    
    # Python check
    print("\n🐍 Checking Python:")
    checks["Python version"] = check_python()
    
    # Import checks
    checks["Dependencies"] = check_imports()
    
    # Configuration check
    checks["Configuration"] = check_config()
    
    # Code check
    checks["Main code"] = check_code()
    
    # Documentation check
    checks["Documentation"] = check_documentation()
    
    # Test suite check
    checks["Test suite"] = check_test_suite()
    
    # Print summary
    print_summary(checks)
    
    return all(checks.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
