from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from functools import wraps
from sqlalchemy import func
from datetime import datetime
from flask_migrate import Migrate
import os
from models import db



app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['SESSION_TYPE'] = 'filesystem'


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///leave_requests.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session(app)
db.init_app(app)
migrate = Migrate(app, db)

from models import Employee, LeaveRequest

with app.app_context(): 
    db.create_all()

# Exemple de dictionnaire de données utilisateur 
users = {
    'user1': {
        'username': 'user1',
        'password': 'password1',
        'role': 'user'
    },
    'admin': {
        'username': 'admin',
        'password': 'adminpassword',
        'role': 'admin'
    }
}

# Route pour la page de login
@app.route('/')
def login():
    return render_template('login.html')

# Route pour gérer l'authentification
@app.route('/auth', methods=['POST'])
def auth():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['role'] = users[username]['role']
        if users[username]['role'] == 'admin':
            return redirect(url_for('homepage_admin'))
        else:
            return redirect(url_for('homepage_user'))
    else:
        return render_template('login.html', error=True)

# Décorateur pour vérifier si l'utilisateur est connecté
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Page d'accueil pour l'utilisateur
@app.route('/homepage_user')
@login_required
def homepage_user():
    username = session['username']
    user = Employee.query.filter_by(username=username).first()
    
    if user:
        JrsTotal = 20  
        used_leave_days = LeaveRequest.query.filter_by(username=username, status='Approved').with_entities(func.sum(LeaveRequest.duration)).scalar()
        JrsRestant = JrsTotal - used_leave_days if used_leave_days else JrsTotal

        user_info = {
            'cin': user.cin,
            'nom': user.nom,
            'prenom': user.prenom,
            'matricule': user.id,
            'date_debut': user.date_debut,
            'utilisateur': user.utilisateur,
            'JrsTotal': JrsTotal,
            'JrsRestant': JrsRestant
        }
    else:
        user_info = {}

    return render_template('Homepage_user.html', user_info=user_info)

@app.route('/homepage_admin')
@login_required
def homepage_admin():
    username = session['username']
    admin = Employee.query.filter_by(username=username).first()
    
    if admin:
        JrsTotal = 20
        used_leave_days = LeaveRequest.query.filter_by(username=username, status='Approved').with_entities(func.sum(LeaveRequest.duration)).scalar()
        JrsRestant = JrsTotal - used_leave_days if used_leave_days else JrsTotal

        admin_info = {
            'cin': admin.cin,
            'nom': admin.nom,
            'prenom': admin.prenom,
            'grade': admin.id,  
            'tel': admin.date_debut,      
            'email': admin.utilisateur,  
            'JrsTotal': JrsTotal,
            'JrsRestant': JrsRestant
        }
    else:
        admin_info = {}

    return render_template('homepageadmin.html', admin_info=admin_info)


# Route to display all leave requests for admin
@app.route('/toutes_les_demandes')
@login_required
def toutes_les_demandes():
    if session['role'] == 'admin':
        requests = LeaveRequest.query.all()
        return render_template('toutes_les_demandes.html', requests=requests)
    return redirect(url_for('homepage_user'))

# Route to approve a leave request
@app.route('/approve_request/<int:request_id>', methods=['POST'])
@login_required
def approve_request(request_id):
    if session['role'] == 'admin':
        leave_request = LeaveRequest.query.get(request_id)
        leave_request.status = 'Approved'
        db.session.commit()
    return redirect(url_for('toutes_les_demandes'))

# Route to reject a leave request
@app.route('/reject_request/<int:request_id>', methods=['POST'])
@login_required
def reject_request(request_id):
    if session['role'] == 'admin':
        leave_request = LeaveRequest.query.get(request_id)
        leave_request.status = 'Rejected'
        db.session.commit()
    return redirect(url_for('toutes_les_demandes'))

# Route to display approved leave requests
@app.route('/demandes_acceptees')
@login_required
def demandes_acceptees():
    if session['role'] == 'admin':
        approved_requests = LeaveRequest.query.filter_by(status='Approved').all()
        print(approved_requests)
        return render_template('demandes_acceptees.html', requests=approved_requests)
    return redirect(url_for('homepage_user'))

# Route to display rejected leave requests
@app.route('/demandes_refusees')
@login_required
def demandes_refusees():
    if session['role'] == 'admin':
        rejected_requests = LeaveRequest.query.filter_by(status='Rejected').all()
        return render_template('demandes_refusees.html', requests=rejected_requests)
    return redirect(url_for('homepage_user'))

@app.route('/ajouter_employe', methods=['GET', 'POST'])
@login_required
def ajouter_employe():
    if session['role'] != 'admin':
        return redirect(url_for('homepage_user'))
    if request.method == 'POST':
        print(request.form)
        cin = request.form['cin']
        matricule = request.form['id']
        nom = request.form['nom']
        prenom = request.form['prenom']
        responsable = request.form['responsable']
        username = request.form['username']
        mot_de_passe = request.form['password']
        adresse = request.form['adresse']
        date_naiss = datetime.strptime(request.form['date_naiss'], '%Y-%m-%d')
        date_debut = datetime.strptime(request.form['date_debut'], '%Y-%m-%d')
        nom_entite = request.form['nom_entite']
        id_service = request.form['id_service']
        id_type_emp = request.form['id_type_emp']
        jrs_total = request.form['jrs_total']
        jrs_restant = request.form['jrs_restant']

        # Vérifier si tous les champs requis sont remplis
        if not (cin and matricule and nom and prenom and responsable and username and mot_de_passe and adresse and date_naiss and date_debut and nom_entite and id_service and id_type_emp and jrs_total and jrs_restant):
            flash('Veuillez remplir tous les champs.', 'error')
            return redirect(url_for('ajouter_employe'))

        # Créer une instance Employee avec les données du formulaire
        new_employee = Employee(cin=cin, matricule=matricule, nom=nom, prenom=prenom, responsable=responsable, utilisateur=username,
                                mot_de_passe=mot_de_passe, adresse=adresse, date_naiss=date_naiss, date_debut=date_debut,
                                nom_entite=nom_entite, id_service=id_service, id_type_emp=id_type_emp,
                                jrs_total=jrs_total, jrs_restant=jrs_restant, username=username)

        try:
            # Ajouter et commit l'employé à la base de données
            db.session.add(new_employee)
            db.session.commit()
            flash('Employé ajouté avec succès!', 'success')
            return redirect(url_for('list_employees'))

        except Exception as e:
            flash(f'Erreur lors de l\'ajout de l\'employé: {str(e)}', 'error')
            db.session.rollback()  # Annuler les changements en cas d'erreur
            return redirect(url_for('ajouter_employe'))

    return render_template('ajouteremploye.html')

@app.route('/list_employees' )
@login_required
def list_employees():
    employees = Employee.query.all()
    return render_template('list_employees.html', employees=employees)

@app.route('/edit_employee/<int:emp_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(emp_id):
    employee = Employee.query.get(emp_id)
    if request.method == 'POST':
        
        employee.cin = request.form['cin']
        employee.matricule = request.form['matricule']
        employee.nom = request.form['nom']
        employee.prenom = request.form['prenom']
        employee.responsable = request.form['responsable']
        employee.utilisateur = request.form['utilisateur']
        employee.mot_de_passe = request.form['mot_de_passe']
        employee.adresse = request.form['adresse']
        employee.date_naiss = request.form['date_naiss']
        employee.date_debut = request.form['date_debut']
        employee.nom_entite = request.form['nom_entite']
        employee.id_service = request.form['id_service']
        employee.id_type_emp = request.form['id_type_emp']
        employee.jrs_total = request.form['jrs_total']
        employee.jrs_restant = request.form['jrs_restant']
        
       
        db.session.commit()
        flash('Informations de l\'employé mises à jour avec succès.', 'success')
        return redirect(url_for('list_employees'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/delete_employee/<int:emp_id>')
@login_required
def delete_employee(emp_id):
    if session.get('role') != 'admin':
        flash('Vous n\'avez pas la permission de supprimer des employés.', 'error')
        return redirect(url_for('homepage_user'))

    employee = Employee.query.get(emp_id)
    if not employee:
        flash('Employé introuvable.', 'error')
        return redirect(url_for('list_employees'))

    db.session.delete(employee)
    db.session.commit()
    flash('Employé supprimé avec succès!', 'success')
    return redirect(url_for('list_employees'))


# Fonction pour calculer la durée en jours
def calculate_duration(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    duration = (end - start).days + 1  
    return duration

@app.route('/demandeconge', methods=['GET', 'POST'])
@login_required
def demandeconge():
    if request.method == 'POST':
        print(request.form)
        username = session['username']
        leave_type = request.form['type-conge']
        start_date = request.form['date-depart']
        end_date = request.form['date-retour']
        reason = request.form['file-upload']
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        duration = (end_date_obj - start_date_obj).days
        
        try:
            new_request = LeaveRequest(username=username, leave_type=leave_type, start_date=start_date, end_date=end_date, duration=duration, reason=reason)
            db.session.add(new_request)
            db.session.commit()
            flash('Demande de congé soumise avec succès.', 'success')
            return redirect(url_for('homepage_user'))

        except Exception as e:
            flash(f'Erreur lors de la soumission de la demande de congé: {str(e)}', 'error')
            db.session.rollback()
            return redirect(url_for('demandeconge'))
        
    return render_template('demandeconge.html')


@app.route('/mesdemandes')
@login_required
def mesdemandes():
    username = session['username']
    requests = LeaveRequest.query.filter_by(username=username).all()
    return render_template('lesdemandes.html', requests=requests)

@app.route('/cancel_request/<int:request_id>', methods=['POST'])
@login_required
def cancel_request(request_id):
    username = session['username'] 
    leave_request = LeaveRequest.query.get(request_id)
    if leave_request.username == username and leave_request.status == 'Pending':
        db.session.delete(leave_request)
        db.session.commit()
        flash('Demande de congé annulée avec succès.', 'success')
    return redirect(url_for('mesdemandes'))

# Route pour déconnecter l'utilisateur
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
