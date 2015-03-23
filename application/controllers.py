from application import app
from application import scheduler
from application import schedules

@app.route('/')
def index():
	return 'Hello World!'

@app.route('/add/<int:TIME>/<JOB_ID>')
def add(TIME, JOB_ID):
	scheduler.add_job(schedules.scheduler_job, 
		'interval', 
		seconds=TIME, 
		id=JOB_ID,
		replace_existing=True)
	return 'job scheduled: %s' %(JOB_ID)

@app.route('/remove/<JOB_ID>')
def remove(JOB_ID):
	scheduler.remove_job(JOB_ID)
	return 'job removed: %s' %(JOB_ID)