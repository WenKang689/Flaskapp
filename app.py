from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

app= Flask(__name__)

#database configuration
db=yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
app.secret_key = db["secret_key"]

mysql = MySQL(app)

#login for all
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
                return redirect("/homepage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("login.html")

#register
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
            cur.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NULL)",(username,password,name,email,phone,dob,address,occupation))
            mysql.connection.commit()
            flash("Register Successful.")
            cur.close()
            return redirect("/")
    return render_template("register.html")

#forgot password
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        userdata = request.form
        username = userdata["username"]
        email = userdata["email"]
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT username, email FROM user WHERE username=%s AND email=%s", (username, email))

        if value > 0:
            # User found, prepare to send email
            try:
                token = generate_token(email)
                reset_link = f"http://localhost:5000/reset_password?token={token}"
                # Set up the SMTP server
                server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                server.starttls()
                server.login('laptopkawkaw@outlook.com', 'kawkawlaptop123')

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = 'laptopkawkaw@outlook.com'
                msg['To'] = email
                msg['Subject'] = "Password Reset"
                body = f"Here is your password reset link: {reset_link}"
                msg.attach(MIMEText(body, 'plain'))

                # Send the email
                server.send_message(msg)
                del msg  # Clean up
                
                flash("Password reset link has been sent to your email.")
            except Exception as e:
                flash("An error occurred while sending the email.")
                print(e)  # For debugging purposes
            finally:
                server.quit()
        else:
            flash("User or email incorrect. Please try again.")
        cur.close()
    return render_template("forgot_password.html")

def generate_token(email):
    s = URLSafeTimedSerializer(app.secret_key)
    return s.dumps(email)

def verify_token(token, expiration=3600):
    s = URLSafeTimedSerializer(app.secret_key)
    if not token:
        return "No token provided", None
    try:
        # Assuming the token includes the email
        email = s.loads(token, max_age=expiration)
        return None, email
    except SignatureExpired:
        return "Token expired", None
    except BadSignature:
        return "Invalid token", None
    except Exception as e:
        return f"Error verifying token: {e}", None

#reset password
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token")
    if request.method == 'GET':
        error, email = verify_token(token)
        if error:
            flash(error)
            return render_template("reset_password.html")
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM user WHERE email=%s", (email,))
        user = cur.fetchone()
        if user:
            session['username_for_password_reset'] = user[0]
            return render_template("reset_password.html", email=email)
    elif request.method == "POST":
        userdata = request.form
        password = userdata["password"]
        confirm_password = userdata["confirm_password"]  # Get the confirm password field
        un=userdata["username"]
        username = session.get('username_for_password_reset')
        if not username or un!=username:
            flash("Username incorrect, please try again.")
            return redirect("/reset_password")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return render_template("reset_password.html")

        # Proceed with password reset if passwords match
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user SET password=%s WHERE username=%s", (password, username))
        mysql.connection.commit()
        flash("Password reset successful.")
        cur.close()
        session.pop('username_for_password_reset', None)
        return redirect("/")
    return render_template("reset_password.html")

#staff login
@app.route("/staff/login", methods=["GET","POST"])
def staff_login():
    if request.method == "POST":
        userdata=request.form
        staff_id=userdata["stf_id"]
        staff_psw=userdata["stf_psw"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT stf_id, stf_psw, stf_role FROM user WHERE stf_id=%s",(staff_id,))

        if value>0:
            data=cur.fetchone()
            passw=data["stf_psw"]
            role=data["stf_role"]
            if staff_psw==passw:
                if role=="Manager":
                    session["logged_in"]=True
                    session["staff_id"]=staff_id
                    flash("Login Successful","success")
                    return redirect("/manager/homepage")
                elif role=="Admin":
                    session["logged_in"]=True
                    session["staff_id"]=staff_id
                    flash("Login Successful","success")
                    return redirect("/admin/homepage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("staff_login.html")

#Client Section (Timi)
#C-home page
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html")

#C-setting/profile
@app.route("/user/setting/profile", methods=["GET","POST"])
def setting_profile():
    return render_template("setting_profile.html")

#C-setting/profile/edit profile
@app.route("/user/setting/profile/edit", methods=["GET","POST"])
def setting_profile_edit():
    return render_template("setting_profile_edit.html")

#C-setting/profile/payment method
@app.route("/user/setting/payment", methods=["GET"])
def setting_payment():
    return render_template("setting_payment.html")

#C-setting/profile/edit payment method(add,delete)
@app.route("/user/setting/payment/edit", methods=["GET","POST"])
def setting_payment_edit():
    return render_template("setting_payment_edit.html")

#C-setting/history(default purchase)
@app.route("/user/setting/history/purchase", methods=["GET","POST"])
def setting_history_purchase():
    return render_template("setting_history_purchase.html")

#C-setting/history/search history
@app.route("/user/setting/history/search", methods=["GET","POST"])
def setting_history_search():
    return render_template("setting_history_search.html")

#C-survey/fill in survey
@app.route("/recommend/survey/form", methods=["GET","POST"])
def recommend_survey_form():
    return render_template("recommend_survey_form.html")

#C-auto recommend page
@app.route("/recommend/auto", methods=["GET","POST"])
def recommend_auto():
    return render_template("recommend_auto.html")

#C-laptop(all)
@app.route("/laptop", methods=["GET","POST"])
def laptop():
    return render_template("laptop.html")

#C-laptop/search result(include filter)
@app.route("/laptop/search", methods=["GET","POST"])
def laptop_filter():
    return render_template("laptop_search.html")

#C-laptop/detail
@app.route("/laptop/<product_id>", methods=["GET","POST"])
def laptop_detail():
    return render_template("laptop_detail.html")

#C-cart(all)
@app.route("/cart", methods=["GET","POST"])
def cart():
    return render_template("cart.html")

#C-cart/checkout(choose payment method,address)
@app.route("/cart/checkout", methods=["GET","POST"])
def cart_checkout():
    return render_template("cart_checkout.html")

#C-cart/payment
@app.route("/cart/payment", methods=["GET","POST"])
def cart_payment():
    return render_template("cart_payment.html")

#C-cart/payment success
@app.route("/cart/payment/success", methods=["GET","POST"])
def cart_payment_success():
    return render_template("cart_payment_success.html")

#C-cart/payment failed
@app.route("/cart/payment/failed", methods=["GET","POST"])
def cart_payment_failed():
    return render_template("cart_payment_failed.html")

#Admin section (Ying Xin)
#A-home page
@app.route("/admin/homepage", methods=["GET","POST"])
def admin_homepage():
    return render_template("admin_homepage.html")

#A-laptop
@app.route("/admin/laptop", methods=["GET","POST"])
def admin_laptop():
    return render_template("admin_laptop.html")

#A-laptop/edit laptop
@app.route("/admin/laptop/edit", methods=["GET","POST"])
def admin_laptop_edit():
    return render_template("admin_laptop_edit.html")

#A-laptop/detail
@app.route("/admin/laptop/detail", methods=["GET","POST"])
def admin_laptop_detail():
    return render_template("admin_laptop_detail.html")

#A-feedback(view+reply)
@app.route("/admin/feedback/user", methods=["GET","POST"])
def admin_feedback_user():
    return render_template("admin_feedback_user.html")

#A-feedback/send feedback
@app.route("/admin/feedback/send", methods=["GET","POST"])
def admin_feedback_send():
    return render_template("admin_feedback_send.html")

#A-orders
@app.route("/admin/orders", methods=["GET","POST"])
def admin_orders():
    return render_template("admin_orders.html")

#Manager section (Zhi Xian)
#M-home page
@app.route("/manager/homepage", methods=["GET","POST"])
def manager_homepage():
    return render_template("manager_homepage.html")

#M-laptop
@app.route("/manager/laptop", methods=["GET","POST"])
def manager_laptop():
    return render_template("manager_laptop.html")

#M-laptop/detail
@app.route("/manager/laptop/detail", methods=["GET","POST"])
def manager_laptop_detail():
    return render_template("manager_laptop_detail.html")

#M-view account
@app.route("/manager/account", methods=["GET","POST"])
def manager_account():
    return render_template("manager_account.html")

#M-view account/add new account
@app.route("/manager/account/new", methods=["GET","POST"])
def manager_account_new():
    return render_template("manager_account_new.html")

#M-reports/daily
@app.route("/manager/reports/daily", methods=["GET","POST"])
def manager_reports_daily():
    return render_template("manager_reports_daily.html")

#M-reports/weekly
@app.route("/manager/reports/weekly", methods=["GET","POST"])
def manager_reports_weekly():
    return render_template("manager_reports_weekly.html")

#M-reports/monthly
@app.route("/manager/reports/monthly", methods=["GET","POST"])
def manager_reports_monthly():
    return render_template("manager_reports_monthly.html")

#M-reports/yearly
@app.route("/manager/reports/yearly", methods=["GET","POST"])
def manager_reports_yearly():
    return render_template("manager_reports_yearly.html")

#M-feedbacks
@app.route("/manager/feedback", methods=["GET","POST"])
def manager_feedback():
    return render_template("manager_feedback.html")

if __name__=='__main__':
    app.run(debug=True)