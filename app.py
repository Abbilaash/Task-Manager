from flask import Flask, render_template, request, redirect, url_for,jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# Initialize Firebase with credentials
cred = credentials.Certificate("task-manager-7833f-firebase-adminsdk-age2s-27c1943206.json")  # Replace with your own service account key path
firebase_admin.initialize_app(cred)
db = firestore.client()

c = datetime.now()
current_time = c.strftime('%H:%M')

session = {}
session['gmail'] = "abbilaashat@gmail.com"

# Routes
@app.route('/')
def index():
    tasks_ref = db.collection('tasks')
    tasks = tasks_ref.stream()
    flags = []
    for i in tasks:
        #print(i.to_dict())
        if i.to_dict()['gmail'] == session['gmail'] and i.to_dict()['task_status'] == 0:
            flags.append({'id':i.id,'name':i.to_dict()['task_name'],'time':i.to_dict()['task_time']})
    return render_template('index.html', tasks=flags)

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_time = current_time
    new_task = {'gmail':session['gmail'],'task_name': task_name, 'task_time': task_time,'task_status':0}    
    tasks_ref = db.collection('tasks')
    tasks_ref.add(new_task)
    return redirect(url_for('index'))


@app.route('/edit_task/<task_id>', methods=['POST'])
def edit_task(task_id):
    new_name = request.form['new_name']
    new_time = current_time
    tasks_ref = db.collection('tasks')
    task_doc = tasks_ref.document(task_id)
    task_doc.update({'task_name': new_name, 'task_time': new_time})
    return redirect(url_for('index'))

@app.route('/complete_task/<task_id>', methods=['POST'])
def complete_task(task_id):
    data = request.get_json()
    completed = data.get('completed')
    tasks_ref = db.collection('tasks')
    task_doc = tasks_ref.document(task_id)
    task_doc.update({'task_status':1})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
