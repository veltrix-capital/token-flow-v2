# Token Flow Analytics API

A Django-based backend API to trace and analyze token movements such as rewards, redemptions, transfers, and swaps between users and businesses.

---

## Setup Instructions

1. Clone the repository

   - git clone https://github.com/veltrix-capital/token-flow-v2.git
   - cd token-flow-v2

2. Create and activate a virtual environment

   ### On Unix/macOS

   - python3 -m venv venv
   - source venv/bin/activate

   ### On Windows

   - python -m venv venv
   - .\venv\Scripts\activate.bat

3. Install dependencies

   - pip install -r requirements.txt

4. Apply database migrations

   - python manage.py makemigrations
   - python manage.py migrate

5. Seed sample data

   - python manage.py seed

6. Run the development server

   - python manage.py runserver

---

## API Endpoints

Base URL: http://localhost:8000/api/

### Users

- GET /api/users/ — List all users
- GET /api/users/<id>/ — Get user by ID
- GET /api/users/<id>/events/ — Get all events for a user
- GET /api/users/<id>/reward/ — User's reward events
- GET /api/users/<id>/redeem/ — User's redeem events
- GET /api/users/<id>/transfer-in/ — Transfers received by the user
- GET /api/users/<id>/transfer-out/ — Transfers sent by the user
- GET /api/users/<id>/swap/ — All swaps involving the user

### Businesses

- GET /api/businesses/ — List all businesses
- GET /api/businesses/<id>/ — Get business by ID
- GET /api/businesses/<id>/rewards — Get list of reward events
- GET /api/businesses/<id>/redeems — Get list of redeem events
- GET /api/businesses/<id>/balance/?user=<user_address> — Get balance of token for a user
- GET /api/businesses/<id>/token-inflows/?user=<user_address> — Token inflows for a user

### Events

- GET /api/events/ — List all events (Reward, Redeem, Transfer, Swap)

Each event includes a `type` field that indicates the event type.

---

## Technologies

- Python 3.11+
- Django 5.x
- Django REST Framework
- django-polymorphic

---

## Running Tests (optional)

    python manage.py test

---

## License

This project is licensed under the MIT License.
