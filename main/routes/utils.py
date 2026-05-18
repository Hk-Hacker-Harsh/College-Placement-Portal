import os
from werkzeug.utils import secure_filename
from flask import request, url_for

# File Upload for both Student and Company, Will return URL
def file_upload(file_key, form_link_key, upload_dir, prefix):
    file = request.files.get(file_key)
    
    if file and file.filename != '':
        filename = secure_filename(f"{prefix}_{file.filename}")
        
        full_dir = os.path.join('main/static/uploads', upload_dir)
            
        file.save(os.path.join(full_dir, filename))
        return url_for('static', filename=f'uploads/{upload_dir}/{filename}', _external=True)
    
    return request.form.get(form_link_key)