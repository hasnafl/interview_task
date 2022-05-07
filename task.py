from flask import Flask, request, jsonify, json, flash
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import time, datetime
from sqlalchemy import func
from flask_mail import Mail, Message
import redis
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from celery import Celery
import celeryconfig
import pytz


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

@celery.task
def sending_email_with_celery():
	print("Executing task : Sending email...")
	# sending email
	re = []
	recipients = session.query(email_recipients).all()
	#check the time
	time_now = datetime.datetime.now(AS).replace(second=0, microsecond=0)
	time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
	time_now = datetime.datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S")

	email = session.query(emails).filter(emails.timestamp==time_now).all()
	for r in recipients:
		re.append(r.email_address)
	if email:
		for data in email:
			msg = Message(data.email_subject, sender = 'clatte555@gmail.com', recipients = re)
			msg.body = data.email_content
			mail.send(msg)
			print(f"Email with timestamp {data.timestamp} is sent")
	else:
		print(f"No Email was Sent")
	print("Task complete!")
	return "Success"

if __name__ == "__main__":
	app.run(debug=True)