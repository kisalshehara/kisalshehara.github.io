from flask import Flask, render_template, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
attendance_password = 'code@123'

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    attendance = db.relationship('Attendance', backref='student', lazy=True, cascade='all,delete-orphan')

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/')
def index():
    students = Student.query.all()
    messages = get_flashed_messages()
    context = {}
    if messages:
        context['messages'] = messages

    return render_template('index.html', students=students, context=context)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        try:
            student = Student(name=name)
            db.session.add(student)
            db.session.commit()
            flash('Student added successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Error: Student with the same name already exists', 'danger')

    return redirect('/')


@app.route('/remove_student/<int:id>', methods=['GET', 'POST'])
def remove_student(id):
    if request.method == 'POST':
        student = Student.query.get(id)
        if student:
            Attendance.query.filter_by(student_id=id).delete()
            db.session.delete(student)
            db.session.commit()
            flash('Student and their attendance records removed successfully', 'success')
        else:
            flash('Error: Student not found', 'danger')
            return render_template('confirmation_page.html', student_id=id)  # Render the template here

    return redirect('/')

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if request.method == 'POST':
        student_name = request.form['student_name']
        date_str = request.form['date']
        password = request.form['password']

        if password == attendance_password:
            student = Student.query.filter_by(name=student_name).first()
            if student:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                attendance = Attendance(student_id=student.id, date=date)
                db.session.add(attendance)
                db.session.commit()
                flash(f'Attendance marked for {student_name} successfully', 'success')
            else:
                flash('Error: Student not found', 'danger')
        else:
            flash('Error: Invalid Key', 'danger')

    return redirect('/')

@app.route('/change_password', methods=['POST'])
def change_password():
    if request.method == 'POST':
        admin_password = request.form['admin_password']
        new_password = request.form['new_password']

        if admin_password == 'kisal@2003':  # Replace with your admin password
            global attendance_password  
            attendance_password = new_password
            flash('Attendance Key changed successfully', 'success')
        else:
            flash('Error: Incorrect admin password', 'danger')

    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
