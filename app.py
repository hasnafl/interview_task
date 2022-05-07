from flask import Flask, request, jsonify, json, flash, render_template, url_for, redirect
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import time, datetime
from sqlalchemy.sql import func
from flask_mail import Mail, Message
import redis
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from task import sending_email_with_celery
from celery import Celery
import pytz
import celeryconfig
from datetime import timedelta

app = Flask(__name__)
api = Api(app)

db = SQLAlchemy(app)
engine = db.create_engine("mariadb+mariadbconnector://root:hasna06798@127.0.0.1:3306/emails_db", {})
Base = declarative_base()
app.secret_key = "super secret key"
AS = pytz.timezone('Asia/Singapore')

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'clatte555@gmail.com'
app.config['MAIL_PASSWORD'] = 'clatte12345'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# celery config
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_IMPORTS=["task.sending_email_with_celery"]

# initialize celery app
def get_celery_app_instance(app):
	celery = Celery(
		app.import_name,
		backend=CELERY_BROKER_URL,
		broker=CELERY_BROKER_URL
	)
	celery.conf.update(app.config)
	celery.config_from_object(celeryconfig)

	class ContextTask(celery.Task):
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return self.run(*args, **kwargs)

	celery.Task = ContextTask
	return celery

celery = get_celery_app_instance(app)

@app.route("/long_running_task_celery")
def long_running_task_celery():
    sending_email_with_celery.delay()
    return f"running task triggered with Celery! Check terminal to see the logs..."

class email_recipients(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	email_address = db.Column(db.String(100))

class emails(db.Model):
	__tablename__ = 'emails'
	event_id = db.Column(db.Integer, primary_key = True)
	email_subject = db.Column(db.String(100))
	email_content = db.Column(db.String(200)) 
	timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now())

Base.metadata.create_all(engine)

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

@app.route("/")
def index():
	return render_template('home.html')

@app.route("/email_save", methods=['POST'])
def email_save():
	if request.method == 'POST':
		max_id = session.query(func.max(emails.event_id)).first()
		if max_id and max_id[0]:
			max_id = max_id[0]+1
		else:
			max_id = 1
		event_id = max_id
		email_subject = request.form['email_subject']
		email_content = request.form['email_content']
		timestamp = datetime.datetime.now(AS) + timedelta(minutes=2)
		timestamp = timestamp.strftime("%Y-%m-%d %H:%M")
		try:
			email = emails(event_id=event_id, email_subject=email_subject,
				email_content=email_content, timestamp=timestamp)
			session.add(email)
			session.commit()
		except Exception as e:
			return f"Failed to add data. {e}"
	flash("Record was successfully added")
	return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)