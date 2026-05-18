# Routes Related to Authentication, Mainly Login, Logout, and Resgistration

from flask import url_for, redirect, request, render_template, Blueprint, flash
from main.models import db, Users, Student, Company
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from main.decorators import home
from main.routes.utils import file_upload


#Blueprint
auth = Blueprint('auth', __name__)

#Routes
@auth.route("/login", methods=['GET', 'POST'])
@home   # Home for already logged in users
def login():
    if request.method == 'POST':
        username = request.form.get('user').strip()
        password = request.form.get('pass')

        user=Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            login_user(user)

            if user.role == 'admin':
                flash("Admin Login Successfull", "success")
                return redirect(url_for('admin.admin_dash'))
            elif user.role == 'student':
                flash("Student Login Successfull", "success")
                return redirect(url_for('student.student_dash'))
            else:
                flash("Company Login Successfull", "success")
                return redirect(url_for('company.company_dash'))

        
        flash("Incorrect Login Details or User Not Found", "danger")
        return redirect(url_for('auth.login'))
        
    return render_template('login.html')


@auth.route("/register", methods=['GET', 'POST'])
@home # Home for already logged in users
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        username = request.form.get('user').strip()
        password = request.form.get('pass')
        confirm_pass = request.form.get('con-pass')

        # Validation
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "warning")
            return redirect(url_for('auth.register'))

        if not (password == confirm_pass):
            flash("Passwords do not match!", "warning")
            return redirect(url_for('auth.register'))
        
        existing = Users.query.filter_by(username=username).first()
        if existing:
            flash("Username already Used! Please use different username.", "danger")
            return redirect(url_for('auth.register'))
        
        hash = generate_password_hash(password)
        new_user = Users(username=username, pass_hash=hash, role=role)
        db.session.add(new_user)
        db.session.flush () # User id before commiting

        if role == 'student':
            flash("Student Account Created Successfully", "success")
            new_profile = Student(user_id=new_user.id)
        else:
            flash("Company Account Created Successfully", "success")
            new_profile = Company(user_id=new_user.id)

        db.session.add(new_profile)
        db.session.commit()

        # Login User after Registration
        login_user(new_user)

        if new_user.role == 'admin':
            return redirect(url_for('admin.admin_dash'))
        elif new_user.role == 'student':
            return redirect(url_for('student.student_dash'))
        else:
            return redirect(url_for('company.company_dash'))
        
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User Logged Out Successfully", "success")
    return redirect(url_for('auth.login'))

# Onboarding - Student & Company
@auth.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    if current_user.profile_completed:
        if current_user.role == 'student':
            return redirect(url_for('student.student_dash'))
        return redirect(url_for('company.company_dash'))
    
    if request.method == 'POST':
        if current_user.role == 'student':
            student = Student.query.filter_by(user_id=current_user.id).first()
            
            # Student Fields
            resume_result = file_upload(
                file_key='resume_file',
                form_link_key='resume_url',
                upload_dir='resumes', 
                prefix=f"resume_{student.id}"
                )

            if resume_result:
                student.resume = resume_result

            # Validation Added
            student.fname = request.form.get('fname').strip()
            student.lname = request.form.get('lname').strip()
            student.roll = request.form.get('roll').strip()
            student.email = request.form.get('email').strip()
            student.phone = request.form.get('phone').strip()
            student.cgpa = request.form.get('cgpa').strip()
            student.graduation_year = request.form.get('graduation').strip()
            student.degree_field = request.form.get('degree').strip()
            student.batch = request.form.get('batch').strip()
            student.skills = request.form.get('skills').strip()
            student.bio = request.form.get('bio').strip()
            student.github = request.form.get('github').strip()
            student.linkedin = request.form.get('linkedin').strip()
            student.portfolio = request.form.get('portfolio').strip()

            
        elif current_user.role == 'company':
            company = Company.query.filter_by(user_id=current_user.id).first()
            
            # Company Fields
            logo_result = file_upload(
                file_key='logo_file',
                form_link_key='logo_url',
                upload_dir='logos', 
                prefix=f"logo_{company.id}"
            )

            if logo_result:
                company.logo = logo_result
                
            company.name = request.form.get('name').strip()
            company.industry = request.form.get('industry').strip()
            company.short_desc = request.form.get('short-desc').strip()
            company.description = request.form.get('desc').strip()
            company.location = request.form.get('location').strip()
            company.hr_contact = request.form.get('contact').strip()
            company.email = request.form.get('email').strip()
            company.employees_count = request.form.get('count').strip()
            company.website = request.form.get('website').strip()

        else:
            flash("Something went wrong", "danger")
            return redirect(url_for('auth.onboarding'))

        # Change Value of Profile Completed
        current_user.profile_completed = True
        
        db.session.commit()

        flash("Profile Completed.", "success")
        
        if current_user.role == 'student':
            return redirect(url_for('student.student_dash'))
        return redirect(url_for('company.company_dash'))

    flash("Provide Neccessary Details to Continue", "info")
    return render_template('onboarding.html')