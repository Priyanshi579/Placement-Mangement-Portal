# from celery_worker import celery_app
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart 
# from email.mime.text import MIMEText
# import smtplib 
# from models import User, PlacementDrive, Company, Application,Student,Company
# from flask import render_template
# from datetime import datetime
# SERVER_SMTP_HOST = 'localhost'
# SERVER_SMTP_PORT = 1025
# SENDER_ADDRESS='priyanshi@gmail.com'
# SENDER_PASSWORD=''

# def send_email(to_address,subject,message,content="text",attachment=None):
#     msg = MIMEMultipart()
#     msg['To']=to_address
#     msg['From']=SENDER_ADDRESS
#     msg['Subject']=subject
#     if content == "html":
#         msg.attach(MIMEText(message,'html'))
#     else:
#         msg.attach(MIMEText(message, 'plain'))

#     if attachment:
#         with open(attachment,"rb") as a:
#             part = MIMEBase("application", "octet-stream")
#             part.set_payload(a.read())
#         encoders.encode_base64(part)
#         part.add_header("Content-Disposition", f"attachment: filename={attachment}")
#         msg.attach(part)          

#     s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
#     s.login(SENDER_ADDRESS,SENDER_PASSWORD)
#     s.send_message(msg)
#     s.quit()
#     return True

# @celery_app.task
# def send_monthly_report():
#     admin = User.query.filter_by(role = 'admin').first()
#     if not admin:
#         return "No admin  user finded"
#     companys = Company.query.all()
#     Drives = PlacementDrive.query.all()
#     applications = Application.query.all()  
#     Companys_list = []
#     #[{company_name:company_name}]
#     for company in companys:
#         count_drive = 0
#         count_applications = 0
#         selected = 0
#         for drive in Drives:
#             if drive.company_id == company.id:
#                 count_drive += 1
#         for application in applications:
#             if application.company_id == company.id:
#                 count_applications += 1
#                 if application.status == "shortlisted":
#                     selected = selected + 1
#         Companys_list.append({"company_name":company.name,"count_drive":count_drive,"count_applications":count_applications,"selected":selected})
#     html = render_template("monthly_report.html",companys = Companys_list)
#     send_email(admin.email,"Monthly Report",html,content = "html")  

#     return "Monthly Report sent successfully"  

# @celery_app.task
# def send_daily_reminder():
#     users = User.query.filter_by(is_active = True , role = "student").all()
#     live_applications = []
#     for user in users:
#         applications = PlacementDrive.query.filter(PlacementDrive.status == "Pending" , PlacementDrive.deadline >= datetime.now()).all()
#         for application in applications:
#             company = Company.query.filter_by(id = application.company_id).first()
#             drive = PlacementDrive.query.filter_by(id = application.id).first()
#             live_applications.append({"company_name":company.name,"drive_name":drive.name,"deadline":drive.deadline})
#         html = render_template("appl.html",applications = live_applications)
        
#         send_email(user.email,"Daily Reminder",html,content = "html")
#     return "Daily Reminder sent successfully"

# @celery_app.task
# def export(student_id):
#     student = Student.query.filter_by(id = student_id).first()
#     if not student:
#         return "Student not found"
#     user = User.query.filter_by(id = student.user_id).first()
#     if not user:
#         return "No sunch user found"
#     Applied_lists = Application.query.filter(Application.student_id == student.id , Application.status.in_(['Applied', 'shortlisted', 'rejected', 'waiting'])).all()
#     if not Applied_lists:
#         return 'No application for this student is found'
#     forms = []
#     for apply in Applied_lists:
#         drive = PlacementDrive.query.filter_by(id = apply.drive_id).first()
#         company = Company.query.filter_by(id = drive.company_id).first()
#         forms.append({
#             "student_id":student.id,
#             "company_name":company.name,
#             "drive_name":drive.name,
#             "date":apply.application_date,
#             "status":apply.status
#         })
#         print(student.id,company.name,drive.name,apply.application_date,apply.status)
#     html = render_template("export.html",forms = forms)
#     send_email(user.email,"Application History",html,content = "html")
#     return "Application History sent successfully"


import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery_worker import celery_app
from models import User, PlacementDrive, Company, Application, Student
from flask import render_template
from datetime import datetime


# Email configuration from environment variables
SERVER_SMTP_HOST = os.getenv("MAIL_SERVER", "smtp.gmail.com")
SERVER_SMTP_PORT = int(os.getenv("MAIL_PORT", "587"))

SENDER_ADDRESS = os.getenv("MAIL_USERNAME")
SENDER_PASSWORD = os.getenv("MAIL_PASSWORD")


# Email sending function
def send_email(to_address, subject, message, content="text", attachment=None):

    if not SENDER_ADDRESS or not SENDER_PASSWORD:
        raise RuntimeError("Email credentials are missing")

    msg = MIMEMultipart()

    msg["To"] = to_address
    msg["From"] = SENDER_ADDRESS
    msg["Subject"] = subject

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    # Attach file if provided
    if attachment:
        with open(attachment, "rb") as file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(attachment)}"'
        )

        msg.attach(part)

    # Connect to SMTP server and send email
    with smtplib.SMTP(SERVER_SMTP_HOST, SERVER_SMTP_PORT) as server:

        server.starttls()

        server.login(SENDER_ADDRESS, SENDER_PASSWORD)

        server.send_message(msg)

    return True


# Monthly report task
@celery_app.task
def send_monthly_report():

    admin = User.query.filter_by(role="admin").first()

    if not admin:
        return "No admin user found"

    companies = Company.query.all()
    drives = PlacementDrive.query.all()
    applications = Application.query.all()

    companies_list = []

    for company in companies:

        count_drive = 0
        count_applications = 0
        selected = 0

        for drive in drives:
            if drive.company_id == company.id:
                count_drive += 1

        for application in applications:

            if application.company_id == company.id:

                count_applications += 1

                if application.status == "shortlisted":
                    selected += 1

        companies_list.append({
            "company_name": company.name,
            "count_drive": count_drive,
            "count_applications": count_applications,
            "selected": selected
        })

    html = render_template(
        "monthly_report.html",
        companys=companies_list
    )

    send_email(
        admin.email,
        "Monthly Report",
        html,
        content="html"
    )

    return "Monthly Report sent successfully"


# Daily reminder task
@celery_app.task
def send_daily_reminder():

    users = User.query.filter_by(
        is_active=True,
        role="student"
    ).all()

    for user in users:

        # Create a fresh list for each student
        live_applications = []

        applications = PlacementDrive.query.filter(
            PlacementDrive.status == "Pending",
            PlacementDrive.deadline >= datetime.now()
        ).all()

        for application in applications:

            company = Company.query.filter_by(
                id=application.company_id
            ).first()

            drive = PlacementDrive.query.filter_by(
                id=application.id
            ).first()

            if company and drive:

                live_applications.append({
                    "company_name": company.name,
                    "drive_name": drive.name,
                    "deadline": drive.deadline
                })

        html = render_template(
            "appl.html",
            applications=live_applications
        )

        send_email(
            user.email,
            "Daily Reminder",
            html,
            content="html"
        )

    return "Daily Reminder sent successfully"


# Export application history task
@celery_app.task
def export(student_id):

    student = Student.query.filter_by(
        id=student_id
    ).first()

    if not student:
        return "Student not found"

    user = User.query.filter_by(
        id=student.user_id
    ).first()

    if not user:
        return "No such user found"

    applied_lists = Application.query.filter(
        Application.student_id == student.id,
        Application.status.in_([
            "Applied",
            "shortlisted",
            "rejected",
            "waiting"
        ])
    ).all()

    if not applied_lists:
        return "No application for this student is found"

    forms = []

    for apply in applied_lists:

        drive = PlacementDrive.query.filter_by(
            id=apply.drive_id
        ).first()

        if not drive:
            continue

        company = Company.query.filter_by(
            id=drive.company_id
        ).first()

        if not company:
            continue

        forms.append({
            "student_id": student.id,
            "company_name": company.name,
            "drive_name": drive.name,
            "date": apply.application_date,
            "status": apply.status
        })

    if not forms:
        return "No valid application records found"

    html = render_template(
        "export.html",
        forms=forms
    )

    send_email(
        user.email,
        "Application History",
        html,
        content="html"
    )

    return "Application History sent successfully"
