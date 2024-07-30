import os
import sys
import pytest
from app import app, db, Employee, LeaveRequest



sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    with app.app_context():
        db.drop_all()
