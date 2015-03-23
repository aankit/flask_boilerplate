from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import json

app = Flask(__name__)

app.config.from_object('application.settings')

app.url_map.strict_slashes = False

import application.core
# import app.models
from application.schedulerConfig import jobstores, executors, job_defaults, timezone
scheduler = BackgroundScheduler(jobstores=jobstores, 
	executors=executors, 
	job_defaults=job_defaults, 
	timezone=timezone)
import application.schedules
import application.controllers



