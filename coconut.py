from flask import Flask
from flask import request
from flask import render_template, send_file
coconut = Flask(__name__)

@coconut.route("/")
def main():
    return render_template("index.html")


@coconut.route("/project")
def project():
    return render_template("info.html")

@coconut.route("/about")
def about():
    return render_template("about.html")

   
if __name__ == "__main__":
    coconut.run(host="0.0.0.0", port=8080)