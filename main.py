from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///therapie_en_ligne.db'
db = SQLAlchemy(app)


##################################################################################################################################################
#Création du modèle de la base de données 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    questions_repondues = db.Column(db.Boolean, default=False) 
    
    rendez_vous = db.relationship('RendezVous', backref='user', lazy=True)
    threads = db.relationship('Thread', backref='createur', lazy=True)
    commentaires = db.relationship('Comment', backref='auteur', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='user', lazy=True)
    
    def __init__(self, name, email, password, questions_repondues):
        self.name = name
        self.email = email
        self.password = password
        self.questions_repondues = questions_repondues


class Therapeute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    specialite = db.Column(db.String(100), nullable =False)
    description = db.Column(db.Text, nullable=False )
    photo_profil = db.relationship('Img', backref='auteur', lazy=True)
    max_sessions = db.Column(db.Integer, default=10)
    nb_experience = db.Column(db.Integer) #nombre d'années d'experience
    formation = db.Column(db.Text)
    
    rendez_vous = db.relationship('RendezVous', backref='therapeute', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='therapeute', lazy=True)
    
    
    def __init__(self, name, email, password, specialite, description, max_sessions, nb_experiences, formation):
        self.name = name
        self.email = email
        self.password = password
        self.specialite = specialite
        self.description = description
        self.max_sessions = max_sessions
        self.nb_experiences = nb_experiences
        self.formation = formation


        
class RendezVous(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_therapeute = db.Column(db.Integer, db.ForeignKey('therapeute.id'))
    prix_consultation = db.Column(db.Float, nullable=False)
    date_rdv = db.Column(db.Date, nullable = False)
    heure_rdv = db.Column(db.Time, nullable = False)
    completed = db.Column(db.Boolean, default = False, nullable=False) #rdv déjà fini ou pas
    canceled_id = db.Column(db.Integer, default = 0) #id de la personne qui a annulé sinon 0
    
    def __init__ (self, id_user, id_therapeute, prix_consultation, date_rdv, heure_rdv, completed, canceled_id):
        self.id_user = id_user
        self.id_therapeute = id_therapeute
        self.prix_consultation = prix_consultation
        self.date_rdv = date_rdv
        self.heure_rdv = heure_rdv
        self.completed = completed
        self.canceled_id = canceled_id
        
        
        
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    answer = db.Column(db.Text)
    
    def __init__(self,content, id_user, answer):
        self.content = content
        self.id_user = id_user
        self.answer = answer
    

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    content = db.Column(db.Text)
    anonyme = db.Column(db.Boolean, default=False)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_pub = db.Column(db.DateTime, default=db.func.now())
    
    commentaires = db.relationship('Commentaire', backref='thread', lazy=True)
    
    def __init__(self, titre, content, anonyme, id_user, date_pub):
        self.titre = titre
        self.content = content
        self.anonyme = anonyme
        self.id_user = id_user
        self.date_pub = date_pub

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_thread = db.Column(db.Integer, db.ForeignKey('thread.id'))
    anonyme = db.Column(db.Boolean, default=False)
    date_pub = db.Column(db.DateTime, default=db.func.now())
    
    def __init__(self, contenu, id_user, id_thread, anonyme, date_pub):
        self.contenu = contenu
        self.id_user = id_user
        self.id_thread = id_thread
        self.anonyme = anonyme
        self.date_pub = date_pub
    
class Temoignage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, contenu, id_user):
        self.contenu = contenu
        self.id_user = id_user

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable = False)
    contenu = db.Column(db.Text, nullable = False)
    
    def __init__(self, titre, contenu):
        self.titre = titre
        self.contenu = contenu
    
    
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable = False)
    articles = db.relationship('Article', backref='categorie', lazy=True)
    
    def __init__(self, nom):
        self.nom = nom

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_commentaire = db.Column(db.Integer, db.ForeignKey('commentaire.id'))
    
    def __init__(self, id_user, id_commentaire):
        self.id_user = id_user
        self.id_commentaire = id_commentaire
    
class Facturation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    montant = db.Column(db.Float)
    date_facturation = db.Column(db.DateTime, default=datetime.utcnow, nullable = False)
    
    def __init__(self, id_user, montant, date_facturation):
        self.id_user = id_user
        self.montant = montant
        self.date_facturation = date_facturation
    
class SessionVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_therapeute = db.Column(db.Integer, db.ForeignKey('therapeute.id'))
    date_session = db.Column(db.DateTime, default=datetime.utcnow)
    lien_video = db.Column(db.String(200))
    canceled = db.Column(db.Boolean, default=False)  # indique si la session est annulée
    extended = db.Column(db.Boolean, default=False)  # indique si la session est prolongée
    
    def __init__(self, id_user, id_therapeute, date_session, lien_video, canceled, extended):
        self.id_user=id_user
        self.id_therapeute = id_therapeute
        self.date_session = date_session
        self.lien_video = lien_video
        self.canceled = canceled
        self.extended = extended
    
class Img(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, unique= True, nullable = False)
    name = db.Column(db.Text, nullable=False)
    img_type = db.Column(db.Text, nullable =False) #type de l'image : JPEG, PNG etc.
    id_user = db.Column(db.Integer, db.ForeignKey('therapeute.id'))
    
    def __init__(self,img, name, img_type, id_user):
        self.img = img
        self.name = name
        self.img_type = img_type
        self.id_user = id_user
    
#Création de la base de données
with app.app_context():
    db.drop_all()
    db.create_all()
    
 
##################################################################################################################################################    
#Routage du site web 

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    remember_me = request.form.get("remember_me")  # Récupère la valeur de la case à cocher "remember_me"

    # Vérifie les informations de connexion et authentifie l'utilisateur
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        session["user_id"] = user.id

        if remember_me:
            # Si la case "Se souvenir de moi" est cochée, définit un cookie pour se souvenir de l'utilisateur pendant 30 jours
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)

        return redirect(url_for("home"))
    else:
        return render_template("login.html", error="Invalid email or password")

@app.route("/signup-user", methods=["POST"])
def signup_user():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    user = User(name, email, password)
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    session["password"] = request.form["password"]
    
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("signup-pro", methods = ["POST"])
def signup_pro():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    specialite = request.form["specialite"]
    description = request.form["description"]
    nb_experience = request.form["nb_experience"]
    max_sessions = request.form["max_sessions"]
    formation = request.form["formation"]
    
    photo_profil = request.files["photo_profil"]
    if not photo_profil :
        return "No pic uploaded",400 #error bad request
    
    filename=secure_filename(photo_profil.filename)
    phototype = photo_profil.mimetype
    img = Img(photo_profil.read(),phototype, filename, name)
    
    
    
    
    
    pro = Therapeute(name, email, password, specialite, description,max_sessions, nb_experience, formation)
    
    photo_profil = request.files["photo_profil"]
    if not photo_profil :
        return "No pic uploaded",400 #error bad request
    
    filename=secure_filename(photo_profil.filename)
    phototype = photo_profil.mimetype
    img = Img(photo_profil.read(),phototype, filename, name)
    
    pro.photo_profil = img
    
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    session["password"] = request.form["password"]
    
    db.session.add(pro)
    db.session.commit()
    return redirect(url_for("home"))




##################################################################################################################################################
#AFFICHAGE DU FORUM

@app.route("/forum")
def forum():
    threads = Thread.query.all()
    name = session["name"]
    email = session["email"]
    return render_template("forum.html", all_threads = threads, name=name, email=email)

@app.route("/add-thread",methods=["POST"])
def add_thread():
    return render_template("new_thread.html")

@app.route("/new-thread", methods =["POST"])
def new_thread():
    titre = request.form["titre"]
    contenu = request.form["contenu"]
    anonyme=request.form["anonyme"]
    author = session["name"]
    date_pub = datetime.utcnow
    
    thread = Thread(titre, contenu, anonyme, author, date_pub)
    db.session.add(thread)
    db.session.commit()
    return redirect(url_for("forum")) #à changer pour le redirect vers la page du thread créé si possible


@app.route("/delete-thread/<int:comment_id>")
def delete_thread(thread_id):
    Thread.query.filter(Thread.id == thread_id).delete()
    db.session.commit()
    return redirect(url_for("forum"))

@app.route("/edit-thread/<int:comment_id>")
def edit_thread(thread_id):
    new_title = request.form["new_title"]
    new_content = request.form["new_content"]
    thread_object = Thread.query.get(thread_id)
    
    thread_object.content = new_content
    thread_object.title = new_title
    
    db.session.commit()
    return redirect(url_for("forum"))


##################################################################################################################################################
#AFFICHAGE D'UN THREAD

@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    thread = Thread.query.get(thread_id)
    comments = Comment.query.all(id_thread = thread_id)
    name = session["name"]
    email = session["email"]
    return render_template("thread.html", thread = thread, all_comments=comments,name=name, email=email)

@app.route("/add-comment", methods=["POST"])
def add_comment(thread_id):
    author = session["name"]
    content = request.form["comment"]
    date_pub = datetime.today()
    anonyme = request.form["anonyme"]
    comment = Comment(content,author, thread_id, anonyme, date_pub)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("thread"))

@app.route("/delete-comment/<int:comment_id>")
def delete_comment(comment_id):
    Comment.query.filter(Comment.id == comment_id).delete()
    db.session.commit()
    return redirect(url_for("thread"))


@app.route("/edit/<int:comment_id>")
def edit_page(comment_id):
    comment = Comment.query.get(comment_id)
    return render_template("edit.html", comment=comment)

@app.route("/edit-comment/<int:comment_id>", methods=["POST"])
def edit_comment(comment_id):
    new_content = request.form["comment"]
    comment_object = Comment.query.get(comment_id)
    comment_object.contenu = new_content
    db.session.commit()
    return redirect(url_for("thread"))


##################################################################################################################################################


if __name__ == "__main__":
    app.debug = True
    app.run()
