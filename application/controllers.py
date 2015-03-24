from flask import request, Response, session, escape, redirect, flash
from flask import render_template, send_from_directory, url_for
from application import app
from application import scheduler
from application import schedules
from application.forms import SignupForm

# routing for API endpoints (generated from the models designated as API_MODELS)
from application.core import api_manager
from application.models import *

for model_name in app.config['API_MODELS']:
    model_class = app.config['API_MODELS'][model_name]
    api_manager.create_api(model_class, methods=['GET', 'POST'])

api_session = api_manager.session

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        return 'You are not logged in'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"
    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


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