from flask import Flask, render_template, request, session, flash, redirect, url_for, make_response
from flask_mysqldb import MySQL
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import boto3
from datetime import datetime, timezone, timedelta
import os
import MySQLdb
from urllib.parse import urlparse
import re

app= Flask(__name__)

db=yaml.load(open('db.yaml'), Loader=yaml.FullLoader) #database configuration
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
app.secret_key = db["secret_key"]


mysql = MySQL(app)

S3= boto3.client('s3') #AWS S3 credentials and bucket configuration
S3_BUCKET = 'sourc-wk-sdp-project' 
S3_LOCATION = 'https://sourc-wk-sdp-project.s3.amazonaws.com/User+Profile+Picture/'

#login for all (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form['action'] == 'login':
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
                    flash("Password incorrect.")
            else:
                flash("User not found.")
            cur.close()
        elif request.form['action'] == 'forgot_password':
            return redirect("/forgot_password")
    return render_template("login.html")

#register (flash message left)
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
        if len(password) < 8 and len(password) > 20:
            flash("Password must be between 8 and 20 characters.", "danger")
            cur.close()
            return redirect("/register")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            flash("Password must between 8 and 20 characters, and contain at least one letter, one number, and one special character.", "danger")
            cur.close()
            return redirect("/register")
        if not phone.isdigit() and len(phone) != 10:
            flash("Phone number must be 10 digits only.", "danger")
            cur.close()
            return redirect("/register")

        cur.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NULL)",(username,password,name,email,phone,dob,address,occupation))
        mysql.connection.commit()
        flash("Register Successful.")
        cur.close()
        return redirect("/")
    return render_template("register.html")

#forgot password (DONE)-----------------------------------------------------------------------------------------------------------------
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
            flash("Username or email incorrect. Please try again.")
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

#reset password (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    token = request.args.get("token")
    if request.method == 'GET':
        error, email = verify_token(token)
        if error:
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
        if len(password) < 8 and len(password) > 20:
            flash("Password must be between 8 and 20 characters.")
            return redirect("/reset_password")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            flash("Password must contain at least one letter, one number, and one special character.")
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

#staff login (html left)
@app.route("/staff/login", methods=["GET","POST"])
def staff_login():
    if request.method == "POST":
        userdata=request.form
        staff_id=userdata["stf_id"]
        staff_psw=userdata["stf_psw"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT stf_id, stf_psw, stf_role FROM staff WHERE stf_id=%s AND status=1",(staff_id,)) 

        if value>0:
            data=cur.fetchone()
            passw=data[1]
            role=data[2]
            if staff_psw==passw:
                if role=="Manager":
                    session["logged_in"]=True
                    session["staff_id"]=staff_id
                    session["role"]=role
                    flash("Login Successful","success")
                    return redirect("/manager/homepage")
                elif role=="Admin":
                    session["logged_in"]=True
                    session["staff_id"]=staff_id
                    session["role"]=role
                    flash("Login Successful","success")
<<<<<<< HEAD
                    return redirect("/admin/laptop")
=======
                    return redirect("/admin/homepage")
>>>>>>> manager
            else:
                flash("Password incorrect.")
        else:
            flash("User not found.")
        cur.close()
    return render_template("staff_login.html")

#staff forgot password
@app.route("/staff/forgot_password", methods=["GET", "POST"])
def staff_forgot_password():
    if request.method == "POST":
        print("Received POST request for forgot password.")
        userdata = request.form
        staff_id = userdata["stf_id"]
        email = userdata["stf_email"]
        cur = mysql.connection.cursor()
        print(f"Looking for staff ID: {staff_id} and email: {email}")
        value = cur.execute("SELECT stf_id, stf_email FROM staff WHERE stf_id=%s AND stf_email=%s", (staff_id, email))

        if value > 0:
            print("Staff ID and email found in the database.")
            try:
                token = generate_token(email)
                reset_link = f"http://localhost:5000/staff/reset_password?token={token}"
                print(f"Generated reset link: {reset_link}")
                
                # Set up the SMTP server
                server = smtplib.SMTP('smtp-mail.outlook.com', 587)
                server.starttls()
                print("SMTP server connection established.")
                server.login('laptopkawkaw@outlook.com', 'kawkawlaptop123')
                print("Logged in to SMTP server.")

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = 'laptopkawkaw@outlook.com'
                msg['To'] = email
                msg['Subject'] = "Staff Password Reset"
                body = f"Here is your staff password reset link: {reset_link}"
                msg.attach(MIMEText(body, 'plain'))
                print("Email prepared for sending.")

                # Send the email
                server.send_message(msg)
                del msg  # Clean up
                print("Password reset email sent.")
                
                flash("Password reset link has been sent to your email.")
            except Exception as e:
                flash("An error occurred while sending the email.")
                print(f"Error occurred: {e}")  # For debugging purposes
            finally:
                server.quit()
                print("SMTP server connection closed.")
        else:
            print("Staff ID or email not found in the database.")
            flash("Staff ID or email incorrect. Please try again.")
        cur.close()
    return render_template("staff_forgot_password.html")

#staff reset password
@app.route("/staff/reset_password", methods=["GET", "POST"])
def staff_reset_password():
    token = request.args.get("token")
    print(f"Received token: {token}")
    if request.method == 'GET':
        print("Processing GET request for password reset.")
        error, email = verify_token(token)
        if error:
            print("Token verification failed.")
            return render_template("staff_reset_password.html")
        cur = mysql.connection.cursor()
        cur.execute("SELECT stf_id FROM staff WHERE stf_email=%s", (email,))
        staff = cur.fetchone()
        if staff:
            print(f"Email {email} found in database, associated with staff ID: {staff[0]}")
            session['staff_id_for_password_reset'] = staff[0]
            return render_template("staff_reset_password.html", email=email)
    elif request.method == "POST":
        print("Processing POST request for password reset.")
        userdata = request.form
        password = userdata["password"]
        confirm_password = userdata["confirm_password"]
        staff_id = userdata["staff_id"]
        session_staff_id = session.get('staff_id_for_password_reset')
        
        if not session_staff_id or staff_id != session_staff_id:
            print("Staff ID mismatch or session expired.")
            flash("Staff ID incorrect, please try again.")
            return redirect("/staff/reset_password")
        if len(password) < 8 or len(password) > 20:
            print("Password length validation failed.")
            flash("Password must be between 8 and 20 characters.")
            return redirect("/staff/reset_password")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            print("Password complexity validation failed.")
            flash("Password must contain at least one letter, one number, and one special character.")
            return redirect("/staff/reset_password")
        
        if password != confirm_password:
            print("Password and confirm password do not match.")
            flash("Passwords do not match. Please try again.")
            return render_template("staff_reset_password.html")
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE staff SET stf_psw=%s WHERE stf_id=%s", (password, staff_id))
        mysql.connection.commit()
        print(f"Password updated for staff ID: {staff_id}")
        flash("Password reset successful.")
        cur.close()
        session.pop('staff_id_for_password_reset', None)
        return redirect("/staff/login")
    return render_template("staff_reset_password.html")

#Client Section (Timi)
#C-home page (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        #Search bar
        if request.method == 'POST':
            search_query = request.form['query']
            session['homepage_search_query'] = search_query
            return redirect("/laptop")
        
        # Fetch top 3 recommended laptops with their first picture and score
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT p.product_id, p.product_name, p.price, r.score, pic.pic_url, p.status
            FROM recommendation r
            JOIN product p ON r.product_id = p.product_id
            LEFT JOIN (
                SELECT product_id, MIN(pic_url) as pic_url
                FROM product_pic
                GROUP BY product_id
            ) pic ON p.product_id = pic.product_id
            WHERE r.username = %s and p.status = 1
            ORDER BY r.score DESC 
            LIMIT 3
        """, (session.get('username'),))
        top_recommendations = cur.fetchall()

        # Check if recommendations are empty
        if not top_recommendations:
            return redirect('/recommend')

        cur.close()

    return render_template('homepage.html', top_recommendations=top_recommendations)

#C-setting/profile (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/user/setting/profile", methods=["GET","POST"])
def setting_profile():
    if 'logged_in' in session:
        username = session["username"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password, name, email, phone, dob, address, occupation, prof_pic FROM user WHERE username = %s", (username,))
        profile_data = cur.fetchone()
        cur.close()

        if profile_data:
            profile = {
                'username': profile_data[0],
                'password': profile_data[1],
                'name': profile_data[2],
                'email': profile_data[3],
                'phone': profile_data[4],
                'dob': profile_data[5],
                'address': profile_data[6],
                'occupation': profile_data[7],
                'profile_pic': profile_data[8]
            }
            # Pass the profile data to the template to view
            timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
            response = make_response(render_template('setting_profile.html', profile=profile,timestamp=timestamp))
        else:
            flash("User not found.", "danger")
            response = make_response(render_template('setting_profile.html', profile=None))
        
        response.headers['Cache-Control'] = 'no-store'
        return response
    
    else:
        flash("Please log in to view this page.", "warning")
        return render_template('login.html')

#C-setting/profile/edit profile (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/user/setting/profile/edit", methods=["GET","POST"])
def edit_profile():
    current_username = session["username"]

    if request.method == "POST":
        # Handle update action
        new_username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        phone = request.form.get('phone', '')  # Optional fields can use .get to avoid KeyError
        dob = request.form.get('dob', '')
        address = request.form.get('address', '')
        occupation = request.form.get('occupation', '')
        profile_pic_url = None

        # Handle profile picture upload
        if 'profile_pic' in request.files and request.files['profile_pic'].filename != '':
            profile_pic = request.files['profile_pic']

            object_name = f"User Profile Picture/{new_username}"
            try:
                profile_pic_url = upload_file_to_s3(profile_pic, S3_BUCKET, object_name)
            except Exception as e:
                flash("Failed to upload profile picture. Please try again.", "danger")
                return redirect("/user/setting/profile/edit")
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT prof_pic FROM user WHERE username = %s", (current_username,))
            profile_pic_url = cur.fetchone()[0]
            cur.close()

        # Check if the updated username conflicts with existing usernames
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM user WHERE username = %s", (new_username,))
        existing_user = cur.fetchone()
        if existing_user and existing_user[0] != current_username: 
            flash(f"Username '{new_username}' already exists. Please choose a different username.", "danger")
            cur.close() 
            return redirect("/user/setting/profile/edit")

        # Validate input lengths
        if len(new_username) > 30:
            flash("Username must be 30 characters or fewer.", "danger")
            return redirect("/user/setting/profile/edit")
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password):
            flash("Use 8 or more characters with a mix of capital letters, small letters, numbers and symbols for password.", "danger")
            cur.close()
            return redirect("/user/setting/profile/edit")
        if len(name) > 30:
            flash("Name must be 30 characters or fewer.", "danger")
            return redirect("/user/setting/profile/edit")
        if len(email) > 30:
            flash("Email must be 30 characters or fewer.", "danger")
            return redirect("/user/setting/profile/edit")
        if len(phone) !=10 or not phone.isdigit():
            flash("Phone number must be 10 digits only.", "danger")
            return redirect("/user/setting/profile/edit")
        # No need to check 'dob' as it's a date field and will always follow the date format
        if len(address) > 255:
            flash("Address must be 255 characters or fewer.", "danger")
            return redirect("/user/setting/profile/edit")
        if len(occupation) > 30:
            flash("Occupation must be 30 characters or fewer.", "danger")
            return redirect("/user/setting/profile/edit")

        # Update query for the user table
        query = """
        UPDATE user 
        SET username = %s, password = %s, name = %s, email = %s, phone = %s, dob = %s, address = %s, occupation = %s, prof_pic = %s
        WHERE username = %s
        """
        data = (new_username, password, name, email, phone, dob, address, occupation, profile_pic_url, current_username)

        cur.execute(query, data)
        mysql.connection.commit()
        flash("Profile updated successfully", "success")
        cur.close()

        # Update session username if it was changed
        if new_username != current_username:
            session['username'] = new_username
        return redirect("/user/setting/profile")

    cur = mysql.connection.cursor()
    # Selecting user information to pre-fill the form
    cur.execute("SELECT name, username, dob, email, password, phone, occupation, address, prof_pic FROM user WHERE username = %s", (current_username,))
    profile_data = cur.fetchone()
    cur.close()

    if profile_data:
        # Pass the profile data to the template to pre-fill the form
        profile = {
            'name': profile_data[0],
            'username': profile_data[1],
            'dob': profile_data[2],
            'email': profile_data[3],
            'password': profile_data[4],
            'phone': profile_data[5],
            'occupation': profile_data[6],
            'address': profile_data[7],
            'profile_pic': profile_data[8]
        }
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        response = make_response(render_template('edit_profile.html', profile=profile,timestamp=timestamp))
    else:
        flash("User not found.", "danger")
        return redirect("/user/setting/profile")
    response.headers['Cache-Control'] = 'no-store'
    return response

def upload_file_to_s3(file_obj, bucket_name, object_name):
    s3_client = boto3.client('s3')

    try:
        print(f"Uploading file: {object_name}")
        s3_client.upload_fileobj(file_obj, bucket_name, object_name)
        
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        print(f"File uploaded successfully: {object_url}")
        return object_url
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return None

#C-setting/payment method (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/user/setting/payment", methods=["GET", "POST"])
def setting_payment():

    username = session.get('username')

    cur = mysql.connection.cursor()
    
    cur.execute("SELECT saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date FROM payment WHERE username = %s AND status = 1", [username])
    payment_data = cur.fetchall()

    payment_methods = []

    if payment_data:
        for row in payment_data:
            payment_method = {
                'saved_card_id': row[0],
                'username': row[1],
                'pay_email': row[2],
                'name_on_card': row[3],
                'card_no': row[4],
                'cvv': row[5],
                'expiry_date': row[6]
            }
            payment_methods.append(payment_method)
        
        # Pass the payment methods data to the template to view
        if payment_methods:
            return render_template('setting_payment_detail.html', payment_methods=payment_methods)
        else:
            flash("No payment methods found for the user.", "danger")
            return redirect("/user/setting/payment")
    
    return render_template("setting_payment_detail.html", payment_methods=payment_methods)

#C-setting/payment method/edit (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route('/user/setting/payment/edit', methods=['GET','POST'])
def setting_payment_edit():
    current_username = session.get('username')
    saved_card_id = generate_next_saved_card_id()
    
    # Retrieve previous URL from session
    previous_url = session.get('previous_url', None)

             
    # Initialize errors dictionary
    errors = {
        "pay_email": False,
        "name_on_card": False,
        "card_no_format": False,
        "cvv": False,
        "expiry_date": False,
        "card_no_exists": False
    }
    
    if request.method == "POST":
        action = request.form.get('action')
        
        if action == "add":
            cur = mysql.connection.cursor()

            pay_email = request.form.get('pay_email', '')
            name_on_card = request.form.get('name_on_card', '')
            card_no = request.form.get('card_no', '').replace(" ", "")  # Remove spaces from card number
            cvv = request.form.get('cvv', '')
            expiry_date = request.form.get('expiry_date', '')

            # Input validation
            errors["pay_email"] = "Invalid email address." if not is_valid_email(pay_email) else None
            errors["name_on_card"] = "This field is required." if not name_on_card.strip() else None
            errors["card_no_format"] = "Card number must be 16 digits." if not is_valid_card_number(card_no) else None
            errors["cvv"] = "CVV must be 3 digits." if not is_valid_cvv(cvv) else None
            errors["expiry_date"] = "Invalid expiry date." if not is_valid_expiry_date(expiry_date) else None

            # If there are any errors, render the template with errors
            if any(errors.values()):
                return render_template("setting_payment_edit.html", errors=errors, form_data=request.form)
            
            # Check if card number already exists
            if card_exists(card_no):
                errors["card_no_exists"] = "Card number already exists."
                flash("This card number is already in use.", "danger")
                return render_template("setting_payment_edit.html", errors=errors, form_data=request.form)

            # Proceed with the database insert if all fields are valid
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO payment (saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (saved_card_id, current_username, pay_email, name_on_card, card_no, cvv, expiry_date, 1))
            mysql.connection.commit()
            cur.close()

            flash("Payment method added successfully.", "success")

            # Redirect based on previous URL or fallback
            if previous_url:
                session.pop('previous_url', None)  # Clear the session after use
                return redirect(previous_url)
            else:
                return redirect("/user/setting/payment")

        elif action == "remove":
            saved_card_id = request.form.get('saved_card_id')
            cur = mysql.connection.cursor()
            
            # Update the status to 0 instead of deleting the record
            cur.execute("UPDATE payment SET status = 0 WHERE saved_card_id = %s AND username = %s", (saved_card_id, current_username))
            
            mysql.connection.commit()
            flash("Payment method removed successfully.", "success")
            cur.close()
            
            return redirect("/user/setting/payment")
        
        else:
            flash("Invalid action.", "danger")
    
    # Render template with errors initialized
    return render_template("setting_payment_edit.html", errors=errors)

@app.route('/store_previous_url', methods=['POST'])
def store_previous_url():
    previous_url = request.form.get('previous_url')
    session['previous_url'] = previous_url
    return '', 204  # Return no content

def card_exists(card_no):
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM payment WHERE card_no = %s AND status = 1", [card_no])
    exists = cur.fetchone()[0] > 0
    cur.close()
    return exists

def generate_next_saved_card_id(): #generate next saved card id
    cur = mysql.connection.cursor()
    cur.execute("SELECT saved_card_id FROM payment ORDER BY saved_card_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is PC000X
        new_num = last_num + 1
        new_id = f"PC{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with PC0001
        new_id = "PC0001"
    return new_id

def is_valid_email(email):
    return "@" in email and "." in email.split('@')[-1]

def is_valid_card_number(card_number):
    return card_number.isdigit() and len(card_number) == 16

def is_valid_cvv(cvv):
    return cvv.isdigit() and len(cvv) == 3

def is_valid_expiry_date(expiry_date):
    if len(expiry_date) == 5 and expiry_date[2] == '/':
        month, year = expiry_date.split('/')
        return month.isdigit() and year.isdigit() and 1 <= int(month) <= 12
    return False

#C-setting/history(default purchase) (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/user/setting/history/purchase", methods=["GET","POST"])
def setting_history_purchase():
    username = session.get("username")
    
    cur = mysql.connection.cursor()

    if request.method == "POST":
        # Handle review submission
        product_id = request.form.get("product_id")
        order_id = request.form.get("order_id")
        review_text = request.form.get("review")
        rating = int(request.form.get("rating"))
        current_time = datetime.now()
        reply = None

        # Check if review already exists
        cur.execute("""
            SELECT review_id FROM review
            WHERE product_id = %s AND username = %s AND order_id = %s
        """, (product_id, username, order_id))
        existing_review = cur.fetchone()

        if existing_review:
            flash("You have already reviewed this product.", "warning")
        else:
            review_id = generate_next_review_id()
            # Save review and rating to the database
            cur.execute("""
                INSERT INTO review (review_id, order_id, product_id, username, review, rating, review_time, reply)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (review_id, order_id, product_id, username, review_text, rating, current_time, reply))
            mysql.connection.commit()
            flash("Review submitted successfully.", "success")

        cur.close()
        return redirect("/user/setting/history/purchase")

    try:
        # Retrieve purchase history with product images
        query = """
        SELECT p.order_id, p.product_id, p.pur_date, p.pur_amount, p.pur_status, p.pur_quantity,
               (SELECT pic_url FROM product_pic pic WHERE pic.product_id = p.product_id LIMIT 1) AS pic_url,
               (SELECT product_name FROM product prod WHERE prod.product_id = p.product_id) AS product_name
        FROM purchase p
        WHERE p.username = %s
        ORDER BY p.pur_date DESC
        """
        cur.execute(query, (username,))
        purchase_history = cur.fetchall()

        # Initialize the dictionary for existing reviews
        existing_reviews = {}
        for row in purchase_history:
            order_id, product_id, pur_date, pur_amount, pur_status, pur_quantity, pic_url, product_name = row
            cur.execute("""
                SELECT review_id, review, rating, reply FROM review
                WHERE product_id = %s AND username = %s AND order_id = %s
            """, (product_id, username, order_id))
            review = cur.fetchone()
            if review:
                existing_reviews[(order_id, product_id)] = {
                    "review_id": review[0],
                    "review": review[1],
                    "rating": review[2],
                    "reply": review[3]
                }
        cur.close()

        # Organize purchase history by order_id
        orders = {}
        for row in purchase_history:
            order_id, product_id, pur_date, pur_amount, pur_status, pur_quantity, pic_url, product_name = row
            if order_id not in orders:
                orders[order_id] = {
                    'date': pur_date,
                    'status': pur_status,
                    'products': []
                }
            orders[order_id]['products'].append({
                'product_id': product_id,
                'name': product_name,
                'amount': pur_amount,
                'quantity': pur_quantity,
                'pic_url': pic_url
            })

        
        if not purchase_history:
            return render_template("setting_history_purchase.html", purchase_history=[], message="No purchase history available.")
        else:
            return render_template('setting_history_purchase.html', orders=orders, existing_reviews=existing_reviews)

    
    except Exception as e:
        cur.close()
        # Handle the exception and possibly log it
        print(f"An error occurred: {e}")
        flash("An error occurred while retrieving purchase history. Please try again later.", "error")
        return redirect("/user/setting/history/purchase")

def generate_next_review_id(): #generate review id
    cur = mysql.connection.cursor()
    # Assuming 'saved_card_id' is stored in a table named 'saved_cards'
    cur.execute("SELECT review_id FROM review ORDER BY review_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is PC000X
        new_num = last_num + 1
        new_id = f"RV{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with PC0001
        new_id = "RV0001"
    return new_id

def mask_username(username): # Function to mask the username
    if len(username) <= 1:
        return '*'  # If the role_id is 1 character or fewer, show the first character
    elif len(username) == 2:
        return username[0] + '*'  # If the role_id is 2 characters, show the first character and mask the second
    else:
        return username[0] + '*' * (len(username) - 2) + username[-1]  # Mask all characters except first and last

#C-setting/history/search history (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/user/setting/history/search", methods=["GET","POST"])
def setting_history_search():
    username = session.get('username')

    try:
        cur = mysql.connection.cursor()
        query = "SELECT search_id, search_query, search_time FROM search_history WHERE username = %s ORDER BY search_time DESC"
        cur.execute(query, (username,))
        search_history = cur.fetchall()
        cur.close()

        return render_template('setting_search_history.html', search_history=search_history)
    except Exception as e:
        flash(f"Failed to retrieve search history: {str(e)}", "danger")
        return redirect('/')
    
def generate_next_search_id(): #generate search_id
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT search_id FROM search_history ORDER BY search_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is SC000X
        new_num = last_num + 1
        new_id = f"SC{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with SC0001
        new_id = "SC0001"
    return new_id

#C-recommend options (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    if not session.get('logged_in'):
        return redirect('/login')
    
    if request.method == 'POST':
        choice = request.form.get('recommendation_option')
        if choice == 'auto':
            return redirect('/recommend/auto')
        elif choice == 'survey':
            return redirect('/recommend/survey/form')
    
    return render_template('recommend.html')
    
#C-survey/fill in survey (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/recommend/survey/form", methods=["GET","POST"])
def survey_form():
    if request.method == "POST":    
        
        df = fetch_data()

        df["combined_features"] = df.apply(combine_features, axis=1)

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"])

        # Computing the cosine similarity based on the count matrix
        cosine_sim = cosine_similarity(count_matrix)

        data = request.form
        specs = get_specs_from_survey(data)
        combined_query = combine_features(pd.Series(specs))


        recommendations = get_recommendations(combined_query, cosine_sim, df)

        if not recommendations:
            flash("No similar laptops found.")
            return redirect("/homepage")
        
        username = session.get('username') 
        save_recommendations_to_db(username, recommendations)

        # Redirect to homepage after saving recommendations
        return redirect("/homepage")

    else:
        # Show the survey form
        return render_template('survey.html')

def fetch_data():
    cur=mysql.connection.cursor()
    query = """
    SELECT 
        product_id, product_name, brand, processor, graphics, 
        dimensions, weight, os, memory, storage, 
        power_supply, battery, price, status
    FROM product
    WHERE status = 1
    """
    cur.execute(query)
    data= cur.fetchall()
    cur.close()

    # Convert the list of tuples to a DataFrame
    df = pd.DataFrame(data, columns=[
        'Product ID', 'Product Name', 'Brand', 'Processor', 'Graphics', 
        'Dimensions', 'Weight (g)', 'Operating System', 'Memory', 'Storage', 
        'Power Supply', 'Battery', 'Price (MYR)', 'Status'
    ])

    return df
    
# Function to combine features
def combine_features(row):
    return (
        row['Brand'] + " " +
        row['Processor'] + " " +
        row['Graphics'] + " " +
        row['Dimensions'] + " " +
        row['Operating System'] + " " +
        row['Memory'] + " " +
        row['Storage'] + " " +
        row['Power Supply'] + " " +
        row['Battery']
    )

def classify_laptop(processor, graphics, memory, storage, battery, weight):
    # Determine the performance tier based on processor
    if 'i7' in processor or 'i9' in processor or 'Ryzen 7' in processor or 'Ryzen 9' in processor:
        cpu_tier = 'high-end'
    elif 'i5' in processor or 'Ryzen 5' in processor:
        cpu_tier = 'mid-tier'
    else:
        cpu_tier = 'low-end'

    # Determine the performance tier based on graphics
    if 'RTX' in graphics and any(num in graphics for num in ['3000', '4000']):
        gpu_tier = 'high-end'
    elif 'GTX' in graphics or 'RTX 2000' in graphics:
        gpu_tier = 'mid-tier'
    else:
        gpu_tier = 'low-end'

    # Determine the performance tier based on memory
    if memory >= 16:
        memory_tier = 'high-end'
    elif memory == 8:
        memory_tier = 'mid-tier'
    else:
        memory_tier = 'low-end'

    # Determine the performance tier based on storage
    if storage >= 1024:
        storage_tier = 'high-end'
    elif storage == 512:
        storage_tier = 'mid-tier'
    else:
        storage_tier = 'low-end'

    # Determine the performance tier based on battery
    if battery >= 70:
        battery_tier = 'high-end'
    elif battery >= 50:
        battery_tier = 'mid-tier'
    else:
        battery_tier = 'low-end'

    # Determine the portability based on weight
    if weight < 1500:
        weight_class = 'portable'
    elif weight <= 2500:
        weight_class = 'standard'
    else:
        weight_class = 'heavy'

    return {
        'cpu_tier': cpu_tier,
        'gpu_tier': gpu_tier,
        'memory_tier': memory_tier,
        'storage_tier': storage_tier,
        'battery_tier': battery_tier,
    
        'weight_class': weight_class
    }

def get_specs_from_survey(data):
    specs = {
        'Brand': '',
        'Processor': '',
        'Graphics': '',
        'Dimensions': '',
        'Operating System': '',
        'Memory': '',
        'Storage': '',
        'Power Supply': '',
        'Battery': ''
    }

    if data['primary_use'] == 'general-use':
        specs.update({'Processor': 'i3', 'Graphics': 'Integrated', 'Memory': '4GB'})
    
    elif data['primary_use'] == 'education':
        if data.get('education_activities') == 'writing':
            specs.update({'Processor': 'i3', 'Graphics': 'Integrated', 'Memory': '4GB'})
        elif data.get('education_activities') == 'programming':
            if data.get('high-performance') == 'yes':
                specs.update({'Processor': 'i7', 'Graphics': 'GTX 1660', 'Memory': '16GB'})
            else:
                specs.update({'Processor': 'i5', 'Graphics': 'Integrated', 'Memory': '8GB'})
        elif data.get('education_activities') == 'design':
            if data.get('high-performance') == 'yes':
                specs.update({'Processor': 'i7', 'Graphics': 'RTX 2060', 'Memory': '16GB'})
            else:
                specs.update({'Processor': 'i5', 'Graphics': 'GTX 1050', 'Memory': '8GB'})
    
    elif data['primary_use'] == 'gaming':
        if data.get('gaming_type') == 'high-end':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 3080', 'Memory': '16GB'})
        elif data.get('gaming_type') == 'mid-tier':
            specs.update({'Processor': 'i5', 'Graphics': 'GTX 1660', 'Memory': '8GB'})
        else:
            specs.update({'Processor': 'i3', 'Graphics': 'Intel HD', 'Memory': '4GB'})
    
    elif data['primary_use'] == 'professional-work':
        if data.get('professional_work') == 'graphic-design':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 2060', 'Memory': '16GB'})
        elif data.get('professional_work') == 'programming':
            specs.update({'Processor': 'i5', 'Graphics': 'Integrated', 'Memory': '8GB'})
        elif data.get('professional_work') == 'video-editing':
            specs.update({'Processor': 'i7', 'Graphics': 'RTX 3080', 'Memory': '32GB'})
    
    if data['brand'] != 'no-preference':
        specs['Brand'] = data['brand']
    
    if data['os'] != 'no-preference':
        specs['Operating System'] = data['os']
    
    if data['price'] == 'budget':
        specs['Price (MYR)'] = '<500'
    elif data['price'] == 'mid-range':
        specs['Price (MYR)'] = '500-1000'
    elif data['price'] == 'high-end':
        specs['Price (MYR)'] = '1000-2000'
    elif data['price'] == 'premium':
        specs['Price (MYR)'] = '>2000'
    
    return specs

def get_recommendations(combined_query, cosine_sim, df):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])

    query_vec = cv.transform([combined_query])
    query_sim = cosine_similarity(query_vec, count_matrix)

    # Get the indices of the most similar products
    similar_laptops = list(enumerate(query_sim[0]))
    similar_laptops = sorted(similar_laptops, key=lambda x: x[1], reverse=True)
    
    # Normalize similarity scores to a range of 1 to 100
    min_sim = min(similarity for index, similarity in similar_laptops)
    max_sim = max(similarity for index, similarity in similar_laptops)
    
    # Ensure no division by zero
    if max_sim == min_sim:
        normalized_scores = [(index, 100) for index, _ in similar_laptops]
    else:
        normalized_scores = [
            (index, 1 + 99 * (similarity - min_sim) / (max_sim - min_sim))
            for index, similarity in similar_laptops
        ]
    
    # Collect top laptop IDs and their normalized similarity scores
    recommendations = []
    for idx, score in normalized_scores:
        product_id = df.iloc[idx]['Product ID']
        recommendations.append((product_id, round(score)))  # Round the score for better readability

    return recommendations

def get_categories():
    # Define categories and associated keywords
    categories = {
        'Productivity': ['onedrive', 'keynote', 'onenote', 'microsoft word', 'microsoft excel', 'microsoft powerpoint', 'calendar', 'numbers', 'pages', 'draw.io', 'canva', 'apspace'],
        'Media': ['audacity', 'ffmpeg', 'media player', 'photo viewer', 'imovie', 'garageband', 'bandicam'],
        'Development': ['visual studio code', 'netbeans', 'azure data studio', 'git', 'obs-studio', 'mysqlworkbench', 'swi-prolog', 'docker', 'rapidminer studio'],
        'Utilities': ['teams', 'bonjour', 'windows defender', 'windows mail', 'putty', 'hp', 'wsl', '7-zip', 'dotnet', 'faceit', 'nzxt cam', 'streamlabs', 'testproject', 'winpcap'],
        'Games': ['game', 'launcher', 'hoyoplay', 'steam', 'wildgames', 'riot vanguard', 'easyanticheat'],
        'Other': []
    }
    return categories

#C-auto recommend page (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/recommend/auto", methods=["GET","POST"])
def recommend_auto():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'accept':
            # User accepted the privacy policy
            if 'accept_policy_checkbox' not in request.form:
                flash('You must accept the privacy policy to proceed.', 'warning')
                return redirect('/recommend/auto')

            # Process auto-recommendations
            categories = get_categories()
            program_files_dirs = [
                r"C:\Program Files",
                r"C:\Program Files (x86)"
            ]
            
            categorized_apps = {category: 0 for category in categories}
            categorized_apps['Other'] = 0
            
            for directory in program_files_dirs:
                if os.path.exists(directory):
                    apps_in_dir = detect_top_level_apps(directory)
                    for app in apps_in_dir:
                        category = categorize_app(app, categories)
                        categorized_apps[category] += 1
            
            recommendations = recommend_laptops(categorized_apps)
            
            username = session.get('username')
            try:
                save_recommendations_to_db(username, recommendations)
            except Exception as e:
                flash(f"Failed to save recommendations: {str(e)}", "danger")
                return redirect('/homepage')
            
            return redirect(url_for('homepage'))

        elif action == 'reject':
            # User rejected the privacy policy
            flash('You have rejected the privacy policy. Returning to recommendations page.', 'warning')
            return redirect('/recommend')

    # Render the page to accept privacy policy
    return render_template('accept_policy.html')

def detect_top_level_apps(directory):
    apps = []
    
    try:
        for entry in os.listdir(directory):
            subdir_path = os.path.join(directory, entry)
            
            if os.path.isdir(subdir_path):
                try:
                    for file in os.listdir(subdir_path):
                        if file.endswith('.exe'):
                            apps.append(os.path.join(subdir_path, file))
                            break
                except (PermissionError, OSError):
                    print(f"Permission denied or OS error for {subdir_path}. Skipping.")
                
    except (PermissionError, OSError):
        print(f"Permission denied or OS error for {directory}. Skipping.")
    return apps

def categorize_app(app,categories):
    # Define categories and associated keywords
    for category, apps in categories.items():
        if app.lower() in apps:
            return category
    return 'Other'

def get_laptops_from_db():

    cur=mysql.connection.cursor()
    query = """
        SELECT 
            product_id, product_name, brand, processor, graphics, 
            dimensions, weight, os, memory, storage, 
            power_supply, battery, price, status
        FROM product
        WHERE status = 1
        GROUP BY product_id
    """
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    
    return data

def recommend_laptops(category_counts):

    categories=get_categories()
    laptops = get_laptops_from_db()
    
    category_priority = {
        'Productivity': 5,
        'Media': 4,
        'Development': 3,
        'Utilities': 2,
        'Games': 1,
        'Other': 0
    }
    
    recommendations = []
    
    for laptop in laptops:
        basic_score = sum(category_counts.get(category, 0) * category_priority.get(category, 0) for category in categories)
        score_adjustment = 0
        if 'gaming' in laptop[1].lower():
            score_adjustment += 10  
        if 'productivity' in laptop[1].lower():
            score_adjustment += 5 
        
        price = laptop[12]
        normalized_price = max(1, price / 1000)  
        final_score = basic_score + score_adjustment - normalized_price
        
        recommendations.append((laptop[0], final_score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Normalize the scores between 1 and 100
    if recommendations:
        max_score = recommendations[0][1]
        min_score = recommendations[-1][1]
        score_range = max_score - min_score

        for i in range(len(recommendations)):
            normalized_score = ((recommendations[i][1] - min_score) / score_range) * 99 + 1
            recommendations[i] = (recommendations[i][0], normalized_score)
        return recommendations
    else:
        print("No recommendations found.")
        recommendations=[]
        return recommendations

def save_recommendations_to_db(username,recommendations):
    if not recommendations:
        print("No recommendations to save.")
        return

    # Prepare the insert/update query
    print(f"Recommendations: {recommendations}")
    upsert_query = """
    INSERT INTO recommendation (username, product_id, score)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE score = VALUES(score)
    """
    
    values = [(username, product_id, score) for product_id, score in recommendations]
    
    try:
        cur = mysql.connection.cursor()
        cur.executemany(upsert_query, values)
        mysql.connection.commit()
        flash("Recommendation Success.", "success")
    except Exception as e:
        mysql.connection.rollback()
        raise e
    finally:
        cur.close()

#C-laptop (display all laptop + search result + filter) (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/laptop", methods=["GET","POST"])
def laptop():
    username = session.get('username')

    # Clear filters if the button is clicked
    if request.args.get('clear_filters'):
        session.pop('homepage_search_query', None)
        return redirect('/laptop')

    # Retrieve the search query from session or request args
    search_query = session.get('homepage_search_query', request.args.get('search', ''))

    # Check if any filters are applied; if yes, clear the session search query
    if any([
        request.args.get('brand'),
        request.args.get('min_price'),
        request.args.get('max_price'),
        request.args.get('memory'),
        request.args.get('graphics'),
        request.args.get('storage'),
        request.args.get('battery'),
        request.args.get('processor'),
        request.args.get('os'),
        request.args.get('min_weight'),
        request.args.get('max_weight'),
        request.args.get('score')
    ]):
        session.pop('homepage_search_query', None)  # Clear session search query

    # Retrieve the search query from the request args if session query was cleared
    search_query = request.args.get('search', search_query)

        
    brand = request.args.get('brand', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    memory = request.args.get('memory', '')
    graphics = request.args.get('graphics', '')
    storage = request.args.get('storage', '')
    battery = request.args.get('battery', '')
    processor = request.args.get('processor', '')
    os = request.args.get('os', '')
    min_weight = request.args.get('min_weight', '')
    max_weight = request.args.get('max_weight', '')
    sort_by_score = request.args.get('sort_by_score','')


    # Generate a unique search_id
    search_id = generate_next_search_id()

    # Record the search history
    # Ensure search_query is not empty before saving to the database
    if search_query:
        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO search_history (search_id, username, search_query, search_time) VALUES (%s, %s, %s, %s)",
                        (search_id, username, search_query, datetime.now()))
            mysql.connection.commit()
            cur.close()
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Failed to save search query: {str(e)}", "danger")


    # Fetch laptops and their first picture from the database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT p.product_id, p.product_name, p.brand, p.price, p.memory, p.graphics, p.storage, p.battery, p.processor, p.os, p.weight, p.status, pic.pic_url, r.score
        FROM product p
        LEFT JOIN (
            SELECT product_id, MIN(pic_url) as pic_url
            FROM product_pic
            GROUP BY product_id
        ) pic ON p.product_id = pic.product_id
        LEFT JOIN recommendation r ON p.product_id = r.product_id
        AND r.username = %s
        WHERE p.status = 1
    """, (username,))
    all_laptops = cur.fetchall()

    # Fetch distinct values for each filter option
    cur.execute("SELECT DISTINCT brand FROM product")
    brands = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT memory FROM product")
    memories = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT graphics FROM product")
    graphics_options = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT storage FROM product")
    storages = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT battery FROM product")
    batteries = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT processor FROM product")
    processors = [row[0] for row in cur.fetchall()]

    cur.execute("SELECT DISTINCT os FROM product")
    operating_systems = [row[0] for row in cur.fetchall()]

    # Fetch min and max price from the database
    cur.execute("SELECT MIN(price), MAX(price) FROM product")
    min_price_db, max_price_db = cur.fetchone()

    # Fetch min and max weight from the database
    cur.execute("SELECT MIN(weight), MAX(weight) FROM product")
    min_weight_db, max_weight_db = cur.fetchone()

    # Validate user input for price and weight range
    if min_price and max_price and float(min_price) > float(max_price):
        message = "Max price must be greater than min price."
        return render_template('laptop.html', message=message)
    if min_weight and max_weight and float(min_weight) > float(max_weight):
        message = "Max weight must be greater than min weight."
        return render_template('laptop.html', message=message)

    # Filter the laptops based on the criteria
    filtered_laptops = [
        laptop for laptop in all_laptops
        if (search_query.lower() in laptop[1].lower() if search_query else True) and
           (not brand or brand.lower() in laptop[2].lower()) and
           (not min_price or laptop[3] >= float(min_price)) and
           (not max_price or laptop[3] <= float(max_price)) and
           (not memory or memory.lower() in laptop[4].lower()) and
           (not graphics or graphics.lower() in laptop[5].lower()) and
           (not storage or storage.lower() in laptop[6].lower()) and
           (not battery or battery in str(laptop[7])) and
           (not processor or processor.lower() in laptop[8].lower()) and
           (not os or os.lower() in laptop[9].lower()) and
           (not min_weight or laptop[10] >= float(min_weight)) and
           (not max_weight or laptop[10] <= float(max_weight))
    ]

    # Fetch user-specific recommendations if logged in
    user_recommendation_dict = {}
    if username:
        cur.execute("""
            SELECT product_id, score
            FROM recommendation
            WHERE username = %s
        """, (username,))
        user_recommendations = cur.fetchall()
        user_recommendation_dict = {product_id: score for product_id, score in user_recommendations}

    # Integrate user-specific scores if the user is logged in
    if username:
        for i, laptop in enumerate(filtered_laptops):
            product_id = laptop[0]
            filtered_laptops[i] = laptop + (user_recommendation_dict.get(product_id, 0),)

    # Sort the laptops by score if the filter is applied
    if sort_by_score == 'on' and username:
        filtered_laptops.sort(key=lambda x: x[-1] if x[-1] is not None else float('-inf'), reverse=True)  # Descending


    message = None

    if not filtered_laptops:
        message = "No laptops found matching the criteria."

    return render_template('laptop_search.html', laptops=filtered_laptops, brands=brands, memories=memories, graphics_options=graphics_options, storages=storages, batteries=batteries, processors=processors, operating_systems=operating_systems, message=message, min_price=min_price_db, max_price=max_price_db, min_weight=min_weight_db, max_weight=max_weight_db)

#C-laptop/detail (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/laptop/<product_id>", methods=["GET","POST"])
def laptop_detail(product_id):
    
    # Clean up the product_id
    product_id = product_id.replace('<', '').replace('>', '').strip()

    if request.method == "POST":
        username = session.get('username')
        if not username:
            return redirect(url_for('login'))  # Redirect to login if user is not logged in

        try:
            quantity = int(request.form.get('quantity', 1))  # Default quantity is 1
        except ValueError:
            quantity = 1  # Fallback to default if conversion fails

        action = request.form['action']

        with mysql.connection.cursor() as cur:
            try:
                # Check if the same username and product_id exist in the cart
                cur.execute("SELECT quantity FROM cart WHERE username = %s AND product_id = %s", (username, product_id))
                existing_row = cur.fetchone()
                
                if existing_row:
                    # Update the existing row with the new quantity
                    new_quantity = existing_row[0] + quantity
                    cur.execute("UPDATE cart SET quantity = %s WHERE username = %s AND product_id = %s", (new_quantity, username, product_id))
                else:
                    # Insert a new row
                    cur.execute("INSERT INTO cart (username, product_id, quantity) VALUES (%s, %s, %s)", (username, product_id, quantity))
                
                mysql.connection.commit()

                if action == 'add_to_cart':
                    flash('Product added to cart.', 'success')
                    return redirect(url_for('cart'))  # Redirect to cart page
                elif action == 'buy_now':
                    flash('Product added to cart. Redirecting to checkout...', 'success')
                    # Set selected items in session
                    session['selected_items'] = [(product_id, quantity)]
                    session['selected_total_price'] = 0
                    return redirect(url_for('cart_checkout'))  # Redirect to checkout page

            except MySQLdb.Error as e:
                mysql.connection.rollback()
                print(f"Error inserting into cart: {e}")
                flash(f'Error: {str(e)}', 'danger')

    # Fetch laptop details
    with mysql.connection.cursor() as cur:
        cur.execute("""
            SELECT *
            FROM product
            WHERE product_id = %s
        """, (product_id,))
        product = cur.fetchone()

        if not product:
            return render_template("laptop_detail.html", message="Laptop not found.", product_details={})
        
        # Check product status
        if product[14] == 0: 
            return render_template("laptop_detail.html", message="Sorry, the laptop is unavailable now.", product_details={})


        # Fetch laptop images
        cur.execute("SELECT pic_url FROM product_pic WHERE product_id = %s", (product_id,))
        images = cur.fetchall()
        

        # Fetch reviews for the product based on product_id
        cur.execute("""
            SELECT product_id, username, review, rating, review_time, reply
            FROM review 
            WHERE product_id = %s
        """, (product_id,))
        reviews = cur.fetchall()

        reviews_list = []


    # Process and mask the role_id for each review
    for row in reviews:
        masked_username = mask_username(row[1])
        review_data = {
            'username': masked_username,
            'review': row[2],
            'rating': row[3],
            'date': row[4]
        }
        if row[5] is not None:  # Only add the 'reply' field if it is not None
            review_data['reply'] = row[5]
        
        reviews_list.append(review_data)

    # Close cursor after fetching data
    cur.close()

    stock_status = "In Stock" if product[13] > 0 else "Out of Stock"

    product_details = {
        'product_id': product[0],
        'product_name': product[1],
        'brand': product[2],
        'processor': product[3],
        'graphics': product[4],
        'dimensions': product[5],
        'weight': product[6],
        'os': product[7],
        'memory': product[8],
        'storage': product[9],
        'power_supply': product[10],
        'battery': product[11],
        'price': product[12],
        'stock_status': stock_status,
        'images': [image[0] for image in images],
        'reviews': reviews_list,
        'status': product[14]
    }

    # Pass laptop_details to the template
    return render_template("laptop_detail.html", product_details=product_details)

#C-cart(all) (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/cart", methods=["GET","POST"])
def cart():
    username = session.get('username')
    cart_items = []
    cart_total_price = 0

    if request.method == "POST":
        action = request.form.get('action')
        print("Form Data:", request.form)  # Debugging print


        if action == "update":
            for key, value in request.form.items():
                if key.startswith('quantity_'):
                    product_id = key.split('_')[1]
                    print(f"Updating {product_id} to quantity {value}")
                    try:
                        quantity = int(value)
                        if quantity > 0:
                            with mysql.connection.cursor() as cur:
                                # Check stock before updating
                                cur.execute("""
                                    SELECT stock
                                    FROM product
                                    WHERE product_id = %s
                                """, (product_id,))
                                stock = cur.fetchone()[0]

                                if quantity <= stock:
                                    cur.execute("""
                                        UPDATE cart
                                        SET quantity = %s
                                        WHERE username = %s AND product_id = %s
                                    """, (quantity, username, product_id))
                                    mysql.connection.commit()
                                else:
                                    flash(f"Quantity for product {product_id} exceeds available stock.", 'error')
                    except ValueError:
                        print(f"Invalid quantity for {product_id}: {value}")


        elif 'remove_product' in request.form:
            product_id = request.form.get('remove_product')
            with mysql.connection.cursor() as cur:
                cur.execute("""
                    DELETE FROM cart
                    WHERE username = %s AND product_id = %s
                """, (username, product_id))
                mysql.connection.commit()
                flash('Product removed from cart.', 'success')

        elif action == 'checkout':
            # Extract selected items from form data
            selected_items = [key.split('_')[1] for key in request.form if key.startswith('select')]
            print("Selected items for checkout:", selected_items)  # Debug print

            if not selected_items:
                flash('No items selected for checkout.', 'warning')
                return redirect(url_for('cart'))

            # Fetch cart items for selected product IDs
            cart_items = []
            with mysql.connection.cursor() as cur:
                for product_id in selected_items:
                    cur.execute("""
                        SELECT 
                            p.product_id, 
                            p.product_name, 
                            p.price, 
                            c.quantity,
                            (SELECT pic_url FROM product_pic pp WHERE pp.product_id = p.product_id LIMIT 1) AS pic_url,
                            p.status
                        FROM cart c
                        JOIN product p ON c.product_id = p.product_id
                        WHERE c.username = %s AND c.product_id = %s
                    """, (username, product_id))
                    item = cur.fetchone()
                    
                    # Check if product is available (status = 1)
                    if item:
                        if item[5] == 0:
                            flash(f"Sorry, the product '{item[1]}' is currently unavailable.", 'error')
                        cart_items.append(item)

            print("Fetched cart items:", cart_items)  # Debug print

           # Calculate the total price of selected items
            cart_total_price = 0
            for item in cart_items:
                price = float(item[2])
                quantity = int(item[3])
                total_item_price = price * quantity
                cart_total_price += total_item_price
                print(f"Item: {item[1]}, Price: {price}, Quantity: {quantity}, Total: {total_item_price}")

            print("Calculated total price:", cart_total_price)  # Debug print

            # Store session data for checkout
            session['selected_items'] = [(item[0], item[3]) for item in cart_items]  # Storing (product_id, quantity)
            session['checkout_total_price'] = cart_total_price

            # Perform stock check before proceeding
            with mysql.connection.cursor() as cur:
                stock_check_failed = False
                for product_id, quantity in session['selected_items']:
                    cur.execute("""
                        SELECT quantity
                        FROM cart
                        WHERE username = %s AND product_id = %s
                    """, (username, product_id))
                    quantity_in_cart = cur.fetchone()[0]

                    cur.execute("""
                        SELECT stock
                        FROM product
                        WHERE product_id = %s
                    """, (product_id,))
                    stock = cur.fetchone()[0]

                    if quantity_in_cart > stock:
                        flash(f"Quantity for product {product_id} exceeds available stock.", 'error')
                        stock_check_failed = True

                if stock_check_failed:
                    return redirect(url_for('cart'))  # Redirect to the cart page if stock validation fails

            return redirect(url_for('cart_checkout'))  # Redirect to the checkout page if stock validation passes

    # Re-fetch cart items to render updated cart
    with mysql.connection.cursor() as cur:
        cur.execute("""
            SELECT 
                c.product_id, 
                p.product_name, 
                p.price, 
                c.quantity, 
                (SELECT pic_url FROM product_pic pp WHERE pp.product_id = c.product_id LIMIT 1) AS pic_url,
                (SELECT stock FROM product p WHERE p.product_id = c.product_id) AS stock,
                p.status
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.username = %s
        """, (username,))
        cart_items = cur.fetchall()
    
    # Check for unavailable products in the cart
    for item in cart_items:
        if item[6] == 0:  # Assuming status is the 7th column (index 6)
            flash(f"Sorry, the product '{item[1]}' is currently unavailable.", 'error')


    item_count = len(cart_items)
    cart_total_price = sum(item[2] * item[3] for item in cart_items if f'select_{item[0]}' in request.form)

    return render_template("cart.html", cart_items=cart_items, cart_total_price=cart_total_price, item_count=item_count)

#C-cart/checkout(choose payment method,address) (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/cart/checkout", methods=["GET","POST"])
def cart_checkout():
    username = session.get('username')
    errors = {}
    selected_items = session.get('selected_items', [])
    checkout_total_price = 0
    selected_items_details = []

    if request.method == "POST":
        order_id = generate_next_order_id()
        ship_id = generate_next_ship_id()
        saved_card_id = request.form.get('payment_method')
        return_url = request.form.get('return_url', url_for('cart_checkout'))  # Default to current page if not provided

        if saved_card_id == 'new':
            # Store the current URL to the session
            session['previous_url'] = url_for('cart_checkout')
            # Redirect to the payment settings page
            return redirect(url_for('setting_payment_edit', return_url=return_url))
        else:
            # Handle payment method selection and checkout process
            pass

        # Calculate the total price for the selected items
        with mysql.connection.cursor() as cur:
            for product_id, quantity in selected_items:
                cur.execute("""
                    SELECT price
                    FROM product
                    WHERE product_id = %s
                """, (product_id,))
                result = cur.fetchone()
                if result:
                    price = result[0]
                    checkout_total_price += price * quantity


        for product_id, quantity in selected_items:
            try:
                with mysql.connection.cursor() as cur:
                    # Fetch the quantity in the cart for this product
                    cur.execute("""
                        SELECT quantity
                        FROM cart
                        WHERE username = %s AND product_id = %s
                    """, (username, product_id))
                    result = cur.fetchone()

                    if result:
                        quantity_in_cart = result[0]

                        # Validate the quantity in the cart
                        if quantity_in_cart != quantity:
                            flash(f"Quantity for product {product_id} in cart does not match the selected quantity.", 'error')
                            return redirect(url_for('cart'))

                        # Insert into the purchase table
                        query = """
                            INSERT INTO purchase 
                            (order_id, username, product_id, pur_date, pur_amount, pur_status, pur_quantity, processed_by, saved_card_id)
                            VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s)
                        """
                        params = (order_id, username, product_id, checkout_total_price, 'pending', quantity, None, saved_card_id)
                        cur.execute(query, params)
                        
                        # Update stock
                        query = """
                            UPDATE product
                            SET stock = stock - %s
                            WHERE product_id = %s
                        """
                        cur.execute(query, (quantity, product_id))
                        
                    else:
                        flash(f"Product {product_id} not found in the cart.", 'error')
                        return redirect(url_for('cart'))
                    
                mysql.connection.commit()
                print(f"Order {order_id} successfully inserted into purchase table.")
            except Exception as e:
                print(f"Error processing product {product_id}: {e}")
                mysql.connection.rollback()
                return "Error processing purchase"
        
        session['order_id'] = order_id

        # Shipping details validation
        dest_add = request.form.get('dest_add', '')
        receiver_name = request.form.get('receiver_name', '')
        receiver_phone = request.form.get('receiver_phone', '')

        errors.update({
            "dest_add": not (dest_add and dest_add.strip()),
            "receiver_name": not (receiver_name and receiver_name.strip()),
            "receiver_phone": not (receiver_phone and receiver_phone.strip())
        })

        if any(errors.values()):
            print(f"Validation errors: {errors}")
            return render_template("cart_checkout.html", errors=errors, form_data=request.form, selected_items=selected_items, checkout_total_price=checkout_total_price)

        try:
            with mysql.connection.cursor() as cur:
                cur.execute("""
                    INSERT INTO shipping (ship_id, order_id, dest_add, receiver_name, receiver_phone, ship_status, ship_time)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (ship_id, order_id, dest_add, receiver_name, receiver_phone, 'pending'))
                mysql.connection.commit()
        except Exception as e:
            print(f"Error inserting into shipping table: {e}")
            mysql.connection.rollback()
            return "Error processing shipping details"

        # Remove items from cart
        try:
            with mysql.connection.cursor() as cur:
                # Generate placeholders for the number of selected items
                format_strings = ','.join(['%s'] * len(selected_items))
                # Extract product IDs from selected_items
                product_ids = [item[0] for item in selected_items]
                
                # Prepare and execute the delete statement
                cur.execute(f"""
                    DELETE FROM cart
                    WHERE username = %s AND product_id IN ({format_strings})
                """, (username, *product_ids))
                
                mysql.connection.commit()
        except Exception as e:
            print(f"Error removing items from cart: {e}")
            mysql.connection.rollback()
            return "Error removing items from cart"

        session.pop('buy_now', None)
        session.pop('selected_items', None)
        flash("Checkout successful!", "success")
        return redirect(url_for("cart_payment_success", order_id=order_id))

    # Retrieve current payment methods
    payment_methods = []
    try:
        with mysql.connection.cursor() as cur:
            cur.execute("""
                SELECT saved_card_id, card_no, expiry_date, pay_email
                FROM payment
                WHERE username = %s and status = 1
            """, (username,))
            payment_methods = cur.fetchall()
            print("Payment methods retrieved:", payment_methods)
    except Exception as e:
        print(f"Error fetching payment methods: {e}")

    # Fetch details for selected items
    if selected_items:
        with mysql.connection.cursor() as cur:
            for product_id, quantity in selected_items:
                query = """
                    SELECT 
                        p.product_id, 
                        p.product_name, 
                        p.price, 
                        pp.pic_url
                    FROM product p
                    LEFT JOIN product_pic pp ON pp.product_id = p.product_id
                    WHERE p.product_id = %s
                    LIMIT 1
                """
                
                try:
                    cur.execute(query, (product_id,))
                    fetched_item = cur.fetchone()
                    if fetched_item:
                        # Ensure fetched_item has the correct number of elements
                        if len(fetched_item) == 4:
                            product_id, product_name, price, pic_url = fetched_item
                            selected_items_details.append((product_id, product_name, float(price), quantity, pic_url))
                            checkout_total_price += float(price) * quantity
                        else:
                            print(f"Unexpected number of values in fetched_item: {fetched_item}")
                    else:
                        print(f"No item found for product_id: {product_id}")
                except Exception as e:
                    print(f"Error fetching details for product {product_id}: {e}")

    session['checkout_total_price'] = checkout_total_price

    print("Selected Items Details:", selected_items_details)
    print("Checkout Total Price:", checkout_total_price)

    return render_template("cart_checkout.html", payment_methods=payment_methods, errors=errors, form_data=request.form, selected_items=selected_items_details, checkout_total_price=checkout_total_price)

def generate_next_ship_id(): #generate ship_id
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT ship_id FROM shipping ORDER BY ship_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is SH000X
        new_num = last_num + 1
        new_id = f"SH{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with SH0001
        new_id = "SH0001"
    return new_id

def generate_next_order_id(): #generate order_id
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT order_id FROM purchase ORDER BY order_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is IN000X
        new_num = last_num + 1
        new_id = f"IN{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with IN0001
        new_id = "IN0001"
    return new_id

def get_product_price(product_id):
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT price FROM product WHERE product_id = %s", (product_id,))
        result = cur.fetchone()
        return result[0] if result else 0
    
def get_payment_methods(username):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM payment WHERE username = %s", (username,))
    payment_methods = cur.fetchall()
    cur.close()
    return payment_methods

def get_cart_quantity(username, product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT quantity FROM cart WHERE username = %s AND product_id = %s", (username, product_id))
    result = cur.fetchone()
    cur.close()
    return result[0] if result else 0

#C-cart/payment success (DONE)-----------------------------------------------------------------------------------------------------------------
@app.route("/cart/payment/success", methods=["GET","POST"])
def cart_payment_success():
    order_id = request.args.get('order_id') or session.get('order_id')
    if not order_id:
        return "No order ID found.", 400

    try:
        with mysql.connection.cursor() as cur:
            # Fetch order summary
            cur.execute("""
                SELECT 
                    MAX(pu.pur_date) AS order_date,
                    MAX(s.dest_add) AS shipping_address,
                    MAX(s.receiver_name) AS receiver_name,
                    MAX(s.receiver_phone) AS receiver_phone,
                    SUM(p.price * pu.pur_quantity) AS total_amount
                FROM purchase pu
                JOIN product p ON pu.product_id = p.product_id
                JOIN shipping s ON pu.order_id = s.order_id
                WHERE pu.order_id = %s
                GROUP BY pu.order_id
            """, (order_id,))
            order_summary = cur.fetchone()

            if not order_summary:
                return "Order details not found.", 404

            order_date, shipping_address, receiver_name, receiver_phone, total_amount = order_summary

            # Fetch order details
            cur.execute("""
                SELECT 
                    p.product_name, 
                    p.price, 
                    pu.pur_quantity AS quantity, 
                    (p.price * pu.pur_quantity) AS total
                FROM purchase pu
                JOIN product p ON pu.product_id = p.product_id
                WHERE pu.order_id = %s
            """, (order_id,))
            invoice_details = cur.fetchall()

            # Fetch payment method details
            cur.execute("""
                SELECT 
                    pm.card_no, 
                    pm.expiry_date, 
                    pm.pay_email
                FROM payment pm
                JOIN purchase pu ON pm.saved_card_id = pu.saved_card_id
                WHERE pu.order_id = %s
                LIMIT 1
            """, (order_id,))
            payment_method = cur.fetchone()

            if not payment_method:
                card_no, expiry_date, pay_email = "N/A", "N/A", "N/A"
            else:
                card_no, expiry_date, pay_email = payment_method

    except Exception as e:
        print(f"Error fetching invoice details: {e}")
        return "Error fetching invoice details.", 500

    return render_template("cart_payment_success.html", 
                           order_id=order_id, 
                           order_date=order_date,
                           shipping_address=shipping_address,
                           receiver_name=receiver_name,
                           receiver_phone=receiver_phone,
                           invoice_details=invoice_details,
                           total_amount=total_amount,
                           card_no=card_no,
                           expiry_date=expiry_date,
                           pay_email=pay_email)

#Admin section (Zhi Xian)
#A-homepage(laptop mainpage)
@app.route('/admin/laptop', methods=['GET', 'POST'])
def admin_laptop():
    if not session.get('logged_in'):
        return redirect('/staff/login')
    
    search_query = ''
    if request.method == 'POST':
        if request.form.get('action') == 'search':
            search_query = request.form.get('query', '')
            session['admin_homepage_search_query'] = search_query
            return redirect(f"/admin/laptop?search={search_query}")

    # Default to the search query from the URL if no POST data
    search_query = request.args.get('search', search_query)
    
    sql_query = """
    SELECT p.product_id, p.product_name, p.brand, p.price, p.memory, p.graphics, p.storage, p.battery, p.processor, p.os, p.weight, pic.pic_url, p.stock, p.status
    FROM product p
    LEFT JOIN (
        SELECT product_id, MIN(pic_url) as pic_url
        FROM product_pic
        GROUP BY product_id
    ) pic ON p.product_id = pic.product_id
    WHERE (p.product_name LIKE %s OR p.brand LIKE %s OR p.processor LIKE %s)
    """

    search_term = f'%{search_query}%'
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (search_term, search_term, search_term))
    all_laptops = cur.fetchall()
    cur.close()

    return render_template('admin_laptop_search.html', laptops=all_laptops, search_query=search_query)

#A-toggle laptop status
@app.route('/admin/laptop/toggle_status/<product_id>', methods=['POST'])
def toggle_status(product_id):
    if not session.get('logged_in'):
        return redirect('/staff/login')

    cur = mysql.connection.cursor()

    # Get the current status of the product
    cur.execute("SELECT status FROM product WHERE product_id = %s", (product_id,))
    current_status = cur.fetchone()[0]  # Accessing the first element of the tuple

    # Toggle the status
    new_status = 0 if current_status == 1 else 1

    # Update the status in the database
    cur.execute("UPDATE product SET status = %s WHERE product_id = %s", (new_status, product_id))
    mysql.connection.commit()

    # Print a confirmation message
    print(f"Product ID {product_id}: Status successfully toggled to {new_status}")

    cur.close()

    return redirect('/admin/laptop')

#A-add-laptops
@app.route("/admin/laptop/add", methods=["GET", "POST"])
def admin_laptop_add():
    if request.method == "POST":
        product_name = request.form.get('product_name')
        brand = request.form.get('brand')
        processor = request.form.get('processor')
        graphics = request.form.get('graphics')
        dimensions = request.form.get('dimensions')
        weight = request.form.get('weight')
        os = request.form.get('os')
        memory = request.form.get('memory')
        storage = request.form.get('storage')
        power_supply = request.form.get('power_supply')
        battery = request.form.get('battery')
        price = request.form.get('price')
        stock = request.form.get('stock')

        cur = mysql.connection.cursor()

        # Get the latest product_id from the database
        cur.execute("SELECT product_id FROM product ORDER BY product_id DESC LIMIT 1")
        latest_id = cur.fetchone()

        # Generate new product_id based on the latest one
        if latest_id:
            latest_id_num = int(latest_id[0][2:])  # Extract the numeric part of the ID
            new_id_num = latest_id_num + 1
            product_id = f"LP{new_id_num:04d}"  # Format as LPxxxx
        else:
            product_id = "LP0001"  # Start with LP0001 if no records exist

        # Insert the new product with the auto-generated product_id
        cur.execute('''INSERT INTO product (product_id, product_name, brand, processor, graphics, dimensions, weight, os, memory, storage, power_supply, battery, price, stock)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                     (product_id, product_name, brand, processor, graphics, dimensions, weight, os, memory, storage, power_supply, battery, price, stock))

        mysql.connection.commit()
        print(f"New laptop added with ID: {product_id}, Name: {product_name}")
        cur.close()

        # Print statement after successful save
        print(f"Laptop successfully added with ID {product_id}.")

        flash(f"Laptop added successfully with ID {product_id}.", "success")
        return redirect(f"/admin/laptop_images/{product_id}")

    return render_template("admin_laptop_add.html")

#A-edit laptop
@app.route("/admin/laptop/edit", methods=["GET", "POST"])
def admin_laptop_edit():
    if request.method == "POST":
        product_id = request.form.get('product_id')
        if product_id:
            cur = mysql.connection.cursor()

            # Fetch existing laptop details
            cur.execute('SELECT * FROM product WHERE product_id = %s', (product_id,))
            laptop = cur.fetchone()

            if laptop:
                column_names = [desc[0] for desc in cur.description]
                laptop_dict = dict(zip(column_names, laptop))

                # Get updated values from form or use existing values
                product_name = request.form.get('product_name') or laptop_dict['product_name']
                brand = request.form.get('brand') or laptop_dict['brand']
                processor = request.form.get('processor') or laptop_dict['processor']
                graphics = request.form.get('graphics') or laptop_dict['graphics']
                dimensions = request.form.get('dimensions') or laptop_dict['dimensions']
                weight = request.form.get('weight') or laptop_dict['weight']
                os = request.form.get('os') or laptop_dict['os']
                memory = request.form.get('memory') or laptop_dict['memory']
                storage = request.form.get('storage') or laptop_dict['storage']
                power_supply = request.form.get('power_supply') or laptop_dict['power_supply']
                battery = request.form.get('battery') or laptop_dict['battery']
                price = request.form.get('price') or laptop_dict['price']
                stock = request.form.get('stock') or laptop_dict['stock']

                # Update product details and stock
                cur.execute('''UPDATE product SET product_name = %s, brand = %s, processor = %s, graphics = %s, dimensions = %s,
                               weight = %s, os = %s, memory = %s, storage = %s, power_supply = %s, battery = %s, price = %s, stock = %s 
                               WHERE product_id = %s''',
                             (product_name, brand, processor, graphics, dimensions, weight, os, memory, storage, power_supply, battery, price, stock, product_id))

                mysql.connection.commit()
                cur.close()

                # Print statement after successful update
                print(f"Laptop with ID {product_id} updated successfully.")

                flash("Laptop details and stock updated successfully.", "success")
                return redirect("/admin/laptop")
            else:
                flash("Laptop not found.", "danger")
                cur.close()
                return render_template("admin_laptop_edit_id.html")
        else:
            flash("Please enter a Product ID.", "danger")
            return render_template("admin_laptop_edit_id.html")
    
    else:  # GET request
        product_id = request.args.get('product_id')
        if product_id:
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM product WHERE product_id = %s', (product_id,))
            laptop = cur.fetchone()

            if laptop:
                column_names = [desc[0] for desc in cur.description]
                laptop_dict = dict(zip(column_names, laptop))
                cur.close()

                return render_template("admin_laptop_edit_form.html", laptop=laptop_dict)
            else:
                flash("Laptop not found.", "danger")
                cur.close()
                return redirect("/admin/laptop")
        else:
            flash("Please provide a Product ID.", "danger")
            return redirect("/admin/laptop")

#A-remove laptop
@app.route("/admin/laptop/remove", methods=["GET", "POST"])
def admin_laptop_remove():
    if request.method == "POST":
        product_id = request.form['product_id']

        # Update the status to 0 instead of deleting the row
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE product SET status = 0 WHERE product_id = %s', (product_id,))
        
        mysql.connection.commit()
        cursor.close()

        # Print statement after successful status update
        print(f"Laptop with ID {product_id} marked as removed (status set to 0).")

        flash("Laptop successfully marked as removed.", "success")
        return redirect("/admin/laptop")

#A-laptop images
@app.route('/admin/laptop_images/<product_id>', methods=['GET', 'POST'])
def laptop_images(product_id):
    if request.method == 'POST':
        # Handle image upload
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            if image_file.filename != '':
                # Define the S3 path
                sql_query = "SELECT product_name FROM product WHERE product_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(sql_query, (product_id,))
                laptop_name = cur.fetchone()[0]
                cur.close()

                object_name = f"New Laptops/{product_id} {laptop_name}/Image-{generate_next_pic_id()}.jpg"
                pic_url = upload_file_to_s3(image_file, S3_BUCKET, object_name)

                if pic_url:
                    # Save the URL in the database
                    pic_id = generate_next_pic_id()
                    sql_insert = """
                    INSERT INTO product_pic (pic_id, product_id, pic_url)
                    VALUES (%s, %s, %s)
                    """
                    cur = mysql.connection.cursor()
                    cur.execute(sql_insert, (pic_id, product_id, pic_url))
                    mysql.connection.commit()
                    cur.close()

                    # Print statement after successful database insert
                    print(f"Image with ID {pic_id} uploaded and saved to database for product ID {product_id}. URL: {pic_url}")

                    flash("Image uploaded successfully.", "success")
                else:
                    flash("Failed to upload image to S3.", "danger")

            return redirect(url_for('laptop_images', product_id=product_id))

        # Handle image deletion
        if 'delete_pic_id' in request.form:
            delete_pic_id = request.form['delete_pic_id']

            # Retrieve pic_url from the database using delete_pic_id
            sql_select = "SELECT pic_url FROM product_pic WHERE pic_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(sql_select, (delete_pic_id,))
            pic_url = cur.fetchone()  # Fetch the pic_url

            if pic_url:  # If the pic_url is found
                pic_url = pic_url[0]  # Extract the URL from the tuple

                # Delete image from S3
                if delete_file_from_s3(pic_url):
                    # Delete image entry from the database
                    sql_delete = "DELETE FROM product_pic WHERE pic_id = %s"
                    cur.execute(sql_delete, (delete_pic_id,))
                    mysql.connection.commit()
                    
                    # Print statement after successful database delete
                    print(f"Image with ID {delete_pic_id} deleted from database and S3. URL: {pic_url}")

                    flash("Image deleted successfully.", "success")
                else:
                    flash("Failed to delete image from S3.", "danger")

            else:
                flash("Image not found.", "error")

            cur.close()

            return redirect(url_for('laptop_images', product_id=product_id))

    # Display existing images
    sql_query = "SELECT pic_id, pic_url FROM product_pic WHERE product_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (product_id,))
    images = cur.fetchall()
    cur.close()

    return render_template('admin_laptop_images.html', product_id=product_id, images=images)

def delete_file_from_s3(pic_url):
    # Parse the URL to get bucket name and object key
    parsed_url = urlparse(pic_url)
    bucket_name = parsed_url.netloc.split('.')[0]
    object_name = parsed_url.path.lstrip('/')

    s3_client = boto3.client('s3')

    try:
        print(f"Deleting file: {object_name} from bucket: {bucket_name}")
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        
        print(f"File deleted successfully: {pic_url}")
        return True
    except Exception as e:
        print(f"Error deleting file from S3: {str(e)}")
        return False

def upload_file_to_s3(file_obj, bucket_name, object_name):
    try:
        print(f"Uploading file: {object_name}")
        S3.upload_fileobj(file_obj, bucket_name, object_name)

        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
        print(f"File uploaded successfully: {object_url}")
        return object_url
    except Exception as e:
        print(f"Error uploading file to S3: {str(e)}")
        return None
    
def generate_next_pic_id(): #generate pic_id
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT pic_id FROM product_pic ORDER BY pic_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is PP000X
        new_num = last_num + 1
        new_id = f"PP{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with PP0001
        new_id = "PP0001"
    return new_id

# A-review(view + reply to client review)
@app.route("/admin/reviews", methods=["GET", "POST"])
def admin_reviews():
    if not session.get("logged_in"):
        return redirect("/login")

    cur = mysql.connection.cursor()

    if request.method == "POST":
        # Handle reply submission
        review_id = request.form.get("review_id")
        reply_text = request.form.get("reply")
        
        try:
            # Update review with the admin's reply
            cur.execute("""
                UPDATE review 
                SET reply = %s 
                WHERE review_id = %s
            """, (reply_text, review_id))
            mysql.connection.commit()

            # Print statement after successful reply update
            print(f"Successfully updated review with ID {review_id}. Admin's reply: {reply_text}")

            flash("Reply sent successfully.", "success")
        except Exception as e:
            print(f"An error occurred while updating review with ID {review_id}: {e}")
            flash("An error occurred while submitting the reply. Please try again.", "error")
        finally:
            cur.close()

        return redirect("/admin/reviews")

    try:
        # Retrieve unreplied reviews only
        query = """
        SELECT review.review_id, review.product_id, review.username, review.review, review.rating, 
               review.review_time, review.reply, product.product_name 
        FROM review 
        JOIN product ON review.product_id = product.product_id
        WHERE review.reply IS NULL
        ORDER BY review.review_time ASC
        """
        cur.execute(query)
        reviews = cur.fetchall()

        # Print statement after successfully retrieving reviews
        print(f"Retrieved {len(reviews)} unreplied reviews.")

        cur.close()

        # Check if any reviews are fetched
        if not reviews:
            flash("All reviews have been replied to.", "info")

        return render_template("admin_reviews.html", reviews=reviews)

    except Exception as e:
        cur.close()
        print(f"An error occurred while retrieving reviews: {e}")
        flash("An error occurred while retrieving reviews. Please try again later.", "error")
        return redirect("/admin/laptop")

#A-send feedback to manager
@app.route("/admin/feedback/send", methods=["GET", "POST"])
def admin_feedback_send():
    if not session.get('logged_in'):
        return redirect('/login')

    staff_id = session.get('staff_id')

    if request.method == "POST":
        feedback_text = request.form.get('feedback')
        feedback_time = datetime.now()

        if staff_id is None:
            flash("Error: Staff ID is not set.", "error")
            return redirect("/admin/feedback/send")

        # Generate a new feedback_id based on the last one
        cur = mysql.connection.cursor()
        cur.execute("SELECT MAX(feedback_id) FROM feedback")
        result = cur.fetchone()

        last_id = result[0] if result[0] is not None else 'FB0000'
        last_number = int(last_id[2:])  # Get the numeric part and convert to integer
        next_number = last_number + 1
        feedback_id = f'FB{next_number:04d}'  # Format as F#### with leading zeros

        try:
            # Insert feedback into the database
            cur.execute("""
                INSERT INTO feedback (feedback_id, stf_id, feedback, feedback_time) 
                VALUES (%s, %s, %s, %s)
            """, (feedback_id, staff_id, feedback_text, feedback_time))
            mysql.connection.commit()
            
            # Print statement after successful database insert
            print(f"Feedback inserted successfully. ID: {feedback_id}, Staff ID: {staff_id}, Feedback: {feedback_text}")

            flash("Feedback sent successfully.", "success")
        except Exception as e:
            print(f"An error occurred while inserting feedback: {e}")
            flash("An error occurred while sending feedback. Please try again.", "error")
        finally:
            cur.close()

        return redirect("/admin/feedback/send")

    return render_template("admin_feedback_send.html")

def generate_next_feedback_id(): #generate feedback_id
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT feedback_id FROM feedback ORDER BY feedback_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is FB000X
        new_num = last_num + 1
        new_id = f"FB{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with FB0001
        new_id = "FB0001"
    return new_id

#A-Manage orders
@app.route("/admin/orders", methods=["GET", "POST"])
def admin_orders():
    if not session.get('logged_in'):
        return redirect('/login')

<<<<<<< HEAD
    cur = mysql.connection.cursor()

    # Handle order status update
    if request.method == "POST":
        order_id = request.form.get('order_id')
        action = request.form.get('action')  # Expecting "complete" or "cancel"
        staff_id = session.get('staff_id')  # Get staff_id from session
        print(f"Staff {staff_id} attempting to update order: {order_id} to {action}")

        # Determine the new status based on the action
        new_status = "completed" if action == "complete" else "cancelled"

        try:
            # Update the order status and set the staff_id in the processed_by column
            cur.execute("""
                UPDATE purchase
                SET pur_status = %s, processed_by = %s
                WHERE order_id = %s
            """, (new_status, staff_id, order_id))

            mysql.connection.commit()
            print(f"Order {order_id} successfully updated to {new_status} by staff {staff_id}.")
            flash(f"Order {order_id} has been marked as {new_status}.", "success")
        except Exception as e:
            print(f"An error occurred while updating order {order_id}: {e}")
            mysql.connection.rollback()
            flash("An error occurred while updating the order. Please try again.", "error")
        finally:
            cur.close()
        return redirect("/admin/orders")

    try:
        query = """
        SELECT 
            p.order_id, p.username, p.pur_date, p.pur_amount, p.pur_status, 
            s.dest_add, s.receiver_name, s.receiver_phone, s.ship_status, s.ship_time
        FROM purchase p
        LEFT JOIN shipping s ON p.order_id = s.order_id
        WHERE p.pur_status = 'pending'
        ORDER BY p.pur_date ASC
        """
        cur.execute(query)
        orders = cur.fetchall()
        
        # Print statement after successfully retrieving orders
        print(f"Retrieved {len(orders)} pending orders from the database.")

        cur.close()
        return render_template("admin_orders.html", orders=orders)
    
    except Exception as e:
        cur.close()
        print(f"An error occurred while retrieving orders: {e}")
        flash("An error occurred while retrieving orders. Please try again later.", "error")
        return redirect("/admin/orders")

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    debug_mode = False
else:
    debug_mode = True

app.run(debug=debug_mode)
=======
#Manager section (Ying Xin)
#M-home page (browser and view laptop)
@app.route("/manager/homepage", methods=["GET", "POST"])
def manager_homepage():
    if not session.get('logged_in'):
        return redirect('/staff/login')
    
    search_query = ''
    if request.method == 'POST':
        if request.form.get('action') == 'search':
            print("Search button clicked")
            search_query = request.form.get('query')
            print(f"Search query: {search_query}")
            session['manager_homepage_search_query'] = search_query
            return redirect(f"/manager/homepage?search={search_query}")

    # Default to the search query from the URL if no POST data
    search_query = request.args.get('search', search_query)
    
    sql_query = """
    SELECT p.product_id, p.product_name, p.brand, p.price, p.memory, p.graphics, p.storage, p.battery, p.processor, p.os, p.weight, pic.pic_url, p.stock, p.status
    FROM product p
    LEFT JOIN (
        SELECT product_id, MIN(pic_url) as pic_url
        FROM product_pic
        GROUP BY product_id
    ) pic ON p.product_id = pic.product_id
    WHERE (p.product_name LIKE %s OR p.brand LIKE %s OR p.processor LIKE %s)
    """

    search_term = f'%{search_query}%'
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (search_term, search_term, search_term))
    all_laptops = cur.fetchall()
    cur.close()

    return render_template('manager_homepage.html', laptops=all_laptops, search_query=search_query)
    

#M-manage account
@app.route("/manager/account", methods=["GET","POST"])
def manager_account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT stf_id, stf_name, stf_role, status FROM staff WHERE stf_role='admin'")
    staff= cur.fetchall()
    cur.close()

    staff = [
        {'stf_id': row[0], 'stf_name': row[1], 'stf_role': row[2], 'status': row[3]}
        for row in staff
    ]

    #add button
    if request.method == "POST":
        action = request.form.get("action")
        stf_id = request.form.get("stf_id")
        print(stf_id) 
        if action == "activate":
            return redirect(url_for("manager_account_remove", action=action, stf_id=stf_id))
        elif action == "deactivate":
            return redirect(url_for("manager_account_remove", action=action, stf_id=stf_id))

    return render_template("manager_account.html",staff=staff)
    
#M-view account
@app.route("/manager/account/detail/<string:stf_id>", methods=["GET", "POST"])
def manager_view_account(stf_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE stf_id = %s AND status=1", (stf_id,))
    admin = cur.fetchone()
    cur.close()

    admin = {
        'stf_id': admin[0],
        'stf_name': admin[2],
        'stf_email': admin[3],
        'stf_phone': admin[4],
        'stf_dob': admin[5],
        'stf_address': admin[6],
        'stf_emer_contact': admin[7],
        'stf_role': admin[8],
    }

    if request.method == "POST":
        action = request.form("action")
        #edit button
        if action == "edit":
            return redirect ("/manager/account/edit")
        #back button
        if action == "Back to Manage Accounts":
            return redirect ("/manager/account")

    return render_template("manager_view_account.html", admin=admin)
    
#M-add new account
def generate_stf_id():
    cur = mysql.connection.cursor()
    # Assuming 'saved_card_id' is stored in a table named 'saved_cards'
    cur.execute("SELECT stf_id FROM staff ORDER BY stf_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is SF000X
        new_num = last_num + 1
        new_id = f"SF{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with SF0001
        new_id = "SF0001"
    return new_id

@app.route("/manager/account/new", methods=["GET","POST"])
def manager_account_new():
    if request.method == "POST":
        staffdata = request.form
        stf_id = generate_stf_id()
        stf_psw = staffdata.get("Password")
        stf_name = staffdata.get("Name")
        stf_email = staffdata.get("Email")
        stf_phone = staffdata.get("Phone")
        stf_dob = staffdata.get("dob")
        stf_address = staffdata.get("Address")
        stf_emer_contact = staffdata.get("Emergency Contact")
        stf_role = staffdata.get("Role")
        
        try: 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO staff (stf_id, stf_psw, stf_name, stf_email, stf_phone, stf_dob, stf_address, stf_emer_contact, stf_role, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (stf_id, stf_psw, stf_name, stf_email, stf_phone, stf_dob, stf_address, stf_emer_contact, stf_role,1))
            mysql.connection.commit()
            cur.close()
            print("Data inserted successfully.")
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            print(f"Error: {e}")
            return "An error occurred, please try again."
        
        return redirect(url_for('manager_account'))
    
    return render_template("manager_account_new.html")

#M-edit account
@app.route("/manager/account/edit/<string:stf_id>", methods=["GET", "POST"])
def manager_account_edit(stf_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE stf_id = %s", (stf_id,))
    admin = cur.fetchone()
    cur.close()

    admin = {
        'stf_id': admin[0],
        'stf_name': admin[2],
        'stf_email': admin[3],
        'stf_phone': admin[4],
        'stf_dob': admin[5],
        'stf_address': admin[6],
        'stf_emer_contact': admin[7],
        'stf_role': admin[8],
    }
    if request.method == "POST":
        editadmin = request.form
        stf_name = editadmin.get("stf_name")
        stf_email = editadmin.get("stf_email")
        stf_phone = editadmin.get("stf_phone")
        stf_dob = editadmin.get("stf_dob")
        stf_address = editadmin.get("stf_address")
        stf_emer_contact = editadmin.get("stf_emer_contact")
        stf_role = editadmin.get("stf_role")

        action = request.form.get("action")
        #done button
        if action == "Done":
            cur = mysql.connection.cursor()
            cur.execute("UPDATE staff SET stf_name = %s, stf_email = %s, stf_phone = %s, stf_dob = %s,stf_address = %s, stf_emer_contact = %s, stf_role = %s WHERE stf_id = %s"
                        ,(stf_name, stf_email, stf_phone, stf_dob, stf_address, stf_emer_contact, stf_role, stf_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('manager_view_account', stf_id=stf_id))
        #cancel button
        elif action == "Cancel":
            return redirect (url_for("manager_view_account",stf_id=stf_id))
    
    return render_template("manager_account_edit.html",admin=admin)

#M-remove account
@app.route("/manager/account/remove", methods=["GET","POST"])
def manager_account_remove():
    if request.method == "GET":
        stf_id = request.args.get("stf_id")
        act=request.args.get("action")
        if act == "activate":
            status = 1
        elif act == "deactivate":
            status = 0
        
    if request.method == "POST":
        action = request.form.get("action")
        sta = request.form.get("status")
        stf_id = request.form.get("stf_id")

        if sta == "activate":
            status = 1
            current_status = 0
        elif sta == "deactivate":
            status = 0
            current_status = 1

        #cancel button
        if action == "Cancel":
            return redirect ("/manager/account")
        #confirm button
        if action == "Confirm":
            cur = mysql.connection.cursor()
            cur.execute("UPDATE staff SET status=%s WHERE stf_id = %s AND status = %s", (status, stf_id, current_status))
            print("Data updated successfully.")
            mysql.connection.commit()
            cur.close()
            return redirect ("/manager/account")
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM staff WHERE stf_id = %s", (stf_id,))
    staff = cur.fetchone()
    cur.close()

    staff = {
        'stf_id': staff[0],
        'stf_name': staff[2],
        'stf_email': staff[3],
        'stf_phone': staff[4],
        'stf_dob': staff[5],
        'stf_address': staff[6],
        'stf_emer_contact': staff[7],
        'stf_role': staff[8]
    }

    return render_template("manager_account_remove.html", staff=staff, action=act)

@app.route("/manager/reports", methods=["GET","POST"])
def manager_reports():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "Daily":
            return redirect("/manager/reports/daily")
        elif action == "Weekly":
            return redirect("/manager/reports/weekly")
        elif action == "Monthly":
            return redirect("/manager/reports/monthly")
        elif action == "Yearly":
            return redirect("/manager/reports/yearly")
    
    update_report_table()
    return render_template("manager_reports.html")

def update_report_table():
    cur = mysql.connection.cursor()

    cur.execute("TRUNCATE TABLE report")  # Clear the report table
    print("Report table cleared.")
    cur.execute("TRUNCATE TABLE user_tracking")  # Clear the user_tracking table
    print("User tracking table cleared.")

    # Initialize the tracking table if it does not have an entry
    cur.execute("INSERT IGNORE INTO user_tracking (id, previous_total_user) VALUES (1, 0)")

    # Get current total number of users
    cur.execute("SELECT COUNT(username) FROM user")
    current_total_user = cur.fetchone()[0]

    # Extract distinct pur_dates from the purchase table
    cur.execute("SELECT DISTINCT DATE(pur_date) FROM purchase")
    dates = cur.fetchall()

    for date_tuple in dates:
        pur_date = date_tuple[0]
        if not pur_date:
            continue

        # Calculate date values
        date_day = pur_date.strftime("%Y-%m-%d")
        start_of_week = pur_date - timedelta(days=pur_date.weekday())
        date_week = start_of_week.strftime("%Y-%m-%d")
        date_month = pur_date.replace(day=1).strftime("%Y-%m-%d")
        date_year = pur_date.replace(month=1, day=1).strftime("%Y-%m-%d")

        # Aggregate sales and product_sold for the specific date
        cur.execute("""
            SELECT SUM(pur_amount), SUM(pur_quantity), product_id, order_id
            FROM purchase
            WHERE DATE(pur_date) = %s
            GROUP BY product_id, order_id
        """, [pur_date])
        purchase_data = cur.fetchall()

        for pur_amount, pur_quantity, product_id, order_id in purchase_data:
            cur.execute("SELECT product_name FROM product WHERE product_id = %s", [product_id])
            product_name = cur.fetchone()[0]

            cur.execute("SELECT COUNT(order_id) FROM purchase WHERE DATE(pur_date) = %s", [pur_date])
            total_orders = cur.fetchone()[0]

            # Get previous total_user from user_tracking table
            cur.execute("SELECT previous_total_user FROM user_tracking WHERE id = 1")
            previous_total_user = cur.fetchone()[0]

            # Calculate new_user based on previous_total_user
            new_user = current_total_user - previous_total_user
            
            # Check if the record already exists in the report table
            cur.execute("SELECT COUNT(*) FROM report WHERE order_id = %s", [order_id])
            if cur.fetchone()[0] == 0:
                # Insert new record if it does not exist
                cur.execute("""
                    INSERT INTO report (order_id, date_day, date_week, date_month, date_year, sales, product_sold, product_id, product_name, total_order, total_user, new_user)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (order_id, date_day, date_week, date_month, date_year, pur_amount, pur_quantity, product_id, product_name, total_orders, current_total_user, new_user))

    # Update the user_tracking table with the new total_user
    cur.execute("UPDATE user_tracking SET previous_total_user = %s WHERE id = 1", (current_total_user,))

    mysql.connection.commit()
    cur.close()

#M-reports/daily
@app.route("/manager/reports/daily", methods=["GET", "POST"])
def manager_reports_daily():
    # Get the date from the form or use today as default
    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    cur = mysql.connection.cursor()
    
    # Fetch the top-selling product for the selected date
    cur.execute("""
        SELECT product_id, 
               product_name, 
               SUM(product_sold) AS total_product_sold
        FROM report
        WHERE date_day = %s
        GROUP BY product_id, product_name
        ORDER BY total_product_sold DESC
        LIMIT 1
    """, (selected_date,))
    
    top_product = cur.fetchone()  # Fetch one record for the top product
    
    # Fetch daily report data for the selected date
    cur.execute("""
        SELECT date_day, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               MAX(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        WHERE date_day = %s
        GROUP BY date_day
    """, (selected_date,))
    
    daily_report = cur.fetchall()

    # Fetch all daily report data for chart
    cur.execute("""
        SELECT date_day, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               MAX(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        GROUP BY date_day
        ORDER BY date_day
    """)
    
    daily_chart = cur.fetchall()
    cur.close()

    return render_template("manager_reports_daily.html", 
                           daily_report=daily_report, 
                           selected_date=selected_date, 
                           top_product=top_product,daily_chart=daily_chart)

#M-reports/weekly
@app.route("/manager/reports/weekly", methods=["GET", "POST"])
def manager_reports_weekly():
    # Get the date from the form or use the start of the current week as default
    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    cur = mysql.connection.cursor()

    # Calculate the start of the week for the selected_date
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    start_of_week = selected_date_obj - timedelta(days=selected_date_obj.weekday())
    date_week = start_of_week.strftime("%Y-%m-%d")

    # Fetch the top 3 selling products for the selected week
    cur.execute("""
        SELECT product_id, 
               product_name, 
               SUM(product_sold) AS total_product_sold
        FROM report
        WHERE date_week = %s
        GROUP BY product_id, product_name
        ORDER BY total_product_sold DESC
        LIMIT 3
    """, (date_week,))
    
    top_product = cur.fetchall()

    # Fetch weekly report data for the selected week
    cur.execute("""
        SELECT date_week, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        WHERE date_week = %s
        GROUP BY date_week
    """, (date_week,))
    
    weekly_report = cur.fetchall()

    # Fetch all weekly report data for chart
    cur.execute("""
        SELECT date_week, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        GROUP BY date_week
        ORDER BY date_week
    """)
    
    weekly_chart = cur.fetchall()
    cur.close()

    return render_template("manager_reports_weekly.html", weekly_report=weekly_report,date_week=date_week,top_product=top_product,weekly_chart=weekly_chart)

#M-reports/monthly
@app.route("/manager/reports/monthly", methods=["GET", "POST"])
def manager_reports_monthly():
    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m")
    print(selected_date)

    if len(selected_date) == 10:  # Format: YYYY-MM-DD
        selected_date = selected_date[:7]  # Extract YYYY-MM
    print(f"Processed Date: {selected_date}")

    cur = mysql.connection.cursor()

    # Calculate the start of the month for the selected_date
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m")
    date_month = selected_date_obj.strftime("%Y-%m-%d")


    # Fetch the top 3 selling products for the selected month
    cur.execute("""
        SELECT product_id, 
               product_name, 
               SUM(product_sold) AS total_product_sold
        FROM report
        WHERE date_month = %s
        GROUP BY product_id, product_name
        ORDER BY total_product_sold DESC
        LIMIT 3
    """, (date_month,))
    
    top_product = cur.fetchall()

    # Fetch monthly report data for the selected month
    cur.execute("""
        SELECT date_month, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        WHERE date_month = %s
        GROUP BY date_month
    """, (date_month,))
    
    monthly_report = cur.fetchall()

    # Fetch all monthly report data for chart
    cur.execute("""
        SELECT DATE_FORMAT(date_month, '%Y/%m') AS formatted_date_month, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        GROUP BY formatted_date_month
        ORDER BY formatted_date_month
    """)
    
    monthly_chart = cur.fetchall()

    # Calculate sales growth
    sales_growth = []
    for i in range(1, len(monthly_chart)):
        current_sales = monthly_chart[i][1]
        previous_sales = monthly_chart[i-1][1]
        growth = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales else None
        sales_growth.append({
            'date_month': monthly_chart[i][0],
            'growth': growth
        })
    
    cur.close()

    # Format the date for display as "Month Year"
    formatted_date_month = selected_date_obj.strftime("%B %Y")

    return render_template("manager_reports_monthly.html", 
                           monthly_report=monthly_report, 
                           date_month=formatted_date_month,
                           top_product=top_product, 
                           monthly_chart=monthly_chart,
                           sales_growth=sales_growth)

#M-reports/yearly
@app.route("/manager/reports/yearly", methods=["GET","POST"])
def manager_reports_yearly():
    current_year = datetime.now().year

    selected_year = request.form.get("year") or datetime.now().strftime("%Y")
    
    cur = mysql.connection.cursor()

    # Set the start and end of the selected year
    selected_date_obj = datetime.strptime(selected_year, "%Y")
    date_year = selected_date_obj.strftime("%Y-%m-%d")
    

    # Fetch the top 3 selling products for the selected year
    cur.execute("""
        SELECT product_id, 
               product_name, 
               SUM(product_sold) AS total_product_sold
        FROM report
        WHERE date_year = %s
        GROUP BY product_id, product_name
        ORDER BY total_product_sold DESC
        LIMIT 3
    """, (date_year,))
    
    top_product = cur.fetchall()

    # Fetch yearly report data for the selected year
    cur.execute("""
        SELECT date_year, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        WHERE date_year = %s
        GROUP BY YEAR(date_year)
    """, (date_year,))
    
    yearly_report = cur.fetchall()

    # Fetch all yearly report data for chart
    cur.execute("""
        SELECT date_year,
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        GROUP BY date_year
        ORDER BY date_year
    """)
    
    yearly_chart = cur.fetchall()

    # Calculate sales growth
    sales_growth = []
    for i in range(1, len(yearly_chart)):
        current_sales = yearly_chart[i][1]
        previous_sales = yearly_chart[i-1][1]
        growth = ((current_sales - previous_sales) / previous_sales * 100) if previous_sales else None
        sales_growth.append({
            'date_year': yearly_chart[i][0],
            'growth': growth
        })
    
    #calculate customer retention rate for the year
    retention_rate = None
    if len(yearly_chart) > 1:
        start_year_users = yearly_chart[0][4]  # Users at the beginning of the year
        end_year_users = yearly_chart[-1][4]   # Users at the end of the year
        if start_year_users:
            # Calculate the retention rate: ((end_users - new_users) / start_users) * 100
            new_users_during_year = yearly_chart[-1][3] - yearly_chart[0][3]  # New users during the year
            retention_rate = ((end_year_users - new_users_during_year) / start_year_users) * 100

    cur.close()

    # Format the date for display as "Year"
    formatted_date_year = selected_date_obj.strftime("%Y")

    return render_template("manager_reports_yearly.html", 
                           yearly_report=yearly_report, 
                           date_year=formatted_date_year,
                           top_product=top_product, 
                           yearly_chart=yearly_chart,
                           sales_growth=sales_growth,retention_rate=retention_rate,
                           current_year=current_year)

#M-view feedbacks
@app.route("/manager/feedback", methods=["GET","POST"])
def view_feedback():
    if not session.get('logged_in'):
        return redirect('/staff/login')
    
    if request.method == "POST":
        feedback_id = request.form.get('feedback_id')
        return redirect(f"/manager/feedback/reply?feedback_id={feedback_id}")

    # Fetch feedback from the database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT feedback_id, stf_id, feedback, feedback_time
        FROM feedback
        WHERE reply IS NULL
    """)
    feedback_list = cur.fetchall()
    cur.close()

    return render_template("manager_view_feedback.html", feedback_list=feedback_list)

@app.route("/manager/feedback/reply", methods=["GET", "POST"])
def reply_feedback():
    if not session.get('logged_in'):
        return redirect('/login')
    
    if request.method == 'POST':
        reply = request.form.get('reply')
        feedback_id = request.form.get('feedback_id')

        # Insert the reply into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE feedback SET reply = %s WHERE feedback_id = %s
        """, (reply, feedback_id))
        mysql.connection.commit()
        cur.close()

        return redirect('/manager/feedback')  # Redirect to the feedback list after submitting

    feedback_id = request.args.get('feedback_id')
    if not feedback_id:
        return redirect('/manager/feedback')

    # Fetch the specific feedback from the database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT feedback_id, feedback, stf_id, feedback_time
        FROM feedback
        WHERE feedback_id = %s
    """, (feedback_id,))
    feedback = cur.fetchone()
    cur.close()

    return render_template("manager_reply_feedback.html", feedback=feedback)

if __name__=='__main__':
    app.run(debug=True)
>>>>>>> manager
