# Routes for admin User
# URL : /admin/...

from flask import Flask, url_for, redirect, request, render_template, Blueprint, flash
from sqlalchemy import or_
from flask_login import current_user, login_required
from main.decorators import admin_required
from main.models import db, Company, Drive, Student, Users, Application
from datetime import date


#Blueprint

admin = Blueprint('admin', __name__)

@admin.route("/dashboard")
@login_required
@admin_required
def admin_dash():
    # Send Data to Dashboard
    stats = {
        'students': Student.query.count(),
        'companies': Company.query.filter_by(status='approved').count(),
        'pending_companies': Company.query.filter_by(status='pending').count(),
        'drives': Drive.query.count(),
        'total_apps': Application.query.count(),
        'blacklisted': Student.query.filter_by(status='blacklisted').count(),
        'current_time':date.today(),
        'selected': Application.query.filter_by(status='selected').count(),
        'shortlisted' : Application.query.filter_by(status='shortlisted').count(),
        'rejected' : Application.query.filter_by(status='rejected').count(),
        'applied' : Application.query.filter_by(status='applied').count()
    }

    # Chart
    pie=[stats['selected'], stats['shortlisted'], stats['rejected'], stats['applied']]
    bar=[stats['drives'], stats['total_apps'], stats['selected']]

    stats['success_rate'] = round((stats['selected'] / stats['total_apps'] * 100), 1) if stats['total_apps'] > 0 else 0

    recent_companies = Company.query.order_by(Company.id.desc()).limit(5).all()
    recent_drives = Drive.query.order_by(Drive.id.desc()).limit(5).all()

    return render_template('admin/dashboard.html', stats=stats, recent_companies=recent_companies, recent_drives=recent_drives, pie=pie, bar=bar)

@admin.route("/company")
@login_required
@admin_required
def company():
    # Company Data
    company_pending=Company.query.filter_by(status='pending').all()
    company_approved=Company.query.filter_by(status='approved').all()
    company_rejected_or_blacklisted=Company.query.filter(Company.status.in_(['rejected', 'blacklisted'])).all()

    return render_template('admin/company.html', companies_pending=company_pending, companies_approved=company_approved, company_rejected_or_blacklisted=company_rejected_or_blacklisted)

@admin.route("/drive")
@login_required
@admin_required
def drive():
    # Drive Data
    drive_pending=Drive.query.filter_by(status='pending').all()
    drive_approved=Drive.query.filter_by(status='approved').all()
    drive_rejected=Drive.query.filter_by(status='rejected').all()
    drive_closed=Drive.query.filter_by(status='closed').all()
    print(drive_pending)

    return render_template('admin/drive.html', drive_pending=drive_pending, drive_approved=drive_approved, drive_rejected=drive_rejected, drive_closed=drive_closed)

@admin.route("/student")
@login_required
@admin_required
def student():
    # Student Data
    student_approved=Student.query.filter_by(status='approved').all()
    student_blacklisted=Student.query.filter_by(status='blacklisted').all()

    return render_template('admin/student.html', student_approved=student_approved, student_blacklisted=student_blacklisted)

@admin.route("/application")
@login_required
@admin_required
def application():
    # Applications Data
    app_all=Application.query.all()
    app_applied=Application.query.filter_by(status="applied").all()
    app_shortlisted=Application.query.filter_by(status="shortlisted").all()
    app_selected=Application.query.filter_by(status="selected").all()
    app_rejected=Application.query.filter_by(status="rejected").all()

    return render_template('admin/application.html', app_all=app_all, app_applied=app_applied, app_shortlisted=app_shortlisted, app_selected=app_selected, app_rejected=app_rejected)

@admin.route("/")
def redirect_admin():
    return redirect(url_for('admin.admin_dash'))

# Company Action Buttons
@admin.route("/approve_company/<int:id>", methods=['POST'])
@login_required
@admin_required
def approve_company(id): # Approve Button
    company=Company.query.get(id)
    company.status='approved'
    db.session.commit()
    
    flash("Company Approved", "success")
    # Redirect back to company page
    return redirect(url_for('admin.company'))

@admin.route("/delete_company/<int:id>", methods=['POST'])
@login_required
@admin_required
def delete_company(id): # Delete Button
    company=Company.query.get(id)
    # Before Company, We first need to delete Companies Drives.
    Drive.query.filter_by(company_id=id).delete()
    
    # Delete Respective User Record from Users Table
    user = Users.query.get(company.user_id)

    db.session.delete(user)
    db.session.delete(company)
    db.session.commit()

    flash("Company Deleted", "danger")
    return redirect(url_for('admin.company'))

@admin.route("/reject_company/<int:id>", methods=['POST'])
@login_required
@admin_required
def reject_company(id): # Reject Button
    company=Company.query.get(id)
    company.status='rejected'
    db.session.commit()
    
    flash("Company Rejected", "warning")
    # Redirect back to company page
    return redirect(url_for('admin.company'))

@admin.route("/blacklist_company/<int:id>", methods=['POST'])
@login_required
@admin_required
def blacklist_company(id): # Backlist Button
    company=Company.query.get(id)
    company.status='blacklisted'
    db.session.commit()
    
    flash("Company Blacklisted", "warning")
    # Redirect back to company page
    return redirect(url_for('admin.company'))


# Student Action Buttons
@admin.route("/delete_student/<int:id>", methods=['POST'])
@login_required
@admin_required
def delete_student(id): # Delete Button
    student=Student.query.get(id)

    # Before Company, We first need to delete Companies Drives.
    Application.query.filter_by(student_id=id).delete()
    
    # Delete Respective User Record from Users Table
    user = Users.query.get(student.user_id)

    db.session.delete(user)
    db.session.delete(student)
    db.session.commit()
    
    flash("Student Deleted", "danger")
    return redirect(url_for('admin.student'))

@admin.route("/blacklist_student/<int:id>", methods=['POST'])
@login_required
@admin_required
def blacklist_student(id): # Blacklist Button
    student=Student.query.get(id)
    student.status='blacklisted'
    db.session.commit()
    
    flash("Student Blacklisted", "warning")
    # Redirect back to company page
    return redirect(url_for('admin.student'))

@admin.route("/approve_student/<int:id>", methods=['POST'])
@login_required
@admin_required
def approve_student(id): # Approve Button
    student=Student.query.get(id)
    student.status='approved'
    db.session.commit()

    flash("Student Approved", "success")
    # Redirect back to company page
    return redirect(url_for('admin.student'))

# Drive Action Buttons
@admin.route("/delete_drive/<int:id>", methods=['POST'])
@login_required
@admin_required
def delete_drive(id): # Delete Button
    drive=Drive.query.get(id)

    # Before Company, We first need to delete Companies Drives.
    Application.query.filter_by(drive_id=id).delete()

    db.session.delete(drive)
    db.session.commit()

    flash("Drive Deleted", "danger")
    return redirect(url_for('admin.drive'))

@admin.route("/close_drive/<int:id>", methods=['POST'])
@login_required
@admin_required
def close_drive(id): # Close Button
    drive=Drive.query.get(id)
    drive.status='closed'
    db.session.commit()
    
    flash("Drive Closed", "warning")
    # Redirect back to company page
    return redirect(url_for('admin.drive'))

@admin.route("/approve_drive/<int:id>", methods=['POST'])
@login_required
@admin_required
def approve_drive(id): #Approve Button
    drive=Drive.query.get(id)
    drive.status='approved'
    db.session.commit()
    
    flash("Drive Approved", "success")
    # Redirect back to company page
    return redirect(url_for('admin.drive'))

@admin.route("/reject_drive/<int:id>", methods=['POST'])
@login_required
@admin_required
def reject_drive(id): #Reject Button
    drive=Drive.query.get(id)
    drive.status='rejected'
    db.session.commit()
    
    flash("Drive Rejected", "warning")
    # Redirect back to company page
    return redirect(url_for('admin.drive'))

# Applications Action Buttons
@admin.route("/delete_app/<int:id>", methods=['POST'])
@login_required
@admin_required
def delete_app(id): #Delete Button
    app=Application.query.get(id)

    db.session.delete(app)
    db.session.commit()

    flash("Application Deleted", "danger")
    return redirect(url_for('admin.application'))

# Search
@admin.route('/search')
@login_required
@admin_required
def admin_search():
    # Get the query and the "Type" (company, student, or drive)
    q = request.args.get('q', '')
    category = request.args.get('type')
    
    results = []

    if category == 'company':
        results = Company.query.filter(or_(
            Company.id.ilike(f'%{q}%'),
            Company.name.ilike(f'%{q}%'),
            Company.website.ilike(f'%{q}%'),
            Company.hr_contact.ilike(f'%{q}%'),
            Company.description.ilike(f'%{q}%')
            )).all()
    elif category == 'student':
        results = Student.query.filter(or_(
            Student.id.ilike(f'%{q}%'),
            Student.fname.ilike(f'%{q}%'),
            Student.lname.ilike(f'%{q}%'),
            Student.roll.ilike(f'%{q}%'),
            Student.skills.ilike(f'%{q}%')
            )).all()
    elif category == 'drive':
        results = Drive.query.filter(or_(
            Drive.id.ilike(f'%{q}%'),
            Drive.title.ilike(f'%{q}%'),
            Drive.description.ilike(f'%{q}%'),
            Drive.requirements.ilike(f'%{q}%')
            )).all()

    return render_template('admin/search_results.html', 
                           results=results, 
                           q=q, 
                           category=category)

# Single Route for Show Details
@admin.route('/view/<string:category>/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def view(category, id):
    item = None
    if category == 'company':
        item = Company.query.get(id)
    elif category == 'student':
        item = Student.query.get(id)
    elif category == 'drive':
        item = Drive.query.get(id)
    elif category == 'application':
        item = Application.query.get(id)

    if request.method=='POST':
        # Company, Student Status
        new_status = request.form.get('status')
        
        if new_status:
            item.status=new_status
            db.session.commit()
            return redirect(url_for('admin.view', category=category, id=id))

    return render_template(f'admin/view/view_{category}.html', item=item)