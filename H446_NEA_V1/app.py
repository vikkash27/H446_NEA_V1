from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'vikkash123'

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('projects', lazy=False))

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    priority = db.Column(db.String(20), nullable=False)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    

    


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect(url_for('home'))
    
    user = User.query.get(user_id)

    
    return render_template('dashboard.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    with app.app_context():
        user = User.query.filter_by(username=username, password=password).first()
        if user is not None:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('home'))
        
@app.route('/projects', methods=['GET', 'POST'])
def projects():
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect(url_for('home'))

    user = User.query.get(user_id)
    projects = Project.query.all()

    if request.method == 'POST':
        # Process the form data and add a new project to the database
        name = request.form['name']
        description = request.form['description']
        due_date_str = request.form['due_date']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        priority = request.form['priority']
        status = request.form['status']

        new_project = Project(name=name, description=description, due_date=due_date, priority=priority, status=status, user=user)
        db.session.add(new_project)
        db.session.commit()

        flash('New project created successfully!', 'success')
        return redirect(url_for('projects'))

    # If the request method is not POST, render the projects template as usual
    return render_template('projects.html', user=user, projects=projects)




@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/collaboration')
def collaboration():
    return render_template('collaboration.html')


@app.route('/tasks')
def tasks():
    user_id = session.get('user_id', None)
    if not user_id:
        return redirect(url_for('home'))

    user = User.query.get(user_id)
    return render_template('tasks.html' ,user=user)
    

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



