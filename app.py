"""
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║ NoteVibe – Flask Web Application                                                     ║
║ Purpose: Main entry point defining routes and email handling.                        ║
║ Author: NoteVibe Team | Proprietary License | https://www.notevibe.onrender.com      ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import warnings

# Suppress noisy warnings from python-dotenv when it encounters decorative
# header lines in the .env file. These warnings do not affect functionality
# because only valid KEY=VALUE pairs are loaded; the malformed banner lines
# are safely ignored.
warnings.filterwarnings("ignore", message="Python-dotenv could not parse statement*")

# ── Environment Setup ───────────────────────────────────────────────────────
# Try to import python-dotenv so developers can keep secrets in a local .env
# file. If the package is unavailable (e.g., on production servers configured
# via system env vars) we simply skip loading.
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ModuleNotFoundError:
    # python-dotenv not installed – proceed using existing environment vars.
    pass

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY", os.urandom(24).hex())  # Fallback key

# Email configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Make email address available in all Jinja templates
@app.context_processor
def inject_site_email():
    """Inject the public contact email into every template as 'site_email'."""
    return dict(site_email=EMAIL_ADDRESS)

# ── Logging Configuration ───────────────────────────────────────────────────
# Configure a root logger so that important events are printed to stdout.
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
)

logger = logging.getLogger(__name__)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors by displaying a custom error page."""
    return render_template('404.html'), 404

# Route definitions
@app.route('/')
@app.route('/home')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/services')
def services():
    """Render the services page."""
    return render_template('services.html')

@app.route('/notes')
def notes():
    """Render the notes page with programming resources."""
    return render_template('notes.html')

@app.route('/files/python-note')
def python_note():
    """Render the Python notes page with specific Python resources."""
    return render_template('files/python-note.html')

@app.route('/cheatsheets')
def cheatsheets():
    """Render the cheatsheets page with programming reference materials."""
    return render_template('cheatsheets.html')

@app.route('/interview-prep')
def interview_prep():
    """Render the interview preparation page with resources for technical interviews."""
    return render_template('interview-prep.html')

@app.route('/updates')
def updates():
    """Render the updates page with latest site news and changes."""
    return render_template('updates.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page with contact information and form."""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        # Validate form inputs - all fields required
        if not name or not email or not message:
            flash('All fields are required. Please fill in name, email, and message.', 'error')
            return redirect(url_for('contact'))

        # Verify that email credentials are available before attempting to send
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            flash('Email service is temporarily unavailable. Please try again later.', 'error')
            return redirect(url_for('contact'))

        try:
            # Build email
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS  # Send to owner inbox
            msg['Subject'] = f'New Contact Form Submission from {name}'

            # Format email content as requested
            body = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'
            msg.attach(MIMEText(body, 'plain'))

            # Connect & send using TLS
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            flash('Message sent successfully! We\'ll reach you soon.', 'success')
            logger.info("Contact form submitted by %s <%s>", name, email)

        except smtplib.SMTPAuthenticationError:
            flash('Authentication with the email server failed. Please check server credentials.', 'error')
            logger.exception("SMTP authentication failed when handling contact form.")
        except Exception as e:
            flash('Message sending failed. Please try again later.', 'error')
            logger.exception("Unexpected error while sending contact form email.")

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/about')
def about():
    """Render the about page with information about NoteVibe."""
    return render_template('about.html')

@app.route('/my-gear')
def my_gear():
    """Render the my gear page showing equipment and tools used."""
    return render_template('my-gear.html')

@app.route('/coming-soon')
def coming_soon():
    """Render the coming soon page for features under development."""
    return render_template('coming-soon.html')

@app.route('/terms')
def terms():
    """Render the terms of service page."""
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    """Render the privacy policy page."""
    return render_template('privacy.html')

# Run the application
if __name__ == '__main__':
    # Development server configuration
    # For production deployment, use a WSGI server like Gunicorn
    app.run(debug=True)
    
    # To access from other devices on the network:
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # Run python -m http.server in terminal
    # Visit http://192.168.10.75:5000
