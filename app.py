from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app= Flask(__name__)
app.secret_key = "d03811b6f39d7a1ef40400f3a96648b4"

db=yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]

mysql = MySQL(app)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT username, password FROM user WHERE username=%s",(username,))

        if value>0:
            data=cur.fetchone()
            passw=data[1]
            if password==passw:
                session["logged_in"]=True
                session["username"]=username
                flash("Login Successful","success")
                #return redirect("/Mainpage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        name=userdata["name"]
        email=userdata["email"]
        phone=userdata["phone"]
        dob=userdata["dob"]
        address=userdata["address"]
        occupation=userdata["occupation"]
        cur=mysql.connection.cursor()

        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        existing_user=cur.fetchone()
        if existing_user:
            flash(f"Username '{username}' already exists. Please choose a different username.", "danger")
            cur.close()
            return redirect("/register")
        else:
            cur.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,name,email,phone,dob,address,occupation))
            mysql.connection.commit()
            flash("Register Successful.")
            cur.close()
            return redirect("/")
    return render_template("register.html")

@app.route("/stafflogin", methods=["GET","POST"])
def staff_login():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT username, password FROM user WHERE username=%s",(username,))

        if value>0:
            data=cur.fetchone()
            passw=data["password"]
            if password==passw:
                session["logged_in"]=True
                session["username"]=username
                flash("Login Successful","success")
                #return redirect("Staffpage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("staff_login.html")

if __name__=='__main__':
    app.run(debug=True)