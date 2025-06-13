"""
NoteVibe - Flask Web Application
--------------------------------
A modern web application providing programming resources, notes, and community support.

This file serves as the main entry point for the Flask application, defining routes
and handling HTTP requests for all pages of the NoteVibe website.

Author: NoteVibe Team
Version: 1.0.0
"""

from flask import Flask, render_template

# Initialize Flask application
app = Flask(__name__)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors by displaying a custom error page."""
    return render_template('404.html'), 404

# Route definitions
@app.route('/')
@app.route('/home.html')  
def home():
    """Render the home page."""
    return render_template("home.html")

@app.route('/services.html')
def services():
    """Render the services page."""
    return render_template("services.html")

@app.route('/notes.html')
def notes():
    """Render the notes page with programming resources."""
    return render_template("notes.html")

@app.route('/files/python-note.html')
def python_note():
    """Render the Python notes page with specific Python resources."""
    return render_template("files/python-note.html")

@app.route('/cheatsheets.html')
def cheatsheets():
    """Render the cheatsheets page with programming reference materials."""
    return render_template("cheatsheets.html")

@app.route('/interview-prep.html')
def interview_prep():
    """Render the interview preparation page with resources for technical interviews."""
    return render_template("interview-prep.html")

@app.route('/updates.html')
def updates():
    """Render the updates page with latest site news and changes."""
    return render_template("updates.html")

@app.route('/contact.html')
def contact():
    """Render the contact page with contact information and form."""
    return render_template("contact.html")

@app.route('/about.html')
def about():
    """Render the about page with information about NoteVibe."""
    return render_template("about.html")

@app.route('/my-gear.html')
def my_gear():
    """Render the my gear page showing equipment and tools used."""
    return render_template("my-gear.html")

@app.route('/comming-soon.html')
def coming_soon():
    """Render the coming soon page for features under development."""
    return render_template("comming-soon.html")

# Run the application
if __name__ == '__main__':
    # Development server configuration
    # For production deployment, use a WSGI server like Gunicorn
    app.run(debug=True)
    
    # To access from other devices on the network:
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # Run python -m http.server in terminal
    # Visit http://192.168.10.75:5000
