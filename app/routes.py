from flask import Flask, render_template, request, redirect, url_for, session
from .models import Internship, User, Application, Alert
from .forms import InternshipForm, ApplicationForm
from .utils.automation import recommend_internships, auto_apply
from .utils.ml import process_resume, get_skill_match, resume_screening
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Home Route (Display Internships)
@app.route('/')
def home():
    internships = Internship.query.all()
    return render_template('index.html', internships=internships)

# Add Internship Route (Admin Only)
@app.route('/add', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))

    return render_template('add_internship.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# Dashboard Route with ML-based Recommendations
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    recommended_internships = recommend_internships(user_id)
    return render_template('dashboard.html', recommended_internships=recommended_internships)

# Auto Apply Route
@app.route('/auto_apply', methods=['GET', 'POST'])
def auto_apply_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        internship_id = request.form['internship_id']
        cover_letter = request.form['cover_letter']
        auto_apply(session['user_id'], internship_id, cover_letter)
        return redirect(url_for('dashboard'))
    internships = Internship.query.all()
    return render_template('auto_apply.html', internships=internships)

# Resume Screening Automation (Company Side)
@app.route('/resume_screening', methods=['POST'])
def resume_screening_route():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        resume_file = request.files['resume']
        skills = resume_screening(resume_file)
        return render_template('resume_screening_result.html', skills=skills)

# Application Tracking Route
@app.route('/track_application', methods=['GET'])
def track_application():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    applications = Application.query.filter_by(user_id=user_id).all()
    return render_template('track_application.html', applications=applications)

# Platform Monitoring and Alerting Route
@app.route('/monitor', methods=['GET'])
def monitor():
    alerts = Alert.query.all()
    return render_template('monitor.html', alerts=alerts)

# Admin Panel Route
@app.route('/admin', methods=['GET'])
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return redirect(url_for('home'))
    all_internships = Internship.query.all()
    all_applications = Application.query.all()
    return render_template('admin.html', internships=all_internships, applications=all_applications)

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))
