from flask import Flask, render_template, request, session, flash, redirect, url_for,make_response
from flask_mysqldb import MySQL
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import boto3
from datetime import datetime, timezone
import os

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
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        #Search bar
        if request.method == 'POST':
            if request.form['action'] == 'search':
                query = request.form['query']
                return redirect("/laptop/search",query=query)
        return render_template('homepage.html')

#C-setting/profile
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

#C-setting/profile/edit profile
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
        if len(password) > 20:
            flash("Password must be 20 characters or fewer.", "danger")
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

#generate next saved card id
def generate_next_saved_card_id():
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

#C-laptop/ (display all laptop + search result + filter)
@app.route("/laptop", methods=["GET","POST"])
def laptop_filter():
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

    # For debugging: print out the fetched laptops
    print("Fetched laptops with pictures:")
    for laptop in all_laptops:
        print(laptop)

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
        return render_template('laptop_search.html', message=message)
    if min_weight and max_weight and float(min_weight) > float(max_weight):
        message = "Max weight must be greater than min weight."
        return render_template('laptop_search.html', message=message)

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