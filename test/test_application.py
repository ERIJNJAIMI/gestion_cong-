import pytest
import sys
import os
from datetime import datetime
from app import app, db, Employee, LeaveRequest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_homepage(client):
    response = client.get('/homepage_user')
    assert response.status_code == 200
    assert b"Bienvenue" in response.data


def test_delete_employee_as_admin(client, admin):
    with app.app_context():
        employee_to_delete = Employee(
            cin="11223344",
            matricule="emp002",
            nom="John",
            prenom="Doe",
            responsable="No",
            utilisateur="johndoe",
            mot_de_passe="password",
            adresse="Doe Street",
            date_naiss=datetime(1990, 1, 1),
            date_debut=datetime(2020, 1, 1),
            nom_entite="HR",
            id_service="HR001",
            id_type_emp="Employee",
            jrs_total=20,
            jrs_restant=20,
            username="johndoe"
        )
        db.session.add(employee_to_delete)
        db.session.commit()

        # Se connecter en tant qu'administrateur
        with client.session_transaction() as sess:
            sess['username'] = 'admin'
            sess['role'] = 'admin'

        response = client.get(f'/delete_employee/{employee_to_delete.id}', follow_redirects=True)
        assert response.status_code == 200

        deleted_employee = Employee.query.get(employee_to_delete.id)
        assert deleted_employee is None

def test_delete_employee_as_user(client, user):
    with app.app_context():
        # Ajouter un employé de test à supprimer
        employee_to_delete = Employee(
            cin="11223344",
            matricule="emp002",
            nom="John",
            prenom="Doe",
            responsable="No",
            utilisateur="johndoe",
            mot_de_passe="password",
            adresse="Doe Street",
            date_naiss=datetime(1990, 1, 1),
            date_debut=datetime(2020, 1, 1),
            nom_entite="HR",
            id_service="HR001",
            id_type_emp="Employee",
            jrs_total=20,
            jrs_restant=20,
            username="johndoe"
        )
        db.session.add(employee_to_delete)
        db.session.commit()

        # Se connecter en tant qu'utilisateur normal
        with client.session_transaction() as sess:
            sess['username'] = 'user1'
            sess['role'] = 'user'

        # Essayer de supprimer l'employé de test
        response = client.get(f'/delete_employee/{employee_to_delete.id}', follow_redirects=True)
        assert response.status_code == 403  

        # Vérifier que l'employé n'a pas été supprimé de la base de données
        not_deleted_employee = Employee.query.get(employee_to_delete.id)
        assert not_deleted_employee is not None

def test_add_employee(client):
    with app.app_context():
        response = client.post('/add_employee', data={
            'cin': '98765432',
            'matricule': 'emp003',
            'nom': 'Jane',
            'prenom': 'Doe',
            'responsable': 'No',
            'utilisateur': 'janedoe',
            'mot_de_passe': 'password',
            'adresse': 'Doe Avenue',
            'date_naiss': '1992-02-02',
            'date_debut': '2022-01-01',
            'nom_entite': 'Finance',
            'id_service': 'FN002',
            'id_type_emp': 'Employee',
            'jrs_total': 25,
            'jrs_restant': 25,
            'username': 'janedoe'
        })
        assert response.status_code == 200
        employee = Employee.query.filter_by(username='janedoe').first()
        assert employee is not None

def test_edit_employee(client, admin):
    with app.app_context():
        employee = Employee.query.first()  
        response = client.post(f'/edit_employee/{employee.id}', data={
            'username': 'newusername',
            'role': 'Manager',
            'email': 'newemail@example.com'
        })
        assert response.status_code == 200
        updated_employee = Employee.query.get(employee.id)
        assert updated_employee.username == 'newusername'
        assert updated_employee.email == 'newemail@example.com'

def create_leave_request(username, leave_type, start_date, end_date, reason):
    with app.app_context():
        duration = calculate_leave_duration(start_date, end_date)
        new_request = LeaveRequest(
            username=username,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            duration=duration,
            reason=reason
        )
        db.session.add(new_request)
        db.session.commit()

def calculate_leave_duration(start_date: str, end_date: str) -> int:
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    duration = (end_date - start_date).days
    return duration
