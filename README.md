# Lahore Car Rental API

This repository contains a Django and Django REST Framework backend API for Lahore car Rental. The application serves as the backend for managing users, vehicles, and bookings for an independent car rental business.


## Table of Contents
- [1Now](#1now)
- [Frontend Connection](#frontend-connection)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Running Tests](#running-tests)
- [Sample Requests/Responses](#sample-requestsresponses)
- [API Documentation](#api-documentation)
- [Implemented Bonus Tasks](#implemented-bonus-tasks)
- [Assumptions](#assumptions)


## 1Now

- 1Now is a car rental service that allows users to put up their vehicles for rent and other users can then book them as needed after communicating with the owner.
- 1Now is an alternative to Turo, which is the popular car rental service. It provides a unified platform for owners and renters to provide and book vehicles.
- 1Now differs from Turo in the way that it provides the customers (especially big rental companies) with a private service such that they do not need to share the revenue made on the platform with anyone else which is the case with Turo.


## Frontend Connection

- The backend is bulit using REST APIs making it very easy for frontend applications (Mobile or Web) to connect with it.
- Users can use any library that their development stack provides (e.g. fetch for JavaScript) to request the APIs for authentication and then further use the data-centric APIs requesting them with the obtained Authentication JWT token in the headers to get and modify the data as needed by the customers.


## Features

- **User Authentication:**
  - **Register:** POST `/register/`
  - **Login:** POST `/login/` (returns JWT access and refresh tokens)
  - **Access Token Refresh:** POST `/auth-refresh/`

- **Vehicle Management:**
  - **List Vehicles:** GET `/vehicles/` (shows vehicles belonging to the authenticated user)
  - **Create Vehicle:** POST `/vehicles/`
  - **Update Vehicle:** PUT `/vehicles/{id}/`
  - **Delete Vehicle:** DELETE `/vehicles/{id}/`

- **Booking Management:**
  - **List Bookings:** GET `/bookings/` (returns bookings for the authenticated user)
  - **Create Booking:** POST `/bookings/`
    - Prevents overlapping bookings with custom validation in the serializer.

- **Security:**
  - JWT is used for authentication.
  - Only logged-in users can access the vehicles and the bookings.

- **API Documentation:**
  - Swagger UI available at `/api/schema/swagger-ui/` (powered by drf-spectacular).

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hammadbinsajjad/Lahore-Car-Rental.git
   cd lahore-car-rental
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python3 manage.py migrate
   ```

5. **Run the development server:**

   ```bash
   python3 manage.py runserver
   ```

   The API will be accessible locally at `http://localhost:8000/`.

## Running Tests

Execute the tests using Django’s test runner:

```bash
python3 manage.py test
```

Each module (Authentication, Vehicles, Bookings) includes unit tests covering each's functionality (authentication, edge cases etc).

## Sample Requests/Responses

### Register a New User

**POST** `/register/`

**Request Body:**
```json
{
  "username": "hammad",
  "password": "Pass_123"
}
```

**Response:**
```json
{
	"email": "",
	"username": "hammad",
	"id": 1
}
```

### Login

**POST** `/login/`

**Request Body:**
```json
{
  "username": "hammad",
  "password": "Pass_123"
}
```

**Response:**
```json
{
  "access": "<access_token_here>",
  "refresh": "<refresh_token_here>"
}
```


#### Authentication

All endpoints for vehicles and bookings require authentication. Use the JWT access token obtained from the login endpoint in the `Authorization` header as follows:
```
{
	"Authorization": "Bearer <access_token_here>",
}
```

### List Vehicles
**GET** `/vehicles/`

**Response:**
```json
[
  {
    "id": 2,
    "make": "test2-make",
    "model": "test2-model",
    "year": 2024,
    "plate": "test2-plate"
  },
  {
    "id": 3,
    "make": "test3-make",
    "model": "test3-model",
    "year": 2025,
    "plate": "test3-plate"
  },
  {
    "id": 4,
    "make": "test4-make",
    "model": "test4-model",
    "year": 2025,
    "plate": "test4-plate"
  }
]
```


### Create a Booking (Preventing Overlaps)

When a booking overlaps with an existing booking, the response is:


**POST** `/bookings/`

**Request Body:**
```json
{
	"vehicle": 4,
	"start_date": "2024-12-10",
	"end_date": "2024-12-11"
}
```

**Response (HTTP 201):**
```json
{
	"id": 5,
	"vehicle": 4,
	"start_date": "2024-12-10",
	"end_date": "2024-12-11"
}
```


**Response (HTTP 400):**
```json
{
  "error": "Booking already exists on 01 November 2025 to 02 November 2025"
}
```

## API Documentation

While there are some sample API endpoints shown above, for full documentation, please setup the project and see the Swagger UI.

Access the interactive Swagger UI for the documentation at:
`http://localhost:8000/api/schema/swagger-ui/`

The API schema is generated using [drf-spectacular](https://drf-spectacular.readthedocs.io/).

## Implemented Bonus Tasks

- **Booking Overlap Prevention:**
  The system prevents overlapping bookings using custom validators in the Booking serializer. The validator checks if there exists some other booking for the same vehicle that with the new booking's start and end dates. If none exists, the booking is created successfully. Otherwise, an error is returned indicating that a booking already exists and its duration to notify the user from and till when it is not available.


## Assumptions

Some assumptitions I made while implementing the project are:

- The vehicle fields `[make, model, plate]` are all set to be string types.
- The vehicle field `year` is set to be an integer type (for simplicity) as year will always be an integer.
- The booking fields `[start_date, end_date]` are set to be date types and do not have any info related to the exact timings for the booked cars.
- I have used Django's built-in User model for all user related tasks.
- I have used the following third-party libraries:
  - `djangorestframework` for building the core REST API.
  - `djangorestframework-simplejwt` for JWT creation and authentication.
  - `djoser` for user registration (to save time as it has many features).
  - `drf-spectacular` for generating the OpenAPI schema and Swagger UI.
