from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date, time

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///therapie_en_ligne.db'
db = SQLAlchemy(app)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



##################################################################################################################################################
##################################################################################################################################################
#Création du modèle de la base de données 



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False,  unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    questions_repondues = db.Column(db.Boolean, default=False) 
    
    rendez_vous = db.relationship('RendezVous', backref='user', lazy=True)
    threads = db.relationship('Thread', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='user', lazy=True)
    
    def __init__(self, name, email, password, questions_repondues):
        self.name = name
        self.email = email
        self.password = password
        self.questions_repondues = questions_repondues


class Therapeute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    specialite = db.Column(db.String(100), nullable =False)
    description = db.Column(db.Text, nullable=False )
    max_sessions = db.Column(db.Integer, default=10)
    nb_experience = db.Column(db.Integer) #nombre d'années d'experience
    formation = db.Column(db.Text)
    
    rendez_vous = db.relationship('RendezVous', backref='therapeute', lazy=True)
    sessions_video = db.relationship('SessionVideo', backref='therapeute', lazy=True)
    photo_profil = db.relationship('Image', backref='therapeute', lazy=True)
    
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
    name_user = db.Column(db.String(100), db.ForeignKey('user.name'))
    name_therapeute = db.Column(db.String(100), db.ForeignKey('therapeute.name'))
    date_rdv = db.Column(db.Date, nullable = False)
    heure_rdv = db.Column(db.Time, nullable = False)
    details = db.Column(db.Text)
    completed = db.Column(db.Boolean, default = False, nullable=False) #rdv déjà fini ou pas
    canceled_id = db.Column(db.Integer, default = 0) #id de la personne qui a annulé sinon 0
    
    
    def __init__ (self, name_user, name_therapeute, date_rdv, heure_rdv, details, completed, canceled_id):
        self.name_user = name_user
        self.name_therapeute = name_therapeute
        self.date_rdv = date_rdv
        self.heure_rdv = heure_rdv
        self.details = details
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
    
    comments = db.relationship('Comment', backref='thread', lazy=True)
    
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
    categorie_id = db.Column(db.Integer, db.ForeignKey('categorie.id'), nullable=False)
    
    def __init__(self, titre, contenu, categorie_id):
        self.titre = titre
        self.contenu = contenu
        self.categorie_id = categorie_id
    
    
class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable = False)
    articles = db.relationship('Article', backref='categorie', lazy=True)
    
    def __init__(self, nom):
        self.nom = nom

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_comment = db.Column(db.Integer, db.ForeignKey('comment.id'))
    
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
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
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
    
class Image(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    img = db.Column(db.Text, nullable = False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable =False) #type de l'image : JPEG, PNG etc.
    
    username = db.Column(db.Integer, db.ForeignKey('therapeute.name'))
    
    def __init__(self, img, name, mimetype, username):
        self.img = img
        self.name = name
        self.mimetype = mimetype
        self.username = username
 
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

   
#Création de la base de données
with app.app_context():
    #db.drop_all()
    db.create_all()



    
    
##################################################################################################################################################
##################################################################################################################################################    
#Routage du site web 



@app.route("/")
def home():
    try :
        mail = session["email"]
        print(mail)
    except:
        mail = None
        print(mail)
        
    if mail is not None:
        user = User.query.filter_by(email=mail).first()
        therapeute = Therapeute.query.filter_by(email=mail).first()
        name = session["name"]
        connected = True
        
        if (user is not None):
            pro = False
            print("je suis un user")       
            return render_template("home.html", user = user, name=name, pro=pro, connected = connected)
        
    
        elif (therapeute is not None):
            pro = True
            print("je suis un pro")
            return render_template("home.html", therapeute = therapeute, name=name, pro=pro, connected = connected)
    print("je ne suis personne")
    connected = False
    return render_template("home.html", connected = connected)



@app.route("/login")
def login():
    return render_template("login.html")
    
@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    remember_me = request.form.get("remember_me")  # Récupère la valeur de la case à cocher "remember_me"

    
    # Vérifie les informations de connexion et authentifie l'utilisateur
    user = User.query.filter_by(email=email).first()
    therapeute = Therapeute.query.filter_by(email=email).first()
    
    if (user is not None) and user.password == password:        
        session["name"] = user.name
        session["email"] = user.email
        
        if remember_me:
            # Si la case "Se souvenir de moi" est cochée, définit un cookie pour se souvenir de l'utilisateur pendant 30 jours
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)
        return redirect(url_for("home"))
    
    elif (therapeute is not None) and therapeute.password == password :
        session["name"] = therapeute.name
        session["email"] = therapeute.email
        
        if remember_me:
            # Si la case "Se souvenir de moi" est cochée, définit un cookie pour se souvenir de l'utilisateur pendant 30 jours
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)
        return redirect(url_for("home"))
    
    else:
        return render_template("login.html", error="Invalid email or password")




@app.route("/signup-user", methods=["GET","POST"])
def signup_user():
    return render_template("signup_user.html")

@app.route("/create-account", methods=["POST"])
def create_account():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    user = User(name, email, password, False)
    
    session["email"] = request.form["email"]
    session["name"] = request.form["name"]
    
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/signup-pro", methods = ["GET","POST"])
def signup_pro():
    return render_template("signup_pro.html")
    
@app.route("/create-account-pro", methods=["GET","POST"])
def create_pro_account():
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    specialite = request.form["specialite"]
    description = request.form["description"]
    max_sessions = request.form["max_sessions"]
    nb_experience = request.form["nb_experience"]
    formation = request.form["formation"]
    

    photo_profil = request.files['photo_profil']
        
    if photo_profil is None :
        return "No pic uploaded", 400 #error bad request"""
    
    if photo_profil and allowed_file(photo_profil.filename):
        filename = secure_filename(photo_profil.filename)
        print("Im secure")
    else:
        filename = secure_filename(photo_profil.filename)
        print("Im not secure")
    
   
    phototype = photo_profil.mimetype
    
    img = Image(img=photo_profil.read(), mimetype=phototype, name=filename, username=name)
    
    db.session.add(img)
    db.session.commit()
    
    pro = Therapeute(name, email, password, specialite, description,max_sessions, nb_experience, formation)
    
    #pro.photo_profil = img
    
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    
    
    db.session.add(pro)
    db.session.commit()
    return redirect(url_for("home"))


##################################################################################################################################################
#LOG OUT    

@app.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("name", None)
    return redirect(url_for("home"))



##################################################################################################################################################
#Profil USER

@app.route("/user/<int:user_id>")
def profil(user_id):
    email = session["email"]
    name=session["name"]
    user = User.query.get(user_id)
    
    liste_rendezvous = RendezVous.query.filter_by(name_user = name)
    
    
    return render_template("user.html", email=email, user=user, liste_rendezvous=liste_rendezvous)

@app.route("/update-profile/<int:user_id>", methods=["POST"])
def update_profile(user_id):
    new_name = request.form["name"]
    new_email = request.form["email"]
    new_password = request.form["password"]
    user_object = User.query.get(user_id)
    
    user_object.name = new_name
    user_object.email = new_email
    user_object.password = new_password
    
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/delete-profile/<int:user_id>")
def delete_profile(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    print("je retourne à la page d'accueil")
    return redirect(url_for("logout"))
    


##################################################################################################################################################
#Profil USER PRO

@app.route("/therapeute/<int:therapeute_id>")
def profil_pro(therapeute_id):
    email = session["email"]
    name=session["name"]
    therapeute = Therapeute.query.get(therapeute_id)
    
    liste_rendezvous = RendezVous.query.filter_by(name_therapeute=name)
    
    return render_template("user_pro.html", email=email, therapeute=therapeute, liste_rendezvous = liste_rendezvous)

@app.route("/update-profile-pro/<int:therapeute_id>",methods=["POST"])
def update_profile_pro(therapeute_id):
    new_name = request.form["name"]
    new_email = request.form["email"]
    new_password = request.form["password"]
    new_specialite = request.form["specialite"]
    new_description = request.form["description"]
    new_max_sessions = request.form["max_sessions"]
    new_nb_experience = request.form["nb_experience"]
    new_formation = request.form["formation"]
    
    
    therapeute_object = Therapeute.query.get(therapeute_id)
    
    therapeute_object.name = new_name
    therapeute_object.email = new_email
    therapeute_object.password = new_password
    therapeute_object.specialite = new_specialite
    therapeute_object.description = new_description
    therapeute_object.max_sessions = new_max_sessions
    therapeute_object.nb_experience = new_nb_experience
    therapeute_object.formation = new_formation
    
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/upload-profile-picture/<int:therapeute_id>", methods=["POST"])
def upload_profile_picture(therapeute_id):
    name = session["name"]
    email=session["email"]
    new_photo = request.files["photo_profil"]
    if not new_photo:
        return "No pic uploaded",400 #error bad request
    filename=secure_filename(new_photo.filename)
    phototype = new_photo.mimetype
    new_photo_profil = Image(new_photo.read(),phototype, filename, name)
    
    therapeute_object = Therapeute.query.get(therapeute_id)
    therapeute_object.photo_profil = new_photo_profil
    
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete-profile-pro/<int:therapeute_id>")
def delete_profile_pro(therapeute_id):
    therapeute = Therapeute.query.get(therapeute_id)
    db.session.delete(therapeute)
    db.session.commit()
    
    return redirect(url_for("home"))    

##################################################################################################################################################
#AFFICHAGE DU FORUM

@app.route("/forum")
def forum():
    threads = Thread.query.all()
    name = session["name"]
    email = session["email"]
    return render_template("forum.html", all_threads = threads, name=name)

@app.route("/add-thread",methods=["GET","POST"])
def add_thread():
    return render_template("new_thread.html")

@app.route("/new-thread", methods =["POST"])
def new_thread():
    titre = request.form["topic"]
    contenu = request.form["description"]
    anonyme = request.form["anonyme"]
    if anonyme == "yes":
        anonyme = True
    else :
        anonyme = False
        
    author = session["name"]
    date_pub = datetime.now()
    
    thread = Thread(titre, contenu, anonyme, author, date_pub)
    db.session.add(thread)
    db.session.commit()
    return redirect(url_for("thread", thread_id = thread.id))


@app.route("/delete-thread/<int:thread_id>")
def delete_thread(thread_id):
    Thread.query.filter(Thread.id == thread_id).delete()
    db.session.commit()
    return redirect(url_for("forum"))

@app.route("/edit-thread/<int:thread_id>")
def edit_thread(thread_id):
    thread = Thread.query.get(thread_id)
    return render_template("edit_thread.html", thread = thread)

@app.route("/change-thread/<int:thread_id>", methods=["POST"])
def change_thread(thread_id):
    new_title = request.form["new_title"]
    new_content = request.form["new_content"]
    thread_object = Thread.query.get(thread_id)
    
    thread_object.content = new_content
    thread_object.title = new_title
    
    db.session.commit()
    return redirect(url_for("thread", thread_id = thread_object.id))


##################################################################################################################################################
#AFFICHAGE D'UN THREAD

@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    thread = Thread.query.get(thread_id)
    comments = Comment.query.filter_by(id_thread = thread.id)
    name = session["name"]
    return render_template("thread.html", thread = thread, all_comments=comments, thread_id=thread.id, name=name)

@app.route("/add-comment/<int:thread_id>", methods=["POST"])
def add_comment(thread_id):
    
    email = session["email"]
    
    user = User.query.filter_by(email=email).first()
    id_user = user.id
    
    content = request.form["comment"]
    anonyme =  request.form["anonyme"]
    
    if anonyme == "yes" :
        anonyme = True
    else :
        anonyme = False
   
    print(anonyme)
    date = datetime.today()
    
    comment = Comment(content, id_user, thread_id, anonyme, date)
    print("le commentaire a été créé")
    
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("thread", thread_id = thread_id))

@app.route("/delete-comment/<int:comment_id>")
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    thread_id = comment.id_thread
    Comment.query.filter(Comment.id == comment_id).delete()
    db.session.commit()
    return redirect(url_for("thread",thread_id=thread_id))

@app.route("/edit-comment/<int:comment_id>")
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)
    return render_template("edit.html", comment=comment)
    
@app.route("/change-comment/<int:comment_id>", methods=["POST"])
def change_comment(comment_id):
    new_content = request.form["comment"]
    comment_object = Comment.query.get(comment_id)
    comment_object.contenu = new_content
    thread_id = comment_object.id_thread
    db.session.commit()
    return redirect(url_for("thread", thread_id=thread_id))



##################################################################################################################################################
# Feature : Affichage des articles
@app.route("/articles")
def articles():
    # Récupérer les articles depuis la base de données ou autre source de données
    articles = Article.query.all()
    liste_articles = []
    
    for article in articles:
        article_dico = {'titre': article.titre , 'contenu': article.contenu}
        liste_articles.append(article_dico)
        
    return render_template('articles.html', articles=liste_articles)

@app.route('/ressource')
def ressource():
    return render_template('ressources.html')


##################################################################################################################################################
# Feature : Prise de rendez-vous 
@app.route('/booking')
def booking():
    if 'name' in session:
        # Vérifier si l'utilisateur est connecté si Utilisateur connecté, afficher le formulaire de prise de rdv
        therapists = Therapeute.query.all()
        name = session["name"]

        date_min = date.today()
        date_max = date_min + timedelta(days=30)
        
        return render_template('rdv.html',therapists=therapists, name= name, date_min= date_min, date_max=date_max)
     
    else:
        # Utilisateur non connecté, rediriger vers la page de connexion 
        return redirect(url_for('login'))
    

# Route pour enregistrer un rendez-vous

@app.route('/create-rdv', methods=['POST'])
def booking_submit():
    # Récupérer les données du formulaire
    name_user = session["name"]

    name_therapeute = request.form['therapist']
    

    date_rdv_str = request.form['date_rdv']
    date_rdv = datetime.strptime(date_rdv_str, '%Y-%m-%d')
    
    heure_rdv_str = request.form['heure_rdv']
    heure_rdv = datetime.strptime(heure_rdv_str, '%H:%M').time()
    
    details = request.form["details"]
    
    completed = False  # Nouveau rendez-vous, donc completé à False
    canceled_id = 0  # Nouveau rendez-vous, donc canceled_id à 0
    
    rendezvous = RendezVous(name_user=name_user, name_therapeute=name_therapeute, date_rdv=date_rdv, heure_rdv=heure_rdv, details = details, completed=completed, canceled_id=canceled_id)
    db.session.add(rendezvous)
    db.session.commit()
    
    return redirect(url_for("home"))


@app.route('/cancel-rdv/<int:rdv_id>')
#On ne supprime pas le rdv de la base de données, simplement il ne s'affichera plus sur les profils users et therapeute
def cancel_rdv(rdv_id):
    rdv = RendezVous.query.filter_by(rdv_id).first()
    name_therapeute = rdv.name_therapeute
    therapeute = Therapeute.query.filter_by(name_therapeute).first()
    
    rdv.canceled_id = therapeute.id
    db.session.commit()
    
    return redirect(url_for('profil_pro', therapeute_id = therapeute.id))

##################################################################################################################################################
# Feature : Webchat en ligne

##################################################################################################################################################
# Feature : Facturation, paiement en ligne 

##################################################################################################################################################
# Feature : ...


##################################################################################################################################################


if __name__ == "__main__":
    app.debug = True
    app.run()
