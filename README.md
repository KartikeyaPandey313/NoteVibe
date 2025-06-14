# NoteVibe

![NoteVibe Logo](static/images/logo.ico)

A modern Flask web application providing programming resources, notes, and community support.

---

## Features
- Home, About, Services, Notes, Cheatsheets, Interview Prep, Updates, Contact, My Gear, and Coming Soon pages
- Custom 404 error page
- Organized project structure with templates and static files
- Easy to extend and customize

## Project Structure
See `structure.txt` for a detailed overview.

## Setup Instructions
1. **Clone the repository**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python app.py
   ```
4. **Open your browser** and visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Usage
- Browse the site for programming notes, cheatsheets, and resources
- Use the navigation bar to access different sections

## Logo
The project logo is shown above. To use it in your site:
1. Save the provided logo image as `logo.ico`
2. Place it in the `static/images/` directory
3. Reference it in your HTML templates as:
   ```html
   <img src="{{ url_for('static', filename='images/logo.ico') }}" alt="NoteVibe Logo">
   ```

---

**Author:** NoteVibe Team

For more details, see the source code and comments in `app.py`. 