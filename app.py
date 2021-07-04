from flask import Flask, render_template, request, session, redirect, url_for, g, flash
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField, StringField, TextAreaField
import model
import os

app = Flask(__name__)

username = ''
user = model.user.check_users()

class InfoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start = DateField('Start', format='%Y-%m-$d', validators=[DataRequired()])
    end = DateField('End', format='%Y-%m-$d', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods = ['GET', 'POST'])
def get_home():

    if 'username' in session:
        g.user = session['username']
        flash('You have signed up, successfully!!!')
        return redirect(url_for('get_userpage'))
    else:
        return render_template('home/index.html')

#Signup/Login routes
@app.route("/login", methods = ['GET', 'POST'])
def get_credentials():
    try:
       if request.method == 'POST':
           session.pop('username', None)
           is_user = request.form['username']
           password = model.user.check_password(is_user)
           if request.form['password'] == password:
               session['username'] = request.form['username']
               return redirect(url_for('get_home')) 
    except:
        return 'User does not exist'
    else:
        return render_template('home/index.html')
    
@app.route("/profile")
def get_userpage():
    return render_template('user/userpage.html')

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route("/signup", methods = ['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('user/signup.html')
    else:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        message = model.user.create_user(username, password, email)

        return render_template("user/signup.html", message = message)

@app.route('/getsession')
def get_session():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('get_home'))

#CRUD routes
@app.route("/create", methods = ['GET', 'POST'])
def create_todo():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     description = request.form['description']
    #     status = 0
    #     if 'username' in session:
    #         creator = session['username']

    #     message = model.task.create_task(title, description, status, creator)
    #     return render_template('tasks.html', message = message)
    # else:
    #     return render_template('tasks.html')
    
    form = InfoForm()        
    return render_template('tasks.html', form = form)


@app.route("/retrieve", methods = ['GET'])
def retrieve_todo():
    if request.method == 'GET':
        creator = session['username']
        tasks = model.task.retrieve_tasks(creator)
        return render_template("alltask.html", tasks = tasks)

@app.route("/edit/<int:id>", methods = ['GET'])
def edit_todo(id):
    if request.method == 'GET':
        task = model.task.edit_task(id)
        return render_template('task/edit.html', task = task)
    else:
        return 'No task found!'

@app.route("/update", methods = ['GET', 'POST'])
def update_todo():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = 0

        message = model.task.update_task(title, description, status)

        return render_template('task/update.html', message = message )
    else:
        return 'unable to update database'

@app.route("/delete/<int:id>", methods = ['GET', 'POST', 'DELETE'])
def delete_todo(id):

    deleted = model.task.delete_task(id)

    return deleted

#Admin
@app.route("/admin", methods = ['GET', 'POST'])
def get_admin_credentials():
    if request.method == 'GET':
        return render_template('admin/admin.html')
    else:
        if request.form['username'] == 'admin' and request.form['password'] == '1234Pa55w0rd':
            
            all_users = len(model.admin.get_all_users())
            all_tasks = model.admin.get_all_tasks()
            signups = model.admin.get_last_24hrs_users()
            result = model.admin.get_last_24hrs_tasks()     
            
            return render_template('admin/dashboard.html', all_users = all_users, all_tasks = all_tasks, signups = signups, result = result )

@app.route("/allusers", methods = ['GET'])
def get_all_users():
    
    all_users = model.admin.get_all_users()    
    return render_template('admin/allusers.html', all_users = all_users )

@app.route("/editusers/<int:id>", methods = ['GET', 'POST'])
def edit_user(id):
    if request.method == 'GET':
        user = model.admin.edit_user(id)
    
        return render_template('admin/edituser.html', user = user)
    else:
        return 'no user found'
    
@app.route("/updateuser", methods = ['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        id = request.form.get('id')
        username = request.form['username']
        email = request.form['email']

        message = model.admin.update_user(id, username, email)

        return render_template('admin/update.html', message = message )
    else:
        return 'unable to update database'
    
@app.route("/deleteuser/<username>", methods = [ 'GET', 'POST', 'DELETE' ])
def delete_user(username):
    
    deleted = model.admin.delete_user(username)

    return deleted

@app.route("/calendar")
def get_calendar():
    return render_template('calendar/calendar.html')

@app.route("/terms", methods = ['GET'])
def get_terms_of_use():
    return render_template('home/terms.html')

@app.route("/privacy", methods = ['GET'])
def get_privacy():
    return render_template('home/privacy.html')

@app.route("/about", methods = ['GET'])
def get_about():
    return render_template('home/about.html')

@app.route("/changes")
def get_changes():
    if request.method == 'GET':
        creator = session['username']
        tasks = model.task.retrieve_tasks(creator)
        return render_template("changes.html", tasks = tasks)

@app.route("/sidebar")
def get_sidebar():
    return render_template("sidebar.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8000, debug = True)

