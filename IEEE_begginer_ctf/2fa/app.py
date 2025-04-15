from flask import Flask,render_template,request,session,redirect,Response,send_from_directory
import sqlite3
app = Flask(__name__)

app.secret_key = 'Random_Secret_Key_IEEE_2025'
app.static_folder = 'static'

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.execute(f'SELECT * FROM users WHERE username = \'{username}\' AND password = \'{password}\'')
        if cursor.fetchone():
            session['logged_in'] = True
            session['2fa'] = 'no'
            return redirect('/dashboard')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        if session.get('2fa') == 'yes':
            return render_template('dashboard.html')
        else:
            return render_template('2fa.html')
    else:
        return redirect('/')

@app.route('/2fa',methods=['POST'])
def two_factor_auth():
    if request.method == 'POST':
        if request.form['2fa'] == '512':
            session['2fa'] = 'yes'
            return redirect('/dashboard')
        else:
            return 'Invalid 2FA code'

@app.route('/van_persie_flag')
def flag():
    response = Response('Your heading skill is: -99')
    response.headers['Flag'] = 'it has became 99, congrats you have found the flag IEEE{G0000000000l}'
    return response

if __name__ == '__main__':
    app.run()