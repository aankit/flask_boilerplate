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

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        return request.get_data()
    elif request.method == 'GET':
        return 'hi there'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('schedule'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/signin', methods=['GET', 'POST'])
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

@app.route('/signout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/schedule')
def schedule():
    if 'email' not in session:
        return redirect(url_for('signin'))
    user = User.query.filter_by(email = session['email']).first()
    if user is None:
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')

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