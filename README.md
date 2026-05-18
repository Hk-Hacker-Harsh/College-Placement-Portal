# College Placement Portal Application

A comprehensive, role-based Web Application built to streamline campus recruitments. The portal facilitates seamless interactions between the Institute Admin, Corporate Recruiters (Companies), and Students throughout the hiring lifecycle.

---

## 🚀 Features

### 👤 Multi-Role Functionality
* **Admin Dashboard:** Full supervision of the platform. View platform metrics such as Success Rate, Total Students, and Active Drives. Approve or reject job drives, manage or blacklist student accounts, and handle company approvals.
* **Company Dashboard:** Complete profile setup, corporate onboarding, job drive management (create, update, or close recruitment drives), and real-time applicant tracking.
* **Student Dashboard:** Comprehensive profile construction (academic details, skills, resume upload), personalized job recommendations based on skills, simple one-click applications, and automated status update notifications.

### 🛡️ Security & Core System Features
* **Secure Authentication:** User authentication, password hashing, and session management using `Flask-Login` and `Werkzeug.security`.
* **Mandatory Onboarding:** Strict guard rails preventing students or companies from accessing internal portal features until their profile onboarding form is submitted.
* **Data Analytics:** Integrated visual tracking via `Chart.js` rendering statistics cards and interactive graphs on dashboards.
* **Responsive UI:** Clean, mobile-friendly interface designed with `Bootstrap`.

---

## 🛠️ Technologies & Frameworks Used

| Technology/Library | Purpose |
| :--- | :--- |
| **Flask** | Python Backend Lib |
| **SQLAlchemy** | Connection between Python and SQLite DB |
| **SQLite** | DataBase |
| **Jinja** | Template Engine for Dynamic HTML Pages |
| **Bootstrap** | Frontend Styling and Responsive Design |
| **Chart.js** | Graphs and Analytics |
| **Flask-Login** | User Authentication and Session Management |
| **Werkzeug.security** | Converting Password to Hash |

---

## 📁 Project Structure

The codebase follows a structured modular layout:

```
Project Folder/
├── app.py                # Main Python File (Application Entry Point)
└── main/
    ├── decorators/       # Custom Route Protection & Role-Based Access Controls
    ├── models/           # SQLAlchemy Database Schema Definitions
    ├── routes/           # Blueprint Route Definitions (Admin, Company, Student)
    └── templates/        # Jinja2 Dynamic HTML Templates
        ├── admin/        # Admin HTML Files
        ├── company/      # Company HTML Files
        └── student/      # Student HTML Files
```

*(Note: Static assets such as custom CSS, JS, and user uploads are managed within the standard static/ folder directory).*

---

## 📊 Database Schema & Relationships

The backend relies on an SQLite database mapped via SQLAlchemy with the following core entity definitions and relationships:

### Tables
* **Users:** Stores User Id, Password (hashed), and Role (Admin, Student, or Company).
* **Student:** Stores details related to students (Academic records, skills, resume link).
* **Company:** Stores corporate details (Name, website, profile verification status, and logo).
* **Drive:** Stores Job Drives and recruitment criteria posted by verified companies.
* **Application:** Stores individual application transactions linking students to specific drives.
* **Notification:** Stores dynamic application status update notifications alerts for students.

### Relationships
* **One-to-One:**
  * Users <-> Student
  * Users <-> Company
* **One-to-Many:**
  * Company -> Drive
  * Drive -> Application
  * Student -> Application
  * Student -> Notification

---

## ⚙️ Installation & Setup

Follow these steps to set up and run the application locally:

### 1. Clone the Repository
git clone https://github.com/your-username/college-placement-portal.git
cd college-placement-portal

### 2. Set Up a Virtual Environment
# Windows
```
python -m venv venv
venv\Scripts\activate
``` 
# macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Required Dependencies
Create a requirements.txt file targeting the system dependencies (Flask, Flask-SQLAlchemy, Flask-Login, etc.) and execute:
```pip install -r requirements.txt```

### 4. Initialize Database & Run the Server
Launch the application execution script:
```
python app.py
```

The application will deploy locally at http://127.0.0.1:5000/.

---

## 📝 License

This project was built as part of the College Placement Portal Framework initiative. All rights reserved.



----------------------
# Placement Portal MAD-1 Project Jan 2026

- placement-portal-application-mad1-jan-2026
- A Placement Portal Application web application that allows Admin (Institute), Company, and students to interact with the system based on their roles.

### How to Run this Project
- git clone < Project Git Repo URL >
- pip install -r requirements.txt
- python3 app.py

### Access
- Open http://127.0.0.1:5000/ On Browser


### Other Details
Doc : https://getbootstrap.com/docs/5.3/


### Milestone commits:
git add .
git commit -m "<message>"
git status
git push origin main


### Updates
24 Mar 26 : Added Models, done connection, db realted things done, admin on db creation, milestone 1 completed.
till now i have completed my project file structure
now will work on db and models.py first

31 Mar 26 : Login : All, Registration : Company & Students, Company Approve or Delete in Admin, Company Approval Pending Page on Admin, Nav Bar Dynamic, Page Access Restrictions as Per Role.  

03 Apr 26 : Change in Compant Model (is_approved to Status) added Actions like Rejected or Blacklisted and new tab Rejected/Blacklisted in Company Page for Admin. Added status attribute in students. Onboarding page and Attributes in Company and Student. login/registration UI. Complete Admin Panel (inc. Dashboard, Paths, View Profile, Search Bar etc.), Landing Page.

07 Apr 26 : Approval Pending Page : Student, Company. Student : Dashboard, Profile, Jobs Page, Applications, Job View

08 Apr 26 : Company : Dashboard, Drive Page, Profile, add drive, manage drive, view drive, view student, view applicants. Resume And Logo Upload. 
Search Drive Company and Student.

08 Apr 26 : Notifications. Jobs Milestone all Requirements already fullfilled. Flash Messages. Testing

09 Apr 26 : Improvements. Milestone: Flask-Login Integration and Security : Already Completed, just highlight using comments and improvement, flask login already implemented.

09 Apr 26 : Added Viewport Metatag for REsponsiveness. Bootstrap Already Implemented in HTML.

09 Apr 26 : Backend and Frontend Validations (Specially in Onboarding and Registration)

09 Apr 26 : Chart.js. 1 chart in student (doughnut), 1 in company (horizontal bar chart), 2 in admin (pie, bar)

09 Apr 26 : Testing. Deadline Bug Repair. Report. Video. Final Submission.