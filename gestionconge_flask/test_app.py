import pytest
from app import app, db, Employee, LeaveRequest
from datetime import datetime

def test_delete_employee_as_admin(client, admin):
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

    # Se connecter en tant qu'administrateur
    with client.session_transaction() as sess:
        sess['username'] = 'admin'
        sess['role'] = 'admin'

    # Supprimer l'employé de test
    response = client.get(f'/delete_employee/{employee_to_delete.id}', follow_redirects=True)
    assert response.status_code == 200

    # Vérifier que l'employé a été supprimé de la base de données
    deleted_employee = Employee.query.get(employee_to_delete.id)
    assert deleted_employee is None

def test_delete_employee_as_user(client, user):
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
    assert response.status_code == 403  # Vérifie que l'accès est interdit pour un utilisateur normal

    # Vérifier que l'employé n'a pas été supprimé de la base de données
    not_deleted_employee = Employee.query.get(employee_to_delete.id)
    assert not_deleted_employee is not None
