# Routes for Student Pages
# URL : /...

from flask import url_for, redirect, render_template, Blueprint, request, flash
from flask_login import current_user, login_required
from main.decorators import student_required
from main.models import db, Company, Drive, Student, Users, Application, Notification
from sqlalchemy import or_
from datetime import date, datetime
from main.routes.utils import file_upload


#Blueprint
student = Blueprint('student', __name__)

# Dashboard
@student.route("/dashboard")
@login_required
@student_required
def student_dash():
    # Check for Empty Fields
    student = Student.query.filter_by(user_id=current_user.id).first()
    col=['fname', 'lname', 'roll', 'email', 'phone', 'cgpa', 'graduation_year', 'degree_field', 'batch', 'skills', 'bio', 'resume', 'github', 'linkedin', 'portfolio']
    count=0
    for i in col:
        val=getattr(student, i)
        if val and str(val).strip():
            count+=1
    profile_percentage=round(count/len(col)*100)

    # Recommended Drives
    skills_str = current_user.student_data.skills
    recommended_drives = []
    skill_filters = []

    if skills_str:
        skills = [s.strip() for s in skills_str.split(',') if s.strip()]
        for i in skills:
            skill_filters.append(Drive.requirements.contains(i))
            skill_filters.append(Drive.description.contains(i))
        recommended_drives = Drive.query.filter(Drive.status == 'approved', or_(*skill_filters)).limit(5).all()

    else:
        recommended_drives = Drive.query.filter_by(status='approved').order_by(Drive.id.desc()).limit(5).all()

    # recommended_drives=Drive.query.filter( or_(Drive.requirements.contains(current_user.student_data.skills), Drive.description.contains(current_user.student_data.skills))).limit(5)

    # Stats
    stats = {
    'selected' : Application.query.filter_by(student_id=student.id, status='selected').count(),
    'applied': Application.query.filter_by(student_id=student.id).count(),
    'shortlisted': Application.query.filter_by(student_id=student.id, status='shortlisted').count(),
    'open_drives': Drive.query.filter_by(status='approved').count(),
    'rejected' : Application.query.filter_by(student_id=student.id, status='rejected').count(),
    'curr_applied' : Application.query.filter_by(student_id=student.id, status='applied').count()
    }

    chart=[stats['selected'], stats['shortlisted'], stats['rejected'], stats['curr_applied']]

    print(stats)
    
    return render_template('student/dashboard.html', profile_percentage=profile_percentage, recommended_drives=recommended_drives, stats=stats, chart=chart)

# Drives
@student.route("/jobs")
@login_required
@student_required
def jobs():
    # Search
    search_query = request.args.get('search', '').strip()
    query = Drive.query.filter_by(status='approved')

    if search_query:
        query = query.join(Company).filter(
            db.or_(
                Drive.title.ilike(f'%{search_query}%'),
                Drive.description.ilike(f'%{search_query}%'),
                Company.name.ilike(f'%{search_query}%'),
                Drive.requirements.ilike(f'%{search_query}%')
            )
        )


    drives = query.order_by(Drive.id.desc()).all()
    
    applied_drive_ids = [app.drive_id for app in current_user.student_data.stu_application]

    return render_template('student/jobs.html', drives=drives, applied_ids=applied_drive_ids, search=search_query)

# Profile
@student.route("/profile", methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if request.method=='POST':
        resume_result = file_upload(
                file_key='resume_file',
                form_link_key='resume_url',
                upload_dir='resumes', 
                prefix=f"resume_{student.id}"
            )

        if resume_result:
            student.resume = resume_result

        student.fname = request.form.get('fname')
        student.lname = request.form.get('lname')
        student.email = request.form.get('email')
        student.phone = request.form.get('phone')
        student.cgpa = request.form.get('cgpa')
        student.graduation_year = request.form.get('graduation')
        student.degree_field = request.form.get('degree')
        student.batch = request.form.get('batch')
        student.skills = request.form.get('skills')
        student.bio = request.form.get('bio')
        student.github = request.form.get('github')
        student.linkedin = request.form.get('linkedin')
        student.portfolio = request.form.get('portfolio')

        db.session.commit()

        flash("Profile Updated", "success")
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html', student=student)

# Applications
@student.route("/applications")
@login_required
@student_required
def applications():
    student = current_user.student_data
    apps = Application.query.filter_by(student_id=student.id).order_by(Application.applied_at.desc()).all()

    return render_template('student/applications.html', applications=apps)

# Job View Details
@student.route("/job_view/<int:drive_id>", methods=['GET','POST'])
@login_required
@student_required
def job_view(drive_id):
    drive = Drive.query.get(drive_id)
    student = current_user.student_data
    already_applied = Application.query.filter_by(student_id=student.id, drive_id=drive.id).first()

    # Apply Button
    if request.method == 'POST':
        if already_applied:
            return redirect(url_for('student.job_view', drive_id=drive.id))
        
        # Validation for deadline
        if drive.deadline < datetime.now().date():
            flash("Deadline Crossed. Applications are no longer accepted.", "danger")
            return redirect(url_for('student.job_view', drive_id=drive_id))

        if drive.status != 'approved':
            flash("This drive is currently unavailable.", "warning")
            return redirect(url_for('student.job_view', drive_id=drive_id))

        new = Application(student_id=student.id, drive_id=drive.id, status='applied', applied_at=datetime.now())

        # add record to Applications
        db.session.add(new)
        db.session.commit()

        flash("Applied Successfully", "success")
        return redirect(url_for('student.applications'))

    return render_template('student/job_view.html', drive=drive, applied=already_applied)

# Student Notifications
@student.route("/notifications")
@student_required
@login_required
def notifications():
    noti=current_user.student_data.notifications
    
    return render_template('student/notifications.html', notifications=noti)

# Mark as read
@student.route("/notifications/mark-as-read", methods=['POST'])
@student_required
@login_required
def mark_as_read():
    student = current_user.student_data
    unread_notifications = Notification.query.filter_by(student_id=student.id, is_read=False).all()

    if request.method=='POST':
        for i in unread_notifications:
            i.is_read = True

    db.session.commit()

    flash("All Notifications Marked As Read.", "info")
    return redirect(url_for('student.notifications'))


# Not Approved Page - Blacklisted
@student.route("/not_approved")
@login_required
def not_approved():
    if current_user.role != 'student':
        return redirect(url_for('auth.login'))
    
    if current_user.student_data.status == 'approved':
        return redirect(url_for('student.student_dash'))
    
    return render_template('student/not_approved.html')