from re import T
from flask import Flask,request, render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

#create flask app object
coconut = Flask(__name__)

#Configure Database
coconut.config['SECRET_KEY'] = 'secretcoconutkey'
coconut.config['SQLALCHEMY_DATABASE_URI']='sqlite:///UserRecords.sqlite'
coconut.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

#Initiate SQLAlchemy
db = SQLAlchemy(coconut)


# Create user model using SQLAlchemy
class User(db.Model):

    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(15))
    last_name = db.Column(db.String(15))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256))

    def __init__(self,first_name,last_name,username,password):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.password=password

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
            account = User.query.filter_by(username= username, password = password).first()
            if account:
              flash('You have successfully logged in.', username)
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
        new_account =User(first_name,last_name,username,password)

        if first_name == '' or last_name == '' or username == '' or password =='':
           print("Incomplete!")
           return render_template("reg.html", 
                                  error_message = 'Registered Failed! Please complete all fields!',
                                  first_name=first_name,
                                  last_name=last_name,
                                  username=username,
                                  password = password )
        else:
            account = User.query.filter_by(username= username).first()

            if account:
                 print("Incomplete!")
                 return render_template("reg.html", 
                                  error_message = 'Registered Failed! Username Already Exist!',
                                  first_name=first_name,
                                  last_name=last_name,
                                  username=username,
                                  password = password )
            else:
                 db.session.add(new_account)
                 db.session.commit()
                 print("New Account Added!")

        return render_template("reg.html", success=True,
                                  first_name = first_name,
                                  last_name = last_name,
                                  username = username,
                                  password = password )

   
if __name__ == "__main__":
    db.create_all()
    coconut.run(host="0.0.0.0", port=5050)