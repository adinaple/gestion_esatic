from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
db = SQLAlchemy()
 
class Filiere(db.Model):
    __tablename__ = 'FILIERE'
    code_filiere = db.Column(db.Integer, primary_key=True, autoincrement=True)
    libelle_filiere = db.Column(db.String(50), nullable=False)
 
class Matiere(db.Model):
    __tablename__ = 'MATIERE'
    code_matiere = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_matiere = db.Column(db.String(50), nullable=False)
 
class Periode(db.Model):
    __tablename__ = 'PERIODE'
    id_periode = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_periode = db.Column(db.Date, nullable=False)
 
class Enseignant(db.Model):
    __tablename__ = 'ENSEIGNANT'
    id_enseignant = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    specialite = db.Column(db.String(50))
    diplome = db.Column(db.String(50))
    sexe = db.Column(db.String(1), nullable=False)
 
class Utilisateur(db.Model):
    __tablename__ = 'UTILISATEUR'
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='secretaire')
    nom_complet = db.Column(db.String(100))
    actif = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
 
class Etudiant(db.Model):
    __tablename__ = 'ETUDIANT'
    id_etudiant = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    sexe = db.Column(db.String(1), nullable=False)
    code_filiere = db.Column(db.Integer, db.ForeignKey('FILIERE.code_filiere'), nullable=False)
    filiere = db.relationship('Filiere', backref='etudiants')
 
class Enseignement(db.Model):
    __tablename__ = 'ENSEIGNEMENT'
    id_enseignement = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_enseignement = db.Column(db.Date, nullable=False)
    heure_debut = db.Column(db.Time, nullable=False)
    heure_fin = db.Column(db.Time, nullable=False)
    id_enseignant = db.Column(db.Integer, db.ForeignKey('ENSEIGNANT.id_enseignant'), nullable=False)
    code_filiere = db.Column(db.Integer, db.ForeignKey('FILIERE.code_filiere'), nullable=False)
    id_periode = db.Column(db.Integer, db.ForeignKey('PERIODE.id_periode'), nullable=False)
    code_matiere = db.Column(db.Integer, db.ForeignKey('MATIERE.code_matiere'), nullable=False)
    enseignant = db.relationship('Enseignant', backref='enseignements')
    filiere = db.relationship('Filiere', backref='enseignements')
    periode = db.relationship('Periode', backref='enseignements')
    matiere = db.relationship('Matiere', backref='enseignements')
 
class Correspondre(db.Model):
    __tablename__ = 'CORRESPONDRE'
    code_filiere = db.Column(db.Integer, db.ForeignKey('FILIERE.code_filiere'), primary_key=True)
    code_matiere = db.Column(db.Integer, db.ForeignKey('MATIERE.code_matiere'), primary_key=True)
    volume_horaire = db.Column(db.Integer, nullable=False)
 
class Presence(db.Model):
    __tablename__ = 'PRESENCE'
    id_etudiant = db.Column(db.Integer, db.ForeignKey('ETUDIANT.id_etudiant'), primary_key=True)
    id_enseignement = db.Column(db.Integer, db.ForeignKey('ENSEIGNEMENT.id_enseignement'), primary_key=True)
    statut = db.Column(db.String(10), nullable=False)
    commentaire = db.Column(db.Text)
    etudiant = db.relationship('Etudiant', backref='presences')
    enseignement = db.relationship('Enseignement', backref='presences')
 
class Justification(db.Model):
    __tablename__ = 'JUSTIFICATION'
    id_justification = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_etudiant = db.Column(db.Integer, db.ForeignKey('ETUDIANT.id_etudiant'))
    id_enseignement = db.Column(db.Integer, db.ForeignKey('ENSEIGNEMENT.id_enseignement'))
    motif = db.Column(db.Text)
    fichier = db.Column(db.String(255))
    etudiant = db.relationship('Etudiant', backref='justifications')
    enseignement = db.relationship('Enseignement', backref='justifications')