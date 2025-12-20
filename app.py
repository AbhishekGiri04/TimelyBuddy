import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
import hashlib
from fpdf import FPDF
from datetime import datetime
from functools import wraps
import webbrowser
import threading
import socket

# Import scheduling algorithms
from scheduling.graph_coloring import generate_initial_schedule
from scheduling.backtracking import resolve_conflicts

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'timelybuddy_secret_key_2024')
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'timelybuddy.db')

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, email, role, full_name):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.full_name = full_name

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user['id'], user['username'], user['email'], user['role'], user['full_name'])
    return None

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA busy_timeout=30000;')
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Access denied. Insufficient permissions.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Authentication Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('login'))
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE LOWER(username) = LOWER(?) AND password_hash = ? AND is_active = 1',
            (username, password_hash)
        ).fetchone()
        conn.close()
        
        if user:
            user_obj = User(user['id'], user['username'], user['email'], user['role'], user['full_name'])
            login_user(user_obj, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    else:
        return redirect(url_for('student_dashboard'))

@app.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    conn = get_db_connection()
    
    stats = {}
    try:
        stats['total_teachers'] = conn.execute('SELECT COUNT(*) as count FROM teachers').fetchone()['count']
        stats['total_students'] = conn.execute('SELECT COUNT(*) as count FROM students').fetchone()['count']
        stats['total_classes'] = conn.execute('SELECT COUNT(*) as count FROM classes').fetchone()['count']
        stats['total_subjects'] = conn.execute('SELECT COUNT(*) as count FROM subjects').fetchone()['count']
        stats['total_assignments'] = conn.execute('SELECT COUNT(*) as count FROM assignments').fetchone()['count']
    except:
        stats = {'total_teachers': 0, 'total_students': 0, 'total_classes': 0, 'total_subjects': 0, 'total_assignments': 0}
    
    try:
        notifications = conn.execute(
            'SELECT DISTINCT title, message, created_at FROM notifications ORDER BY created_at DESC LIMIT 5'
        ).fetchall()
    except:
        notifications = []
    
    conn.close()
    return render_template('dashboard_admin.html', stats=stats, notifications=notifications)

@app.route('/teacher_dashboard')
@login_required
@role_required('teacher')
def teacher_dashboard():
    conn = get_db_connection()
    
    teacher = conn.execute('SELECT *, COALESCE(profile_photo, "") as profile_photo FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    stats = {}
    if teacher:
        try:
            stats['my_subjects'] = conn.execute('SELECT COUNT(DISTINCT subject_id) as count FROM teacher_subject_class WHERE teacher_id = ?', (teacher['id'],)).fetchone()['count']
            stats['my_classes'] = conn.execute('SELECT COUNT(DISTINCT class_id) as count FROM teacher_subject_class WHERE teacher_id = ?', (teacher['id'],)).fetchone()['count']
            stats['assignments_created'] = conn.execute('SELECT COUNT(*) as count FROM assignments WHERE teacher_id = ?', (teacher['id'],)).fetchone()['count']
        except:
            stats = {'my_subjects': 0, 'my_classes': 0, 'assignments_created': 0}
    
    try:
        notifications = conn.execute(
            'SELECT DISTINCT title, message, created_at FROM notifications WHERE target_role IN ("all", "teacher") ORDER BY created_at DESC LIMIT 5'
        ).fetchall()
    except:
        notifications = []
    
    conn.close()
    return render_template('dashboard_teacher.html', stats=stats, notifications=notifications, teacher=teacher)

@app.route('/student_dashboard')
@login_required
@role_required('student')
def student_dashboard():
    conn = get_db_connection()
    
    student = conn.execute('SELECT *, COALESCE(profile_photo, "") as profile_photo FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
    
    stats = {}
    if student:
        try:
            stats['my_subjects'] = conn.execute('SELECT COUNT(DISTINCT subject_id) as count FROM teacher_subject_class WHERE class_id = ?', (student['class_id'],)).fetchone()['count']
            stats['assignments_pending'] = conn.execute('''
                SELECT COUNT(*) as count FROM assignments a 
                WHERE a.class_id = ? AND a.id NOT IN (
                    SELECT assignment_id FROM assignment_submissions WHERE student_id = ?
                )
            ''', (student['class_id'], student['id'])).fetchone()['count']
            
            # Calculate attendance percentage
            total_attendance = conn.execute('SELECT COUNT(*) as count FROM attendance WHERE student_id = ?', (student['id'],)).fetchone()['count']
            present_count = conn.execute('SELECT COUNT(*) as count FROM attendance WHERE student_id = ? AND status = "present"', (student['id'],)).fetchone()['count']
            stats['attendance_percentage'] = round((present_count / total_attendance * 100) if total_attendance > 0 else 0, 1)
        except:
            stats = {'my_subjects': 0, 'assignments_pending': 0, 'attendance_percentage': 0}
    
    try:
        notifications = conn.execute(
            'SELECT DISTINCT title, message, created_at FROM notifications WHERE target_role IN ("all", "student") ORDER BY created_at DESC LIMIT 5'
        ).fetchall()
    except:
        notifications = []
    
    conn.close()
    return render_template('dashboard_student.html', stats=stats, notifications=notifications, student=student)

# Admin Routes
@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    conn = get_db_connection()
    
    teachers = conn.execute('''
        SELECT t.*, u.full_name, u.email, u.is_active 
        FROM teachers t 
        JOIN users u ON t.user_id = u.id
    ''').fetchall()
    
    classes = conn.execute('SELECT * FROM classes').fetchall()
    classrooms = conn.execute('SELECT * FROM classrooms').fetchall()
    
    # Get subjects with their assignments
    try:
        subjects_with_assignments = conn.execute('''
            SELECT s.*, 
                   GROUP_CONCAT(DISTINCT u.full_name) as teacher_names,
                   GROUP_CONCAT(c.name || ' - ' || c.section) as class_names
            FROM subjects s
            LEFT JOIN teacher_subject_class tsc ON s.id = tsc.subject_id
            LEFT JOIN teachers t ON tsc.teacher_id = t.id
            LEFT JOIN users u ON t.user_id = u.id
            LEFT JOIN classes c ON tsc.class_id = c.id
            GROUP BY s.id
        ''').fetchall()
        subjects = subjects_with_assignments
    except:
        subjects = conn.execute('SELECT * FROM subjects').fetchall()
    
    try:
        assignments = conn.execute('''
            SELECT tsc.*, s.name as subject_name, u.full_name as teacher_name, c.name as class_name
            FROM teacher_subject_class tsc
            JOIN subjects s ON tsc.subject_id = s.id
            JOIN teachers t ON tsc.teacher_id = t.id
            JOIN users u ON t.user_id = u.id
            JOIN classes c ON tsc.class_id = c.id
        ''').fetchall()
    except:
        assignments = []
    
    conn.close()
    return render_template('admin.html', teachers=teachers, classes=classes, 
                         classrooms=classrooms, subjects=subjects, assignments=assignments)

@app.route('/add_teacher', methods=['POST'])
@login_required
@role_required('admin')
def add_teacher():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    full_name = request.form['full_name']
    employee_id = request.form['employee_id']
    department = request.form['department']
    specialization = request.form['specialization']
    
    password_hash = hash_password(password)
    
    conn = get_db_connection()
    try:
        # Check if username or email exists
        existing = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('admin_panel'))
            
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, 'teacher', full_name))
        
        user_id = c.lastrowid
        
        c.execute('''
            INSERT INTO teachers (user_id, employee_id, department, specialization)
            VALUES (?, ?, ?, ?)
        ''', (user_id, employee_id, department, specialization))
        
        conn.commit()
        flash('Teacher added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error adding teacher. Please try again.', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_panel'))

@app.route('/add_class', methods=['POST'])
@login_required
@role_required('admin')
def add_class():
    name = request.form['name']
    year = request.form['year']
    section = request.form['section']
    capacity = request.form['capacity']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO classes (name, year, section, capacity)
        VALUES (?, ?, ?, ?)
    ''', (name, year, section, capacity))
    conn.commit()
    conn.close()
    
    flash('Class added successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/add_classroom', methods=['POST'])
@login_required
@role_required('admin')
def add_classroom():
    name = request.form['name']
    building = request.form['building']
    floor = request.form['floor']
    capacity = request.form['capacity']
    equipment = request.form['equipment']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO classrooms (name, building, floor, capacity, equipment)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, building, floor, capacity, equipment))
    conn.commit()
    conn.close()
    
    flash('Classroom added successfully!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/add_subject', methods=['POST'])
@login_required
@role_required('admin')
def add_subject():
    name = request.form['name']
    code = request.form['code']
    credits = request.form['credits']
    num_lectures = request.form['num_lectures']
    semester = request.form['semester']
    teacher_id = request.form.get('teacher_id')
    class_id = request.form.get('class_id')
    
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute('''
            INSERT INTO subjects (name, code, credits, num_lectures, semester)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, code, credits, num_lectures, semester))
        
        subject_id = c.lastrowid
        
        # If teacher and class are selected, create the assignment
        if teacher_id and class_id and teacher_id != '' and class_id != '':
            c.execute('''
                INSERT OR IGNORE INTO teacher_subject_class (teacher_id, subject_id, class_id)
                VALUES (?, ?, ?)
            ''', (teacher_id, subject_id, class_id))
        
        conn.commit()
        flash('Subject added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash(f'Error adding subject: {str(e)}', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_panel'))

@app.route('/assign_teacher_subject', methods=['POST'])
@login_required
@role_required('admin')
def assign_teacher_subject():
    teacher_id = request.form['teacher_id']
    subject_id = request.form['subject_id']
    class_ids = request.form.getlist('class_ids')
    
    if not class_ids:
        flash('Please select at least one class!', 'error')
        return redirect(url_for('admin_panel'))
    
    conn = get_db_connection()
    try:
        for class_id in class_ids:
            conn.execute('INSERT OR IGNORE INTO teacher_subject_class (teacher_id, subject_id, class_id) VALUES (?, ?, ?)',
                        (teacher_id, subject_id, class_id))
        conn.commit()
        flash(f'Assignment successful! Teacher assigned to {len(class_ids)} class(es).', 'success')
    except Exception:
        conn.rollback()
        flash('Error in assignment.', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('admin_panel'))

@app.route('/delete_teacher/<int:teacher_id>')
@login_required
@role_required('admin')
def delete_teacher(teacher_id):
    conn = get_db_connection()
    try:
        teacher = conn.execute('SELECT user_id FROM teachers WHERE id = ?', (teacher_id,)).fetchone()
        if teacher:
            # Delete related records first
            conn.execute('DELETE FROM teacher_subject_class WHERE teacher_id = ?', (teacher_id,))
            # Delete teacher record
            conn.execute('DELETE FROM teachers WHERE id = ?', (teacher_id,))
            # Delete user record
            conn.execute('DELETE FROM users WHERE id = ?', (teacher['user_id'],))
            conn.commit()
            flash('Teacher deleted successfully!', 'success')
        else:
            flash('Teacher not found!', 'error')
    except Exception as e:
        conn.rollback()
        flash('Error deleting teacher. Please try again.', 'error')
    finally:
        conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/delete_class/<int:class_id>')
@login_required
@role_required('admin')
def delete_class(class_id):
    conn = get_db_connection()
    try:
        # Delete related records first
        conn.execute('DELETE FROM timetable WHERE class_id = ?', (class_id,))
        conn.execute('DELETE FROM assignments WHERE class_id = ?', (class_id,))
        conn.execute('DELETE FROM subjects WHERE class_id = ?', (class_id,))
        conn.execute('UPDATE students SET class_id = NULL WHERE class_id = ?', (class_id,))
        # Delete class record
        conn.execute('DELETE FROM classes WHERE id = ?', (class_id,))
        conn.commit()
        flash('Class deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error deleting class. Please try again.', 'error')
    finally:
        conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/delete_classroom/<int:classroom_id>')
@login_required
@role_required('admin')
def delete_classroom(classroom_id):
    conn = get_db_connection()
    try:
        # Delete related records first
        conn.execute('DELETE FROM timetable WHERE classroom_id = ?', (classroom_id,))
        # Delete classroom record
        conn.execute('DELETE FROM classrooms WHERE id = ?', (classroom_id,))
        conn.commit()
        flash('Classroom deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error deleting classroom. Please try again.', 'error')
    finally:
        conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/delete_subject/<int:subject_id>')
@login_required
@role_required('admin')
def delete_subject(subject_id):
    conn = get_db_connection()
    try:
        # Delete related records first
        conn.execute('DELETE FROM timetable WHERE subject_id = ?', (subject_id,))
        conn.execute('DELETE FROM assignments WHERE subject_id = ?', (subject_id,))
        conn.execute('DELETE FROM attendance WHERE subject_id = ?', (subject_id,))
        # Delete subject record
        conn.execute('DELETE FROM subjects WHERE id = ?', (subject_id,))
        conn.commit()
        flash('Subject deleted successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error deleting subject. Please try again.', 'error')
    finally:
        conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/generate_timetable')
@login_required
@role_required('admin')
def generate_timetable():
    conn = get_db_connection()
    
    # Get subjects with their teacher and class assignments
    subjects = conn.execute('''
        SELECT s.*, tsc.teacher_id, tsc.class_id
        FROM subjects s
        JOIN teacher_subject_class tsc ON s.id = tsc.subject_id
    ''').fetchall()
    
    teachers = conn.execute('SELECT * FROM teachers').fetchall()
    classrooms = conn.execute('SELECT * FROM classrooms WHERE is_available = 1').fetchall()
    classes = conn.execute('SELECT * FROM classes').fetchall()
    
    try:
        teacher_availability = conn.execute('SELECT * FROM teacher_availability').fetchall()
    except:
        teacher_availability = []
    
    if not subjects:
        flash('No subjects with teacher assignments found. Please assign teachers to subjects first.', 'warning')
        return redirect(url_for('admin_panel'))
    
    initial_schedule, shortages = generate_initial_schedule(
        subjects, teachers, classrooms, classes, teacher_availability
    )
    final_schedule = resolve_conflicts(
        initial_schedule, subjects, teachers, classrooms, classes
    )
    
    conn.execute('DELETE FROM timetable')
    for entry in final_schedule:
        conn.execute('''
            INSERT INTO timetable (subject_id, teacher_id, classroom_id, class_id, timeslot)
            VALUES (?, ?, ?, ?, ?)
        ''', (entry['subject_id'], entry['teacher_id'],
              entry['classroom_id'], entry['class_id'], entry['timeslot']))
    
    conn.commit()
    conn.close()
    
    create_notification_for_all('Timetable Updated', 'New timetable has been generated and is now available.')
    
    flash('Timetable generated successfully!', 'success')
    return redirect(url_for('view_timetable'))

@app.route('/timetable')
@login_required
def view_timetable():
    conn = get_db_connection()
    
    if current_user.role == 'admin':
        timetable = conn.execute('''
            SELECT t.*, s.name as subject_name, s.code, 
                   u.full_name as teacher_name, cr.name as classroom_name, 
                   c.section as class_name
            FROM timetable t
            JOIN subjects s ON t.subject_id = s.id
            JOIN teachers te ON t.teacher_id = te.id
            JOIN users u ON te.user_id = u.id
            JOIN classrooms cr ON t.classroom_id = cr.id
            JOIN classes c ON t.class_id = c.id
            ORDER BY c.section, t.timeslot
        ''').fetchall()
    elif current_user.role == 'teacher':
        teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
        if teacher:
            timetable = conn.execute('''
                SELECT t.*, s.name as subject_name, s.code, 
                       u.full_name as teacher_name, cr.name as classroom_name, 
                       c.section as class_name
                FROM timetable t
                JOIN subjects s ON t.subject_id = s.id
                JOIN teachers te ON t.teacher_id = te.id
                JOIN users u ON te.user_id = u.id
                JOIN classrooms cr ON t.classroom_id = cr.id
                JOIN classes c ON t.class_id = c.id
                WHERE t.teacher_id = ?
                ORDER BY t.timeslot
            ''', (teacher['id'],)).fetchall()
        else:
            timetable = []
    else:
        student = conn.execute('SELECT * FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
        if student:
            timetable = conn.execute('''
                SELECT t.*, s.name as subject_name, s.code, 
                       u.full_name as teacher_name, cr.name as classroom_name, 
                       c.section as class_name
                FROM timetable t
                JOIN subjects s ON t.subject_id = s.id
                JOIN teachers te ON t.teacher_id = te.id
                JOIN users u ON te.user_id = u.id
                JOIN classrooms cr ON t.classroom_id = cr.id
                JOIN classes c ON t.class_id = c.id
                WHERE t.class_id = ?
                ORDER BY t.timeslot
            ''', (student['class_id'],)).fetchall()
        else:
            timetable = []
    
    conn.close()
    return render_template('timetable.html', timetable=timetable)

@app.route('/export/excel')
@login_required
def export_excel():
    flash('Excel export temporarily disabled', 'info')
    return redirect(url_for('view_timetable'))

@app.route('/export/pdf')
@login_required
def export_pdf():
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT c.name as class, s.name as subject, s.code, 
               u.full_name as teacher, cr.name as classroom, t.timeslot
        FROM timetable t
        JOIN subjects s ON t.subject_id = s.id
        JOIN teachers te ON t.teacher_id = te.id
        JOIN users u ON te.user_id = u.id
        JOIN classrooms cr ON t.classroom_id = cr.id
        JOIN classes c ON t.class_id = c.id
        ORDER BY c.name, t.timeslot
    ''').fetchall()
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'TimelyBuddy - Smart Academic ERP System - Generated Timetable', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 10)
    
    current_class = ''
    for row in rows:
        if row['class'] != current_class:
            current_class = row['class']
            pdf.ln(5)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, f"Class: {current_class}", ln=True)
            pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, f"{row['timeslot']} - {row['subject']} ({row['code']}) - {row['teacher']} in {row['classroom']}", ln=True)
    
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    file_path = os.path.join(exports_dir, 'timetable.pdf')
    pdf.output(file_path)
    conn.close()
    return send_file(file_path, as_attachment=True)

def create_notification_for_all(title, message):
    conn = get_db_connection()
    
    # Check if notification already exists in last 5 minutes
    existing = conn.execute('''
        SELECT id FROM notifications 
        WHERE title = ? AND message = ? 
        AND datetime(created_at) > datetime('now', '-5 minutes')
        LIMIT 1
    ''', (title, message)).fetchone()
    
    if not existing:
        users = conn.execute('SELECT id FROM users WHERE is_active = 1').fetchall()
        for user in users:
            conn.execute('''
                INSERT OR IGNORE INTO notifications (user_id, title, message, target_role)
                VALUES (?, ?, ?, ?)
            ''', (user['id'], title, message, 'all'))
        conn.commit()
    
    conn.close()

@app.route('/notifications')
@login_required
def notifications():
    conn = get_db_connection()
    try:
        notifications = conn.execute('''
            SELECT * FROM notifications 
            WHERE user_id = ? OR target_role IN ('all', ?) 
            ORDER BY created_at DESC
        ''', (current_user.id, current_user.role)).fetchall()
    except:
        notifications = []
    conn.close()
    return render_template('notifications.html', notifications=notifications)

@app.route('/add_availability', methods=['POST'])
@login_required
@role_required('admin')
def add_availability():
    teacher_id = request.form['teacher_id']
    day = request.form['day']
    start_hour = request.form['start_hour']
    end_hour = request.form['end_hour']
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO teacher_availability (teacher_id, day, start_hour, end_hour)
        VALUES (?, ?, ?, ?)
    ''', (teacher_id, day, start_hour, end_hour))
    conn.commit()
    conn.close()
    
    flash('Teacher availability added successfully!', 'success')
    return redirect(url_for('admin_panel'))

# Attendance Management
@app.route('/attendance')
@login_required
def attendance():
    if current_user.role == 'teacher':
        return redirect(url_for('teacher_attendance'))
    elif current_user.role == 'student':
        return redirect(url_for('student_attendance'))
    else:
        return redirect(url_for('admin_attendance'))

@app.route('/teacher_attendance')
@login_required
@role_required('teacher')
def teacher_attendance():
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        subjects = conn.execute('''
            SELECT DISTINCT s.*, s.name || ' (' || c.section || ')' as display_name, 
                   tsc.class_id, c.section, c.name as class_name
            FROM subjects s
            JOIN teacher_subject_class tsc ON s.id = tsc.subject_id
            JOIN classes c ON tsc.class_id = c.id
            WHERE tsc.teacher_id = ?
            ORDER BY c.section, s.name
        ''', (teacher['id'],)).fetchall()
        
        # Get all students from classes where teacher teaches (for JavaScript filtering)
        students = conn.execute('''
            SELECT DISTINCT st.*, u.full_name, c.section as class_name, st.class_id 
            FROM students st
            JOIN users u ON st.user_id = u.id
            JOIN classes c ON st.class_id = c.id
            WHERE st.class_id IN (SELECT DISTINCT class_id FROM teacher_subject_class WHERE teacher_id = ?)
            ORDER BY c.section, u.full_name
        ''', (teacher['id'],)).fetchall()
    else:
        subjects = []
        students = []
    
    conn.close()
    return render_template('attendance_teacher.html', subjects=subjects, students=students)

@app.route('/mark_attendance', methods=['POST'])
@login_required
@role_required('teacher')
def mark_attendance():
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    status = request.form['status']
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if not subject_id:
        return jsonify({'success': False, 'message': 'Please select a subject first'})
    
    conn = None
    try:
        conn = get_db_connection()
        teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
        
        if teacher:
            # Verify teacher has access to this subject and student
            access_check = conn.execute('''
                SELECT 1 FROM teacher_subject_class tsc
                JOIN students s ON s.class_id = tsc.class_id
                WHERE tsc.teacher_id = ? AND tsc.subject_id = ? AND s.id = ?
            ''', (teacher['id'], subject_id, student_id)).fetchone()
            
            if not access_check:
                return jsonify({'success': False, 'message': 'Access denied'})
            
            # Check if attendance already marked
            existing = conn.execute('''
                SELECT * FROM attendance WHERE student_id = ? AND subject_id = ? AND date = ?
            ''', (student_id, subject_id, date)).fetchone()
            
            if existing:
                conn.execute('''
                    UPDATE attendance SET status = ?, marked_at = CURRENT_TIMESTAMP 
                    WHERE student_id = ? AND subject_id = ? AND date = ?
                ''', (status, student_id, subject_id, date))
            else:
                conn.execute('''
                    INSERT INTO attendance (student_id, subject_id, teacher_id, date, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student_id, subject_id, teacher['id'], date, status))
            
            conn.commit()
            return jsonify({'success': True, 'message': 'Attendance marked successfully'})
        else:
            return jsonify({'success': False, 'message': 'Teacher not found'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'message': 'Error marking attendance'})
    finally:
        if conn:
            conn.close()

@app.route('/student_attendance')
@login_required
@role_required('student')
def student_attendance():
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if student:
        attendance_records = conn.execute('''
            SELECT a.*, s.name as subject_name, s.code as subject_code, u.full_name as teacher_name
            FROM attendance a
            JOIN subjects s ON a.subject_id = s.id
            JOIN teachers t ON a.teacher_id = t.id
            JOIN users u ON t.user_id = u.id
            WHERE a.student_id = ?
            ORDER BY a.date DESC, s.name
        ''', (student['id'],)).fetchall()
    else:
        attendance_records = []
    
    conn.close()
    return render_template('attendance_student.html', attendance_records=attendance_records)

# Assignment Management
@app.route('/assignments')
@login_required
def assignments():
    if current_user.role == 'teacher':
        return redirect(url_for('teacher_assignments'))
    elif current_user.role == 'student':
        return redirect(url_for('student_assignments'))
    else:
        return redirect(url_for('admin_assignments'))

@app.route('/teacher_assignments')
@login_required
@role_required('teacher')
def teacher_assignments():
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        assignments = conn.execute('''
            SELECT a.*, s.name as subject_name, c.name as class_name,
                   COUNT(sub.id) as submission_count,
                   (SELECT COUNT(*) FROM students st WHERE st.class_id = a.class_id) as total_students
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            JOIN classes c ON a.class_id = c.id
            LEFT JOIN assignment_submissions sub ON a.id = sub.assignment_id
            WHERE a.teacher_id = ?
            GROUP BY a.id
            ORDER BY a.created_at DESC
        ''', (teacher['id'],)).fetchall()
        
        subjects = conn.execute('''
            SELECT s.*, c.name as class_name, tsc.class_id FROM subjects s
            JOIN teacher_subject_class tsc ON s.id = tsc.subject_id
            JOIN classes c ON tsc.class_id = c.id
            WHERE tsc.teacher_id = ?
        ''', (teacher['id'],)).fetchall()
    else:
        assignments = []
        subjects = []
    
    conn.close()
    return render_template('assignments_teacher.html', assignments=assignments, subjects=subjects, today=datetime.now().strftime('%Y-%m-%d'))

@app.route('/create_assignment', methods=['POST'])
@login_required
@role_required('teacher')
def create_assignment():
    title = request.form['title']
    description = request.form['description']
    subject_id = request.form['subject_id']
    due_date = request.form['due_date']
    
    # Handle file upload
    file_path = None
    if 'assignment_file' in request.files:
        file = request.files['assignment_file']
        if file and file.filename != '':
            import os
            import uuid
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'assignments')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            file_path = f'uploads/assignments/{unique_filename}'
    
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    subject_class = conn.execute('SELECT * FROM teacher_subject_class WHERE subject_id = ? AND teacher_id = ?', (subject_id, teacher['id'])).fetchone()
    
    if teacher and subject_class:
        conn.execute('''
            INSERT INTO assignments (title, description, subject_id, teacher_id, class_id, due_date, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, subject_id, teacher['id'], subject_class['class_id'], due_date, file_path))
        conn.commit()
        flash('Assignment created successfully!', 'success')
    
    conn.close()
    return redirect(url_for('teacher_assignments'))

@app.route('/student_assignments')
@login_required
@role_required('student')
def student_assignments():
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if student:
        assignments = conn.execute('''
            SELECT a.*, s.name as subject_name, u.full_name as teacher_name,
                   CASE WHEN sub.id IS NOT NULL THEN 1 ELSE 0 END as submitted,
                   sub.file_path
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            JOIN teachers t ON a.teacher_id = t.id
            JOIN users u ON t.user_id = u.id
            LEFT JOIN assignment_submissions sub ON a.id = sub.assignment_id AND sub.student_id = ?
            WHERE a.class_id = ?
            ORDER BY a.due_date ASC
        ''', (student['id'], student['class_id'])).fetchall()
    else:
        assignments = []
    
    conn.close()
    return render_template('assignments_student.html', assignments=assignments)

@app.route('/submit_assignment', methods=['POST'])
@login_required
@role_required('student')
def submit_assignment():
    assignment_id = request.form['assignment_id']
    
    # Handle file upload
    file_path = None
    if 'submission_file' in request.files:
        file = request.files['submission_file']
        if file and file.filename != '':
            import os
            import uuid
            # Create uploads directory if it doesn't exist
            upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'submissions')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = str(uuid.uuid4()) + file_extension
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            file_path = f'uploads/submissions/{unique_filename}'
    
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if student and file_path:
        # Check if submission already exists
        existing = conn.execute('SELECT * FROM assignment_submissions WHERE assignment_id = ? AND student_id = ?', 
                               (assignment_id, student['id'])).fetchone()
        
        if existing:
            # Update existing submission
            conn.execute('UPDATE assignment_submissions SET file_path = ?, submitted_at = CURRENT_TIMESTAMP WHERE assignment_id = ? AND student_id = ?', 
                        (file_path, assignment_id, student['id']))
        else:
            # Create new submission
            conn.execute('INSERT INTO assignment_submissions (assignment_id, student_id, file_path) VALUES (?, ?, ?)', 
                        (assignment_id, student['id'], file_path))
        
        conn.commit()
        flash('Assignment submitted successfully!', 'success')
    else:
        flash('Error submitting assignment. Please try again.', 'error')
    
    conn.close()
    return redirect(url_for('student_assignments'))

# Notice Management
@app.route('/create_notice', methods=['POST'])
@login_required
@role_required('admin')
def create_notice():
    title = request.form['title']
    message = request.form['message']
    target_role = request.form['target_role']
    
    conn = get_db_connection()
    
    # Check if notification already exists in last 5 minutes
    existing = conn.execute('''
        SELECT id FROM notifications 
        WHERE title = ? AND message = ? AND target_role = ?
        AND datetime(created_at) > datetime('now', '-5 minutes')
        LIMIT 1
    ''', (title, message, target_role)).fetchone()
    
    if existing:
        flash('Similar notification was already sent recently!', 'warning')
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    if target_role == 'all':
        users = conn.execute('SELECT id FROM users WHERE is_active = 1').fetchall()
        for user in users:
            conn.execute('''
                INSERT OR IGNORE INTO notifications (user_id, title, message, target_role)
                VALUES (?, ?, ?, ?)
            ''', (user['id'], title, message, target_role))
    else:
        users = conn.execute('SELECT id FROM users WHERE role = ? AND is_active = 1', (target_role,)).fetchall()
        for user in users:
            conn.execute('''
                INSERT OR IGNORE INTO notifications (user_id, title, message, target_role)
                VALUES (?, ?, ?, ?)
            ''', (user['id'], title, message, target_role))
    
    conn.commit()
    conn.close()
    
    flash('Notice published successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# Teacher Student Management
@app.route('/teacher_students')
@login_required
@role_required('teacher')
def teacher_students():
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        students = conn.execute('''
            SELECT DISTINCT st.*, u.full_name, u.email, c.name as class_name, st.profile_photo
            FROM students st
            JOIN users u ON st.user_id = u.id
            JOIN classes c ON st.class_id = c.id
            WHERE st.class_id IN (SELECT DISTINCT class_id FROM teacher_subject_class WHERE teacher_id = ?)
        ''', (teacher['id'],)).fetchall()
        
        classes = conn.execute('''
            SELECT DISTINCT c.* FROM classes c
            JOIN teacher_subject_class tsc ON c.id = tsc.class_id
            WHERE tsc.teacher_id = ?
        ''', (teacher['id'],)).fetchall()
    else:
        students = []
        classes = []
    
    conn.close()
    return render_template('teacher_students.html', students=students, classes=classes)

@app.route('/add_student', methods=['POST'])
@login_required
@role_required('teacher')
def add_student():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    full_name = request.form['full_name']
    student_id = request.form['student_id']
    class_id = request.form['class_id']
    year = request.form['year']
    section = request.form['section']
    
    password_hash = hash_password(password)
    
    conn = get_db_connection()
    try:
        # Check if username or email exists
        existing = conn.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
        if existing:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('teacher_students'))
            
        c = conn.cursor()
        c.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, 'student', full_name))
        
        user_id = c.lastrowid
        
        c.execute('''
            INSERT INTO students (user_id, student_id, class_id, year, section)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, student_id, class_id, year, section))
        
        conn.commit()
        flash('Student added successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error adding student. Please try again.', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('teacher_students'))

@app.route('/delete_student/<int:student_id>')
@login_required
@role_required('teacher')
def delete_student(student_id):
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        student = conn.execute('''
            SELECT st.* FROM students st
            WHERE st.id = ? AND st.class_id IN (SELECT DISTINCT class_id FROM teacher_subject_class WHERE teacher_id = ?)
        ''', (student_id, teacher['id'])).fetchone()
        
        if student:
            try:
                # Delete related records first
                conn.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
                conn.execute('DELETE FROM assignment_submissions WHERE student_id = ?', (student_id,))
                # Delete student record
                conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
                # Delete user record
                conn.execute('DELETE FROM users WHERE id = ?', (student['user_id'],))
                conn.commit()
                flash('Student removed successfully!', 'success')
            except Exception as e:
                conn.rollback()
                flash('Error removing student. Please try again.', 'error')
        else:
            flash('Access denied. You can only remove students from your classes.', 'error')
    
    conn.close()
    return redirect(url_for('teacher_students'))

@app.route('/update_student', methods=['POST'])
@login_required
@role_required('teacher')
def update_student():
    student_id = request.form['student_id']
    full_name = request.form['full_name']
    student_id_field = request.form['student_id_field']
    year = request.form['year']
    section = request.form['section']
    
    conn = get_db_connection()
    try:
        # Update user table
        conn.execute('UPDATE users SET full_name = ? WHERE id = (SELECT user_id FROM students WHERE id = ?)', 
                    (full_name, student_id))
        # Update students table
        conn.execute('UPDATE students SET student_id = ?, year = ?, section = ? WHERE id = ?', 
                    (student_id_field, year, section, student_id))
        conn.commit()
        flash('Student updated successfully!', 'success')
    except Exception as e:
        conn.rollback()
        flash('Error updating student. Please try again.', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('teacher_students'))

@app.route('/get_attendance_status', methods=['POST'])
@login_required
@role_required('teacher')
def get_attendance_status():
    subject_id = request.form.get('subject_id')
    date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    if not subject_id:
        return jsonify({'success': False, 'message': 'Subject ID required'})
    
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        # Get attendance records for the selected subject and date
        attendance_records = conn.execute('''
            SELECT a.student_id, a.status FROM attendance a
            WHERE a.subject_id = ? AND a.date = ? AND a.teacher_id = ?
        ''', (subject_id, date, teacher['id'])).fetchall()
        
        # Convert to dictionary for easy lookup
        attendance_dict = {record['student_id']: record['status'] for record in attendance_records}
        
        conn.close()
        return jsonify({'success': True, 'attendance': attendance_dict})
    
    conn.close()
    return jsonify({'success': False, 'message': 'Teacher not found'})

@app.route('/upload_profile_photo', methods=['POST'])
@login_required
def upload_profile_photo():
    try:
        if 'profile_photo' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['profile_photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        import os
        import uuid
        
        # Create uploads directory
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'profiles')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.gif']:
            return jsonify({'success': False, 'message': 'Invalid file type'})
        
        unique_filename = str(uuid.uuid4()) + file_extension
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Save to database
        photo_url = f'uploads/profiles/{unique_filename}'
        conn = get_db_connection()
        
        if current_user.role == 'teacher':
            conn.execute('UPDATE teachers SET profile_photo = ? WHERE user_id = ?', (photo_url, current_user.id))
        elif current_user.role == 'student':
            conn.execute('UPDATE students SET profile_photo = ? WHERE user_id = ?', (photo_url, current_user.id))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'photo_url': photo_url})
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/upload_assignment_photo', methods=['POST'])
@login_required
@role_required('student')
def upload_assignment_photo():
    try:
        assignment_id = request.form.get('assignment_id')
        if not assignment_id:
            return jsonify({'success': False, 'message': 'Assignment ID required'})
        
        if 'assignment_photo' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'})
        
        file = request.files['assignment_photo']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        
        import os
        import uuid
        
        # Create uploads directory
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'assignments')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.gif', '.pdf']:
            return jsonify({'success': False, 'message': 'Invalid file type'})
        
        unique_filename = str(uuid.uuid4()) + file_extension
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Save to database
        photo_url = f'uploads/assignments/{unique_filename}'
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE user_id = ?', (current_user.id,)).fetchone()
        
        if student:
            # Check if submission already exists
            existing = conn.execute('SELECT id FROM assignment_submissions WHERE student_id = ? AND assignment_id = ?', 
                                  (student['id'], assignment_id)).fetchone()
            
            if existing:
                conn.execute('UPDATE assignment_submissions SET file_path = ?, submitted_at = ? WHERE id = ?', 
                           (photo_url, datetime.now(), existing['id']))
            else:
                conn.execute('INSERT INTO assignment_submissions (student_id, assignment_id, file_path, submitted_at) VALUES (?, ?, ?, ?)', 
                           (student['id'], assignment_id, photo_url, datetime.now()))
            
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'photo_url': photo_url})
        
        conn.close()
        return jsonify({'success': False, 'message': 'Student not found'})
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@app.route('/view_submissions/<int:assignment_id>')
@login_required
@role_required('teacher')
def view_submissions(assignment_id):
    conn = get_db_connection()
    teacher = conn.execute('SELECT * FROM teachers WHERE user_id = ?', (current_user.id,)).fetchone()
    
    if teacher:
        # Get assignment details
        assignment = conn.execute('''
            SELECT a.*, s.name as subject_name, c.name as class_name
            FROM assignments a
            JOIN subjects s ON a.subject_id = s.id
            JOIN classes c ON a.class_id = c.id
            WHERE a.id = ? AND a.teacher_id = ?
        ''', (assignment_id, teacher['id'])).fetchone()
        
        if assignment:
            # Get all students in the class with their submissions
            submissions = conn.execute('''
                SELECT st.*, u.full_name, sub.file_path, sub.submitted_at,
                       CASE WHEN sub.id IS NOT NULL THEN 'Submitted' ELSE 'Not Submitted' END as status,
                       st.profile_photo
                FROM students st
                JOIN users u ON st.user_id = u.id
                LEFT JOIN assignment_submissions sub ON st.id = sub.student_id AND sub.assignment_id = ?
                WHERE st.class_id = ?
                ORDER BY u.full_name
            ''', (assignment_id, assignment['class_id'])).fetchall()
            
            conn.close()
            return render_template('assignment_submissions.html', assignment=assignment, submissions=submissions)
    
    conn.close()
    flash('Assignment not found or access denied.', 'error')
    return redirect(url_for('teacher_assignments'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    import os
    from flask import send_from_directory
    # Handle both full paths and just filenames
    if filename.startswith('uploads/'):
        # Remove 'uploads/' prefix if present
        filename = filename[8:]
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'uploads'), filename)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def open_browser(port):
    webbrowser.open(f'http://localhost:{port}', new=0)

if __name__ == '__main__':
    # Create necessary directories
    exports_dir = os.path.join(os.path.dirname(__file__), 'exports')
    if not os.path.exists(exports_dir):
        os.makedirs(exports_dir)
    
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        os.makedirs(os.path.join(uploads_dir, 'profiles'))
        os.makedirs(os.path.join(uploads_dir, 'assignments'))
        os.makedirs(os.path.join(uploads_dir, 'submissions'))
    
    # Production vs Development
    if os.environ.get('RENDER'):
        # Production on Render
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development mode
        port = find_free_port()
        
        # Auto-open browser after a short delay (only once)
        if not os.environ.get('WERKZEUG_RUN_MAIN'):
            threading.Timer(1.5, lambda: open_browser(port)).start()
        
        print(f"Starting TimelyBuddy - Smart Academic ERP System on port {port}")
        app.run(debug=True, port=port)