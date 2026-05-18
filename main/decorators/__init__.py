# Special Decorators

from functools import wraps
from flask import redirect, url_for
from flask_login import current_user


# Milestone: Flask-Login Integration and Security - Already Completed - Only Admin can access these pages
# Required Admin role in DB to Access these pages
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            elif current_user.role == 'company':
                return redirect(url_for('company.company_dash'))
            elif current_user.role == 'student':
                return redirect(url_for('student.student_dash'))    
        else:
            return redirect(url_for('auth.login'))
    return decorated_function


# Milestone: Flask-Login Integration and Security - Already Completed - Only Company can access these pages
# Required Company role in DB to Access these pages
def company_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.admin_dash'))
            elif current_user.role == 'company':
                # Check if Company is Approved, If Company's Profile is Completed 
                if current_user.profile_completed:
                    if current_user.company_data.status=='approved':
                        return f(*args, **kwargs)
                    else:
                        return redirect(url_for('company.approval_pending')) 
                else:
                        return redirect(url_for('auth.onboarding'))
            elif current_user.role == 'student':
                return redirect(url_for('student.student_dash'))    
        else:
            return redirect(url_for('auth.login'))
    return decorated_function


# Milestone: Flask-Login Integration and Security - Already Completed - Only Students can access these pages
# Required Student role in DB to Access these pages
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.admin_dash'))
            elif current_user.role == 'company':
                    return redirect(url_for('company.company_dash'))
            elif current_user.role == 'student':
                # Check if Profile IS Completed or not, if Student is Approved
                if current_user.student_data.status=='approved':
                    if current_user.profile_completed:
                        return f(*args, **kwargs)
                    else:
                        return redirect(url_for('auth.onboarding')) 
                else:
                        return redirect(url_for('student.not_approved'))                    
        else:
            return redirect(url_for('auth.login'))
    return decorated_function


# Redirect to respective Home Pages
def home(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.admin_dash'))
            elif current_user.role == 'company':
                if current_user.profile_completed:
                    return redirect(url_for('company.company_dash'))
                else:
                    return redirect(url_for('auth.onboarding'))
            elif current_user.role == 'student':
                if current_user.profile_completed:
                    return redirect(url_for('student.student_dash'))
                else:
                    return redirect(url_for('auth.onboarding'))
        return f(*args, **kwargs)
    return decorated_function