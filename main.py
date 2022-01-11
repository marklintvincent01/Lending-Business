import functools
from flask import Flask, render_template, request, redirect, session, url_for, flash, jsonify
from flask_wtf import form
from forms import RegistrationForm, LoginForm
from flask_mysqldb import MySQL
import MySQLdb.cursors
import string
from random import choice
from datetime import date
from passlib.hash import sha256_crypt
from wtforms.validators import ValidationError
import json

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f9773dc56c46b09f651bfdfad603adc8'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'lending_business'

mysql = MySQL(app)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('id'):
            return redirect(url_for('loginpage'))

        if session.get('roleid') == 2:
            return redirect(url_for('aboutpage'))

        return view(**kwargs)
    return wrapped_view

@app.route('/')
@app.route('/home')
def landingpage():
    return render_template('landingpage.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

#, methods=['GET', 'POST']
@app.route('/employees', methods=['GET', 'POST'])
@login_required
def register():
    register_form = RegistrationForm()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT le.lenderID, CONCAT(le.Lname, ", ", le.Fname, " ", le.Mname) AS "name", le.username, le.age, le.email, le.date_hired, le.dob, le.contact_num, le.address, le.gender, r.role_name
        FROM lender_employee AS le 
        INNER JOIN user_role AS ur
            ON le.lenderID = ur.lenderID
        INNER JOIN roles AS r
            ON ur.role_id = r.role_id
        ORDER BY name ASC
        ''')
    data = cursor.fetchall()
    status = 1
    if request.method == 'POST':
        Fname = register_form.Fname.data
        Mname = register_form.Mname.data
        Lname = register_form.Lname.data
        age = register_form.age.data
        contact_num = register_form.contact_num.data
        address = register_form.address.data
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        date_hired = date.today()
        dob = register_form.dateofbirth.data
        gender = register_form.gender.data
        role = register_form.role.data
        id = IDGeneratorCheck()
        hashed_password = sha256_crypt.hash(password)
        cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            #raise ValidationError("Account already exists!")
            #msg = 'Account already exists!'
            #flash('Account already exists!')
            # errors ={'Error':'Account already exists.'}
            # data = json.dumps(errors)
            # return jsonify(data)
            status = 2
            
        else:
            cursor.execute(f"""
                INSERT INTO lender_employee VALUES
                ('{id}', '{Fname}', '{Mname}', '{Lname}', '{username}', '{hashed_password}', {age}, '{email}', '{date_hired}', '{dob}', '{contact_num}', '{address}', '{gender}');
            """)
            cursor.execute(f"""
                INSERT INTO user_role VALUES
                ({role}, '{id}');
            """)
            mysql.connection.commit()

        if status == 2:
            flash(f'Username "{register_form.username.data}" already exists!', 'danger')
        else:
            flash(f'Account created for {register_form.username.data}!', 'success')
        #return jsonify(status='ok')
        return redirect(url_for('register'))
        
    else:
        return render_template('employees.html', register_form=register_form, data=data)

@app.route('/login', methods=['GET', 'POST'])
def loginpage():
    login_form = LoginForm()

    if request.method == 'POST':
        username = login_form.Lusername.data
        password = login_form.Lpassword.data
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM lender_employee WHERE username = %s', (username,))
            account = cursor.fetchone()
            lender_id = account.get("lenderID")
            cursor.execute('SELECT role_id FROM user_role WHERE lenderID = %s', (lender_id,))
            user_role = cursor.fetchone()
            roleid = user_role.get("role_id")
            lpass_hashed = account.get("lender_password")
            verify = sha256_crypt.verify(password, lpass_hashed)
        except:
            flash("The username you entered isn't connected to an account.")
            return redirect(url_for('loginpage'))

        if verify:
            session['loggedin'] = True
            session['id'] = account['lenderID']
            session['username'] = account['username']
            session['roleid'] = user_role['role_id']
            if roleid == 1:  
                return redirect(url_for('register'))
            else:
                return redirect(url_for('aboutpage'))

        else:
            flash("The password you entered is incorrect.")
            return redirect(url_for('loginpage'))

    else:  
        return render_template('loginpage.html', title='Login', login_form=login_form)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('loginpage'))



def IDGenerator():
    chars = string.digits
    random =  ''.join(choice(chars) for _ in range(4))

    return random

def IDGeneratorCheck():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    idgen = IDGenerator()

    cursor.execute('SELECT * FROM lender_employee WHERE LenderID = %s', (idgen,))
    id = cursor.fetchone()

    while id:
        idgen = IDGenerator()

    return idgen



if __name__ == '__main__':
    app.run(debug = True)
