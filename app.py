from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    done_by = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    """
        This function renders the main Dashboard page and handles Add task feature.
    """
    if request.method == 'POST':
        task_content = request.form['Content']
        done_time = request.form['Time']
        if task_content == '':
            return render_template('error.html')
        if done_time == '':
            return render_template('error.html')
        new_task = Todo(content=task_content, done_by = done_time)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.done_by).all()
        return render_template('index.html', tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    """
    This function handles the delete feature.
    """
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the selected task'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    """
    This function handles the update feature.
    """
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        updated_task_content = request.form['Content']
        updated_time = request.form['Time']
        if updated_task_content == '':
            return render_template('error.html')
        if updated_time == '':
            return render_template('error.html')
        task.content = updated_task_content
        task.done_by = updated_time
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    else:
        tasks = Todo.query.order_by(Todo.done_by).all()
        return render_template('update.html', task = task, tasks = tasks)



if __name__ == "__main__":
    app.run(debug = True)
