from app import db
from app.models import User, Internship, Application
from datetime import datetime


# Create some dummy users

user1 = User(email="alice@example.com", password="test123")
user2 = User(email="bob@example.com", password="test123")

# Create dummy internships
intern1 = Internship(
    title="Data Science Intern",
    company="TechCorp",
    location="Remote",
    description="Analyze data trends using Python.",
    skills="Python, Pandas, ML",
    posted_at=datetime.utcnow()
)

intern2 = Internship(
    title="Web Developer Intern",
    company="WebWorks",
    location="Bangalore",
    description="Work on frontend with React.",
    skills="React, HTML, CSS",
    posted_at=datetime.utcnow()
)

# Create dummy applications
app1 = Application(user=user1, internship=intern1, status="Applied", applied_at=datetime.utcnow())
app2 = Application(user=user2, internship=intern2, status="Shortlisted", applied_at=datetime.utcnow())

# Add to DB
db.session.add_all([user1, user2, intern1, intern2, app1, app2])
db.session.commit()

print("✅ Dummy data inserted!")
