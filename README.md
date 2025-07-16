# 🏥 Medical Appointment Booking System API

A backend system for managing medical appointment bookings, built for university-level backend development practice (year 3 students). It includes user authentication, role-based access control, scheduling logic, and appointment management between patients and doctors.

---

## 🚀 Features

- User registration and login (JWT-based)
- Role-based access (Admin / Doctor / Patient)
- Patient profile management
- Doctor profile and working schedule setup
- Appointment booking by patients
- Appointment approval or cancellation by doctors
- Schedule conflict prevention
- Email notification system (optional)
- RESTful API with Swagger documentation

---

## 🧑‍⚕️ User Roles

| Role    | Permissions                                                                 |
|---------|------------------------------------------------------------------------------|
| Patient | Register/login, view doctors, book appointments, cancel own appointments     |
| Doctor  | View personal appointments, confirm/cancel appointments                      |
| Admin   | Manage all users, doctors, appointments, setup global configurations         |

---

## 🗂️ Entity Models

### User
- `id`, `name`, `email`, `password`, `role` (`admin`, `doctor`, `patient`), `dob`, `gender`

### DoctorProfile
- `user_id`, `specialty`, `work_schedule` (e.g. Mon–Fri: 8AM–5PM)

### Appointment
- `doctor_id`, `patient_id`, `date`, `time`, `status` (`pending`, `confirmed`, `canceled`)

### MedicalNote *(Optional)*
- `appointment_id`, `note`, `created_by`, `created_at`

---

## 🔁 Appointment Flow

```plaintext
[1] Patient login
[2] Select doctor → select date/time → create appointment (pending)
[3] Doctor reviews appointments → confirm/cancel
[4] Patient receives status update
[5] System can send reminders via email (optional)
