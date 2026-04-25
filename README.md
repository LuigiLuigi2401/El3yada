# El3yada - Patient Management System (عيادات العيادة الملكية التخصصية)

![Django](https://img.shields.io/badge/Django-4.1-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

El3yada is a comprehensive backend patient management and ERP system built with Django and Django REST Framework. The system is tailored specifically to digitize and manage the day-to-day operations of **El3yada Clinic (عيادات العيادة الملكية التخصصية)**. It provides a robust architecture for managing patients, doctor appointments, overall financials (patient payments and clinic expenses), and clinical services.

## ✨ Key Features

- **🧑‍⚕️ Patient Management**: Maintain secure, detailed records of patients including personal data, medical notes, admission history, and outstanding debts.
- **📅 Appointment Scheduling**: An efficient booking system that tracks doctors, assigned clinical services, fees, patient attendance (arrived/seen), and payment states.
- **💰 Financial Module**: 
  - Track patient payments against specific appointments.
  - Manage overall clinic expenses (utility bills, internet, medical supplies).
  - Manage suppliers and clinical resources.
- **🩺 Doctor & Service Management**: Dynamically link doctors to various clinical services with specific pricing and cost structures.
- **⚙️ RESTful API**: Exposes a full suite of JSON endpoints using Django REST Framework (DRF) for seamless frontend integration.
- **🔒 Authentication**: Secure JWT-based authentication (via `Rest Framework SimpleJWT`) ensuring that only authorized staff can manage records.

## 🛠️ Technology Stack

- **Backend framework**: Python, Django (v4.1)
- **API framework**: Django REST Framework
- **Authentication**: SimpleJWT
- **Database**: SQLite3 (Configurable to PostgreSQL/MySQL)
- **Data Handling**: Pandas, Openpyxl (For data import/export)
- **Websockets/Async**: Django Channels

## 🚀 Installation & Setup

Follow these steps to get your development environment running:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd El3yada
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install the project dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```bash
   cd El3yada
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create an admin user:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

You can now access the backend at `http://127.0.0.1:8000/`.

## 📡 API Endpoints Overview

The system includes multiple robust API endpoints mainly configured under `MainMenu`. Some of the core endpoints include:

- `GET/POST /api/patients/` - View, create, and manage patient records.
- `GET/POST /api/appointments/` - Track and schedule patient appointments.
- `GET /api/doctors/` - Retrieve a list of doctors and their configured clinical services.
- `GET/POST /api/payments/` - Manage appointment-based payments and financial tracking.
- *(More specific endpoints handle debt management, daily views, and clinic expenses).*

## 🏗️ Project Structure
- **`MainMenu/`**: Core application handling Models (Patient, Appointments, Payments, Expenses) and API endpoints. 
- **`login/`**: Application module containing potential data import/export structures (Excel/Pandas) and authentication hooks.
- **`El3yada/`**: The core Django project configuration folder (settings, urls, asgi/wsgi).

---

**Developed for El3yada Clinic (عيادات العيادة الملكية التخصصية) to streamline administration and enhance patient care.**
