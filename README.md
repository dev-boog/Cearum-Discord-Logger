# Webserver Discord Logger

A Flask-based web dashboard and Discord selfbot logger for tracking and displaying deleted messages from Discord servers. Features a modern UI, configuration page, and persistent message logging to a SQLite database.

---

## Features
- Logs deleted messages from Discord (selfbot)
- Web dashboard with live stats and message previews
- Configuration page for logger options
- SQLite database for persistent storage
- Modern UI with Tailwind CSS and HTMX

---

## Setup Instructions

### 1. Clone the Repository
```
git clone <your-repo-url>
cd WebserverDiscordLogger/Prototyping
```

### 2. Create and Activate a Virtual Environment
```
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configuration
- Edit `config.json` to set your Discord token and logger options.
- Example options:
  - `log_deleted_messages`: Enable/disable logging
  - `ignore_bots`: Ignore bot messages
  - `ignore_self`: Ignore your own messages

### 5. Run the Application
```
python app.py
```
- The dashboard will be available at `http://localhost:5420` (or your configured port).

---

## File Guide

- `app.py` — Main Flask app and webserver
- `config.json` — Configuration for Discord token and logger settings
- `database/db_manager.py` — Handles all database operations (SQLite)
- `logger/discord_logger.py` — Discord selfbot client and event handlers
- `templates/` — HTML templates for dashboard and configuration
  - `dashboard.html` — Main dashboard UI
  - `configuration.html` — Logger configuration UI
  - `error.html` — Error display page
- `static/theme.css` — Custom CSS theme

---

## Notes
- This project uses a Discord selfbot, which is against Discord's Terms of Service. Use at your own risk.
- For development only. Do not use on production Discord accounts.

---

## License
MIT License
