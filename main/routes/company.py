# Routes for Company Pages
# URL : /company/...

from flask import url_for, redirect, render_template, Blueprint, request, flash
from flask_login import current_user, login_required
from main.decorators import company_required
from main.models import db, Drive, Application, Company, Notification
from datetime import datetime
from main.routes.utils import file_upload


#Blueprint
company = Blueprint('company', __name__)


# Dashboard
@company.route("/dashboard")
@login_required
@company_required
def company_dash():
    # Data for Cards
    company = current_user.company_data
    total_drives = Drive.query.filter_by(company_id=company.id).count()
    running_drives = Drive.query.filter_by(company_id=company.id, status='approved').count()
    total_apps = db.session.query(Application).join(Drive).filter(Drive.company_id == company.id).count()
    latest_drives = Drive.query.filter_by(company_id=company.id).order_by(Drive.id.desc()).limit(5).all()

    # Chart Data
    drives = Drive.query.filter_by(company_id=company.id).all()
    labels = [d.title for d in drives]
    values = [len(d.job_application) for d in drives]

    return render_template('company/dashboard.html', company=company, total_drives=total_drives, running_drives=running_drives, total_apps=total_apps, latest_drives=latest_drives, labels=labels, values=values)


# Drives
@company.route("/drives")
@login_required
@company_required
def drives():
    # Search Implemented
    search_query = request.args.get('search', '').strip()
    company_id = current_user.company_data.id

    query = Drive.query.filter_by(company_id=company_id)

    if search_query:
        query = query.filter(
            db.or_(
                Drive.title.ilike(f'%{search_query}%'),
                Drive.status.ilike(f'%{search_query}%'),
                Drive.description.ilike(f'%{search_query}%'),
                Drive.requirements.ilike(f'%{search_query}%')

            )
        )

    all_drives = query.order_by(Drive.id.desc()).all()
    return render_template('company/drives.html', drives=all_drives, search=search_query)


# Profile
@company.route("/profile", methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    company = Company.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':

        logo_result = file_upload(
            file_key='logo_file',
            form_link_key='logo_url',
            upload_dir='logos', 
            prefix=f"logo_{company.id}"
        )

        if logo_result:
            company.logo = logo_result

        company.name = request.form.get('name')
        company.industry = request.form.get('industry')
        company.location = request.form.get('location')
        company.hr_contact = request.form.get('contact')
        company.email = request.form.get('email')
        company.employees_count = request.form.get('count')
        company.website = request.form.get('website')
        company.short_desc = request.form.get('short-desc')
        company.description = request.form.get('desc')

        db.session.commit()

        flash("Profile Updated Successfully", "success")
        return redirect(url_for('company.profile'))

    return render_template('company/profile.html', company=company)


# View Applications
@company.route("/view-applicants/<int:drive_id>")
@login_required
@company_required
def view_applicants(drive_id):
    drive = Drive.query.get(drive_id)
    if drive.company_id != current_user.company_data.id:
        return "Unauthorized", 403
    
    applicants = drive.job_application
    
    return render_template('company/view_applicants.html', drive=drive, applicants=applicants)


# Update Applicant Status
@company.route("/update-status/<int:app_id>", methods=['POST'])
@login_required
@company_required
def update_status(app_id):
    if request.method=='POST':
        app = Application.query.get(app_id)
        new_status = request.form.get('new_status')

        if new_status:
            app.status = new_status

            # Message Update
            new_notif = Notification(student_id=app.student_id,
            message=f"Your application for '{app.drive_details.title}' has been updated to: {new_status.capitalize()}.")
            
            db.session.add(new_notif)
            db.session.commit()
        
        flash("Applicant Status Updated", "success")
        return redirect(url_for('company.view_student', app_id=app_id))
    

# View Student
@company.route("/view-student/<int:app_id>", methods=['GET'])
@login_required
@company_required
def view_student(app_id):
    app = Application.query.get(app_id)
    student = app.student_details

    return render_template('company/view_student.html', item=student, app=app)


# Add Drive
@company.route("/add_drive", methods=['GET', 'POST'])
@login_required
@company_required
def add_drive():
    if request.method == 'POST':
        new = Drive(
            company_id=current_user.company_data.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            requirements=request.form.get('requirements'),
            package=request.form.get('package'),
            deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d').date()
        )
        db.session.add(new)
        db.session.commit()

        flash("Drive Added Successfully", "success")
        return redirect(url_for('company.manage_drive', drive_id=new.id))
    
    return render_template('company/add_drive.html')


# Manage Drive
@company.route("/manage_drive/<int:drive_id>")
@login_required
@company_required
def manage_drive(drive_id):
    item=Drive.query.get(drive_id)

    return render_template('company/manage_drive.html', item=item)


# Approval Pending
@company.route("/pending")
@login_required
def approval_pending():
    if current_user.role != 'company':
        return redirect(url_for('auth.login'))
    
    if current_user.company_data.status == 'approved':
        return redirect(url_for('company.company_dash'))
    
    return render_template('company/approval_pending.html')