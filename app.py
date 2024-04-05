import pickle
import re
import MySQLdb
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt  # Install Flask-Bcrypt using pip

app = Flask(__name__)
bcrypt = Bcrypt(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.secret_key = 'your_secret_key_here'
mysql = MySQL(app)

model = pickle.load(open('model1.pkl', 'rb'))


@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connection
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account and bcrypt.check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully!'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'

    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if not password:  # Check if the password is empty
            msg = 'Password must be non-empty.'
        else:
            # Hash the password before storing in the database
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            conn = mysql.connection
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)  # Use DictCursor instead of dictionary=True
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()

            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                cursor.execute('INSERT INTO accounts (username, password, email) VALUES (%s, %s, %s)',
                               (username, hashed_password, email))
                conn.commit()
                msg = 'You have successfully registered!'

    return render_template('register.html', msg=msg)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        return render_template('profile.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/input', methods=['GET', 'POST'])
def input():
    return render_template('input.html')

@app.route('/pridict',methods=['GET','POST'])
def pridict():
    prediction = model.predict([[
       float( request.form.get('age')),
      float(  request.form.get('sex')),
       float( request.form.get('chest_pain')),
       float( request.form.get('resting_bp')),
       float( request.form.get('cholestrol')),
       float( request.form.get('fasting_blood_sugar')),
      float(  request.form.get('resting_ecg')),
      float(  request.form.get('max_heart_rate')),
       float( request.form.get('exercise_agina')),
       float( request.form.get('old_peak')),
       float( request.form.get('st_slope'))
    ]])
    output =prediction[0]
    #print(output)
    if output > 0:
        return render_template('output.html')
    else:
        return render_template('YESS.html ')
    
   
    
if __name__=='__main__':
    app.run(debug=True)