from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///therapie_en_ligne.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    mot_de_passe = db.Column(db.String(80))
    questions_repondues = db.Column(db.Boolean, default=False)
    rendez_vous = db.relationship('RendezVous', backref='utilisateur', lazy=True)
    threads = db.relationship('Thread', backref='createur', lazy=True)
    commentaires = db.relationship('Commentaire', backref='auteur', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='utilisateur', lazy=True)


class Therapeute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    specialite = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    mot_de_passe = db.Column(db.String(80))
    description = db.Column(db.Text)
    photo_profil = db.Column(db.String(100))
    prix_consultation = db.Column(db.Float)
    rendez_vous = db.relationship('RendezVous', backref='therapeute', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='therapeute', lazy=True)
    max_sessions = db.Column(db.Integer, default=10)  # nbr max de rdv


class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_therapeute = db.Column(db.Integer, db.ForeignKey('therapeute.id'))
    # Ajoutez d'autres colonnes nécessaires pour les informations de rendez-vous

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    # Ajoutez d'autres colonnes nécessaires pour les questions

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    contenu = db.Column(db.Text)
    anonyme = db.Column(db.Boolean, default=False)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    commentaires = db.relationship('Commentaire', backref='thread', lazy=True)

class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_thread = db.Column(db.Integer, db.ForeignKey('thread.id'))
    anonyme = db.Column(db.Boolean, default=False)
    
class Temoignage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    contenu = db.Column(db.Text)

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    articles = db.relationship('Article', backref='categorie', lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_commentaire = db.Column(db.Integer, db.ForeignKey('commentaire.id'))
    
class Facturation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    montant = db.Column(db.Float)
    date_facturation = db.Column(db.DateTime, default=datetime.utcnow)
    
class SessionVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_therapeute = db.Column(db.Integer, db.ForeignKey('therapeute.id'))
    date_session = db.Column(db.DateTime, default=datetime.utcnow)
    lien_video = db.Column(db.String(200))
    canceled = db.Column(db.Boolean, default=False)  # indique si la session est annulée
    extended = db.Column(db.Boolean, default=False)  # indique si la session est prolongée
    

# ... Ajoutez d'autres modèles et relations  ...

if _name_ == '_main_':
    app.run(debug=True)
