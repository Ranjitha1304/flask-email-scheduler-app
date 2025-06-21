# app.py
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
import re

from models import db, ScheduledEmail
from scheduler import schedule_email_job

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///email.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            to_email = request.form['to_email']
            subject = request.form['subject']
            message = request.form['message']
            scheduled_time = request.form['scheduled_time']

            if not re.match(r"[^@]+@[^@]+\.[^@]+", to_email):
                flash('Invalid email address!', 'danger')
                return redirect(url_for('index'))

            try:
                scheduled_dt = datetime.strptime(scheduled_time, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid datetime.', 'danger')
                return redirect(url_for('index'))

            email = ScheduledEmail(
                to_email=to_email,
                subject=subject,
                message=message,
                scheduled_time=scheduled_dt
            )
            db.session.add(email)
            db.session.commit()
            schedule_email_job(app, email)  # ⬅️ pass app explicitly

            flash('Email scheduled successfully!', 'success')
            return redirect(url_for('index'))

        emails = ScheduledEmail.query.order_by(ScheduledEmail.scheduled_time.desc()).all()
        return render_template('index.html', emails=emails)

    return app
