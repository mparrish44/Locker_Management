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

```markdown

locker_app/
│
├── app/                        # Main application directory
│   ├── templates/              # HTML Templates
│   ├── static/                 # Static files (CSS, JS, Images)
│   ├── routes/                 # Flask Routes
│   │   ├── admin.py            # Admin-related views and logic
│   │   ├── teacher.py          # Teacher-related views and logic
│   │   └── student.py          # Student-related views and logic
│   ├── forms.py                # Flask-WTForms
│   ├── models.py               # SQLAlchemy models
│   ├── utils.py                # Utility functions
│   └── __init__.py             # Flask application factory
│
├── migrations/                 # Database migration scripts
├── .venv/                      # Virtual environment (not included in repo)
├── requirements.txt            # Python dependencies
├── config.py                   # App configuration
└── README.md                   # Project documentation
```

---

## How to Use

1. **Login as a user:**
   - Admin: Access the admin dashboard and manage the system.
   - Teacher: Assign, release, or filter lockers assigned to students.
   - Student: Reserve or release lockers.

2. **Add Users and Grade Levels:**  
   Admins can use forms provided in the respective views to add users and grade levels. Ensure correct input validation.

3. **Locker Management:**  
   Based on the user role, take actions such as assigning or releasing lockers. Filters like building, floor, and locker number can aid in searching.

---

## Routes Summary

### Admin Routes
| Method | Route                            | Description                  |
|--------|----------------------------------|------------------------------|
| GET    | `/admin/settings`               | View/Update application settings |
| POST   | `/admin/add_user`               | Add a new user               |
| POST   | `/admin/add_grade_level`        | Add a new grade level        |
| GET    | `/admin/manage_users`           | Manage existing users        |
| GET    | `/admin/manage_graduation_years`| Manage graduation years      |

### Teacher Routes
| Method | Route                            | Description                  |
|--------|----------------------------------|------------------------------|
| GET    | `/teacher/dashboard`            | Teacher Dashboard            |
| GET    | `/teacher/view_lockers`         | View available lockers       |
| POST   | `/teacher/assign_locker`        | Assign a locker to a student |

### Student Routes
| Method | Route                            | Description                  |
|--------|----------------------------------|------------------------------|
| GET    | `/student/available_lockers`    | View available lockers       |
| POST   | `/student/release_locker`       | Release a locker             |

---

## Templates Overview

Some key templates used in the project:
- **Admin:**
  - `admin/settings.html` - Configure email settings, RSS feeds, and allowed domains.
  - `admin/manage_users.html` - Manage registered users.
  - `admin/add_grade_level.html` - Add new grade levels.

- **Teacher:**
  - `teacher/view_lockers.html` - View and filter locker assignments.
  - `teacher/register_teacher.html` - Teacher registration form.

- **Student:**
  - `student/available_lockers.html` - View and claim available lockers.

---

## Contributing

1. Fork the project.
2. Create your feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add some feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

---

## Future Enhancements

- Enable real-time notifications for admins when actions are performed.
- Add a reporting module for locker usage and availability.
- Integration with external authentication providers.

---

## Contact

For any queries or issues, feel free to contact:  
Email: [admin@example.com](mailto:admin@example.com)

---

Happy Locker Management 🚪!
