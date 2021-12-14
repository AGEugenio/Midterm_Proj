from re import T
from flask import Flask,request, render_template,redirect,url_for, session
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired

#create flask app object
coconut = Flask(__name__)


#Set encryption key
coconut.config['SECRET_KEY'] = 'secretcoconutkey'

#Configure Database
coconut.config['SQLALCHEMY_DATABASE_URI']='sqlite:///UserRecords.sqlite'
coconut.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

#Initiate SQLAlchemy
db = SQLAlchemy(coconut)


# Create user model using SQLAlchemy
class User(db.Model):

    __tablename__ = 'usertable'

    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256))

    def __init__(self,first_name,last_name,username,password):
        self.first_name=first_name
        self.last_name=last_name
        self.username=username
        self.password=password
db.create_all()

#Create Registraton Form
class RegisterForm(FlaskForm):
    
    first_name = StringField("FirstName", validators=[validators.Length(min=3, max=32), validators.DataRequired(message="Please Fill This Field")])
    last_name = StringField("LastName", validators=[validators.Length(min=3, max=32), validators.DataRequired(message="Please Fill This Field")])  
    username = StringField("Username", validators=[validators.Length(min=3, max=32), validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])    
    submit = SubmitField('Register')

#Create Login Form
class LoginForm(FlaskForm):
    username  = StringField('UserName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

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

# Route for handling the login page 
@coconut.route("/login", methods = ["GET", "POST"])
def login():
    form=LoginForm()
    if request.method =='POST' and form.validate_on_submit(): 
        #gets the inputs on the form
        username = form.username.data
        password = form.password.data

        #Checks if the entered username and password match the ones in the database
        account = User.query.filter_by(username= username, password = password).first()

        if account:
            session['logged_in'] = True
            session['username'] = account.username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", 
                                  error_message = 'Login Failed! Invalid Inputs!',
                                  form=form )
    return render_template('login.html', form = form)

# Route for handling the register page   
@coconut.route("/register", methods = ["GET","POST"])
def register():
       form=RegisterForm()
       
       if request.method =='POST': 
           username = form.username.data

           #checks if username is already existing in the database
           account = User.query.filter_by(username=username).first()
           if account:
                print("Username already Taken!")
                return render_template("reg.html", error_message = 'Registered Failed!Username Already Exist!',form=form)
        
       #checks the request and validates the fields on the form
       if form.validate_on_submit():
            #gets the inputs on the register form
            first_name = form.first_name.data
            last_name = form.last_name.data   
            username = form.username.data
            password = form.password.data

            #a new User model is created and added to the database
            new_account = User(first_name,last_name, username,password)
            db.session.add(new_account)
            db.session.commit()
            print("New Account Added!")
            return render_template("reg.html",success=True,form=form)
       
       return render_template("reg.html",form=form)

@coconut.route('/logout/')
def logout(): 
    session['logged_in'] = False
    return redirect(url_for('home'))   

if __name__ == "__main__":
    
    coconut.run(host="0.0.0.0", port=5050)