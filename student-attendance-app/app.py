from flask import Flask, render_template, request, redirect, url_for
from models import db, Student, Attendance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

# Create tables before the first request
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form['name']
    class_name = request.form['class']
    email = request.form['email']
    new_student = Student(name=name, class_name=class_name, email=email)
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/mark-attendance/<int:student_id>', methods=['POST'])
def mark_attendance(student_id):
    status = request.form['status']
    date = request.form['date']
    attendance = Attendance(student_id=student_id, date=date, status=status)
    db.session.add(attendance)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
