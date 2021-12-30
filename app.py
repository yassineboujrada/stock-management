from flask import Flask,render_template,redirect,session,request
from flask.helpers import flash, url_for
from flask_pymongo import PyMongo
from data import *  

app = Flask(__name__)
app.secret_key = "maked by yassine boujrada"

app.config["MONGO_URI"] = "mongodb://localhost:27017/mini_project_mongo" # my local host/name of database
myData = PyMongo(app)

@app.route('/', methods =["GET","POST"] )
def login():    
    if request.method=="POST":
        session["email"]=request.form.get("email")
        session["pass"]=request.form.get("password")
        admin = myData.db.admin.find_one({"email":session["email"], "password": session["pass"]})
        if isEmpty(admin): 
            flash("votre email ou mot de pass invalid","problem")
            return redirect(url_for("login"))
        else :
            print("pass test")
            return redirect(url_for("home"))
            # session["prenom"] = admin["prenom"]
            # session["nom"] = admin["nom"]
            # session["img"] = admin["img"]
            # return redirect('/ourStock')
    return render_template('login.html')

@app.route("/home", methods =["GET","POST"])
def home():
    return render_template("home.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)