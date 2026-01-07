# Forms, Registartion and Compliance System

A comprehensive, enterprise-grade web-based platform designed to modernize and streamline the complete student lifecycle management for K-12 schools.

---

![Locker Management](https://github.com/mparrish44/Locker_Management/blob/main/app/images/new_image.png)

## 🎯 Overview

**Locker Management System** is a comprehensive, enterprise-grade web-based platform designed to modernize and streamline the complete student lifecycle management for K-12 schools. Built with Flask and PostgreSQL, this system eliminates manual processes and spreadsheet-based workflows by providing an integrated solution for locker assignments, student registration, compliance tracking, and administrative oversight.

### What It Does

The platform serves as the **central hub for student operations**, enabling seamless coordination between students, teachers, parents, and administrators. Rather than juggling multiple systems, schools can now manage:

- **Locker Assignment & Inventory Management** - Assign and track student lockers across multiple buildings with real-time availability status, accessibility features, and combination storage
- **Student Registration & Compliance** - Collect and track mandatory student registrations (emergency health records, sports participation, pickup authorization, transportation methods, media policies) with automatic progress calculation and deadline tracking
- **Sports Program Management** - Streamline the sports registration workflow with built-in approval processes, health record integration, and roster generation
- **Withdrawal Processing** - Manage student withdrawals from start to finish with multi-stage approval workflows, denial reasons, and archival capabilities
- **Parent Engagement** - Provide parents with their own portal where they can link accounts, submit required forms, and monitor their child's compliance status
- **Reporting & Analytics** - Generate comprehensive reports in multiple formats (CSV, PDF) with advanced filtering, sorting, and compliance dashboards

### Key Benefits

**For Administrators:**
- Centralized control over all school operations, from user management to locker inventory
- Real-time visibility into system-wide compliance status
- Bulk import/export capabilities for large-scale operations
- Complete audit trail of all actions for accountability and compliance

**For Teachers:**
- Quick student management and locker assignment without admin overhead
- Instant view of compliance status across their class rosters
- Ability to send targeted notifications to students with missing requirements
- Access to detailed reports on pickup authorizations, health records, and transportation

**For Students:**
- Single dashboard showing their locker assignment and compliance progress
- Simple form submission for all required registrations
- Real-time percentage tracking toward complete registration
- Ability to release and manage their own locker assignment

**For Parents:**
- Secure account linking to their child's record
- One-stop shop for submitting parental consent forms
- Visibility into child's compliance progress and missing requirements
- Notification system for required actions

### Why This Matters

Schools spend hundreds of hours manually managing lockers, collecting form signatures, and tracking compliance. Multiple spreadsheets, paper forms, and email chains create inefficiencies, increase errors, and make it impossible to see the complete picture. The Locker Management System eliminates this administrative burden by providing:

- **Automation** - Automatic email notifications, progress calculation, and workflow routing
- **Data Integrity** - Centralized database prevents duplicate entries and conflicting information
- **Compliance** - Built-in audit logging ensures accountability for every action
- **Accessibility** - Role-based access means each user only sees what they need
- **Scalability** - Handles schools of any size, from 500 to 5,000+ students

### Technology Stack

- **Backend**: Flask (Python) with SQLAlchemy ORM
- **Database**: PostgreSQL (production) or SQLite (development)
- **Frontend**: Jinja2 templates, Bootstrap 5, responsive design
- **Features**: User authentication, role-based access control, email integration, PDF/CSV export, real-time filtering
- **Deployment**: Docker-ready, cloud-compatible (AWS, Azure, etc.)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL database (or SQLite for development)
- pip package manager

### Installation

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
## 📖 How to Use

### 1. **Login as a User**

#### Admin
- Access the comprehensive admin dashboard with system-wide statistics and oversight
- Manage all user accounts (create, edit, delete, search, bulk import)
- Configure system settings, email templates, and form options
- Manage school buildings, grade levels, graduation years, and other organizational data
- Oversee all locker assignments and inventory across the school
- Process and monitor all sports registrations, withdrawal requests, and compliance status
- View complete system audit logs and activity reports
- Send bulk emails to any user group
- Set up and manage volunteer submissions and tracking

#### Teacher
- Access the teacher dashboard with quick statistics on students and lockers
- Search, create, edit, and manage student profiles and accounts
- Assign and unassign lockers to/from students with building and floor filtering
- View detailed locker inventory with advanced search and filtering capabilities
- Review and approve/reject sports registration submissions
- Process student withdrawal requests with approval/denial workflows
- Monitor the student compliance dashboard to track registration progress
- Send targeted bulk notifications to students with incomplete registrations
- Export compliance reports in multiple formats (CSV, PDF, or bulk ZIP archives)
- Configure dynamic registration requirements and set completion weights
- Access multi-tab reports for pickup authorizations, emergency health records, and transportation data

#### Student
- Access the personal student dashboard showing completion status and locker assignment
- Submit required registration forms (sports, emergency health, pickup authorization, transportation, media policy)
- Track personal compliance progress with a real-time percentage indicator
- View assigned locker details including building, floor, and locker number
- Download a personal PDF compliance report
- Release an assigned locker when no longer needed

#### Parent
- Access the parent portal to monitor child's registration status
- Link parent account to student record using student ID or email address
- Submit required parental consent and permission forms on behalf of the student
- View child's compliance progress and completion percentage
- Track withdrawal requests initiated by the school
- Receive and respond to system notifications about missing form requirements
- Monitor which forms have been completed and which are still pending

---

### 2. **Add Users and Grade Levels**

#### Admin User Management
- **Create New Users**: Use `/admin/add_user` to create accounts for students, teachers, parents, or admins
  - Specify name, email, role, and role-specific details (student ID, grade level, etc.)
  - System automatically generates a temporary password and sends password reset email
  - Validate all required fields before submission

- **Bulk Import Users**: Use `/admin/import_users` to upload a CSV file with multiple user records
  - CSV format: name, email, role, student_id (for students), grade_level, graduation_year
  - Significantly faster than individual account creation for large groups
  - System validates each row and reports any errors during import

- **Add Grade Levels**: Navigate to `/admin/grade_levels` to manage school grade levels
  - Create new grades (9th, 10th, 11th, 12th, etc.)
  - Set sort order for display across the system
  - Activate or deactivate grades as needed
  - Ensure correct input validation (no duplicate names, proper sorting)

- **Add Graduation Years**: Go to `/admin/graduation_years` to configure cohort years
  - Add years for each student class (e.g., Class of 2025, 2026, etc.)
  - Set display order and activate/deactivate as needed

- **Add Buildings**: Access `/admin/manage_buildings` to set up school building locations
  - Create building records with names and sort order
  - Organize by numeric sort (Building 1, 2, 3, etc.)
  - Buildings are used when assigning and filtering lockers

#### Teacher User Management
- **Create Student Accounts**: Teachers can add new student accounts via `/teacher/add_user`
  - Fill in first name, last name, email, and student ID
  - Assign grade level and graduation year
  - System sends account activation email to the student

- **Edit Student Profiles**: Update student information via `/teacher/edit_user/<id>`
  - Modify names, email, student ID, grade level, and graduation year
  - Changes are immediately reflected in the system

---

### 3. **Locker Management**

#### Admin Locker Management
- **Add New Lockers**: Navigate to `/admin/add_locker` to create individual locker records
  - Specify building, floor, locker number, section, size, and accessibility
  - Store locker combination/access code for reference
  - Lockers are unassigned by default and ready for assignment

- **Manage Locker Inventory**: Use `/admin/manage_lockers` to view, search, and filter all lockers
  - Filter by building, floor, status (available/assigned), or search by student name
  - Assign lockers to students using the modal dialog
  - Unassign lockers to return them to available status
  - Edit locker details (location, size, accessibility, combination)
  - Delete lockers no longer in use
  - View assignment date and currently assigned student

- **Bulk Operations**: 
  - **Assign Multiple**: Use bulk assign to quickly assign multiple lockers via dropdown selection
  - **Import via CSV**: Upload a CSV file with locker and student data for batch assignments
  - **Reset All**: Quickly unassign all lockers at once (useful at end of school year)

- **View Statistics**: Access `/admin/locker_stats` for comprehensive locker analytics
  - Total lockers, assigned count, available count, and occupancy percentage
  - Building-by-building breakdown with specific counts
  - Recent assignment history with dates and student information

#### Teacher Locker Management
- **Assign Lockers**: Go to `/teacher/assign_locker` to assign a locker to a student
  - Search for unassigned students by name, email, or student ID
  - Filter available lockers by building to narrow down options
  - Select student and locker, then confirm assignment
  - System records assignment date and student relationship

- **View Locker Inventory**: Access `/teacher/view_lockers` to see all locker assignments
  - Filter by status (all/available/assigned), building, floor, or student
  - Fast-find search for lockers by assigned student name or student ID
  - See assignment dates and assigned student information
  - Unassign lockers individually when students leave or change lockers
  - Lockers are sorted by building (numeric order) and floor for easy scanning

- **Release Lockers**: Click "Unassign" next to assigned lockers to make them available again
  - Removes student assignment and clears the assignment date
  - Locker immediately becomes available for reassignment

- **View Statistics**: Navigate to `/teacher/locker_stats` for locker analytics
  - View occupancy statistics and trends
  - See building-by-building breakdown
  - View recent assignments history
  - Track available locker counts

#### Student Locker Management
- **View Assigned Locker**: Students can see their assigned locker on the dashboard
  - Shows building name, floor, locker number
  - Displays locker combination/access code if provided
  - View accessibility features if locker is ADA compliant

- **Release Locker**: Students can release their locker via the `/student/dashboard`
  - One-click release button to remove assignment
  - Locker becomes available for another student
  - Release action is logged in system audit trail

---

### Key Tips for All Roles

**Search & Filter Best Practices:**
- Use the search fields to quickly find specific users, lockers, or registrations
- Combine multiple filters (e.g., building + floor + status) for precise results
- Clear filters to reset and view all records

**Bulk Operations:**
- Always review selections before performing bulk actions
- Bulk actions are logged for audit and compliance purposes
- Use "Select All Filtered" to apply actions to all matching records across all pages

**Data Validation:**
- Ensure email addresses are unique (no duplicates allowed)
- Student IDs should follow your school's naming convention
- Building and floor numbers should be consistent for easy navigation

**User Account Management:**
- First-time users receive password reset emails with account activation links
- Teachers and admins can create accounts for multiple roles
- Deleted accounts cannot be recovered; consider archiving instead if possible

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
| Method | Route                                      | Description                         |
|--------|--------------------------------------------|------------------------------------|
| GET    | `/admin/dashboard`                         | Admin Dashboard with stats          |
| GET/POST | `/admin/settings`                        | Configure system settings           |
| GET    | `/admin/manage_users`                      | Search and manage all users         |
| POST   | `/admin/add_user`                          | Create new user account             |
| GET/POST | `/admin/edit_user/<id>`                  | Edit existing user profile          |
| POST   | `/admin/delete_user/<id>`                  | Delete user account                 |
| POST   | `/admin/import_users`                      | Bulk import users from CSV          |
| POST   | `/admin/add_admin_user`                    | Create new admin account            |
| GET/POST | `/admin/manage_relationships`            | Manage relationship types           |
| POST   | `/admin/add_relationship`                  | Create new relationship type        |
| GET/POST | `/admin/edit_relationship/<id>`          | Edit relationship type              |
| POST   | `/admin/delete_relationship/<id>`         | Delete relationship type            |
| GET    | `/admin/manage_lockers`                    | View and search all lockers         |
| POST   | `/admin/bulk_assign`                       | Assign locker to student            |
| POST   | `/admin/bulk_assign_csv`                   | Bulk assign lockers from CSV        |
| POST   | `/admin/add_locker`                        | Create new locker                   |
| GET/POST | `/admin/edit_locker/<id>`                | Edit locker details                 |
| POST   | `/admin/delete_locker/<id>`                | Delete locker                       |
| POST   | `/admin/assign_locker/<id>`                | Assign locker to specific student   |
| POST   | `/admin/unassign_locker/<id>`              | Release locker from student         |
| POST   | `/admin/reset_all_lockers`                 | Unassign all lockers at once        |
| GET/POST | `/admin/manage_buildings`                | Manage school buildings             |
| POST   | `/admin/add_building`                      | Add new building                    |
| GET/POST | `/admin/edit_building/<id>`              | Edit building information           |
| POST   | `/admin/delete_building/<id>`              | Delete building                     |
| GET    | `/admin/grade_levels`                      | Manage grade levels                 |
| POST   | `/admin/add_grade_level`                   | Add new grade level                 |
| GET/POST | `/admin/edit_grade_level/<id>`           | Edit grade level                    |
| POST   | `/admin/delete_grade_level/<id>`           | Delete grade level                  |
| GET    | `/admin/graduation_years`                  | Manage graduation years             |
| POST   | `/admin/add_graduation_year`               | Add new graduation year             |
| GET/POST | `/admin/edit_graduation_year/<id>`       | Edit graduation year                |
| POST   | `/admin/delete_graduation_year/<id>`       | Delete graduation year              |
| GET    | `/admin/manage_genders`                    | Manage gender options               |
| POST   | `/admin/add_gender`                        | Add new gender                      |
| GET/POST | `/admin/edit_gender/<id>`                | Edit gender                         |
| POST   | `/admin/delete_gender/<id>`                | Delete gender                       |
| GET/POST | `/admin/system_settings`                 | Configure system-wide settings      |
| POST   | `/admin/add_domain`                        | Add allowed email domain             |
| POST   | `/admin/delete_domain/<id>`                | Remove email domain restriction     |
| POST   | `/admin/email_users`                       | Send bulk email to users            |
| GET/POST | `/admin/student_locker_agreement`        | Manage locker agreement document    |
| POST   | `/admin/student_locker_agreement_edit`    | Update locker agreement             |
| GET    | `/admin/home_page_content_list`            | Manage home page content            |
| POST   | `/admin/add_home_page_content`             | Add home page content block         |
| GET/POST | `/admin/edit_home_page_content/<id>`    | Edit home page content              |
| POST   | `/admin/delete_home_page_content/<id>`    | Delete home page content            |
| GET    | `/admin/content_list`                      | Manage general content pages        |
| POST   | `/admin/add_content`                       | Add new content page                |
| GET/POST | `/admin/edit_content/<id>`               | Edit content page                   |
| POST   | `/admin/delete_content/<id>`               | Delete content page                 |
| GET    | `/admin/reports/users`                     | View user reports                   |
| GET    | `/admin/reports/users/export/csv`          | Export users as CSV                 |
| GET    | `/admin/reports/users/export/pdf`          | Export users as PDF                 |
| GET    | `/admin/reports/sports`                    | View sports registration reports    |
| GET    | `/admin/reports/sports/export/csv`         | Export sports data as CSV           |
| GET    | `/admin/reports/sports/export/pdf`         | Export sports data as PDF           |
| GET    | `/admin/reports/withdrawals`               | View withdrawal request reports     |
| GET    | `/admin/reports/withdrawals/export/csv`    | Export withdrawals as CSV           |
| GET    | `/admin/reports/withdrawals/export/pdf`    | Export withdrawals as PDF           |
| GET/POST | `/admin/forms_control`                   | Configure form options and display  |
| POST   | `/admin/import_form_options`               | Bulk import form options            |
| GET    | `/admin/manage_form_options`               | Manage form dropdown options        |
| POST   | `/admin/add_form_option`                   | Add new form option                 |
| POST   | `/admin/delete_form_option/<id>`           | Delete form option                  |
| GET    | `/admin/manage_policies`                   | View and manage policies            |
| GET/POST | `/admin/email_templates`                | Manage email templates              |
| POST   | `/admin/add_email_template`                | Create new email template           |
| GET/POST | `/admin/edit_email_template/<id>`        | Edit email template                 |
| POST   | `/admin/delete_email_template/<id>`        | Delete email template               |
| GET    | `/admin/system_logs`                       | View system activity audit trail    |
| POST   | `/admin/delete_system_log/<id>`            | Delete system log entry             |
| GET/POST | `/admin/manage_access`                   | Manage user access controls         |
| POST   | `/admin/update_access`                     | Update access permissions           |
| GET/POST | `/admin/link_parent_to_student`         | Link parent account to student      |
| POST   | `/admin/unlink_account/<id>`               | Remove parent-student link          |
| POST   | `/admin/unlink_all_accounts`               | Remove all parent-student links      |
| GET    | `/admin/withdrawals`                       | Manage withdrawal requests          |
| POST   | `/admin/withdrawals/new/<student_id>`      | Create new withdrawal request       |
| POST   | `/admin/withdrawals/<id>/approve`          | Approve withdrawal request          |
| POST   | `/admin/withdrawals/<id>/deny`             | Deny withdrawal request             |
| POST   | `/admin/withdrawals/<id>/restore`          | Restore archived withdrawal         |
| POST   | `/admin/withdrawals/<id>/edit`             | Edit withdrawal details             |
| POST   | `/admin/withdrawals/<id>/archive`          | Archive withdrawal request          |
| GET    | `/admin/withdrawals/<id>/view`             | View withdrawal details             |
| GET    | `/admin/sports-registrations`               | Manage sports registrations         |
| POST   | `/admin/sports-registrations/<id>/approve`  | Approve sports registration         |
| POST   | `/admin/sports-registrations/<id>/reject`   | Reject sports registration          |
| POST   | `/admin/approve-all-sports-registrations`   | Approve all pending registrations   |
| GET    | `/admin/sports-registrations/<id>/view`     | View registration details           |
| POST   | `/admin/sports-registrations/<id>/delete`   | Delete sports registration          |
| GET    | `/admin/completion_dashboard`               | Monitor all student compliance      |
| POST   | `/admin/bulk_nudge`                        | Send bulk notifications             |
| POST   | `/admin/bulk_export_pdf`                   | Export bulk compliance PDFs         |
| GET    | `/admin/registration_settings`              | Configure registration requirements |
| POST   | `/admin/settings/requirements/delete/<id>`  | Delete requirement                  |
| GET    | `/admin/completion/export`                  | Export compliance roster as CSV     |
| POST   | `/admin/volunteer_submissions`              | View volunteer form submissions      |
| POST   | `/admin/toggle_volunteer_contacted/<id>`    | Mark volunteer as contacted         |

### Teacher Routes
| Method | Route                                    | Description                       |
|--------|------------------------------------------|-----------------------------------|
| GET    | `/teacher/dashboard`                    | Teacher Dashboard with stats     |
| GET    | `/teacher/manage_users`                 | Search and manage students       |
| POST   | `/teacher/add_user`                     | Create new student account       |
| GET/POST | `/teacher/edit_user/<id>`              | Edit student profile             |
| POST   | `/teacher/delete_user/<id>`             | Delete student account           |
| GET    | `/teacher/assign_locker`                | Assign locker to student         |
| POST   | `/teacher/unassign_locker/<id>`         | Release locker from student      |
| GET    | `/teacher/view_lockers`                 | View and filter all lockers      |
| GET    | `/teacher/locker_stats`                 | View locker statistics           |
| GET    | `/teacher/sports-registrations`         | Manage sports registrations      |
| POST   | `/teacher/sports-registrations/<id>/approve` | Approve sports registration |
| POST   | `/teacher/sports-registrations/<id>/reject`  | Reject sports registration  |
| POST   | `/teacher/approve-all-sports-registrations` | Approve all pending registrations |
| GET    | `/teacher/sports-registrations/<id>/view` | View registration details       |
| GET    | `/teacher/dashboard/completion`         | Monitor student compliance       |
| POST   | `/teacher/bulk_nudge`                   | Send bulk notifications          |
| POST   | `/teacher/bulk_export_pdf`              | Export bulk compliance PDFs      |
| GET    | `/teacher/reports`                      | View pickup, health, transport reports |
| GET    | `/teacher/reports/export/csv`           | Export reports as CSV            |
| GET    | `/teacher/reports/export/pdf`           | Export reports as PDF            |
| GET/POST | `/teacher/settings/requirements`      | Configure registration requirements |
| POST   | `/teacher/settings/requirements/delete/<id>` | Delete requirement         |
| GET    | `/teacher/completion/export`            | Export compliance roster as CSV  |
| GET    | `/teacher/withdrawals`                  | Manage withdrawal requests       |
| POST   | `/teacher/withdrawals/new/<student_id>` | Create new withdrawal request    |
| POST   | `/teacher/withdrawals/<id>/approve`     | Approve withdrawal request       |
| POST   | `/teacher/withdrawals/<id>/deny`        | Deny withdrawal request          |
| POST   | `/teacher/withdrawals/<id>/complete`    | Mark withdrawal as completed     |
| POST   | `/teacher/withdrawals/<id>/restore`     | Restore archived withdrawal      |
| POST   | `/teacher/withdrawals/<id>/archive`     | Archive withdrawal request       |

### Student Routes
| Method | Route                                    | Description                       |
|--------|------------------------------------------|-----------------------------------|
| GET    | `/student/dashboard`                    | Student Dashboard                |
| GET    | `/student/registration`                 | Registration forms page           |
| POST   | `/student/submit_sports_registration`   | Submit sports form               |
| POST   | `/student/submit_health_record`         | Submit emergency health form     |
| POST   | `/student/submit_pickup_authorization`  | Submit pickup authorization      |

### Parent Routes
| Method | Route                                    | Description                       |
|--------|------------------------------------------|-----------------------------------|
| GET    | `/parent/dashboard`                     | Parent Portal Dashboard          |
| GET    | `/parent/unlinked_account`              | Account linking page             |
| POST   | `/parent/link_account`                  | Link parent to student           |
| GET    | `/parent/student/<id>`                  | View student compliance status   |

### Authentication Routes
| Method | Route                                    | Description                       |
|--------|------------------------------------------|-----------------------------------|
| GET/POST | `/login`                              | User login                       |
| GET/POST | `/register`                           | User registration                |
| GET/POST | `/forgot_password`                    | Password reset request           |
| GET/POST | `/reset_password/<token>`             | Password reset with token        |
| GET    | `/logout`                              | User logout                      |

---

## 📊 Key Features

### Locker Management System
- **Multi-Building Inventory**: Manage lockers across multiple school buildings
- **Floor & Location Tracking**: Organize by floor and locker number
- **Real-Time Status**: Available, assigned, or maintenance status
- **Assignment History**: Track assignment dates and student history
- **Advanced Search**: Filter by building, floor, student name, or ID
- **Bulk Operations**: Assign/unassign multiple lockers efficiently
- **CSV Import/Export**: Bulk upload locker assignments
- **Reset All Function**: Quickly unassign all lockers (useful at end of year)
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
- **Admin & Teacher Access**: Monitor compliance across all students

### Sports Registration Workflow
- **Status Tracking**: Pending → Approved/Rejected
- **Health Record Integration**: Cross-reference emergency health records
- **Bulk Approval**: Approve all pending registrations at once
- **Detailed Reporting**: Export rosters with student details and EHR status
- **Multi-Format Export**: CSV and PDF report generation
- **Admin Control**: Full management from admin panel

### Withdrawal Processing
- **Multi-Status Workflow**: Pending → Approved/Denied → Completed/Archived
- **Status Toggling**: Deactivate/activate withdrawal requests
- **Denial Reasons**: Capture and store reason for denial
- **Historical Archive**: Restore archived withdrawals if needed
- **Audit Trail**: Complete tracking of who approved/denied and when
- **Admin & Teacher Access**: Both roles can manage withdrawals

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
  - User Reports (all user types)
  - Pickup Authorization Reports
  - Emergency Health Records
  - Transportation Records
  - Sports Registration Rosters
  - Student Compliance Roster
  - Withdrawal Request History
- **Admin Reporting**: Comprehensive system-wide reports

### Notification & Audit System
- **Targeted Notifications**: Send to incomplete students or parents
- **Bulk Nudge**: Notify multiple students matching filter criteria
- **Notification Audit Log**: Track who sent what and when
- **Student Quick-View History**: See recent notifications sent to each student
- **System Activity Log**: Complete audit trail of all actions with IP tracking
- **Log Management**: Delete logs for archival/cleanup

### Email Template Management
- **Customizable Templates**: Create and edit email templates
- **Template Variables**: Support for dynamic variable substitution
- **SMTP Configuration**: Gmail or other SMTP providers supported
- **Bulk Email**: Send messages to filtered user groups

### Administrative Configuration
- **System Settings**: Configure school name, contact info, etc.
- **Domain Restrictions**: Restrict registrations to specific email domains
- **Grade Levels**: Create and manage school grade levels
- **Graduation Years**: Configure years for student cohorts
- **Buildings**: Manage school buildings with sort order
- **Genders**: Configure gender options for student profiles
- **Relationship Types**: Define family relationship types
- **Form Options**: Manage dropdown options for form fields
- **Policies**: Configure school policies and agreements
- **Access Control**: Manage user permissions and roles

---

## 🔧 Configuration

### Environment Variables (`.env`)
