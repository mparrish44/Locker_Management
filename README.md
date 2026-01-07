# AeroSchool: Locker Management & Compliance System

A comprehensive web-based school locker management system built with Flask, designed to streamline locker assignments,
student registrations, sports program management, and administrative tasks.

---

![Locker Management](https://github.com/mparrish44/Locker_Management/blob/main/app/images/new_image.png)

## 🎯 Overview

The Locker Management System provides a complete solution for schools to manage:

- **Student locker assignments** across multiple buildings and floors
- **Sports registration** workflows with approval processes
- **User account management** for students, teachers, parents, and administrators
- **Withdrawal request processing** with detailed tracking
- **Emergency health record** management
- **Pickup authorization** for student releases
- **Transportation and media policy** management
- **System-wide reporting and analytics**
- **Dynamic registration requirements** with weighted completion tracking

[... rest of content ...]

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repository/locker_app.git
   cd Locker_Management
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

4. Set up your `.env` file with environment variables:
   ```bash
   cp .env.example .env
   ```

   Configure your `.env` with:
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URI=postgresql://user:password@localhost:5432/locker_db
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=noreply@school.com
   ```

5. Run database migrations:
   ```bash
   flask db upgrade
   ```

6. Create an admin account:
   ```bash
   flask add-admin
   ```

7. (Optional) Populate sample data:
   ```bash
   flask populate-all
   ```

8. Start the Flask development server:
   ```bash
   flask run
   ```

   The application will be available at `http://localhost:5000`

---

## 📁 Project Structure

```markdown

Locker_Management/
├── app/                          # Main application directory
│   ├── routes/                   # Flask Blueprints (route handlers)
│   │   ├── __init__.py            # Blueprint registration
│   │   ├── admin.py               # Admin dashboard and management
│   │   ├── auth.py                # Authentication and password reset
│   │   ├── teacher.py             # Teacher dashboard and student management
│   │   ├── student.py             # Student forms and registration
│   │   ├── parents.py             # Parent portal and account linking
│   │   └── main.py                # General routes (home, contact, etc.)
│   │
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── base.html              # Base template with navigation
│   │   ├── admin/                 # Admin templates
│   │   ├── teacher/               # Teacher templates
│   │   ├── student/               # Student templates
│   │   ├── parent/                # Parent portal templates
│   │   └── auth/                  # Authentication templates
│   │
│   ├── static/                   # Static assets
│   │   ├── css/                   # Stylesheets (theme.css, custom styles)
│   │   ├── js/                    # JavaScript files
│   │   └── images/                # Images and icons
│   │
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── forms.py                  # WTForms form definitions
│   ├── extensions.py             # Flask extension initialization
│   ├── utils.py                  # Utility functions and decorators
│   ├── commands.py               # Flask CLI commands
│   └── __init__.py               # Application factory
│
├── migrations/                   # Alembic database migrations
├── config.py                     # Configuration classes
├── .env.example                  # Example environment variables
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # Project documentation

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
   Based on the user role, take actions such as assigning or releasing lockers. Filters like building, floor, and locker
   number can aid in searching.

---

## 👤 User Roles & Capabilities

### **Admin**
- Access to admin dashboard with system overview
- Manage all users (create, edit, delete, search, import bulk)
- Configure system settings and email templates
- Manage grade levels, graduation years, buildings, and genders
- Define and manage relationship types (family member types)
- Manage all lockers (add, edit, delete, assign, unassign, bulk operations)
- Manage sports registrations and approvals
- Process and manage all withdrawal requests
- Monitor system-wide activity logs
- Configure form options and policies
- Manage volunteer submissions
- View comprehensive system reports and analytics

### **Teacher**

- View teacher dashboard with student statistics
- Manage student profiles (search, edit, create, delete)
- Assign and unassign lockers to/from students
- View detailed locker inventory and statistics
- Search lockers by student, building, floor, availability status
- Process and approve sports registrations
- Manage student withdrawal requests
- Monitor student registration completion dashboard
- Send targeted bulk notifications to incomplete students
- Export compliance reports in multiple formats (CSV, PDF, bulk ZIP)
- Create and apply custom dashboard filters
- View detailed student quick-view with notification history
- Configure dynamic registration requirements and weights
- Access pickup authorization, emergency health, and transportation reports

### **Student**

- View personal dashboard with completion status
- Submit registration forms (sports, health, pickup, transportation, media)
- Track personal compliance progress percentage
- View locker assignment details
- Download personal compliance report as PDF

### **Parent**

- Access parent portal with child's registration status
- Link account to student record using student ID or email
- Submit required parental consent forms
- View child's completion progress
- Track withdrawal requests
- Receive system notifications about missing requirements

---

## 🛣️ Routes Summary

### Admin Routes

| Method     | Route                                        | Description                          |
|------------|----------------------------------------------|--------------------------------------|
| GET        | `/admin/dashboard`                           | Admin Dashboard with stats           |
| GET/POST   | `/admin/settings`                            | Configure system settings            |
| GET        | `/admin/manage_users`                        | Search and manage all users          |
| POST       | `/admin/add_user`                            | Create new user account              |
| GET/POST   | `/admin/manage_email_templates`              | Configure email templates            |
| GET/POST   | `/admin/manage_relationships`                | Manage relationship types            |
| GET        | `/admin/system_logs`                         | View system activity audit trail     |
| POST       | `/admin/delete_system_log/<id>`              | Delete system log entry              |
| GET/POST   | `/admin/manage_access`                       | Manage user access controls          |
| POST       | `/admin/update_access`                       | Update access permissions            |
| GET/POST   | `/admin/link_parent_to_student`              | Link parent account to student       |
| POST       | `/admin/unlink_account/<id>`                 | Remove parent-student link           |
| POST       | `/admin/unlink_all_accounts`                 | Remove all parent-student links      |
| GET        | `/admin/withdrawals`                         | Manage withdrawal requests           |
| POST       | `/admin/withdrawals/new/<student_id>`        | Create new withdrawal request        |
| POST       | `/admin/withdrawals/<id>/approve`            | Approve withdrawal request           |
| POST       | `/admin/withdrawals/<id>/deny`               | Deny withdrawal request              |
| POST       | `/admin/withdrawals/<id>/restore`            | Restore archived withdrawal          |
| POST       | `/admin/withdrawals/<id>/edit`               | Edit withdrawal details              |
| POST       | `/admin/withdrawals/<id>/archive`            | Archive withdrawal request           |
| GET        | `/admin/withdrawals/<id>/view`               | View withdrawal details              |
| GET        | `/admin/sports-registrations`                | Manage sports registrations          |
| POST       | `/admin/sports-registrations/<id>/approve`   | Approve sports registration          |
| POST       | `/admin/sports-registrations/<id>/reject`    | Reject sports registration           |
| POST       | `/admin/approve-all-sports-registrations`    | Approve all pending registrations    |
| GET        | `/admin/sports-registrations/<id>/view`      | View registration details            |
| POST       | `/admin/sports-registrations/<id>/delete`    | Delete sports registration           |
| GET        | `/admin/completion_dashboard`                | Monitor all student compliance       |
| POST       | `/admin/bulk_nudge`                          | Send bulk notifications              |
| POST       | `/admin/bulk_export_pdf`                     | Export bulk compliance PDFs          |
| GET        | `/admin/registration_settings`               | Configure registration requirements  |
| POST       | `/admin/settings/requirements/delete/<id>`   | Delete requirement                   |
| GET        | `/admin/completion/export`                   | Export compliance roster as CSV      |
| POST       | `/admin/volunteer_submissions`               | View volunteer form submissions      |
| POST       | `/admin/toggle_volunteer_contacted/<id>`     | Mark volunteer as contacted          |

### Teacher Routes

| Method   | Route                                        | Description                            |
|----------|----------------------------------------------|----------------------------------------|
| GET      | `/teacher/dashboard`                         | Teacher Dashboard with stats           |
| GET      | `/teacher/manage_users`                      | Search and manage students             |
| POST     | `/teacher/add_user`                          | Create new student account             |
| GET/POST | `/teacher/assign_locker`                     | Assign locker to student               |
| POST     | `/teacher/unassign_locker/<id>`              | Release locker from student            |
| GET      | `/teacher/view_lockers`                      | View and filter all lockers            |
| GET      | `/teacher/locker_stats`                      | View locker statistics                 |
| GET      | `/teacher/sports-registrations`              | Manage sports registrations            |
| POST     | `/teacher/sports-registrations/<id>/approve` | Approve sports registration            |
| POST     | `/teacher/sports-registrations/<id>/reject`  | Reject sports registration             |
| GET      | `/teacher/dashboard/completion`              | Monitor student compliance             |
| POST     | `/teacher/bulk_nudge`                        | Send bulk notifications                |
| POST     | `/teacher/bulk_export_pdf`                   | Export bulk compliance PDFs            |
| GET      | `/teacher/reports`                           | View pickup, health, transport reports |
| GET      | `/teacher/reports/export/csv`                | Export reports as CSV                  |
| GET      | `/teacher/reports/export/pdf`                | Export reports as PDF                  |
| GET/POST | `/teacher/settings/requirements`             | Configure registration requirements    |

### Student Routes

| Method | Route                                  | Description                  |
|--------|----------------------------------------|------------------------------|
| GET    | `/student/dashboard`                   | Student Dashboard            |
| GET    | `/student/registration`                | Registration forms page      |
| POST   | `/student/submit_sports_registration`  | Submit sports form           |
| POST   | `/student/submit_health_record`        | Submit emergency health form |
| POST   | `/student/submit_pickup_authorization` | Submit pickup authorization  |

### Parent Routes

| Method | Route                      | Description                    |
|--------|----------------------------|--------------------------------|
| GET    | `/parent/dashboard`        | Parent Portal Dashboard        |
| GET    | `/parent/unlinked_account` | Account linking page           |
| POST   | `/parent/link_account`     | Link parent to student         |
| GET    | `/parent/student/<id>`     | View student compliance status |

### Authentication Routes

| Method   | Route                     | Description               |
|----------|---------------------------|---------------------------|
| GET/POST | `/login`                  | User login                |
| GET/POST | `/register`               | User registration         |
| GET/POST | `/forgot_password`        | Password reset request    |
| GET/POST | `/reset_password/<token>` | Password reset with token |
| GET      | `/logout`                 | User logout               |

---

## 📊 Key Features

### Locker Management System

- **Multi-Building Inventory**: Manage lockers across multiple school buildings
- **Floor & Location Tracking**: Organize by floor and locker number
- **Real-Time Status**: Available, assigned, or maintenance status
- **Assignment History**: Track assignment dates and student history
- **Advanced Search**: Filter by building, floor, student name, or ID
- **Bulk Operations**: Assign/unassign multiple lockers efficiently
- **Analytics Dashboard**: Occupancy percentage, availability trends

### Student Registration & Compliance

- **Dynamic Requirements**: Configurable form requirements with weighted importance
- **Automatic Completion Calculation**: Real-time progress percentage based on weights
- **Multi-Step Forms**:
    - Emergency Health Records
    - Sports Registration
    - Pickup Authorization
    - Transportation Records
    - Media Policy Release
- **Current vs. Historical**: Track current and previous records
- **Compliance Dashboard**: Visual progress for all students with filtering/sorting

### Sports Registration Workflow

- **Status Tracking**: Pending → Approved/Rejected
- **Health Record Integration**: Cross-reference emergency health records
- **Bulk Approval**: Approve all pending registrations at once
- **Detailed Reporting**: Export rosters with student details and EHR status
- **Multi-Format Export**: CSV and PDF report generation

### Withdrawal Processing

- **Multi-Status Workflow**: Pending → Approved/Denied → Completed/Archived
- **Status Toggling**: Deactivate/activate withdrawal requests
- **Historical Archive**: Restore archived withdrawals if needed
- **Audit Trail**: Complete tracking of who approved/denied and when

### Reporting & Export Capabilities

- **Completion Dashboard**: Real-time student compliance monitoring
    - Filter by grade, graduation year, completion status, missing requirements
    - Sort by name or completion percentage
    - Quick-view modal with notification history
    - Custom saveable dashboard filters
- **Multi-Format Exports**:
    - CSV for spreadsheet analysis
    - Individual PDF compliance reports
    - Bulk ZIP archives of multiple PDFs
- **Report Types**:
    - Pickup Authorization Reports
    - Emergency Health Records
    - Transportation Records
    - Sports Registration Rosters
    - Student Compliance Roster

### Notification & Audit System

- **Targeted Notifications**: Send to incomplete students or parents
- **Bulk Nudge**: Notify multiple students matching filter criteria
- **Notification Audit Log**: Track who sent what and when
- **Student Quick-View History**: See recent notifications sent to each student
- **System Activity Log**: Complete audit trail of all actions with IP tracking

### Email Template Management

- **Customizable Templates**: Create and edit email templates
- **Template Variables**: Support for dynamic variable substitution
- **SMTP Configuration**: Gmail or other SMTP providers supported

---

## 📊 Database Models

### Core Models

- **User** - Students, teachers, parents, admins with roles
- **RoleEnum** - Role types (ADMIN, TEACHER, STUDENT, PARENT)
- **Locker** - Physical locker inventory
- **Building** - School buildings with sort order
- **GradeLevel** - Grade levels (9th, 10th, etc.)
- **GraduationYear** - Graduation years
- **Season** - Sports seasons (Fall, Winter, Spring)
- **Sport** - Available sports programs

### Registration & Compliance Models

- **RegistrationRequirement** - Dynamic form requirements with weights
- **SportsRegistration** - Sports program registrations with approval
- **EmergencyHealthRecord** - Medical information and allergies
- **PickupAuthorization** - Authorized pickup contacts (JSON-stored)
- **TransportationRecord** - AM/PM transportation methods and routes
- **MediaPolicyRelease** - Media consent acknowledgments

### Relationship & Tracking Models

- **Relationship** - Family relationship types (Parent, Guardian, etc.)
- **WithdrawalRequest** - Student withdrawal requests with status tracking
- **NotificationLog** - Audit trail for all notifications sent
- **SystemLog** - Complete activity audit with IP tracking
- **SavedFilter** - User-saved dashboard filter configurations
- **TeacherFilter** - Teacher-specific saved filters

---

## 🎨 Frontend Features

### Responsive Design

- Mobile-first responsive layout
- Bootstrap 5 framework for UI components
- Accessible color scheme (WCAG AAA compliant)
- Colorblind-friendly design using CSS variables

### Accessibility

- WCAG AA/AAA compliant colors
- Keyboard navigation support
- Screen reader friendly
- Proper semantic HTML
- Form validation with error messages

### User Interface Components

- Interactive data tables with sorting/filtering
- Modal dialogs for confirmations
- Pagination controls
- Progress indicators
- Status badges
- Search and filter dropdowns
- Export buttons (CSV, PDF, ZIP)

---

## 🐛 Recent Updates & Bug Fixes

### Version 1.0 - Current Release

#### New Features

- Dynamic, configurable registration requirements with weight-based completion
- Targeted bulk notification system with audit logging
- Enhanced completion dashboard with filtering and custom saved views
- Comprehensive reporting suite (CSV, PDF, bulk ZIP export)
- Student quick-view modal with notification history
- Parent account linking and portal access

#### Bug Fixes

- **Fixed**: Pickup authorization export now correctly reads from the `name` column instead of `authorized_list_json`
  field in both CSV and PDF exports
- **Fixed**: Search functionality expanded in Teacher User Management for full name matching
- **Fixed**: Numeric building sort order now consistent across locker views
- **Fixed**: Sports registration export respects all active UI filters

#### Improvements

- Enhanced teacher search functionality across all student management pages
- Improved locker assignment interface with building-specific filtering
- Better error handling and user feedback on form submissions
- Audit logging added to all major administrative actions

---

## 📝 Template Overview

### Layout Templates

- `base.html` - Main layout with navigation bar
- `admin/base.html` - Admin section layout
- `teacher/base.html` - Teacher section layout
- `student/base.html` - Student section layout
- `parent/base.html` - Parent portal layout

### Admin Templates

- `admin/dashboard.html` - Admin overview and statistics
- `admin/manage_users.html` - User search and management
- `admin/add_user.html` - User creation form
- `admin/edit_user.html` - User editing form
- `admin/email_templates.html` - Email template CRUD
- `admin/manage_relationships.html` - Relationship type management
- `admin/settings.html` - System settings configuration

### Teacher Templates

- `teacher/dashboard_teacher.html` - Teacher overview with stats
- `teacher/manage_users.html` - Student search and management
- `teacher/add_user.html` - Student account creation
- `teacher/edit_user.html` - Student profile editing
- `teacher/assign_locker.html` - Locker assignment interface
- `teacher/view_lockers.html` - Locker inventory with filters
- `teacher/locker_stats.html` - Locker statistics and trends
- `teacher/completion_dashboard.html` - Student compliance tracking
- `teacher/manage_sports_registrations.html` - Sports approval workflow
- `teacher/view_sports_registration.html` - Detailed registration view
- `teacher/withdrawal_requests.html` - Withdrawal request processing
- `teacher/reports.html` - Multi-tab reporting interface
- `teacher/registration_settings.html` - Dynamic requirement configuration

### Student Templates

- `student/dashboard_student.html` - Student overview
- `student/registration.html` - Multi-form registration page
- `student/locker_info.html` - Locker assignment details

### Parent Templates

- `parent/dashboard.html` - Parent portal overview
- `parent/unlinked_account.html` - Account linking interface
- `parent/student_profile.html` - Child's compliance status view

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to get started:

1. Fork the repository on GitHub
2. Create your feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and test thoroughly
4. Commit your changes with clear messages:
   ```bash
   git commit -m "Add feature: [description of changes]"
   ```
5. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Open a Pull Request with a detailed description of your changes

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Include docstrings for functions and classes
- Write tests for new features
- Comment complex logic

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for full details.

---

## 🚀 Future Enhancements

- **Real-Time Notifications**: WebSocket-based push notifications
- **SMS Integration**: Text message notifications for urgent alerts
- **Advanced Analytics**: Trend analysis and predictive compliance reporting
- **Single Sign-On (SSO)**: Google, Microsoft, and SAML integration
- **Mobile App**: Native iOS and Android applications
- **QR Code Access**: QR code-based locker access control
- **Automated Backups**: Scheduled database backups and disaster recovery
- **Integration APIs**: RESTful API for third-party integrations
- **Biometric Access**: Fingerprint/facial recognition locker access
- **Multi-Language Support**: Internationalization for diverse student populations

---

## 📞 Support & Issues

### Getting Help

- **Documentation**: Check the project README and inline code comments
- **Issues**: Search existing GitHub issues or create a new one
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact the development team at support@school.com

### Reporting Bugs

When reporting bugs, please include:

1. Steps to reproduce the issue
2. Expected vs. actual behavior
3. Screenshots or error messages
4. Your environment (OS, Python version, etc.)

---

## 🏫 Schools Using This System

*Add your school here by submitting a PR or issue*

---

## 👨‍💻 Development Team

- **Project Lead**: [Your Name]
- **Contributors**: [List contributors here]

---

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [WTForms Documentation](https://wtforms.readthedocs.io/)
- [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)

---

**Happy Locker Management! 🚪**

*Last Updated: January 2026*
