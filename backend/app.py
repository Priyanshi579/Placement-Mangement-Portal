from flask import Flask ,jsonify, request
from flask_cors import CORS
from models import db,User,Student,Company,PlacementDrive,Application,Interview,Notification,Export
from werkzeug.security import generate_password_hash,check_password_hash
import json
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,JWTManager,get_jwt
from datetime import datetime
from flask_caching import Cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

CORS(app)
db.init_app(app)


jwt = JWTManager(app)

cache = Cache(app)

@app.route('/api/register', methods = ['POST'])
def register_user():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)

    if User.query.filter_by(username= data['username']).first():
        return jsonify({'message':'User already exist'}),400
    
    user = User(username = data['username'],email = data['email'],password= generate_password_hash(data['password']),role = data['role'],is_active = True) #password = data['password'],role = data['role'],is_active = True)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message':'User registered successfully'}),200

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data) #change str to json
    
    # 1. Look up the user
    user = User.query.filter_by(username=data['username']).first()
    
    # 2. Check password
    if user and check_password_hash(user.password, data['password']):
        if not user.is_active:
            return jsonify({
                'message': 'User is not active or blacklisted by admin',
                'status': 'blacklisted'
            }), 403
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        # 3. CRITICAL CHECK: Determine if they have already registered their profile
        profile_exists = False
        approval_status = None
        
        if user.role == 'student':
            student_profile = Student.query.filter_by(user_id=user.id).first()
            profile_exists = True if student_profile else False
        elif user.role == 'company':
            company_profile = Company.query.filter_by(user_id=user.id).first()
            if company_profile:
                profile_exists = True if company_profile else False
                approval_status = company_profile.approval_status
            else:
                profile_exists = False
                approval_status = "Pending"
        
        # 4. Return everything in ONE cohesive response payload
        return jsonify({
            'message': 'User login successfully',
            'profile_completed': profile_exists, 
            'approval_status': approval_status,
            'data': {
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "access_token": access_token
            }
        }), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/api/adminlogin', methods = ['POST'])
def admin_login():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)

    user = User.query.filter_by(username = data['username']).first()
    if user and check_password_hash(user.password,data['password']) and user.role == 'admin':
        access_token = create_access_token(identity = str(user.id),additional_claims = {'role':user.role})
        return jsonify({'message':'Admin login successfully','data':{"username":user.username,"email":user.email,"password":user.password,"role":user.role,"access_token":access_token}}),200
    else:
        return jsonify({'message':'Invalid username or password'}),401



@app.route('/api/register/company', methods = ['POST'])
@jwt_required()
def register_company():
    data = request.get_json(force = True)
    if isinstance(data, str):
        data = json.loads(data)
    
    current_user_id = get_jwt_identity()

    if Company.query.filter_by(user_id = int(current_user_id)).first():
        return jsonify({'message':'Company already exista'}),400    


    company = Company(
        user_id = int(current_user_id),
        name = data['name'],
        location   = data['location'],
        contact = int(data['contact']),
        description = data['description'],
    )

    db.session.add(company)
    db.session.commit()

    return jsonify({'message':'Company registered successfully'}),200

@app.route('/api/register/student', methods = ['POST'])
@jwt_required()
def register_student():
    data = request.get_json()
    if isinstance(data, str):
        data = json.loads(data)  
    
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id = int(current_user_id)).first()
    
    student = Student.query.filter_by(user_id = int(current_user_id)).first()
    if student:
        if 'email' in data and data['email']:
            user.email = data['email']
        db.session.commit()
        student.name = data['name']
        student.branch = data['branch']
        student.year = data['year']
        student.cgpa = float(data['cgpa'])
        student.phone = int(data['phone'])#data['phone']
        student.skills = data['skills']
        db.session.commit()
        return jsonify({'message':'Student updated successfully'}),200
    else:
        student = Student(
            user_id = int(current_user_id),
            name = data['name'],
            branch = data['branch'],
            year = data['year'],
            cgpa = float(data['cgpa']),
            phone = int(data['phone']),
            skills = data['skills'],
            )
        
        db.session.add(student)
        db.session.commit()

        return jsonify({'message':'Student registered successfully'}),200



@app.route('/api/get/student', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
@cache.cached(timeout=60)
def get_studnets():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    students = Student.query.all()
    data = []
    for student in students:
        if student.is_blacklisted is not True :
            data.append({
                'id':student.id,
                'name':student.name,
                'email':student.user.email,
                'password':student.user.password,
                'placement_status':student.placement_status,
                "skills":student.skills,
                'branch':student.branch,
                'year':student.year,
                'cgpa':student.cgpa,
                "phone":student.phone
            })

    return jsonify(data)

@app.route('/api/get/company', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
# @cache.cached(timeout=60)
def get_companys():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    
    companys = Company.query.all()
    data = []
    for company in companys:
        if company.is_blacklisted is not True and company.approval_status == 'Approved':
            data.append({
                'id':company.id,
                'name':company.name,
                'email':company.user.email,
                'password':company.user.password,
                'approval_status':company.approval_status,
                'location':company.location,
                'contact':company.contact,
                'description':company.description
            })
    return jsonify(data)
@app.route('/api/get/unapproved/company', methods = ['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_unapproved_companys():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    companys = Company.query.all()
    Unapproved = []
    for company in companys:
        if company.is_blacklisted is not True:
            if company.approval_status == 'Pending':
                Unapproved.append({
                    'id':company.id,
                    'name':company.name,
                    'email':company.user.email,
                    'password':company.user.password,
                    'approval_status':company.approval_status,
                    'location':company.location,
                    'contact':company.contact,
                    'description':company.description
                })
    return jsonify(Unapproved) 

@app.route('/api/approval/company/<int:company_id>', methods = ['PUT'])
@jwt_required()
def approval_company(company_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    company = Company.query.filter_by(id = company_id).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    company.approval_status = 'Approved'
    db.session.commit()
    return jsonify({'message': 'Company approved successfully'}), 200

@app.route('/api/get/application', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
@cache.cached(timeout=60)  
def get_applications():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    applications = Application.query.all()
    data = []
    for application in applications:
        # student = Student.query.filter_by(id = application.student_id).first()
        # company = Company.query.filter_by(id = application.company_id).first()
        if application.status in ['Applied', 'shortlisted', 'rejected', 'waiting']:
            data.append({
                'id':application.id,
                "company_name":Company.query.filter_by(id = application.company_id).first().name,
                'student_name':Student.query.filter_by(id = application.student_id).first().name, #application.student_id,
                'drive_name':PlacementDrive.query.filter_by(id = application.drive_id).first().name, #application.drive_id,
                'application_date':application.application_date,
                'status':application.status,
                'student_id':application.student_id,
                'drive_id':application.drive_id
            })

    return jsonify(data)

@app.route('/api/get/student/<int:application_id>', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
@cache.cached(timeout=60)
def get_student_application(application_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    application = Application.query.filter_by(id = application_id).first()
    if not application:
        return jsonify({'message': 'Application not found'}), 404
    return jsonify({
        'id':application.id,
        "appliaction_date":application.application_date,
        "company_name":Company.query.filter_by(id = application.company_id).first().name,
        'student_name':Student.query.filter_by(id = application.student_id).first().name, #application.student_id,
        'drive_name':PlacementDrive.query.filter_by(id = application.drive_id).first().name,
        'branch':Student.query.filter_by(id = application.student_id).first().branch,
        'jobtitle':PlacementDrive.query.filter_by(id = application.drive_id).first().job_title,
        'status':application.status,
    })

        


@app.route('/api/get/drive', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
@cache.cached(timeout=60)
def get_drives():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    drives = PlacementDrive.query.all()
    data = []
    for drive in drives:
        if drive.status != 'Completed' and drive.deadline > datetime.now():
            data.append({
                'id':drive.id,
                'name':drive.name,
                'company_id':drive.company_id,
                'job_title':drive.job_title,
                'job_description':drive.job_description,
                'min_cgpa':drive.min_cgpa,
                'eligibility':drive.eligibility,
                'salary_package':drive.salary_package,
                'location':drive.location,
                'deadline':drive.deadline.strftime('%Y-%m-%d') if drive.deadline else None,
                'status':drive.status
            })

    return jsonify(data)


@app.route("/api/blacklisted_company/<int:company_id>",methods = ['POST'])
@jwt_required()
def blacklisted_company(company_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    

    company.is_blacklisted = True
    db.session.commit()
    user = User.query.filter_by(id = company.user_id).first()
    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'Company blacklisted successfully'}), 200

@app.route("/api/blacklisted_student/<int:student_id>",methods = ['POST'])
@jwt_required()
def blacklisted_student(student_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    student  = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    

    student.is_blacklisted = True
    db.session.commit()
    user = User.query.filter_by(id = student.user_id).first()
    user.is_active = False
    db.session.commit()
    return jsonify({'message': 'Student  blacklisted successfully'}), 200
    
@app.route("/api/create/drive",methods = ['POST'])
@jwt_required()
def create_drive():
    data = request.get_json()
    if isinstance(data, str):
        data = json.loads(data)  
    current_user_id = get_jwt_identity()

    company = Company.query.filter_by(user_id=int(current_user_id)).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    drive = PlacementDrive(
        company_id = company.id,
        name = data['name'],
        job_title = data['jobtitle'],
        job_description = data['description'],
        eligibility = data['eligbility'],
        min_cgpa = float(data['min_cgpa']),
        salary_package = int(data['salary']),
        location = data['location'],
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%d'),
    )  
    db.session.add(drive)
    db.session.commit()
    return jsonify({'message': 'Drive created successfully'}), 200

@app.route("/api/company/drive",methods = ['GET'])
@jwt_required()
def company_drive():
    current_user_id = get_jwt_identity()
    company = Company.query.filter_by(user_id=int(current_user_id)).first()
    if not company:
        return jsonify({'message': 'Company not found'}), 404
    drives = PlacementDrive.query.filter_by(company_id = company.id).all()
    data = []
    for drive in drives:
        # if drive.status == 'Pending':
            data.append({
                'id':drive.id,
                'name':drive.name,
                'jobtitle':drive.job_title,
                'description':drive.job_description,
                'eligbility':drive.eligibility,
                'min_cgpa':drive.min_cgpa,
                'salary':drive.salary_package,
                'location':drive.location,
                'deadline':drive.deadline,
                'status':drive.status
            })
    return jsonify(data)

@app.route('/api/closed_drives',methods = ['GET'])
@jwt_required()
def closed_drives():
    if get_jwt().get('role') != 'company':
        return jsonify({'message':'Company acesses only'}),401
    drives = PlacementDrive.query.filter_by(status = 'Completed').all()
    data = []
    for drive in drives:
        if drive.status == 'Completed':
            data.append({
                'id':drive.id,
                'name':drive.name,
                'jobtitle':drive.job_title,
                'description':drive.job_description,
                'eligbility':drive.eligibility,
                'min_cgpa':drive.min_cgpa,
                'salary':drive.salary_package,
                'location':drive.location,
                'deadline':drive.deadline,
                'status':drive.status
            })
    return jsonify(data)

@app.route('/api/drive/mark_as_completed/<int:drive_id>',methods = ['POST'])
@jwt_required()
def mark_as_completed(drive_id):
    if get_jwt().get('role') not in ["company", "admin"]:
        return jsonify({"message": "Eiter Company or admin has access only"}),404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    drive.status = 'Completed'
    db.session.commit()
    return jsonify({'message': 'Drive marked as completed successfully'}), 200


@app.route('/api/student_profile',methods = ['GET'])
@jwt_required()
def student_profile():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id = int(current_user_id)).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    student = Student.query.filter_by(user_id = user.id).first()
    if not student:
        return jsonify({'exists': False,'email': user.email,'name': '','branch': '','year': '','cgpa': '','phone': '','skills': ''}), 200
    data = {
        'exists': True,
        'name':student.name,
        'email':user.email,
        'branch':student.branch,
        'year':student.year,
        'cgpa':student.cgpa,
        'phone':student.phone,
        'skills':student.skills,
        'id':student.id
    }
    return jsonify(data)

@app.route('/api/company_profile',methods = ['GET'])
@jwt_required()
def company_profile():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id = int(current_user_id)).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    company = Company.query.filter_by(user_id = user.id).first()
    if not company:
        return jsonify({'exists': False,'email': user.email,'name': '','location': '','contact': '','description': ''}), 200
    data = {
        'exists': True,
        'name':company.name,
        'email':user.email,
        'location':company.location,
        'contact':company.contact,
        'description':company.description,
        'id':company.id
    }
    return jsonify(data)







@app.route('/api/get/student/company', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
def get_student_companys():
    if get_jwt().get('role') != 'student':
        return jsonify({'message':'Student acesses only'}),404
    companys = Company.query.all()
    data = []
    for company in companys:
        if company.is_blacklisted is not True and company.approval_status == 'Approved':
            data.append({
                'id':company.id,
                'name':company.name,
                'email':company.user.email,
                'password':company.user.password,
                'approval_status':company.approval_status,
                'location':company.location,
                'contact':company.contact,
                'description':company.description
            })

    return jsonify(data) 

@app.route("/api/company_drives/<int:company_id>", methods = ['GET'])
@jwt_required()
def get_company_drive(company_id):
    if get_jwt().get('role') != 'student':
        return jsonify({'message':'Student acesses only'}),404
    company = Company.query.filter_by(id = company_id).first()
    drives = PlacementDrive.query.filter_by(company_id = company_id).all()
    data = []
    for drive in drives:
        if drive.status != 'Completed' and drive.deadline > datetime.now():
            data.append({
                'company_id':drive.company_id,
                'id':drive.id,
                'name':drive.name,
                'jobtitle':drive.job_title,
                'description':drive.job_description,
                'eligbility':drive.eligibility,
                'min_cgpa':drive.min_cgpa,
                'salary':drive.salary_package,
                'location':drive.location,
                'deadline':drive.deadline.strftime('%Y-%m-%d') if drive.deadline else None,
                'status':drive.status
            })
    return jsonify({'data':data,'details' : {'name':company.name,}}),200

@app.route('/api/get/drive/<int:drive_id>', methods = ['GET'])
@jwt_required()
def get_drive_details(drive_id):
    if get_jwt().get('role') not in ["student", "admin", "company"]:
        return jsonify({"message": "Eiter Company or Student or admin has access only"}),404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    company_id = drive.company_id
    company = Company.query.filter_by(id = company_id).first()
    
    data = {
        'id': drive.id,
        'name': drive.name,
        'jobtitle': drive.job_title,
        'description': drive.job_description,
        'eligbility': drive.eligibility,
        'min_cgpa': drive.min_cgpa,
        'salary': drive.salary_package,
        'location': drive.location,
        'deadline': drive.deadline.strftime('%Y-%m-%d') if drive.deadline else None,
        'status': drive.status,
        'role': get_jwt().get('role')
    }
    return jsonify({'data':data,'details' : {'name':company.name,}}),200
    # return jsonify({'data': data,'details': {'name':company.name}}),200


@app.route('/api/update/drive/<int:drive_id>', methods = ['PUT'])
@jwt_required()
def update_drive(drive_id):
    if get_jwt().get('role') != "company":
        return jsonify({"message": "Company access only"}),404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    drive.name = request.json.get('name')
    drive.job_title = request.json.get('jobtitle')
    drive.job_description = request.json.get('description')
    drive.eligibility = request.json.get('eligbility')
    drive.min_cgpa = request.json.get('min_cgpa')
    drive.salary_package = request.json.get('salary')
    drive.location = request.json.get('location')    
    drive.deadline = datetime.strptime(request.json.get('deadline'), '%Y-%m-%d')
    drive.status = request.json.get('status')
    db.session.commit()
    return jsonify({'message': 'Drive updated successfully'}), 200  
@app.route('/api/apply/<int:drive_id>', methods = ['POST'])
@jwt_required()
def apply_for_drive(drive_id):
    if get_jwt().get('role') != "student":
        return jsonify({"message": "Student access only"}),404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id = int(current_user_id)).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    student = Student.query.filter_by(user_id = user.id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    apply = Application.query.filter(Application.student_id == student.id , Application.drive_id == drive.id , Application.status.in_(['Applied', 'shortlisted', 'rejected', 'waiting'])).first()
    if apply:
        return jsonify({'message': 'You have already applied for this drive'}), 400
    application = Application(drive_id = drive.id,name = drive.name,student_id = student.id,application_date = datetime.now(),status = 'Applied',company_id = drive.company_id)
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Application submitted successfully'}), 200


@app.route('/api/get/applied/drive', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
def get_applied_drives():
    if get_jwt().get('role') != 'student':
        return jsonify({'message':'Student acesses only'}),404
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id = int(current_user_id)).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    student = Student.query.filter_by(user_id = user.id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    applications = Application.query.filter(Application.student_id == student.id , Application.status.in_(['Applied', 'shortlisted', 'rejected', 'waiting'])).all()
    data = []
    for application in applications:
        data.append({
            'id':application.id,
            'drive_id':application.drive_id,
            'name':application.name,
            'application_date':application.application_date,
            'status':application.status
        })

    return jsonify(data)

@app.route('/api/applied_history/<int:student_id>', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
def get_applied_history(student_id):
    if get_jwt().get('role') != 'student':
        return jsonify({'message':'Student acesses only'}),404
    student = Student.query.filter_by(id = student_id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    applications = Application.query.filter_by(student_id = student.id).all()
    data = []
    for application in applications:
        company = Company.query.filter_by(id = application.company_id).first()
        drive = PlacementDrive.query.filter_by(id = application.drive_id).first()
        data.append({
            'id':application.id,
            'drive_id':drive.name,
            'name':application.name,
            'company': company.name,
            'application_date':application.application_date,
            'status':application.status,
            'student_name':student.name,
            'jobtitle':drive.job_title,
        })
    return jsonify({'data':data,'details':{'student_name':student.name}}),200


@app.route('/api/student_apply/view_details/<int:drive_id>', methods = ['GET'])
@jwt_required() 
def view_drive_details(drive_id):
    if get_jwt().get('role') != "company":
        return jsonify({"message": "Company access only"}),404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    
    student_list = []
    applications = Application.query.filter_by(drive_id = drive.id).all()
    for application in applications:
        student = Student.query.filter_by(id = application.student_id).first()
        student_list.append({
            'name':student.name,
            'id':student.id,
            'drive_id':application.drive_id
        })
    return jsonify({'students':student_list,'jobtitle':drive.job_title}),200

@app.route('/api/get/student_data/<int:student_id>/<int:drive_id>', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
def get_student_data(student_id,drive_id):
    if get_jwt().get('role') != 'company':
        return jsonify({'message':'Company acesses only'}),404
    student = Student.query.filter_by(id = student_id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404,
    user = User.query.filter_by(id = student.user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    if user.is_active == True:
        data = {
            'student_name':student.name,
            'drive_name':drive.name,
            'jobtitle': drive.job_title,
            'branch':student.branch,
            'cgpa':student.cgpa,
            'passing_year':student.year,
            'phone':student.phone,
            'skills':student.skills,
            "drive_id":drive.id,
            'id':student.id,
            'email':user.email
        }
        return jsonify(data),200

@app.route('/api/update/application_status/<int:student_id>/<int:drive_id>', methods = ['PUT'])
@jwt_required() #ask the token check is it correct guy to get the data

def update_application_status(student_id,drive_id):
    if get_jwt().get('role') != 'company':
        return jsonify({'message':'Company acesses only'}),404
    student = Student.query.filter_by(id = student_id).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    drive = PlacementDrive.query.filter_by(id = drive_id).first()
    if not drive:
        return jsonify({'message': 'Drive not found'}), 404
    application = Application.query.filter_by(student_id = student.id,drive_id = drive.id).first()
    if not application:
        return jsonify({'message': 'Application not found'}), 404
    if student.is_blacklisted == False:
        application.status = request.json.get('status')
        db.session.commit()
        return jsonify({'message': 'Application status updated successfully'}), 200


@app.route('/api/search/<user_type>/<search>', methods = ['GET'])
@jwt_required() #ask the token check is it correct guy to get the data
def search(user_type,search):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    if user_type == 'student':
        student = Student.query.filter_by(name = search).first()
        
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        user = User.query.filter_by(id = student.user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        student = {
                'role':user.role,
                'name':student.name,
                'id':student.id,
                'phone':student.phone,
                'branch':student.branch,
                'year':student.year,
                'cgpa':student.cgpa,
                'skills':student.skills,
                'email':user.email,
            }
        return jsonify(student), 200
    elif user_type == 'company':
        company = Company.query.filter_by(name = search).first()
        if not company:
            return jsonify({'message': 'Company not found'}), 404
        user = User.query.filter_by(id = company.user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        company = {
            'role':user.role,
            'name':company.name,
            'id':company.id,
            'phone':company.contact,
            'email':user.email,
            'location':company.location,
            'description':company.description
            }
        return jsonify(company), 200
        
@app.route('/user/summary', methods = ['GET'])
@jwt_required()
def user_summary():
    user = get_jwt_identity()
    student = Student.query.filter_by(user_id=int(user)).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    applied = Application.query.filter_by(student_id = student.id).all()
    total_application = len(applied)
    selected = 0
    waiting = 0
    rejected = 0
    apply = 0

    for application in applied:
        if application.status == 'Applied':
            apply += 1
        elif application.status == 'shortlisted':
            selected += 1
        
        elif application.status == 'waiting':
            waiting += 1
        elif application.status == 'rejected':
            rejected += 1

    return jsonify({
        'total_application':total_application,
        'selected':selected,
        'waiting':waiting,
        'rejected':rejected,
        'apply':apply}),200


@app.route('/api/admin/summary', methods = ['GET'])
@jwt_required()
def admin_summary():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message':'Admin acesses only'}),401
    student = Student.query.count()
    company = Company.query.count()

    active_students = Student.query.filter_by(is_blacklisted=False).count()
    inactive_students = Student.query.filter_by(is_blacklisted=True).count()
    active_companies = Company.query.filter_by(is_blacklisted=False).count()
    inactive_companies = Company.query.filter_by(is_blacklisted=True).count()
    pending_companies = Company.query.filter_by(approval_status='Pending').count()
    
    total =int(student)  + int(company)
    return jsonify({
        'total_student':student,
        'total_company':company,
        'active_students':active_students,
        'inactive_students':inactive_students,
        'active_companies':active_companies,
        'inactive_companies':inactive_companies,
        'pending_companies':pending_companies,
        'total':total
    }),200



@app.route('/api/export/application_history',methods = ['GET'])
@jwt_required()
def export_application():
    user_id = get_jwt_identity()
    if get_jwt().get('role') != 'student':
        return jsonify({"Studnet access only"}),401
    student = Student.query.filter_by(user_id = user_id).first()
    if not student:
        return jsonify({"Studnet not found"}),404
    from tasks import export
    export.delay(student.id)
    return jsonify({"message":"Export started"}),200



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username = 'admin').first():
            admin = User(username = 'admin',email = 'admin@gmail.com',password = generate_password_hash('admin'),role = 'admin',is_active = True)
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)

