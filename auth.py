import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from db import q, run

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = q("SELECT * FROM users WHERE email=?", (email,), one=True)

        # Check credentials
        if not user or not check_password_hash(user["password"], request.form.get("password", "")):
            flash("Hmm, that email or password doesn't look right. Please try again.", "danger")
        elif user["status"] == "inactive":
            flash("Your account has been deactivated. Please get in touch with the Admin.", "danger")
        else:
            session.clear()
            session["uid"] = user["id"]
            return redirect(url_for(user["role"] + ".dashboard"))
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        f = request.form
        role = f.get("role")
        name = f.get("name", "").strip()
        email = f.get("email", "").strip().lower()
        pw = f.get("password", "")

        if role not in ("student", "examiner"):
            flash("Please select a valid role to register.", "danger")
        elif not name or "@" not in email:
            flash("Please enter a valid name and email address.", "danger")
        elif len(pw) < 6:
            flash("Your password should be at least 6 characters long.", "danger")
        else:
            # Examiners need admin approval before they can log in
            status = "pending" if role == "examiner" else "active"
            try:
                run(
                    "INSERT INTO users(name,email,password,role,status,phone,department,roll_no) VALUES(?,?,?,?,?,?,?,?)",
                    (
                        name,
                        email,
                        generate_password_hash(pw, method="pbkdf2:sha256"),
                        role,
                        status,
                        f.get("phone", "").strip(),
                        f.get("department", "").strip(),
                        f.get("roll_no", "").strip(),
                    ),
                )
                if role == "examiner":
                    flash("Registration successful! Just hang tight — the Admin needs to approve your account before you can log in.", "success")
                else:
                    flash("You're all set! Go ahead and log in.", "success")
                return redirect(url_for("auth.login"))
            except sqlite3.IntegrityError:
                flash("Looks like that email is already registered. Try logging in instead.", "danger")
    return render_template("register.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
