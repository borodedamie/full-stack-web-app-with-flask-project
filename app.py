from flask import Flask, render_template, request, session, redirect, url_for, g, flash
import model
import os

app = Flask(__name__)

username = ''
user = model.user.check_users()

@app.route("/", methods = ['GET', 'POST'])
def get_home():

    if 'username' in session:
        g.user = session['username']
        flash('You have signed up, successfully!!!')
        return redirect(url_for('retrieve_todo'))
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

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route("/signup", methods = ['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        message = 'Please sign up!'
        return render_template('user/signup.html', message = message)
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
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = 0
        if 'username' in session:
            creator = session['username']

        message = model.task.create_task(title, description, status, creator)
        return render_template('tasks.html', message = message)
    else:
        return render_template('tasks.html')


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
        id = request.form.get('id')
        title = request.form['title']
        description = request.form['description']
        status = 0

        message = model.task.update_task(id, title, description, status)

        return render_template('task/update.html', message = message )
    else:
        return 'unable to update database'

@app.route("/delete/<int:id>", methods = ['GET', 'POST'])
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
    
    # return str(all_users)
    
    return render_template('admin/allusers.html', all_users = all_users )

@app.route("/terms", methods = ['GET'])
def get_terms_of_use():
    return render_template('home/terms.html')

@app.route("/privacy", methods = ['GET'])
def get_privacy():
    return render_template('home/privacy.html')

@app.route("/about", methods = ['GET'])
def get_about():
    return render_template('home/about.html')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug = True)

