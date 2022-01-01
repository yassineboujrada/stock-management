from flask import Flask,render_template,redirect,session,request
from flask.helpers import flash, url_for
from flask_pymongo import PyMongo
from data import *  
import bson

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
            session["cin"]=admin["_id"]
            return redirect(url_for("home"))
        
    return render_template('login.html')

@app.route("/home", methods =["GET","POST"])
def home():
    co=myData.db.clients.count_documents({})
    price=myData.db.product.find({"prix":{"$exists":1}},{"_id":0,"prix":1})
    total=calc_total(price)
    total_product=myData.db.product.count_documents({})
    save_courbe(myData)
    return render_template("home.html",cont_product=co,total=total,product=total_product)

@app.route("/client_information",methods=["POST","GET"])
def client():
    client_info=myData.db.clients.find({})
    return render_template("client.html",table_info=client_info)

@app.route("/settings",methods=["POST","GET"])
def setting():
    data=myData.db.admin.find_one({"_id":session["cin"]})
    adr=data["adresse"]["city"]+" "+data["adresse"]["street"]
    if request.method=="POST":
        f=request.files["img_file"]
        addpict(f,app)
        
        if data["full_name"] != request.form.get("user_name"):
            modify(myData,session["full_name"],"full_name",request.form.get("user_name"))
        else:
            if data["age"] != request.form.get("age"):
                modify(myData,session["cin"],"age",request.form.get("age"))
            else:
                # if data["password"] == request.form.get("password"):
                #     modify(myData,session["cin"],"password",request.form.get("password"))
                # else:
                    if data["img"] != f.filename:
                        modify(myData,session["cin"],"img",f.filename)
        return redirect(url_for("setting"))
    else:
       return render_template("Setting.html",data=data)
   
@app.route("/product",methods=["POST","GET"])
def product():
    prod=myData.db.product.find({})
    return render_template("product.html",info_product=prod)

@app.route("/product/add_product",methods=["POST","GET"])
def add_product():
    if request.method=="POST":
        try:
            x,y=int(request.form.get("Qte")),int(request.form.get("prix"))           
            if isinstance(x, int) and isinstance(y, int):
                print(myData.db.produddct.count_documents({})+1,request.form.get("categorie"),request.form.get("nomProduit"),request.form.get("Qte"),request.form.get("prix"),request.form.get("description"))
               # myData.db.produit.insert_one({"_id":id,"categorie":str(cat),"nomProduit":str(name),"Qte":qte,"prix":prix,"description":str(desc)})
                insertdb(myData,myData.db.product.count_documents({})+1,request.form.get("categorie"),request.form.get("nomProduit"),request.form.get("Qte"),request.form.get("prix"),request.form.get("description"))
                flash("you're commande added","success")
                return redirect(url_for('add_product'))
        except ValueError:
            flash("you entere incorrect informations","problem")
            return redirect(url_for("add_product"))
    return render_template("add.html")

@app.route("/product/drop_product",methods=["POST","GET"])
def drop_product():
    if request.method=="POST":
        dropprod(myData,request.form.get("categori"),request.form.get("product"))
        flash("you're commande droped","success")
        return redirect(url_for('drop_product'))
    return render_template("drop.html")


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)