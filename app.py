import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Periode, Enseignant, Filiere, Matiere, Etudiant, Enseignement, Presence, Justification, Correspondre
from datetime import datetime, time
 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre_cle_ici')
 
# ---------- CONFIGURATION BASE DE DONNÉES (SQLite) ----------
database_url = os.environ.get('DATABASE_URL')
if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///esatic.db'  # SQLite en local
 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'check_same_thread': False}  # Nécessaire pour SQLite
}
 
db.init_app(app)
 
with app.app_context():
    db.create_all()
 
# ---------- ROUTES (inchangées sauf indication) ----------
@app.route('/verif')
def verif():
    periodes = Periode.query.count()
    enseignants = Enseignant.query.count()
    filieres = Filiere.query.count()
    matieres = Matiere.query.count()
    etudiants = Etudiant.query.count()
    enseignements = Enseignement.query.count()
    presences = Presence.query.count()
    justifications = Justification.query.count()
    return f"""
    <h3>État de la base esatic</h3>
    <ul>
    <li>Périodes : {periodes}</li>
    <li>Enseignants : {enseignants}</li>
    <li>Filières : {filieres}</li>
    <li>Matières : {matieres}</li>
    <li>Étudiants : {etudiants}</li>
    <li>Enseignements : {enseignements}</li>
    <li>Présences : {presences}</li>
    <li>Justifications : {justifications}</li>
    </ul>
    """
 
# ---------- MODULE 1 : PARAMÉTRAGE ----------
@app.route('/')
@app.route('/parametrage')
def parametrage():
    periodes = Periode.query.all()
    enseignants = Enseignant.query.all()
    filieres = Filiere.query.all()
    matieres = Matiere.query.all()
    return render_template('parametrage.html',
                           periodes=periodes,
                           enseignants=enseignants,
                           filieres=filieres,
                           matieres=matieres)
 
# --- Périodes ---
@app.route('/ajouter_periode', methods=['POST'])
def ajouter_periode():
    date_periode = datetime.strptime(request.form['date_periode'], '%Y-%m-%d').date()
    periode = Periode(date_periode=date_periode)
    db.session.add(periode)
    db.session.commit()
    flash('Période ajoutée', 'success')
    return redirect(url_for('parametrage'))
 
@app.route('/supprimer_periode/<int:id>')
def supprimer_periode(id):
    periode = Periode.query.get_or_404(id)
    db.session.delete(periode)
    db.session.commit()
    flash('Période supprimée', 'info')
    return redirect(url_for('parametrage'))
 
# --- Enseignants ---
@app.route('/ajouter_enseignant', methods=['POST'])
def ajouter_enseignant():
    nom = request.form['nom']
    prenom = request.form['prenom']
    mail = request.form['mail']
    sexe = request.form['sexe']
    specialite = request.form.get('specialite', '')
    diplome = request.form.get('diplome', '')
    enseignant = Enseignant(nom=nom, prenom=prenom, mail=mail,
                            sexe=sexe, specialite=specialite, diplome=diplome)
    db.session.add(enseignant)
    db.session.commit()
    flash('Enseignant ajouté', 'success')
    return redirect(url_for('parametrage'))
 
@app.route('/supprimer_enseignant/<int:id>')
def supprimer_enseignant(id):
    enseignant = Enseignant.query.get_or_404(id)
    db.session.delete(enseignant)
    db.session.commit()
    flash('Enseignant supprimé', 'info')
    return redirect(url_for('parametrage'))
 
# --- Filières ---
@app.route('/ajouter_filiere', methods=['POST'])
def ajouter_filiere():
    libelle = request.form['libelle']
    filiere = Filiere(libelle_filiere=libelle)
    db.session.add(filiere)
    db.session.commit()
    flash('Filière ajoutée', 'success')
    return redirect(url_for('parametrage'))
 
@app.route('/supprimer_filiere/<int:id>')
def supprimer_filiere(id):
    filiere = Filiere.query.get_or_404(id)
    db.session.delete(filiere)
    db.session.commit()
    flash('Filière supprimée', 'info')
    return redirect(url_for('parametrage'))
 
# --- Matières ---
@app.route('/ajouter_matiere', methods=['POST'])
def ajouter_matiere():
    nom = request.form['nom']
    matiere = Matiere(nom_matiere=nom)
    db.session.add(matiere)
    db.session.commit()
    flash('Matière ajoutée', 'success')
    return redirect(url_for('parametrage'))
 
@app.route('/supprimer_matiere/<int:id>')
def supprimer_matiere(id):
    matiere = Matiere.query.get_or_404(id)
    db.session.delete(matiere)
    db.session.commit()
    flash('Matière supprimée', 'info')
    return redirect(url_for('parametrage'))
 
# ---------- MODULE 2 : SAISIE ----------
@app.route('/saisie')
def saisie():
    etudiants = Etudiant.query.all()
    matieres = Matiere.query.all()
    filieres = Filiere.query.all()
    enseignants = Enseignant.query.all()
    periodes = Periode.query.all()
    absences_non_justifiees = db.session.query(Presence).filter(Presence.statut == 'ABSENT')\
        .outerjoin(Justification, (Presence.id_etudiant == Justification.id_etudiant) & (Presence.id_enseignement == Justification.id_enseignement))\
        .filter(Justification.id_justification == None).all()
    return render_template('saisie.html',
                           etudiants=etudiants,
                           matieres=matieres,
                           filieres=filieres,
                           enseignants=enseignants,
                           periodes=periodes,
                           absences_non_justifiees=absences_non_justifiees)
 
@app.route('/inscrire_etudiant', methods=['POST'])
def inscrire_etudiant():
    nom = request.form['nom']
    prenom = request.form['prenom']
    code_filiere = request.form['code_filiere']
    sexe = request.form.get('sexe', 'M')
 
    etudiant = Etudiant(nom=nom, prenom=prenom, code_filiere=code_filiere, sexe=sexe)
    db.session.add(etudiant)
    db.session.commit()
    flash('Étudiant inscrit avec succès', 'success')
    return redirect(url_for('saisie'))
 
@app.route('/enregistrer_presence', methods=['POST'])
def enregistrer_presence():
    etudiant_id = request.form['etudiant_id']
    matiere_id = request.form['matiere_id']
    date_ens = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    heure_debut = datetime.strptime(request.form['heure_debut'], '%H:%M').time()
    heure_fin = datetime.strptime(request.form['heure_fin'], '%H:%M').time()
    id_enseignant = request.form['id_enseignant']
    code_filiere = request.form['code_filiere']
    id_periode = request.form['id_periode']
    statut = request.form['statut']
    commentaire = request.form.get('commentaire', '')
    envoyer_message = 'envoyer_message' in request.form
 
    enseignement = Enseignement.query.filter_by(
        date_enseignement=date_ens,
        id_enseignant=id_enseignant,
        code_filiere=code_filiere,
        id_periode=id_periode,
        code_matiere=matiere_id
    ).first()
    if not enseignement:
        enseignement = Enseignement(
            date_enseignement=date_ens,
            heure_debut=heure_debut,
            heure_fin=heure_fin,
            id_enseignant=id_enseignant,
            code_filiere=code_filiere,
            id_periode=id_periode,
            code_matiere=matiere_id
        )
        db.session.add(enseignement)
        db.session.commit()
 
    presence = Presence.query.get((etudiant_id, enseignement.id_enseignement))
    if presence:
        presence.statut = statut
        presence.commentaire = commentaire
    else:
        presence = Presence(
            id_etudiant=etudiant_id,
            id_enseignement=enseignement.id_enseignement,
            statut=statut,
            commentaire=commentaire
        )
        db.session.add(presence)
    db.session.commit()
 
    if statut != 'PRESENT' and envoyer_message:
        flash(f'📨 Message envoyé à l\'étudiant concernant son statut ({statut}) du {date_ens}', 'info')
    flash('Présence enregistrée', 'success')
    return redirect(url_for('saisie'))
 
@app.route('/justifier_absence/<int:id_etudiant>/<int:id_enseignement>', methods=['POST'])
def justifier_absence(id_etudiant, id_enseignement):
    motif = request.form['motif']
    fichier = request.form.get('fichier', '')
    justification = Justification(
        id_etudiant=id_etudiant,
        id_enseignement=id_enseignement,
        motif=motif,
        fichier=fichier
    )
    db.session.add(justification)
    presence = Presence.query.get((id_etudiant, id_enseignement))
    if presence:
        presence.statut = 'JUSTIFIE'
        db.session.commit()
    else:
        db.session.commit()
    flash('Absence justifiée', 'success')
    return redirect(url_for('saisie'))
 
# ---------- MODULE 3 : ÉDITION ----------
@app.route('/edition')
def edition():
    filieres = Filiere.query.all()
    periodes = Periode.query.all()
    etudiants = Etudiant.query.all()
    absences_justifiees = db.session.query(Presence).filter(Presence.statut == 'JUSTIFIE').all()
    return render_template('edition.html',
                           filieres=filieres,
                           periodes=periodes,
                           etudiants=etudiants,
                           absences_justifiees=absences_justifiees)
 
@app.route('/matieres_par_filiere')
def matieres_par_filiere():
    results = db.session.query(Filiere, Matiere, Correspondre.volume_horaire)\
        .join(Correspondre, Filiere.code_filiere == Correspondre.code_filiere)\
        .join(Matiere, Matiere.code_matiere == Correspondre.code_matiere).all()
    return render_template('matieres_par_filiere.html', results=results)
 
@app.route('/absence_par_periode/<int:id_periode>')
def absence_par_periode(id_periode):
    periode = Periode.query.get_or_404(id_periode)
    results = db.session.query(
        Filiere.libelle_filiere,
        db.func.count(Presence.id_etudiant)
    ).join(Etudiant, Etudiant.code_filiere == Filiere.code_filiere
    ).join(Presence, Presence.id_etudiant == Etudiant.id_etudiant
    ).join(Enseignement, Enseignement.id_enseignement == Presence.id_enseignement
    ).filter(
        Enseignement.id_periode == id_periode,
        Presence.statut != 'PRESENT'
    ).group_by(Filiere.code_filiere).all()
    result_dict = {row[0]: row[1] for row in results}
    return render_template('rapport_periode.html', periode=periode, result=result_dict)
 
@app.route('/rapport_etudiant/<int:etudiant_id>')
def rapport_etudiant(etudiant_id):
    etudiant = Etudiant.query.get_or_404(etudiant_id)
    presences = Presence.query.filter_by(id_etudiant=etudiant_id).all()
    presents = [p for p in presences if p.statut == 'PRESENT']
    absents = [p for p in presences if p.statut != 'PRESENT']
    justifiees = [p for p in presences if p.statut == 'JUSTIFIE']
    justifications = { (j.id_etudiant, j.id_enseignement): j for j in Justification.query.filter_by(id_etudiant=etudiant_id).all() }
    return render_template('rapport_etudiant.html',
                           etudiant=etudiant,
                           presents=presents,
                           absents=absents,
                           justifiees=justifiees,
                           justifications=justifications)
 
@app.route('/db_check')
def db_check():
    # Compatible avec MySQL, PostgreSQL, SQLite...
    return f"Base de données utilisée : {db.engine.url}"
 
if __name__ == '__main__':
    app.run(debug=True)