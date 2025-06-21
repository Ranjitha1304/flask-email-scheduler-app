# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from email_config import send_email
from models import db, ScheduledEmail

scheduler = BackgroundScheduler()
scheduler.start()

def send_scheduled_email(app, email_id):
    with app.app_context():
        email = ScheduledEmail.query.get(email_id)
        if email and not email.sent and email.scheduled_time <= datetime.now():
            send_email(email.to_email, email.subject, email.message)
            email.sent = True
            db.session.commit()

def schedule_email_job(app, email):
    scheduler.add_job(
        func=send_scheduled_email,
        trigger='date',
        run_date=email.scheduled_time,
        args=[app, email.id],
        id=f"email_{email.id}",
        replace_existing=True
    )
