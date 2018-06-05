from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def map():
    return render_template('pkmap.html')

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('pklogin.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form['username']
#     pwd = request.form['password']
#     if username =='admin' and pwd=='password':
#         return render_template('pkprofile.html', username=username)
#     return render_template('pklogin.html', message = "Bad username or password", username = username)

@app.route('/pkprofile', methods=['GET', 'POST'])
def profile():
    conn = sqlite3.connect('pk_user.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_list WHERE username = 'admin'")
    data = cursor.fetchone()
    username = data[0]
    wallet = data[2]
    plate = data[3]
    conn.commit()
    conn.close()
    return render_template('pkprofile.html', username = username, wallet = wallet, plate = plate)

@app.route('/charge', methods=['GET'])
def charge_form():
    return '''<form action="/charge" method="POST">
              <p><input name="amount"></p>
              <p><button type="submit">submit</button></p>
              </form>'''

@app.route('/charge', methods=['POST'])
def charge():
    am = request.form['amount']
    conn = sqlite3.connect('pk_user.db')
    cursor = conn.cursor()
    # print(am)

    cursor.execute("SELECT * FROM user_list WHERE username = 'admin'")
    ndata = cursor.fetchone()
    new_am = int(ndata[2]+int(am))
    # print(new_am)


    cursor.execute("UPDATE user_list  SET wallet = ? WHERE plate = '6LIK274'",(new_am,))
    # cursor.execute("SELECT * FROM user_list WHERE username = 'admin'")
    # data = cursor.fetchone()
    # username = data[0]
    # wallet = data[2]
    # plate = data[3]
    conn.commit()
    conn.close()
    return render_template('charge.html')

@app.route('/pklot1', methods=['GET', 'POST'])
def lot1():

    ##Get information from PKLOT object
    conn = sqlite3.connect('pk.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pk_list WHERE pk_name = 'lot1'")
    data = cursor.fetchone()
    occ = data[1]
    total = data[2]
    free = total-occ
    conn.commit()
    conn.close()
    return render_template('pklot1.html', occ = str(occ), total = str(total), free = str(free))
