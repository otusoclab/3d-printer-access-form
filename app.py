from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(9), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

class PrinterLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(9), db.ForeignKey('user.student_id'), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    access_date = db.Column(db.String(10), nullable=False)
    access_time = db.Column(db.String(5), nullable=False)
    printers_used = db.Column(db.String(200), nullable=False)
    print_description = db.Column(db.String(200))
    filament = db.Column(db.String(20), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lookup', methods=['POST'])
def lookup():
    student_id = request.form['student_id']
    if len(student_id) != 9 or not student_id.isdigit():
        return "Invalid Student ID format. Must be 9 digits.", 400

    user = User.query.filter_by(student_id=student_id).first()
    if user:
        return redirect(url_for('printer_form', student_id=student_id))
    else:
        return redirect(url_for('register', student_id=student_id))

@app.route('/form', methods=['GET', 'POST'])
def printer_form():
    student_id = request.args.get('student_id')

    user = User.query.filter_by(student_id=student_id).first()
    if not user:
        return redirect(url_for('register', student_id=student_id))

    if request.method == 'POST':
        reason = request.form['reason']
        access_date = request.form['access_date']
        access_time = request.form['access_time']
        printers = request.form.getlist('printers')
        printers_used = ', '.join(printers)
        print_description = request.form.get('print_description', '')
        filament = request.form['filament']

        new_log = PrinterLog(
            student_id=student_id,
            reason=reason,
            access_date=access_date,
            access_time=access_time,
            printers_used=printers_used,
            print_description=print_description,
            filament=filament
        )
        db.session.add(new_log)
        db.session.commit()

        return redirect(url_for('success'))

    return render_template('form.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        if len(student_id) != 9 or not student_id.isdigit():
            return "Invalid Student ID format.", 400

        existing_user = User.query.filter_by(student_id=student_id).first()
        if existing_user:
            return redirect(url_for('printer_form', student_id=student_id))

        new_user = User(
            student_id=student_id,
            name=name,
            email=email,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('printer_form', student_id=student_id))

    student_id = request.args.get('student_id')
    return render_template('register.html', student_id=student_id)

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    if not os.path.exists('instance'):
        os.makedirs('instance')
    if not os.path.exists('instance/students.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
