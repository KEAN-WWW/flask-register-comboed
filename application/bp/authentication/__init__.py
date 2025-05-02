from flask import Blueprint, render_template, redirect, url_for, flash, request
from application.database import User, db
from application.bp.authentication.forms import RegisterForm

authentication = Blueprint('authentication', __name__, template_folder='templates')


@authentication.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@authentication.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # 🔹 Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Already Registered', 'danger')
            return redirect(url_for('authentication.registration'))

        # Create a new User object
        new_user = User(email=email, password=password)

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('authentication.dashboard'))

    return render_template('registration.html', form=form)
