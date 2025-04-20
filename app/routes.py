from flask import render_template, request, redirect, url_for, session
from .models import Internship, User, Application, Alert
from .forms import InternshipForm, ApplicationForm
from .utils.automation import recommend_internships, auto_apply
from .utils.ml import process_resume, get_skill_match, resume_screening
from .extensions import db  # Import db from extensions.py
from flask import Blueprint

# Define the blueprint
main_bp = Blueprint('main', __name__)

# Register routes with this blueprint
@main_bp.route('/')
def home():
    internships = Internship.query.all()
    return render_template('index.html', internships=internships)

# Add Internship Route (Admin Only)
@main_bp.route('/add', methods=['GET', 'POST'])
def add_internship():
    if request.method == 'POST':
        title = request.form['title']
        company = request.form['company']
        location = request.form['location']
        stipend = request.form['stipend']
        apply_by = request.form['apply_by']

        new_internship = Internship(
            title=title,
            company=company,
            location=location,
            stipend=stipend,
            apply_by=apply_by
        )
        db.session.add(new_internship)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template('add_internship.html')

# Login Route
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

# Register Route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')

# Dashboard Route with ML-based Recommendations
@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    recommended_internships = recommend_internships(user_id)
    return render_template('dashboard.html', recommended_internships=recommended_internships)

# Auto Apply Route
@main_bp.route('/auto_apply', methods=['GET', 'POST'])
def auto_apply_route():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        internship_id = request.form['internship_id']
        cover_letter = request.form['cover_letter']
        auto_apply(session['user_id'], internship_id, cover_letter)
        return redirect(url_for('main.dashboard'))
    internships = Internship.query.all()
    return render_template('auto_apply.html', internships=internships)

# Resume Screening Automation (Company Side)
@main_bp.route('/resume_screening', methods=['POST'])
def resume_screening_route():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    if request.method == 'POST':
        resume_file = request.files['resume']
        skills = resume_screening(resume_file)
        return render_template('resume_screening_result.html', skills=skills)

# Application Tracking Route
@main_bp.route('/track_application', methods=['GET'])
def track_application():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user_id = session['user_id']
    applications = Application.query.filter_by(user_id=user_id).all()
    return render_template('track_application.html', applications=applications)

# Platform Monitoring and Alerting Route
@main_bp.route('/monitor', methods=['GET'])
def monitor():
    alerts = Alert.query.all()
    return render_template('monitor.html', alerts=alerts)

# Admin Panel Route
@main_bp.route('/admin', methods=['GET'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return redirect(url_for('main.home'))
    all_internships = Internship.query.all()
    all_applications = Application.query.all()
    return render_template('admin.html', internships=all_internships, applications=all_applications)

# Logout Route
@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.login'))
