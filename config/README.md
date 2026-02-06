# 🚗 Ride Sharing Backend API

A Django REST Framework based backend API for a basic ride-sharing system.  
This project provides authentication, ride management, driver assignment, ride status updates, real-time location simulation, testing, and interactive API documentation using Swagger.

---

## 🌐 Live Swagger Documentation

https://ride-share-zartek.onrender.com/swagger/

---

## ✅ Features

- User Registration & Login (JWT)
- Create Ride Request
- List & View Rides
- Driver Accept Ride
- Start / Complete / Cancel Ride
- Ride Location Update
- Pagination
- Automated Tests
- Swagger API Docs

---

## ⚙️ Local Setup

```bash
git clone https://github.com/tomkondody/Ride_Share-Zartek.git
cd config
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
