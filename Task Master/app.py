from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading

app = Flask(__name__)  #creates the Flask instance [__name__ is the name of the current Python module]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #Database used for the default engine
DataBase = SQLAlchemy(app) #SQL

class User(DataBase.Model):
    id = DataBase.Column(DataBase.Integer, primary_key=True) #Generate an id for each entry
    content = DataBase.Column(DataBase.String(200), nullable=False)  #Content
    date_created = DataBase.Column(DataBase.DateTime, default=datetime.utcnow) #Date of each content

    def __repr__(self): #Return a string containing a printable representation of an object
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET']) # ('/') is associated with the root URL
def index():  # put application's code here
    DataBase.create_all() #used to create a new table into the database
    if request.method == 'POST': #POST requests are used to send data to the server for processing
        task_content = request.form['content'] #Capture requests as they come in
        new_task = User(content=task_content) #Create the new task

        try:
            DataBase.session.add(new_task) # Adding New or Existing Items
            DataBase.session.commit() #The changes made to the objects in the Session will be persisted into the Database
            return redirect('/') #redirect to root URL
        except:
            return 'There was an issue adding your task'

    else:
        tasks = User.query.order_by(User.date_created).all() #Order the data
        return render_template('index.html', tasks=tasks) #Generate the template

@app.route('/delete/<int:id>') #If Delete is pressed
def delete(id):
    task_to_delete = User.query.get_or_404(id) #Shortcut to query a particular object from the database

    try:
        DataBase.session.delete(task_to_delete) #Delete Task
        DataBase.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET','POST']) #If Update is pressed
def update(id):
    task = User.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            DataBase.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating that task'

    else:
        return render_template('update.html', task = task)

@app.route('/click/', methods=['GET', 'POST'])
def click():

    if request.method == 'POST':
        return render_template('click.html')
    else:
        start_timer()
        return render_template('click.html')


if __name__ == '__main__':
    app.run(debug=True)
