from flask import Flask,render_template, request, redirect
from flask.helpers import url_for

app = Flask(__name__, template_folder='templates')

@app.route('/')
def landingpage():
    return render_template("landingpage.html")

@app.route('/loginpage')
def loginpage():
    return render_template("loginpage.html")

if __name__ == "__main__":
    app.run(debug = True)
