import os
from flask import Flask, render_template, request, redirect, url_for, flash
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

#, methods=['GET', 'POST']
@app.route('/employees', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        flash(f'Account created for {register_form.username.data}!', 'success')
        return redirect(url_for('register'))
         
    return render_template('employees.html', register_form=register_form)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.Lusername.data == 'Tamotsu' and login_form.Lpassword.data == 'amongus132':
            return redirect(url_for('register'))
        else:
            flash('Login unsuccessful. Please check username and password')

    return render_template('loginpage.html', title='Login', login_form=login_form)

#@app.route('/employees')
#def employeepage():
#    return render_template('employees.html')


if __name__ == '__main__':
    app.run(debug = True)
