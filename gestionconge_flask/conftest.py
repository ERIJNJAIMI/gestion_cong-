import pytest
from app import app, db, Employee, LeaveRequest
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Ajouter un utilisateur admin pour les tests
            admin = Employee(
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
            db.session.add(admin)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def admin():
    return Employee.query.filter_by(utilisateur='admin').first()

@pytest.fixture
def user():
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
    db.session.add(user)
    db.session.commit()
    return user
