from flask import Flask,render_template, request, redirect, url_for, flash
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9773dc56c46b09f651bfdfad603adc8'

@app.route('/')
@app.route('/home')
def landingpage():
    return render_template('landingpage.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!')
        
    return render_template('registration.html', title='Register', form=form)

@app.route('/login')
def loginpage():
    form = LoginForm()
    return render_template('loginpage.html', title='Login', form=form)

@app.route('/employees')
def employeepage():
    return render_template('employees.html')


if __name__ == '__main__':
    app.run(debug = True)
