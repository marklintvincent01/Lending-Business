from flask import Flask,render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def landingpage():
    return render_template("landingpage.html")

@app.route('/about')
def aboutpage():
    return render_template("about.html")

@app.route('/login')
def loginpage():
    return render_template("loginpage.html")

if __name__ == "__main__":
    app.run(debug = True)
