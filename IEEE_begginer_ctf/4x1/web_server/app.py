from flask import Flask, request,session, render_template,redirect
import sqlite3


app = Flask(__name__)
app.secret_key = 'Kalawy_random_key'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if 'uid' in session:
            return redirect('/Data_Exfiltration')
        else:
            username = request.form['username']
            password = request.form['password']
            if username == 'IEEE_exfiltration_user' and password == 'IEEE_exfiltration_pass':
                session['uid'] = 1
                return redirect('/Data_Exfiltration')
            else:
                return "Invalid credentials!"
    elif request.method == "GET":
        return render_template("login.html")

@app.route('/Data_Exfiltration/view', methods=['GET'])
def exfiltrate_data():
    if 'uid' in session:
        id = request.args.get('id')
        conn = sqlite3.connect("exfiltrated_data.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT data FROM data where id={id} and uid={session['uid']}")
        rows = cursor.fetchone()
        conn.close()
        if rows != None:
            return rows[0]
        else:
            return "Maybe you are unauthorized or this data is not exfiltrated yet"
    else:
        return redirect('/login')

@app.route('/Data_Exfiltration', methods=['GET'])
def view_exfiltrate_data():
    if 'uid' in session:
        return render_template("view_data.html")
    return redirect('/login')

@app.route('/Data_Exfiltration/send', methods=['POST'])
def send_data():
    return "No More Accepting Exfiltrations"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)