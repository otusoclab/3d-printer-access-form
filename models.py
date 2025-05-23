from app import db

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
    other_text = db.Column(db.String(200))
    filament = db.Column(db.String(20), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
