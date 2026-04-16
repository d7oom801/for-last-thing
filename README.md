# MediSketch

MediSketch is a medical appointment booking system built with Django and Django REST Framework.

## Prerequisites

*   Python 3.8+
*   pip

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/FarisAlanazi/MediSketch.git
    cd MediSketch
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install django djangorestframework django-cors-headers
    ```

4.  **Apply migrations:**
    ```bash
    cd med
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser (admin):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the server:**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Authentication
*   **Login:** `POST /api-token-auth/`
    *   Body: `{"username": "...", "password": "..."}`
    *   Returns: Token, User ID, User Type

### Registration
*   **Register Patient:** `POST /patients/`
    *   Body:
        ```json
        {
            "user": {
                "username": "patient1",
                "password": "password123",
                "email": "patient@example.com",
                "phone_number": "+966500000000"
            },
            "first_name": "John",
            "last_name": "Doe",
            "age": 30,
            "gender": "Male",
            "phone": "0500000000",
            "email": "patient@example.com"
        }
        ```

*   **Register Doctor:** `POST /doctors/`
    *   Body:
        ```json
        {
            "user": {
                "username": "dr_smith",
                "password": "password123",
                "email": "dr.smith@example.com",
                "phone_number": "+966511111111"
            },
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 45,
            "gender": "Female",
            "phone": "0511111111",
            "email": "dr.smith@example.com",
            "price": 200,
            "specialization": 1,
            "clinic_name": "City Clinic",
            "qualification": "MBBS",
            "Med_id": "12345",
            "about_me": "Experienced...",
            "years_of_experience": 15
        }
        ```
