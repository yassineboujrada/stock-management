import os
from flask import Blueprint
import matplotlib.pyplot as plt

def isEmpty(data):
    if data:
        return False
    return True

def calc_total(t):
    sum=0
    for i in t:
        sum+=i["prix"]
    return sum
    
def modify(db,id,champ,value):
    db.db.admin.update_one({"_id":int(id)},{"$set":{str(champ):value}})
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def addpict(f,app):
    UPLOAD_FOLDER = '../projet_mongodb/static/pictures/pofile/'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    auth_print = Blueprint('auth_print', __name__)
    path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    print(allowed_file(f.filename))
    print(f.filename)
    if allowed_file(f.filename):
        print("mmmm")
        f.save(path)

    
def insertdb(db,id,cat,name,qte,prix,desc):
    db.db.product.insert_one({"_id":id,"categorie":str(cat),"nomProduit":str(name),"Qte":qte,"prix":prix,"description":str(desc)})

def dropprod(db,name,cat):
    db.db.product.delete_one({"categorie":str(cat),"nomProduit":str(name)})


def save_courbe(db):
    #plt.figure(figsize=(11,5))
    x=db.db.product.aggregate([{"$group":{"_id":"$categorie","count": { "$count": { } } }}])
    for i in x:
        plt.bar(i["_id"],i["count"])

    # plt.figure(figsize=(8,2))
    plt.title("statistiques of products")
    plt.xlabel('Categoties')
    plt.ylabel('number of categories in stocke')
    plt.legend()
    # plt.show()
    plt.savefig("../projet_mongodb/static/diagramme.png")
    plt.close()