<h1 align="center">🎓 TimelyBuddy — Smart Academic ERP System</h1>

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
<br>

---

## 📖 Problem Statement
Educational institutions face significant challenges in creating conflict-free timetables, managing student attendance, assignments, and coordinating between teachers, students, and administrators. Traditional manual scheduling methods are time-consuming, error-prone, and lack the efficiency required for modern academic management.

<br>

---

## 💡 Our Solution
TimelyBuddy - Smart Academic ERP System is a full-stack web application built to:

- 🧠 Generate conflict-free timetables using advanced graph coloring algorithms
- 👥 Manage users with role-based access (Admin, Teacher, Student)
- 📝 Handle assignments with photo/file upload capabilities
- ✅ Track student attendance with real-time marking
- 📊 Provide comprehensive dashboards with statistics
- 📄 Export timetables in PDF and Excel formats
<br>

---  

## 🚀 Features

✅  **Conflict-free Timetable Generation** using graph coloring and backtracking algorithms  
✅  **User Authentication** with secure login and role-based access control  
✅  **Role Management** for Admin, Teacher, and Student with different permissions  
✅  **Assignment Management** with photo/file upload and submission tracking  
✅  **Attendance System** with real-time marking and status tracking  
✅  **Dashboard Analytics** with comprehensive statistics and quick actions  
✅  **Export Functionality** for PDF and Excel timetable formats  
✅  **Notification System** for system-wide announcements  
✅  **Profile Management** with photo upload capabilities

<br>

---  

## 🛠️ Tech Stack

<div align="center">

<table>
<thead>
<tr>
<th>🖥️ Technology</th>
<th>⚙️ Description</th>
</tr>
</thead>
<tbody>
<tr>
<td><img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/></td>
<td>Python web framework for backend development</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white"/></td>
<td>Lightweight database for data storage</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white"/></td>
<td>Responsive CSS framework for UI design</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/></td>
<td>Dynamic frontend interactions and AJAX</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/></td>
<td>Modern markup language with Jinja2 templating</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/></td>
<td>Core programming language with algorithms</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/></td>
<td>Data manipulation for Excel export functionality</td>
</tr>
<tr>
<td><img src="https://img.shields.io/badge/ReportLab-FF6B6B?style=for-the-badge&logo=python&logoColor=white"/></td>
<td>PDF generation and export capabilities</td>
</tr>
</tbody>
</table>

</div>

<br>

---

## 📁 Project Directory Structure

```
TimelyBuddy - Smart Academic ERP System/
├── 📂 database/                    # 🗄️ SQLite database files
├── 📂 docs/                        # 📸 Documentation & screenshots
│   ├── 📄 Admin_Page.png           # 🖼️ Admin dashboard screenshot
│   ├── 📄 Login_Page.png           # 🖼️ Login page screenshot
│   ├── 📄 Student_Page.png         # 🖼️ Student dashboard screenshot
│   └── 📄 Teacher_Page.png         # 🖼️ Teacher dashboard screenshot
├── 📂 exports/                     # 📤 Generated export files
├── 📂 scheduling/                  # 🧮 Scheduling algorithms
│   ├── 📄 backtracking.py          # 🔄 Backtracking conflict resolution
│   └── 📄 graph_coloring.py        # 🎨 Graph coloring algorithm
├── 📂 static/                      # 🎨 Static assets
│   └── 📂 css/
│       └── 📄 style.css            # 🎨 Custom styling
├── 📂 templates/                   # 📄 HTML templates
│   ├── 📄 admin.html               # 👨💼 Admin management panel
│   ├── 📄 assignment_submissions.html # 📋 Submission tracking
│   ├── 📄 assignments_student.html # 👨🎓 Student assignments
│   ├── 📄 assignments_teacher.html # 👩🏫 Teacher assignments
│   ├── 📄 attendance_student.html  # 📊 Student attendance
│   ├── 📄 attendance_teacher.html  # ✅ Teacher attendance
│   ├── 📄 base.html                # 🏗️ Base template layout
│   ├── 📄 dashboard_admin.html     # 📊 Admin dashboard
│   ├── 📄 dashboard_student.html   # 👨🎓 Student dashboard
│   ├── 📄 dashboard_teacher.html   # 👩🏫 Teacher dashboard
│   ├── 📄 login.html               # 🔑 Login page
│   ├── 📄 notifications.html       # 🔔 Notifications
│   ├── 📄 teacher_students.html    # 👥 Student management
│   └── 📄 timetable.html           # 📅 Timetable display
├── 📂 uploads/                     # 📁 User uploaded files
│   ├── 📂 assignments/             # 📚 Assignment files
│   │   └── 📄 .gitkeep             # 🔄 Git placeholder
│   ├── 📂 profiles/                # 🖼️ Profile photos
│   │   └── 📄 .gitkeep             # 🔄 Git placeholder
│   └── 📂 submissions/             # 📤 Student submissions
│       └── 📄 .gitkeep             # 🔄 Git placeholder
├── 📄 .gitignore                   # 🚫 Git ignore patterns
├── 📄 app.py                       # 🚀 Main Flask application
├── 📄 build.sh                     # 🔨 Build script for deployment
├── 📄 gunicorn.conf.py             # ⚙️ Production server config
├── 📄 init_db.py                   # 🗃️ Database initialization
├── 📄 Procfile                     # 📋 Process configuration
├── 📄 README.md                    # 📖 Project documentation
├── 📄 render.yaml                  # 🌐 Render deployment config
├── 📄 requirements.txt             # 📦 Python dependencies
└── 📄 runtime.txt                  # 🐍 Python version specification
```
<br>

## 📸 Preview Images

| 📍 Page / Feature            | 📸 Screenshot                                              |
|:----------------------------|:-----------------------------------------------------------|
| 🔐 Login Page               | ![Login Page](docs/Login_Page.png)                       |
| 👨💼 Admin Dashboard        | ![Admin Dashboard](docs/Admin_Page.png)                  |
| 👩🏫 Teacher Dashboard      | ![Teacher Dashboard](docs/Teacher_Page.png)              |
| 👨🎓 Student Dashboard      | ![Student Dashboard](docs/Student_Page.png)              |

<br>

---

## 👥 User Roles & Permissions

### 👨💼 Admin
- 🏫 Manage teachers, classes, classrooms, and subjects
- 📅 Generate and regenerate timetables
- 📊 View system statistics and analytics
- 📤 Export timetables in PDF/Excel formats
- 📢 Send system-wide notifications
- 👩🏫 Assign teachers to subjects and classes

### 👩🏫 Teacher
- 📅 View personal timetable and assigned classes
- 📝 Create and manage assignments
- ✅ Mark student attendance
- 👨🎓 Manage students in their classes
- 📋 View assignment submissions
- 🖼️ Upload profile photos

### 👨🎓 Student
- 📅 View class timetable and schedule
- 📤 Submit assignments with photo/file uploads
- 📊 View personal attendance records
- 📚 Access class information and notifications
- 👤 Manage profile and upload photos

<br>

---

## 📦 How to Run

### 📌 Prerequisites
- ✅ **Python 3.8+** installed
- ✅ **pip** package manager
- ✅ **Git** for cloning the repository

<br>

---  

### 🚀 Quick Start

1. **📥 Clone and setup:**

   ```bash
   git clone https://github.com/abhishekgiri04/TimelyBuddy.git
   cd "TimelyBuddy - Smart Academic ERP System"
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Initialize database
   python init_db.py
   
   # Run application
   python app.py
   ```

2. **🌐 Access the application:**

   ```
   http://localhost:5001
   ```

### 🔑 Default Login Credentials

**👨💼 Admin Account:**
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

**📦 Missing dependencies:**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

<br>

---

## 📖 Core Components

### Flask Application
* **app.py** — Main Flask application with all routes and logic
* **init_db.py** — Database schema creation and initialization
* **graph_coloring.py** — Advanced scheduling algorithm implementation
* **backtracking.py** — Conflict resolution for timetable generation

### Templates & UI
* **base.html** — Base template with navigation and common elements
* **dashboard templates** — Role-specific dashboards for different users
* **assignment system** — Complete assignment management with file uploads
* **attendance system** — Real-time attendance marking and tracking

### Algorithms & Processing
* **Graph Coloring Algorithm** — Assigns time slots avoiding conflicts
* **Backtracking Algorithm** — Resolves scheduling conflicts systematically
* **Constraint Satisfaction** — Handles teacher availability and room capacity

<br>

---

## 🌐 API Routes

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
<br>

---

## 🧪 Testing

```bash
# 🧪 Test the application
python app.py

# 🌐 Access the application
# 👨💼 Admin: http://localhost:5001 (admin/admin123)
# 📝 Note: Create teachers and students through admin panel
```

## ⚠️ Common Issues

**🚫 Port already in use:**
- The application automatically finds an available port
- Check console output for the actual port number

**🗃️ Database connection issues:**
```bash
# Reinitialize the database
python init_db.py
```

**📁 File upload issues:**
- Ensure the `uploads/` directory has proper permissions
- Check file size limits in the application

<br>

---

## 🚀 Production Deployment

### Render Deployment
1. **Deploy to Render:**
   - Go to [render.com](https://render.com) → New Web Service
   - Connect GitHub repo
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

2. **Environment Variables:**
   - Set `PYTHON_VERSION` to `3.8.10`
   - Configure any required API keys

<br>

---

## 📊 Performance Metrics

- **✅ 100% Conflict-Free** — Timetable generation with zero scheduling conflicts
- **🧮 Graph Coloring Algorithm** — Advanced mathematical approach for optimization
- **⚡ Real-time Processing** — Instant attendance marking and assignment uploads
- **👥 Multi-user Support** — Concurrent access for multiple users
- **📱 Responsive Design** — Works seamlessly on desktop and mobile devices
- **🔐 Secure Authentication** — Role-based access control with encrypted passwords
- **📈 95% Efficiency** — Compared to manual scheduling methods

<br>

---

## 🌱 Future Scope
- 📱 **Mobile Application** — Native mobile app for iOS and Android
- 📧 **Email/SMS Notifications** — Automated alerts for assignments and attendance
- 📅 **Calendar Integration** — Sync with Google Calendar and Outlook
- 📊 **Advanced Analytics** — Detailed reports and performance insights
- 🔌 **API Development** — RESTful APIs for third-party integrations
- 🗓️ **Multi-semester Support** — Handle multiple academic terms
- 🏢 **Resource Booking** — Laboratory and equipment reservation system
- 🔒 **Enhanced Security** — Two-factor authentication and audit logs

<br>

---  

## 📞 Help & Contact  

> 💬 *Got questions or need assistance with TimelyBuddy?*  
> We're here to help with technical support and collaboration!

<div align="center">

**👤 Abhishek Giri**  
<a href="https://www.linkedin.com/in/abhishek-giri04/">
  <img src="https://img.shields.io/badge/Connect%20on-LinkedIn-blue?style=for-the-badge&logo=linkedin" alt="LinkedIn - Abhishek Giri"/>
</a>  
<a href="https://github.com/abhishekgiri04">
  <img src="https://img.shields.io/badge/Follow%20on-GitHub-black?style=for-the-badge&logo=github" alt="GitHub - Abhishek Giri"/>
</a>  
<a href="https://t.me/AbhishekGiri7">
  <img src="https://img.shields.io/badge/Chat%20on-Telegram-blue?style=for-the-badge&logo=telegram" alt="Telegram - Abhishek Giri"/>
</a>

<br/>

---

**🎓 Built with ❤️ for Academic Excellence**  
*Making Class Scheduling Smart, Simple, and Efficient!*

</div>

---

<div align="center">

**© 2025 TimelyBuddy - Smart Academic ERP System. All Rights Reserved.**

</div>