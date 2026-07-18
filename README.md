# 🏥 MediLink

<div align="center">

### A Modern Healthcare Management Platform built with Flask

*A full-stack healthcare management system that seamlessly connects **Patients**, **Doctors**, **Hospitals**, and **Administrators** through a secure and intuitive web application.*

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge\&logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?style=for-the-badge\&logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge\&logo=sqlite)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge\&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)

</div>

---

# 📌 Overview

MediLink is a comprehensive healthcare management platform designed to simplify communication and workflow between patients, doctors, hospitals, and administrators.

The project focuses on secure authentication, role-based access control, appointment scheduling, prescription management, medical record storage, and analytics dashboards.

This project was built as a portfolio project to demonstrate full-stack web development using Flask.

---

# ✨ Features

## 👤 Patient

* Register and login securely
* Manage personal profile
* Book appointments
* View appointment history
* Upload medical records
* Download uploaded documents
* Delete medical records
* Receive notifications
* View prescriptions

---

## 👨‍⚕️ Doctor

* Secure login
* Manage appointments
* Accept or reject appointments
* Upload prescriptions
* View patient information
* Dashboard with appointment statistics
* Notification support

---

## 🏥 Hospital

* Create and manage hospital profile
* Add doctors
* Edit doctor information
* Remove doctors
* View appointments
* Dashboard analytics
* Track doctors and patients

---

## 🛡️ Administrator

* Admin dashboard
* Platform analytics
* User statistics
* Doctor statistics
* Hospital statistics
* Appointment statistics
* Platform activity monitoring

---

# 🔐 Security Features

* Password hashing
* Flask-Login authentication
* Role-Based Access Control (RBAC)
* Protected routes
* CSRF protection using Flask-WTF
* Secure file uploads
* Upload size restrictions
* Unique filenames using UUID
* SQLAlchemy ORM (prevents SQL Injection)
* IDOR protection for medical records
* Ownership validation before downloads
* Ownership validation before deletion

---

# 🛠 Tech Stack

### Backend

* Python
* Flask
* Flask-Login
* Flask-WTF
* Flask-Mail
* SQLAlchemy

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Jinja2
* Font Awesome

### Database

* SQLite

### Charts

* Chart.js

### Tools

* Git
* GitHub
* VS Code

---

# 📸 Screenshots

> Add screenshots here after uploading them.

## Landing Page

```
images/landing-page.png
```

## Patient Dashboard

```
images/patient-dashboard.png
```

## Doctor Dashboard

```
images/doctor-dashboard.png
```

## Hospital Dashboard

```
images/hospital-dashboard.png
```

## Admin Dashboard

```
images/admin-dashboard.png
```

---

# 📂 Project Structure

```text
MediLink/
│
├── database/
├── models/
├── routes/
├── forms/
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── app.py
├── config.py
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

```bash
# Clone repository
git clone https://github.com/Rohan26096/MediLink.git

# Navigate
cd MediLink

# Create virtual environment
python -m venv venv

# Activate environment

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

---

# 👨‍⚕️ User Roles

| Role     | Features                                              |
| -------- | ----------------------------------------------------- |
| Patient  | Book appointments, upload records, view prescriptions |
| Doctor   | Manage appointments, upload prescriptions             |
| Hospital | Manage doctors, monitor appointments                  |
| Admin    | Manage entire platform                                |

---

# 📊 Database

Core entities include:

* Users
* Patients
* Doctors
* Hospitals
* Appointments
* Prescriptions
* Medical Records
* Notifications

---

# 📈 Project Highlights

* Secure Authentication System
* Role-Based Authorization
* Email Notifications
* Dashboard Analytics
* Medical Record Uploads
* Appointment Management
* Prescription Management
* Responsive UI
* Dark Mode Support
* Modular Flask Blueprints

---

# 🎯 Future Enhancements

* PostgreSQL Support
* Docker Deployment
* REST API
* JWT Authentication
* Video Consultation
* Payment Integration
* AI Health Assistant
* SMS Notifications
* Multi-Hospital Support
* Cloud File Storage

---

# 🤝 Contributing

Contributions, suggestions, and feature requests are welcome.

If you would like to contribute:

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 👨‍💻 Author

**Rohan**

Computer Science Engineering Student

Passionate about Full-Stack Development, Machine Learning, and Data Structures & Algorithms.

---

# 📄 License

This project is intended for educational and portfolio purposes.

---

<div align="center">

### ⭐ If you like this project, don't forget to star the repository!

**Made with ❤️ using Flask**

</div>
