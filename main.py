from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLAlchemy_DATABASE_URI"] = "sqlite:///chat.db"

db = SQLAlchemy(app)


##################################################################################################################################################
#Création du modèle de la base de données 

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(80), nullable=False)
    
    def __init__(self,name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Thread(db.Model): #id,author, topic, category, description, date
    id =  db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    topic = db.Column(db.String(80), nullable = False)
    category = db.Column(db.String(80), nullable = True)
    description = db.Column(db.String(120), nullable=True)
    pub_date = db.Column(db.DateTime, default=db.func.now())
    
    def __init__(self, author, topic, category, description, date):
        self.author = author
        self.topic = topic
        self.category= category
        self.description=description
        self.pub_date=date

class Comment(db.Model): #author, content, date
    id =  db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=db.func.now())
    id_thread = db.Column(db.Integer, foreign_key=Thread.id)
    
    def __init__(self,author,content, date):
        self.author = author
        self.content= content
        self.pub_date = date
    
    
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
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    return redirect(url_for("home"))

@app.route("/sign-up", methods=["POST"])
def sign_up():
    name = request.form["name"]
    email = request.form["email"]
    user = User(name, email)
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    return redirect(url_for("home"))


##################################################################################################################################################
#AFFICHAGE DU FORUM

@app.route("/forum")
def forum():
    threads = Thread.query.all()
    name = session["name"]
    email = session["email"]
    return render_template("forum.html", all_threads = threads,name=name)

@app.route("/add-thread",methods=["POST"])
def add_thread():
    author = session["name"]
    topic = request.form["topic"]
    category = request.form["category"]
    description = request.form["description"]
    date = datetime.today()
    
    thread = Thread(author,topic,category,description,date)
    db.session.add(thread)
    db.session.commit()
    return redirect(url_for("forum"))

@app.route("/delete-thread/<int:comment_id>")
def delete_thread(thread_id):
    Thread.query.filter(Thread.id == thread_id).delete()
    db.session.commit()
    return redirect(url_for("forum"))

@app.route("/edit-thread/<int:comment_id>")
def edit_thread(thread_id):
    new_topic = request.form["topic"]
    new_description = request.form["description"]
    thread_object = Thread.query.get(thread_id)
    thread_object.description = new_description
    thread_object.topic = new_topic
    
    db.session.commit()
    return redirect(url_for("forum"))


##################################################################################################################################################
#AFFICHAGE D'UN THREAD

@app.route("/thread/<int:thread_id>")
def thread():
    comments = Comment.query.all()
    name = session["name"]
    email = session["email"]
    return render_template("thread.html", all_comments=comments,name=name)

@app.route("/add-comment", methods=["POST"])
def add_comment():
    author = session["name"]
    content = request.form["comment"]
    date = datetime.today()
    comment = Comment(author, content, date)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for("thread"))

@app.route("/delete-comment/<int:comment_id>")
def delete_comment(comment_id):
    Comment.query.filter(Comment.id == comment_id).delete()
    db.session.commit()
    return redirect(url_for("thread"))

@app.route("/edit-comment/<int:comment_id>")
def edit_comment(comment_id):
    new_content = request.form["comment"]
    comment_object = Comment.query.get(comment_id)
    comment_object.content = new_content
    db.session.commit()
    return redirect(url_for("thread"))


##################################################################################################################################################


if __name__ == "__main__":
    app.debug = True
    app.run()