from pickle import GET
from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools

# from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b"totoj e zceLa n@@@hodny retezec nejlep os.urandom(24)"
app.secret_key = b"x6\x87j@\xd3\x88\x0e8\xe8pM\x13\r\xafa\x8b\xdbp\x8a\x1f\xd41\xb8"


slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html")


@app.route("/info/")
def info():
    return render_template("info.html")


@app.route("/abc/")
def abc():
    return render_template("abc.html", slova=slova)

@app.route("/banán/", methods=["GET", "POST"])
def banán():
    if 'uživatel' not in session:
        flash('Nejsi příhlášen, tato stránka vyžaduje přihlášení')
        return redirect(url_for('login'))
        
    hmotnost= request.args.get("hmotnost")
    
    výška= request.args.get("výška")

    print(hmotnost, výška)
    if hmotnost and výška != None :  
        bmi=int(hmotnost) / ((int(výška)/100)**2)
    else:
        bmi = 0
    return render_template("banán.html", bmi=bmi)

@app.route("/text/")
def text():
    return """

<h1>Text</h1>

<p>toto je text</p>

"""
@app.route("/login/", methods=["GET"])
def login():
    jmeno = request.args.get('jmeno')
    heslo = request.args.get('heslo')
    print(jmeno, heslo)
    if request.method == 'GET':
        return render_template( 'login.html')

@app.route("/login/", methods=["POST"])
def login_post():
     jmeno = request.form.get('jmeno')
     heslo = request.form.get('heslo')
     if jmeno == 'Martin' and heslo=='umbilikus':
        session['uživatel'] = jmeno
              
     return redirect( url_for ('login'))
        #stejne jako funkce get, jen jiný zápis

@app.route("/logout/", methods=["GET"])
def logout():
    session.pop('uživatel', None)
    return redirect( url_for ('login'))