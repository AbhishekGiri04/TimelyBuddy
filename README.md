# 🎓 TimelyBuddy - Smart Academic ERP System

<p align="center">
  📚 A comprehensive academic ERP system for intelligent timetable scheduling with user authentication, role-based access, and complete academic management features.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
</p>

---

## 🎯 Problem Statement
Educational institutions face significant challenges in creating conflict-free timetables, managing student attendance, assignments, and coordinating between teachers, students, and administrators. Traditional manual scheduling methods are time-consuming, error-prone, and lack the efficiency required for modern academic management.

---

## 💡 Our Solution
TimelyBuddy - Smart Academic ERP System is a full-stack web application built to:

- 🧠 Generate conflict-free timetables using advanced graph coloring algorithms
- 👥 Manage users with role-based access (Admin, Teacher, Student)
- 📝 Handle assignments with photo/file upload capabilities
- ✅ Track student attendance with real-time marking
- 📊 Provide comprehensive dashboards with statistics
- 📄 Export timetables in PDF and Excel formats

---

## ✨ Features

- 🎯 **Conflict-free Timetable Generation** using graph coloring and backtracking algorithms  
- 🔐 **User Authentication** with secure login and role-based access control  
- 👤 **Role Management** for Admin, Teacher, and Student with different permissions  
- 📚 **Assignment Management** with photo/file upload and submission tracking  
- 📋 **Attendance System** with real-time marking and status tracking  
- 📈 **Dashboard Analytics** with comprehensive statistics and quick actions  
- 📤 **Export Functionality** for PDF and Excel timetable formats  
- 🔔 **Notification System** for system-wide announcements  
- 🖼️ **Profile Management** with photo upload capabilities

---

## 🛠️ Tech Stack

<div align="center">

| Technology | Description |
|------------|-------------|
| <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/> | Python web framework for backend development |
| <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/> | Lightweight database for data storage |
| <img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"/> | Responsive CSS framework for UI design |
| <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/> | Dynamic frontend interactions and AJAX |
| <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/> | Modern markup language with Jinja2 templating |
| <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> | Core programming language with algorithms |
| <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/> | Data manipulation for Excel export functionality |

</div>

---

## 📁 Project Directory Structure

```
TimelyBuddy - Smart Academic ERP System/
├── 🗄️ database/                    # SQLite database files
├── 📖 docs/                        # Documentation and screenshots
│   ├── Admin_Page.png
│   ├── Login_Page.png
│   ├── Student_Page.png
│   └── Teacher_Page.png
├── 📤 exports/                     # Generated export files
├── 🧮 scheduling/                  # Scheduling algorithms
│   ├── backtracking.py           # Backtracking conflict resolution
│   └── graph_coloring.py         # Graph coloring algorithm
├── 🎨 static/                      # Static assets
│   └── css/
│       └── style.css             # Custom styling
├── 📄 templates/                   # HTML templates
│   ├── admin.html                # Admin management panel
│   ├── assignment_submissions.html # Submission tracking
│   ├── assignments_student.html   # Student assignments
│   ├── assignments_teacher.html   # Teacher assignments
│   ├── attendance_student.html    # Student attendance
│   ├── attendance_teacher.html    # Teacher attendance
│   ├── base.html                 # Base template layout
│   ├── dashboard_admin.html       # Admin dashboard
│   ├── dashboard_student.html     # Student dashboard
│   ├── dashboard_teacher.html     # Teacher dashboard
│   ├── login.html                # Login page
│   ├── notifications.html        # Notifications
│   ├── teacher_students.html      # Student management
│   └── timetable.html            # Timetable display
├── 📁 uploads/                     # User uploaded files
│   ├── assignments/              # Assignment files
│   ├── profiles/                 # Profile photos
│   └── submissions/              # Student submissions
├── .gitignore                     # Git ignore rules
├── 🚀 app.py                      # Main Flask application
├── 🔨 build.sh                    # Build script for deployment
├── ⚙️ gunicorn.conf.py            # Production server config
├── 🗃️ init_db.py                  # Database initialization
├── 📋 Procfile                    # Process configuration
├── 📖 README.md                   # Project documentation
├── 🌐 render.yaml                 # Render deployment config
├── 📦 requirements.txt            # Python dependencies
└── 🐍 runtime.txt                 # Python version specification
```

---

## 📸 Application Screenshots

| Page / Feature | Screenshot |
|:---------------|:-----------|
| 🔐 Login Page | ![Login Page](docs/Login_Page.png) |
| 👨‍💼 Admin Dashboard | ![Admin Dashboard](docs/Admin_Page.png) |
| 👩‍🏫 Teacher Dashboard | ![Teacher Dashboard](docs/Teacher_Page.png) |
| 👨‍🎓 Student Dashboard | ![Student Dashboard](docs/Student_Page.png) |

---

## 👥 User Roles & Permissions

### 👨‍💼 Admin
- 🏫 Manage teachers, classes, classrooms, and subjects
- 📅 Generate and regenerate timetables
- 📊 View system statistics and analytics
- 📤 Export timetables in PDF/Excel formats
- 📢 Send system-wide notifications
- 👩‍🏫 Assign teachers to subjects and classes

### 👩‍🏫 Teacher
- 📅 View personal timetable and assigned classes
- 📝 Create and manage assignments
- ✅ Mark student attendance
- 👨‍🎓 Manage students in their classes
- 📋 View assignment submissions
- 🖼️ Upload profile photos

### 👨‍🎓 Student
- 📅 View class timetable and schedule
- 📤 Submit assignments with photo/file uploads
- 📊 View personal attendance records
- 📚 Access class information and notifications
- 👤 Manage profile and upload photos

---

## 🚀 How to Run

### 📋 Prerequisites
- 🐍 **Python 3.8+** installed
- 📦 **pip** package manager
- 🔧 **Git** for cloning the repository

### ⚡ Quick Start

1. **📥 Clone the repository:**
   ```bash
   git clone https://github.com/abhishekgiri04/TimelyBuddy.git
   cd "TimelyBuddy - Smart Academic ERP System"
   ```

2. **📦 Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **🗃️ Initialize the database:**
   ```bash
   python init_db.py
   ```

4. **🚀 Run the application:**
   ```bash
   python app.py
   ```

5. **🌐 Access the application:**
   ```
   http://localhost:5001
   ```

### 🔑 Default Login Credentials

**👨‍💼 Admin Account:**
- Username: `admin`
- Password: `admin123`

**📝 Note:** Only admin account is created by default. Teachers and students need to be added through the admin panel after login.

### 🔧 Troubleshooting

**🚫 Port already in use:**
```bash
# The app will automatically find an available port
# Check the console output for the actual port number
```

**🗃️ Database issues:**
```bash
# Reinitialize the database
python init_db.py
```

---

## 🧩 Core Components

- 🚀 **app.py** — Main Flask application with all routes and logic
- 🗃️ **init_db.py** — Database schema creation and initialization
- 🧮 **graph_coloring.py** — Advanced scheduling algorithm implementation
- 🔄 **backtracking.py** — Conflict resolution for timetable generation
- 📄 **base.html** — Base template with navigation and common elements
- 📊 **dashboard templates** — Role-specific dashboards for different users
- 📚 **assignment system** — Complete assignment management with file uploads
- ✅ **attendance system** — Real-time attendance marking and tracking

---

## 🛣️ Key Routes

```bash
# 🔐 Authentication
GET  /                  # Login page
POST /login            # User authentication
GET  /logout           # User logout

# 📊 Dashboard Routes
GET  /dashboard        # Role-based dashboard redirect
GET  /admin_dashboard  # Admin dashboard
GET  /teacher_dashboard # Teacher dashboard
GET  /student_dashboard # Student dashboard

# 📅 Timetable Management
GET  /admin            # Admin management panel
GET  /generate_timetable # Generate new timetable
GET  /timetable        # View timetable
GET  /export/pdf       # Export timetable as PDF
GET  /export/excel     # Export timetable as Excel

# 📚 Assignment System
GET  /assignments      # Assignment management
POST /create_assignment # Create new assignment
POST /submit_assignment # Submit assignment
POST /upload_assignment_photo # Upload assignment files

# ✅ Attendance System
GET  /attendance       # Attendance management
POST /mark_attendance  # Mark student attendance
```

---

## 🧪 Testing

```bash
# 🧪 Test the application
python app.py

# 🌐 Access the application
# 👨‍💼 Admin: http://localhost:5001 (admin/admin123)
# 📝 Note: Create teachers and students through admin panel
```

---

## 🔧 Common Issues

**🚫 Port already in use:**
- The application automatically finds an available port
- Check console output for the actual port number

**🗃️ Database connection issues:**
```bash
# Reinitialize the database
python init_db.py
```

**📦 Missing dependencies:**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

**📁 File upload issues:**
- Ensure the `uploads/` directory has proper permissions
- Check file size limits in the application

---

## 📈 Performance Metrics

- ✅ **100% Conflict-Free** — Timetable generation with zero scheduling conflicts
- 🧮 **Graph Coloring Algorithm** — Advanced mathematical approach for optimization
- ⚡ **Real-time Processing** — Instant attendance marking and assignment uploads
- 👥 **Multi-user Support** — Concurrent access for multiple users
- 📱 **Responsive Design** — Works seamlessly on desktop and mobile devices
- 🔐 **Secure Authentication** — Role-based access control with encrypted passwords

---

## 🚀 Future Scope
- 📱 **Mobile Application** — Native mobile app for iOS and Android
- 📧 **Email/SMS Notifications** — Automated alerts for assignments and attendance
- 📅 **Calendar Integration** — Sync with Google Calendar and Outlook
- 📊 **Advanced Analytics** — Detailed reports and performance insights
- 🔌 **API Development** — RESTful APIs for third-party integrations
- 🗓️ **Multi-semester Support** — Handle multiple academic terms
- 🏢 **Resource Booking** — Laboratory and equipment reservation system
- 🔒 **Enhanced Security** — Two-factor authentication and audit logs

---

## 🧮 Algorithms Used

### 🎨 Graph Coloring Algorithm
- **🎯 Purpose:** Assigns time slots to subjects avoiding conflicts
- **⚡ Complexity:** O(V²) where V is the number of subjects
- **✅ Benefits:** Ensures no teacher/classroom conflicts

### 🔄 Backtracking Algorithm
- **🎯 Purpose:** Resolves scheduling conflicts and constraints
- **🛠️ Approach:** Systematic exploration of solution space
- **✅ Benefits:** Finds optimal solutions with constraint satisfaction

### 📋 Constraint Satisfaction
- **👩‍🏫 Teacher Availability:** Respects teacher time preferences
- **🏫 Room Capacity:** Ensures adequate space for class sizes
- **📚 Subject Requirements:** Handles lab/theory session needs

---

## 📞 Help & Contact

> 💬 Got questions or need assistance with TimelyBuddy?  
> We're here to help with technical support and collaboration!

<div align="center">

**👨‍💻 Abhishek Giri**  
<a href="https://www.linkedin.com/in/abhishek-giri04/">
  <img src="https://img.shields.io/badge/Connect%20on-LinkedIn-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn - Abhishek Giri"/>
</a>  
<a href="https://github.com/abhishekgiri04">
  <img src="https://img.shields.io/badge/Follow%20on-GitHub-black?style=for-the-badge&logo=github" alt="GitHub - Abhishek Giri"/>
</a>  
<a href="https://t.me/AbhishekGiri7">
  <img src="https://img.shields.io/badge/Chat%20on-Telegram-blue?style=for-the-badge&logo=telegram" alt="Telegram - Abhishek Giri"/>
</a>

---

**🎓 Built for Academic Excellence**  
*Making Class Scheduling Smart, Simple, and Efficient!*

</div>

---

<div align="center">

**© 2025 TimelyBuddy - Smart Academic ERP System. All Rights Reserved.**

</div>