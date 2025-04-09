# Locker Management System

A Flask-based application designed for schools and institutions to manage lockers efficiently. This project allows administrators, teachers, and students to manage lockers, assign them, and configure settings within their respective user roles.

---

## Features

- **Admin Features:**
  - Manage users, grade levels, buildings, and lockers.
  - Configure global settings like email options, allowed domains, and RSS feed availability.
  - Flexible user access management.

- **Teacher Features:**
  - Assign lockers to students.
  - Filter and view available lockers by building, floor, or status.
  - Manage locker assignments.

- **Student Features:**
  - View available lockers.
  - Release lockers.

- **Authentication System:**
  - Role-based access control (Admins, Teachers, Students).
  - Password protection and login system.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/locker_app.git
   cd locker_app
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your `.env` file for environment variables such as `SECRET_KEY`, `DATABASE_URI`, and others as needed.

5. Run database migrations:
   ```bash
   flask db upgrade
   ```

6. Start the Flask development server:
   ```bash
   flask run
   ```

---

## Project Structure

'''
locker_app/ │ ├── app/ │ ├── templates/ # HTML Templates │ ├── static/ # Static files (CSS, JS, Images) │ ├── routes/ # Flask Routes │ │ ├── admin.py # Admin-related views and logic │ │ ├── teacher.py # Teacher-related views and logic │ │ └── student.py # Student-related views and logic │ ├── forms.py # Flask-WTForms │ ├── models.py # SQLAlchemy models │ ├── utils.py # Utility functions │ └── **init**.py # Flask application factory │ ├── migrations/ # Database migration scripts ├── .venv/ # Virtual environment (not included in repo) ├── requirements.txt # Python dependencies ├── config.py # App configuration └── README.md # Project documentation
'''
