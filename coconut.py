from re import T
from flask import Flask,request, render_template,redirect,url_for
from flask_pymongo import pymongo

coconut = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://ageugenio:mongopass123@cluster0.5dynv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database("users_db")
users_table=db.users_table

@coconut.route("/")
def main():
    return render_template("index.html")

@coconut.route("/home")
def home():
    return render_template("index2.html")

@coconut.route("/project")
def project():
    return render_template("info.html")

@coconut.route("/about")
def about():
    return render_template("about.html")

@coconut.route("/login", methods = ["GET", "POST"])
def login():
    if request.method =='GET':
         return render_template("login.html")
    if request.method =='POST': 
        username = request.form['username']
        password = request.form['password']
        if username == '' or password =='':
           print("Incomplete!")
           return render_template("login.html", 
                                  error_message = 'Login Failed! Please complete all fields!',
                                  username=username,
                                  password = password )
        else:
            account= tuple(users_table.find({"username":username, "password":password}).limit(1))
            if account:
              print('success')
              return redirect(url_for('home'))

            else: 
              print("Failed")
              return render_template("login.html", 
                                  error_message = 'Login Failed! Invalid Inputs!',
                                  username=username,
                                  password = password )
   

    
@coconut.route("/register", methods = ["GET","POST"])
def register():
       if request.method =='GET':
         return render_template("reg.html") 

       if request.method == 'POST':
        #get the inputs on the answered form
        first_name= request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        password = request.form['password']
        new_account ={
            "first_name":first_name,
            "last_name":last_name,
            "username":username,
            "password":password}

        if first_name == '' or last_name == '' or username == '' or password =='':
           print("Incomplete!")
           return render_template("reg.html", 
                                  error_message = 'Registered Failed! Please complete all fields!',
                                  first_name=first_name,
                                  last_name=last_name,
                                  username=username,
                                  password = password )
        else:
            account= tuple(users_table.find({"username":username}).limit(1))
            if account:
                 print("Incomplete!")
                 return render_template("reg.html", 
                                  error_message = 'Registered Failed!Username Already Exist!',
                                  first_name=first_name,
                                  last_name=last_name,
                                  username=username,
                                  password = password )
            else:
                users_table.insert_one(new_account)
                print("New Account Added!")

        return render_template("reg.html", success=True,
                                  first_name = first_name,
                                  last_name = last_name,
                                  username = username,
                                  password = password )

   
if __name__ == "__main__":
    coconut.run(host="0.0.0.0", port=5050)