from pickle import GET
from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools
import random
import string
from mysqlite import SQLite
import re


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
    if 'uživatel' not in session:
        flash('Nejsi příhlášen, tato stránka vyžaduje přihlášení.', 'error')
        return redirect(url_for('login', page=request.full_path))
    return render_template("abc.html", slova=slova)

@app.route("/banán/", methods=["GET", "POST"])
def banán():
    if 'uživatel' not in session:
        flash('Nejsi příhlášen, tato stránka vyžaduje přihlášení.', 'error')
        return redirect(url_for('login', page=request.full_path))
        
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
     page = request.args.get('page')

     conn = sqlite3.connect('data.db')
     cur = conn.cursor()
     cur.execute(f'SELECT passwd FROM user WHERE login = ?', [jmeno])
     ans = cur.fetchall()

     
        

     if ans and ans[0][0]== heslo:
        flash('Jsi přihlášen!', 'message' )
        session['uživatel'] = jmeno
        if page:
            return redirect(page)
     else:
        flash('Nespávné přihlašovací udaje','error')
     if page:
        return redirect( url_for ('login', page=page))
     return redirect( url_for ('login'))
        #stejne jako funkce get, jen jiný zápis

@app.route("/logout/", methods=["GET"])
def logout():
    session.pop('uživatel', None)
    return redirect( url_for ('login'))

@app.route("/zkracovač/",  methods=["GET"])
def zkracovač():
    new = request.args.get("new")
    if "uživatel" in session:
        with SQLite("data.db") as cur:
            res = cur.execute("SELECT zkratka, adresa FROM adresy Where user=?", [session["uživatel"]])
            zkratky = res.fetchall()
            if not zkratky:
                zkratky = []
    else:
        zkratky = []
    return render_template("zkracovač.html", new=new, zkratky=zkratky)
    
    
    
    return render_template("zkracovač.html", new=new)

@app.route("/zkracovač/", methods=["POST"])
def zkracovač_post():
    url = request.form.get("url")
    if url and re.match("https?://.+", url):
        zkratka = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=5))

        with SQLite("data.db") as cur:
            if "uživatel" in session:
                cur.execute("INSERT INTO adresy (zkratka, adresa, user) VALUES (?, ?, ?)", [zkratka, url, user])
                flash("Adresa uložena")
            else:
                cur.execute("INSERT INTO adresy (zkratka, adresa) VALUES (?, ?)", [zkratka, url])
            return redirect(url_for("zkracovač", new=zkratka))
    else:
        flash("To, co jsi zadal není adresa webové stránky!")
        
    
    return redirect(url_for("zkracovač",))

@app.route("/zkracovač/<zkratka>",  methods=["GET"])
def dezkracovac(zkratka):
    print(zkratka)
    with SQLite("data.db") as cur:
        cur.execute("SELECT adresa FROM adresy WHERE zkratka=? ;", [zkratka])
        odpoved = cur.fetchone()
        print(type(odpoved))
        if odpoved:
            print(odpoved[0])
            return redirect(odpoved[0])

        else:
            flash("Toto ({}) není korektní ZKRATKA".format(zkratka))


    return redirect(url_for("zkracovač"))
