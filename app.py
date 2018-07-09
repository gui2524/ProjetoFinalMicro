import os
import base64
import sqlite3
from importlib import import_module
from flask import Flask, flash, redirect, render_template, request, session, abort, Response
from sqlalchemy.orm import sessionmaker
from Crypto.Cipher import XOR
from tabledef import *
import log


engine = create_engine('sqlite:///security.db', echo=True)

Camera = import_module('camera_opencv').Camera

key = 'secretkey'
 
app = Flask(__name__)

def encrypt(key, plaintext):
  cipher = XOR.new(key)
  log.eventLog("encrypt")
  return base64.b64encode(cipher.encrypt(plaintext))

def decrypt(key, ciphertext):
  cipher = XOR.new(key)
  log.eventLog("decrypt")
  return cipher.decrypt(base64.b64decode(ciphertext))

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('video.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cadastro')
def cadastro():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if not session.get('admin'):
            return render_template('login.html')
        else:
            return render_template('cadastro.html')

@app.route('/stream')
def stream():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('stream.html')
    
@app.route('/signup', methods=['POST'])
def signup():
    log.eventLog("sign up")
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    # Encryption    
    cipher_password = encrypt(key, POST_PASSWORD)
    log.log(cipher_password);
            
    conn = sqlite3.connect('security.db')
    sql = ''' INSERT INTO users (username, password) VALUES (?,?) '''
    project = (POST_USERNAME, cipher_password);
    cur = conn.cursor()
    cur.execute(sql, project)
            
    if cur.lastrowid:
        return render_template('success.html')
    else:
        flash('Erro!')
    return home()

 
@app.route('/login', methods=['POST'])
def do_admin_login():
    log.eventLog("admin login")
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
	
    # Encryption    
    cipher_password = encrypt(key, POST_PASSWORD)
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([cipher_password]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['admin'] = True
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000, threaded=True)
