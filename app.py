"""
╔════════════════════════════════════════════════════════════════════════════╗
║ NoteVibe - Main Flask Application                                        ║
║ Purpose: Application factory, route registration, and global config.     ║
║ Author: NoteVibe Team                                                    ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import logging
import os
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, flash, redirect, render_template, request, url_for

# ── Load environment variables in development ─────────────────────────────
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ModuleNotFoundError:
    pass
warnings.filterwarnings(
    "ignore", message="Python-dotenv could not parse statement*"
)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ╔════════════════════════════════════════════════════════════════════════════╗
# ║ Application Factory                                                      ║
# ╚════════════════════════════════════════════════════════════════════════════╝
def create_app() -> Flask:
    """Application-factory that builds and configures a Flask instance."""

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # ── Configuration ───────────────────────────────────────────────────
    app.config.update(
        SECRET_KEY=os.getenv("APP_SECRET_KEY", os.urandom(24).hex()),
    )

    # ── Logging setup ──────────────────────────────────────────────────
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO").upper(),
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    )

    # ╔════════════════════════════════════════════════════════════════════╗
    # ║ Application Routes                                               ║
    # ╚════════════════════════════════════════════════════════════════════╝

    @app.errorhandler(404)
    def page_not_found(e):
        """Render a custom 404 error page."""
        return render_template("404.html"), 404

    # ── Home Page ──────────────────────────────────────────────────────
    @app.route("/")
    @app.route("/home")
    def home():
        """Render the home page."""
        return render_template("home.html")

    # ── Services Page ──────────────────────────────────────────────────
    @app.route("/services")
    def services():
        """Render the services page."""
        return render_template("services.html")

    # ── Notes Page ─────────────────────────────────────────────────────
    @app.route("/notes")
    def notes():
        """Render the notes page."""
        return render_template("notes.html")

    # ── Python Note File ───────────────────────────────────────────────
    @app.route("/files/python-note")
    def python_note():
        """Render a specific note page."""
        return render_template("files/python-note.html")

    # ── Cheatsheets Page ───────────────────────────────────────────────
    @app.route("/cheatsheets")
    def cheatsheets():
        """Render the cheatsheets page."""
        return render_template("cheatsheets.html")

    # ── Interview Prep Page ────────────────────────────────────────────
    @app.route("/interview-prep")
    def interview_prep():
        """Render the interview preparation page."""
        return render_template("interview-prep.html")

    # ── Updates Page ───────────────────────────────────────────────────
    @app.route("/updates")
    def updates():
        """Render the updates page."""
        return render_template("updates.html")

    # ── Contact Page & Form ────────────────────────────────────────────
    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        """Handle contact form submissions and render the contact page."""
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            message = request.form.get("message", "").strip()

            if not all([name, email, message]):
                flash("All fields are required. Please fill in name, email, and message.", "error")
                return redirect(url_for("contact"))

            if not all([EMAIL_ADDRESS, EMAIL_PASSWORD]):
                flash("Email service is temporarily unavailable.", "error")
                return redirect(url_for("contact"))

            try:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_ADDRESS
                msg["To"] = EMAIL_ADDRESS
                msg["Subject"] = f"Contact form – {name}"
                msg.attach(MIMEText(f"Name: {name}\nEmail: {email}\n\n{message}", "plain"))

                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(msg)

                flash("Message sent!", "success")
            except smtplib.SMTPAuthenticationError:
                flash("Email authentication failed. Please check your email credentials.", "error")
            except smtplib.SMTPException as smtp_error:
                logging.exception("SMTP error occurred: %s", smtp_error)
                flash("Failed to send message due to an SMTP error. Please try again later.", "error")
            except Exception as general_error:
                logging.exception("Unexpected error while sending contact email: %s", general_error)
                flash("An unexpected error occurred. Please try again later.", "error")

            return redirect(url_for("contact"))

        return render_template("contact.html")

    # ── About Page ──────────────────────────────────────────────────────
    @app.route("/about")
    def about():
        """Render the about page."""
        return render_template("about.html")

    # ── My Gear Page ────────────────────────────────────────────────────
    @app.route("/my-gear")
    def my_gear():
        """Render the my gear page."""
        return render_template("my-gear.html")

    # ── Coming Soon Page ────────────────────────────────────────────────
    @app.route("/coming-soon")
    def coming_soon():
        """Render the coming soon page."""
        return render_template("coming-soon.html")

    # ── Terms Page ─────────────────────────────────────────────────────
    @app.route("/terms")
    def terms():
        """Render the terms and conditions page."""
        return render_template("terms.html")

    # ── Privacy Page ───────────────────────────────────────────────────
    @app.route("/privacy")
    def privacy():
        """Render the privacy policy page."""
        return render_template("privacy.html")

    # ── Global Error Handler ───────────────────────────────────────────
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected errors with a generic error page."""
        logging.exception("Unhandled Exception: %s", e)
        return render_template("404.html"), 500

    # ── Shell Context for Flask CLI ────────────────────────────────────
    @app.shell_context_processor
    def _make_shell_context():  # pragma: no cover
        """Provide shell context for Flask CLI."""
        return dict(app=app)

    return app


# ---------------------------------------------------------------------------
# Local development entry-point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    create_app().run(debug=True)
