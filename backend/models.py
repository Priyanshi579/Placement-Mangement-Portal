# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# from datetime import datetime


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(120), nullable=False, default="student")
#     is_active = db.Column(db.Boolean(), nullable=False)
#     students = db.relationship('Student', backref='user', lazy=True)
#     company = db.relationship('Company', backref = 'user',lazy = True)

# class Student(db.Model):
#     id = db.Column(db.Integer,primary_key= True)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     name = db.Column(db.String(120),nullable=False)
#     branch = db.Column(db.String(120),nullable=False)
#     year = db.Column(db.Integer,nullable=False)
#     cgpa = db.Column(db.Float,nullable=False)
#     phone = db.Column(db.Integer,nullable=False,unique = True)
#     skills = db.Column(db.Text(),nullable=False)
#     placement_status = db.Column(db.String(120),nullable=False,default = "Not Placed")
#     is_blacklisted = db.Column(db.Boolean(),nullable=False,default = False) 
#     application = db.relationship('Application',backref = 'student',lazy = True)
#     exports = db.relationship('Export',backref = 'student',lazy = True)
# class Company(db.Model):
#     id = db.Column(db.Integer,primary_key= True)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
#     name = db.Column(db.String(120),nullable=False)
#     location = db.Column(db.String(120),nullable=False)
#     contact = db.Column(db.Integer,nullable=False)
#     description = db.Column(db.Text(),nullable=False)
#     approval_status = db.Column(db.String(120),nullable=False,default = "Pending")
#     is_blacklisted = db.Column(db.Boolean(),nullable=False,default = False)
#     application = db.relationship('Application',backref = 'company',lazy = True)    
#     drives = db.relationship('PlacementDrive',backref = 'company',lazy = True)

# class PlacementDrive(db.Model):
#     id = db.Column(db.Integer,primary_key= True)
#     name = db.Column(db.String(120),nullable=False)
#     company_id = db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
#     job_title = db.Column(db.String(120),nullable=False)
#     job_description = db.Column(db.Text(),nullable=False)
#     min_cgpa = db.Column(db.Float,nullable=False)
#     eligibility = db.Column(db.Text(),nullable=False)
#     salary_package = db.Column(db.Integer,nullable=False)
#     location = db.Column(db.String(120),nullable=False)
#     deadline = db.Column(db.DateTime(120),default = datetime.utcnow,nullable=False)
#     status = db.Column(db.String(120),nullable=False,default = 'Pending')
#     application = db.relationship('Application',backref = 'drive',lazy = True)

# class Application(db.Model):
#     id = db.Column(db.Integer,primary_key= True)
#     company_id = db.Column(db.Integer,db.ForeignKey('company.id'),nullable=False)
#     student_id = db.Column(db.Integer,db.ForeignKey('student.id') ,nullable=False)
#     drive_id = db.Column(db.Integer,db.ForeignKey('placement_drive.id'),nullable=False)
#     name = db.Column(db.String(120),nullable=False)
#     application_date = db.Column(db.DateTime,default = datetime.utcnow,nullable=False)
#     status = db.Column(db.String(120),nullable=False,default = 'Not Applied')# applied , shortlist, select , rejected
#     __table_args__ = (db.UniqueConstraint('student_id','drive_id',name = 'student_drive_unique'),)
    


from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(120), nullable=False, default="student")
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    students = db.relationship("Student", backref="user", lazy=True)
    company = db.relationship("Company", backref="user", lazy=True)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    skills = db.Column(db.Text, nullable=False)
    placement_status = db.Column(
        db.String(120), nullable=False, default="Not Placed"
    )
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)

    application = db.relationship(
        "Application", backref="student", lazy=True
    )


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    approval_status = db.Column(
        db.String(120), nullable=False, default="Pending"
    )
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)

    application = db.relationship(
        "Application", backref="company", lazy=True
    )
    drives = db.relationship(
        "PlacementDrive", backref="company", lazy=True
    )


class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(
        db.Integer, db.ForeignKey("company.id"), nullable=False
    )
    job_title = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    eligibility = db.Column(db.Text, nullable=False)
    salary_package = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    deadline = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    status = db.Column(db.String(120), nullable=False, default="Pending")

    application = db.relationship(
        "Application", backref="drive", lazy=True
    )


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer, db.ForeignKey("company.id"), nullable=False
    )
    student_id = db.Column(
        db.Integer, db.ForeignKey("student.id"), nullable=False
    )
    drive_id = db.Column(
        db.Integer, db.ForeignKey("placement_drive.id"), nullable=False
    )
    name = db.Column(db.String(120), nullable=False)
    application_date = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    status = db.Column(
        db.String(120), nullable=False, default="Not Applied"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "drive_id",
            name="student_drive_unique"
        ),
    )
