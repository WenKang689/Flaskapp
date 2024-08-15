from flask import Flask, render_template, request, session, flash, redirect, url_for, make_response
from flask_mysqldb import MySQL
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import boto3
from datetime import datetime, timezone
import os
import MySQLdb
import re

app= Flask(__name__)

#database configuration
db=yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]
app.secret_key = db["secret_key"]

mysql = MySQL(app)

#AWS S3 credentials and bucket configuration
S3= boto3.client('s3')
S3_BUCKET = 'sourc-wk-sdp-project'
S3_LOCATION = 'https://sourc-wk-sdp-project.s3.amazonaws.com/User+Profile+Picture/'

#login for all (html sent)
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

#register (html sent)
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
            flash("Password must contain at least one letter, one number, and one special character.", "danger")
            cur.close()
            return redirect("/register")

        cur.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NULL)",(username,password,name,email,phone,dob,address,occupation))
        mysql.connection.commit()
        flash("Register Successful.")
        cur.close()
        return redirect("/")
    return render_template("register.html")

#forgot password (html sent)
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

#reset password (html sent)
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
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        #Search bar
        if request.method == 'POST':
            if request.form['action'] == 'search':
                search_query = request.form['query']
                session['homepage_search_query'] = search_query
                return redirect("/laptop",search_query=search_query)
        return render_template('homepage.html')

#C-setting/profile (html sent)
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

#C-setting/profile/edit profile (html sent)
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
        if len(password) > 20 and len(password) < 8:
            flash("Password must be 8 or more characters with a mix of letters, numbers & symbols", "danger")
            return redirect("/user/setting/profile/edit")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$', password):
            flash("Password must contain at least one letter, one number, and one special character.", "danger")
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

#C-setting/payment method
@app.route("/user/setting/payment", methods=["GET", "POST"])
def setting_payment():

    username = session.get('username')

    cur = mysql.connection.cursor()
    
    cur.execute("SELECT saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date FROM payment WHERE username = %s", [username])
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

@app.route('/user/setting/payment/edit', methods=['GET','POST'])
def setting_payment_edit():
    current_username = session.get('username')
    saved_card_id = generate_next_saved_card_id()

    if request.method == "POST":
        action = request.form.get('action')
        
        if action == "add":
            render_template("setting_payment_edit.html")

            cur = mysql.connection.cursor()

            pay_email = request.form.get('pay_email','')
            name_on_card = request.form.get('name_on_card','')
            card_no = request.form.get('card_no','').replace(" ", "")  # Remove spaces from card number
            cvv = request.form.get('cvv','')
            expiry_date = request.form.get('expiry_date','')

            # Input validation
            errors = {
                "pay_email": not is_valid_email(pay_email),
                "card_no": not is_valid_card_number(card_no),
                "cvv": not is_valid_cvv(cvv),
                "expiry_date": not is_valid_expiry_date(expiry_date)
            }

            if any(errors.values()):
                return render_template("setting_payment_edit.html", errors=errors, form_data=request.form)
            else:
                # Proceed with the database insert if all fields are valid
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO payment (saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (saved_card_id, current_username, pay_email, name_on_card, card_no, cvv, expiry_date))
                mysql.connection.commit()
                flash("Payment method added successfully.", "success")
                cur.close()
                return redirect("/user/setting/payment")

        elif action == "remove":
            saved_card_id = request.form.get('saved_card_id')
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM payment WHERE saved_card_id = %s AND username = %s", (saved_card_id, current_username))
            mysql.connection.commit()
            flash("Payment method removed successfully.", "success")
            cur.close()
            return redirect("/user/setting/payment")
        
        else:
            flash("Invalid action.", "danger")
            return render_template("setting_payment_edit.html")
    
    return render_template("setting_payment_edit.html")

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

#C-setting/history(default purchase)
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

#C-setting/history/search history
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

#C-survey/fill in survey
@app.route("/recommend/survey/form", methods=["GET","POST"])
def recommend_survey_form():
    return render_template("recommend_survey_form.html")

#C-auto recommend page
@app.route("/recommend/auto", methods=["GET","POST"])
def recommend_auto():
    # Define categories and associated keywords
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
                category = categorize_app(app)
                categorized_apps[category] += 1
    
    username = "user1"  # Replace with the actual username
    
    recommendations = recommend_laptops(categorized_apps)
    save_recommendations_to_db(username, recommendations)
    
    print("Recommendations saved to database.")
    return render_template("recommend_auto.html")

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

def categorize_app(app_path):

    categories=get_categories()
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
            power_supply, battery, price
        FROM product
    """
    cur.execute(query)
    laptops = cur.fetchall()
    cur.close()
    
    return laptops

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
        if 'gaming' in laptop['product_name'].lower():
            score_adjustment += 10  
        if 'productivity' in laptop['product_name'].lower():
            score_adjustment += 5 
        
        price = laptop['price']
        normalized_price = max(1, price / 1000)  
        final_score = basic_score + score_adjustment - normalized_price
        
        recommendations.append((laptop, final_score))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Normalize the scores between 1 and 100
    max_score = recommendations[0][1]
    min_score = recommendations[-1][1]
    score_range = max_score - min_score

    for i in range(len(recommendations)):
        normalized_score = ((recommendations[i][1] - min_score) / score_range) * 99 + 1
        recommendations[i] = (recommendations[i][0], normalized_score)
    
    return recommendations[:30]  # Return top 30 recommendations

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

def save_recommendations_to_db(username, recommendations):
    # Prepare the insert/update query
    # Assuming the upsert_query is defined somewhere above this code
    upsert_query = """
    INSERT INTO user_recommendations (
        username, product_id_1, score_1, product_id_2, score_2, product_id_3, score_3, 
        product_id_4, score_4, product_id_5, score_5, product_id_6, score_6, 
        product_id_7, score_7, product_id_8, score_8, product_id_9, score_9, 
        product_id_10, score_10, product_id_11, score_11, product_id_12, score_12, 
        product_id_13, score_13, product_id_14, score_14, product_id_15, score_15, 
        product_id_16, score_16, product_id_17, score_17, product_id_18, score_18, 
        product_id_19, score_19, product_id_20, score_20, product_id_21, score_21, 
        product_id_22, score_22, product_id_23, score_23, product_id_24, score_24, 
        product_id_25, score_25, product_id_26, score_26, product_id_27, score_27, 
        product_id_28, score_28, product_id_29, score_29, product_id_30, score_30, 
        last_updated
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, NOW()
    ) ON DUPLICATE KEY UPDATE 
        product_id_1 = VALUES(product_id_1), score_1 = VALUES(score_1),
        product_id_2 = VALUES(product_id_2), score_2 = VALUES(score_2),
        product_id_3 = VALUES(product_id_3), score_3 = VALUES(score_3),
        product_id_4 = VALUES(product_id_4), score_4 = VALUES(score_4),
        product_id_5 = VALUES(product_id_5), score_5 = VALUES(score_5),
        product_id_6 = VALUES(product_id_6), score_6 = VALUES(score_6),
        product_id_7 = VALUES(product_id_7), score_7 = VALUES(score_7),
        product_id_8 = VALUES(product_id_8), score_8 = VALUES(score_8),
        product_id_9 = VALUES(product_id_9), score_9 = VALUES(score_9),
        product_id_10 = VALUES(product_id_10), score_10 = VALUES(score_10),
        product_id_11 = VALUES(product_id_11), score_11 = VALUES(score_11),
        product_id_12 = VALUES(product_id_12), score_12 = VALUES(score_12),
        product_id_13 = VALUES(product_id_13), score_13 = VALUES(score_13),
        product_id_14 = VALUES(product_id_14), score_14 = VALUES(score_14),
        product_id_15 = VALUES(product_id_15), score_15 = VALUES(score_15),
        product_id_16 = VALUES(product_id_16), score_16 = VALUES(score_16),
        product_id_17 = VALUES(product_id_17), score_17 = VALUES(score_17),
        product_id_18 = VALUES(product_id_18), score_18 = VALUES(score_18),
        product_id_19 = VALUES(product_id_19), score_19 = VALUES(score_19),
        product_id_20 = VALUES(product_id_20), score_20 = VALUES(score_20),
        product_id_21 = VALUES(product_id_21), score_21 = VALUES(score_21),
        product_id_22 = VALUES(product_id_22), score_22 = VALUES(score_22),
        product_id_23 = VALUES(product_id_23), score_23 = VALUES(score_23),
        product_id_24 = VALUES(product_id_24), score_24 = VALUES(score_24),
        product_id_25 = VALUES(product_id_25), score_25 = VALUES(score_25),
        product_id_26 = VALUES(product_id_26), score_26 = VALUES(score_26),
        product_id_27 = VALUES(product_id_27), score_27 = VALUES(score_27),
        product_id_28 = VALUES(product_id_28), score_28 = VALUES(score_28),
        product_id_29 = VALUES(product_id_29), score_29 = VALUES(score_29),
        product_id_30 = VALUES(product_id_30), score_30 = VALUES(score_30),
        last_updated = NOW()
    """

    # Prepare the values
    values = [username]
    for i in range(30):
        if i < len(recommendations):
            laptop, score = recommendations[i]
            values.extend([laptop['product_id'], score])
        else:
            values.extend([None, None])

    # Ensure we have the correct number of values
    if len(values) != 61:
        raise ValueError(f"Expected 61 values, but got {len(values)}")

    try:
        # Execute the upsert query
        cur = mysql.connection.cursor()
        cur.execute(upsert_query, tuple(values))
        cur.commit()
        print(f"Recommendations for {username} saved to database.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if cur:
            cur.rollback()
    except ValueError as err:
        print(f"Value error: {err}")

        print("Recommendations saved to database.")

#C-laptop (display all laptop + search result + filter) (html sent)
@app.route("/laptop", methods=["GET","POST"])
def laptop():
    username = session.get('username')

    search_query = session.get('homepage_search_query', '')
    if not search_query:
        search_query = request.args.get('search', '')
        
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
        SELECT p.product_id, p.product_name, p.brand, p.price, p.memory, p.graphics, p.storage, p.battery, p.processor, p.os, p.weight, pic.pic_url
        FROM product p
        LEFT JOIN (
            SELECT product_id, MIN(pic_url) as pic_url
            FROM product_pic
            GROUP BY product_id
        ) pic ON p.product_id = pic.product_id
    """)
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
        if (search_query.lower() in laptop[1].lower()) and
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

    message = None
    if not filtered_laptops:
        message = "No laptops found matching the criteria."

    return render_template('laptop_search.html', laptops=filtered_laptops, brands=brands, memories=memories, graphics_options=graphics_options, storages=storages, batteries=batteries, processors=processors, operating_systems=operating_systems, message=message, min_price=min_price_db, max_price=max_price_db, min_weight=min_weight_db, max_weight=max_weight_db)

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

def mask_username(username): # Function to mask the username
    if len(username) <= 1:
        return '*'  # If the role_id is 1 character or fewer, show the first character
    elif len(username) == 2:
        return username[0] + '*'  # If the role_id is 2 characters, show the first character and mask the second
    else:
        return username[0] + '*' * (len(username) - 2) + username[-1]  # Mask all characters except first and last

#C-laptop/detail (html sent)
@app.route("/laptop/<product_id>", methods=["GET","POST"])
def laptop_detail(product_id):
    
    # Clean up the product_id
    product_id = product_id.replace('<', '').replace('>', '').strip()
    print(f"Processed product_id: {product_id}")  # Debug print

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
        'reviews': reviews_list
    }

    # Pass laptop_details to the template
    return render_template("laptop_detail.html", product_details=product_details)

#C-cart(all) (html sent)
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
            selected_items = [key.split('_')[1] for key in request.form if key.startswith('select_')]
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
                            (SELECT pic_url FROM product_pic pp WHERE pp.product_id = p.product_id LIMIT 1) AS pic_url
                        FROM cart c
                        JOIN product p ON c.product_id = p.product_id
                        WHERE c.username = %s AND c.product_id = %s
                    """, (username, product_id))
                    item = cur.fetchone()
                    if item:
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
                (SELECT stock FROM product p WHERE p.product_id = c.product_id) AS stock
            FROM cart c
            JOIN product p ON c.product_id = p.product_id
            WHERE c.username = %s
        """, (username,))
        cart_items = cur.fetchall()

    item_count = len(cart_items)
    cart_total_price = sum(item[2] * item[3] for item in cart_items if f'select_{item[0]}' in request.form)

    return render_template("cart.html", cart_items=cart_items, cart_total_price=cart_total_price, item_count=item_count)

#C-cart/checkout(choose payment method,address) (html sent)
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

        # Handle payment method insertion if 'new' is selected
        if saved_card_id == 'new':
            pay_email = request.form.get('pay_email', '')
            name_on_card = request.form.get('name_on_card', '')
            card_no = request.form.get('card_no', '').replace(" ", "")
            cvv = request.form.get('cvv', '')
            expiry_date = request.form.get('expiry_date', '')

            errors.update({
                "pay_email": not is_valid_email(pay_email),
                "card_no": not is_valid_card_number(card_no),
                "cvv": not is_valid_cvv(cvv),
                "expiry_date": not is_valid_expiry_date(expiry_date)
            })

            if any(errors.values()):
                print(f"Validation errors: {errors}")
                return render_template("cart_checkout.html", errors=errors, form_data=request.form, selected_items=selected_items, checkout_total_price=checkout_total_price)

            try:
                with mysql.connection.cursor() as cur:
                    new_saved_card_id = generate_next_saved_card_id()
                    cur.execute("""
                        INSERT INTO payment (saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (new_saved_card_id, username, pay_email, name_on_card, card_no, cvv, expiry_date))
                    mysql.connection.commit()
                    saved_card_id = new_saved_card_id
            except Exception as e:
                print(f"Error inserting into payment table: {e}")
                mysql.connection.rollback()
                return "Error processing payment details"
            
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
                WHERE username = %s
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

#C-cart/payment success (html sent)
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

#Manager section (Ying Xin)
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

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    debug_mode = False
else:
    debug_mode = True

app.run(debug=debug_mode)