HI MYSELF NIRANJAN NAGAR

# Examination Management Portal (EMP)

This is my project — an online portal I built to handle the entire exam lifecycle for a IITM. It covers everything from creating courses and scheduling exams all the way to publishing results. I built it using Flask, Jinja2, Bootstrap 5, and SQLite (no extra DB setup needed — the schema gets created automatically when you first run it).

I tried to keep things simple: no React, no heavy frontend frameworks, just server-side rendering with a clean Bootstrap UI.

---

## How to Run It Locally

```bash
pip install -r requirements.txt
python app.py
# Open http://127.0.0.1:5000 in your browser
```

The database (`instance/emp.db`) gets created on first run — you don't need to do anything manually.

**To load some demo data (optional):**
```bash
python seed.py
```

**To run a quick sanity check on the business rules:**
```bash
python smoke_test.py
```

---

## Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@emp.com | admin123 |
| Student (demo) | rao@emp.com | password123 |
| Student (demo) | asha@emp.com | password123 |
| Examiner (pending, unapproved) | pending@emp.com | password123 |

> Admin is baked into the DB on first run — you can't register as admin from the UI.

---

## Exam Lifecycle (Phases)

Each exam goes through these phases, controlled by the admin:

```
Draft → Slot Creation → Booking Open → Closed → Completed
```

- **Draft**: Just created, nothing is open yet
- **Slot Creation**: Examiners can now add time slots (only during the slot-creation date window)
- **Booking Open**: Students can pick and book a slot (only during the booking date window)
- **Closed**: Booking is shut, evaluation starts
- **Completed**: All done; admin can publish results

---

## Project Files

```
app.py          → Main Flask app factory
db.py           → SQLite schema + helper functions
helpers.py      → Business rules, decorators, shared SQL
auth.py         → Login / register / logout
admin.py        → All admin routes (courses, exams, users, slots, etc.)
examiner.py     → Examiner routes (slots, evaluation)
student.py      → Student routes (exams, booking, results)
api.py          → JSON API endpoints (login required, role-scoped)
seed.py         → Demo data
smoke_test.py   → Automated rule checks
templates/      → Jinja2 HTML templates
static/         → CSS
```

---

## JSON API

You need to be logged in to use these. Each endpoint respects your role:

```
GET /api/exams
GET /api/slots
GET /api/bookings
GET /api/examiners   (admin only)
GET /api/students    (admin only)
```

---

## Notes

- Examiner accounts need admin approval before they can log in
- Students can only book one slot per exam
- Once booking starts, slots can't be deleted (only admin can reassign)
- Results are hidden from students until admin explicitly publishes them
