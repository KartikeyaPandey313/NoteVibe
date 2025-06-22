#!/usr/bin/env python3
"""
Test script for NoteVibe contact form functionality
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()  # load .env like a boss

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import flask
        print("✓ Flask imported successfully")

        import smtplib
        print("✓ smtplib imported successfully")

        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        print("✓ email.mime modules imported successfully")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_env_vars():
    """Test if environment variables are properly configured"""
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    if email_address and email_password:
        print("✓ Email credentials found in environment")
        return True
    else:
        print("⚠ Email credentials not found in environment")
        print("  Make sure you have a .env file with:")
        print("  EMAIL_ADDRESS=your-email@gmail.com")
        print("  EMAIL_PASSWORD=your-app-password")
        return False

def test_app_import():
    """Test if the Flask app can be imported"""
    try:
        from app import app  # make sure 'app.py' has 'app = Flask(__name__)'
        print("✓ Flask app imported successfully")

        routes = [str(rule) for rule in app.url_map.iter_rules()]
        if '/contact' in routes:
            print("✓ Contact route found")
            return True
        else:
            print("✗ Contact route not found")
            return False
    except Exception as e:
        print(f"✗ App import error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing NoteVibe Contact Form Setup")
    print("=" * 40)

    tests = [
        test_imports,
        test_env_vars,
        test_app_import
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("🎉 All tests passed! Contact form should work correctly.")
    else:
        print("⚠ Some tests failed. Fix them up, code ninja.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
