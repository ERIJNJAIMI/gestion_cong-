from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    cin = db.Column(db.String(50), unique=True, nullable=False)
    matricule = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    responsable = db.Column(db.String(50), nullable=False)
    utilisateur = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(50), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    date_naiss = db.Column(db.DateTime, nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False)
    nom_entite = db.Column(db.String(50), nullable=False)
    id_service = db.Column(db.String(50), nullable=False)
    id_type_emp = db.Column(db.String(50), nullable=False)
    jrs_total = db.Column(db.Integer, nullable=False)
    jrs_restant = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50))


class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('employee.username'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    date_demande = db.Column(db.String(50), default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))