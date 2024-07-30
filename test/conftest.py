import sys
import os
import pytest
from datetime import datetime
from app import  db, Employee
from models import Employee, LeaveRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



@pytest.fixture
def app():
    #app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.drop_all()

@pytest.fixture
def admin(init_database):
    with init_database.app.app_context():
        admin_user = Employee(
            cin="00000000",
            matricule="admin001",
            nom="Admin",
            prenom="User",
            responsable="Yes",
            utilisateur="admin",
            mot_de_passe="adminpassword",
            adresse="Admin Street",
            date_naiss=datetime(1980, 1, 1),
            date_debut=datetime(2010, 1, 1),
            nom_entite="IT",
            id_service="IT001",
            id_type_emp="Admin",
            jrs_total=30,
            jrs_restant=30,
            username="admin"
        )
        init_database.session.add(admin_user)
        init_database.session.commit()
        return admin_user

@pytest.fixture
def user(init_database):
    with init_database.app.app_context():
        user = Employee(
            cin="12345678",
            matricule="user001",
            nom="Test",
            prenom="User",
            responsable="No",
            utilisateur="user1",
            mot_de_passe="password1",
            adresse="Test Street",
            date_naiss=datetime(1990, 1, 1),
            date_debut=datetime(2020, 1, 1),
            nom_entite="HR",
            id_service="HR001",
            id_type_emp="Employee",
            jrs_total=20,
            jrs_restant=20,
            username="user1"
        )
        init_database.session.add(user)
        init_database.session.commit()
        return user
