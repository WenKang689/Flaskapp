from flask import Flask, render_template, request, session, flash, redirect, url_for
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

#C-laptop/ (display all laptop + search result + filter)
@app.route("/laptop", methods=["GET","POST"])
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
@app.route("/manager/homepage", methods=["GET", "POST"])
def manager_homepage():
    if not session.get('logged_in'):
        return redirect('/staff/login')
        
    search_query = ''
    if request.method == 'POST':
        if request.form.get('action') == 'search':
            search_query = request.form.get('query', '')
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

    return render_template("manager_homepage.html", laptops=all_laptops, search_query=search_query)
    

#M-laptop
@app.route("/laptop", methods=["GET","POST"])
def laptop():
    search_query = request.args.get('search', '')
        
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
    cur.close()

    return render_template('manager_browser_laptop.html', laptops=all_laptops, search_query=search_query)

#M-laptop/detail
# Function to mask the username
def mask_username(username):
    if len(username) <= 1:
        return '*'  # If the role_id is 1 character or fewer, show the first character
    elif len(username) == 2:
        return username[0] + '*'  # If the role_id is 2 characters, show the first character and mask the second
    else:
        return username[0] + '*' * (len(username) - 2) + username[-1]  # Mask all characters except first and last


@app.route("/laptop/<product_id>", methods=["GET","POST"])
def laptop_detail(product_id):
    
    # Clean up the product_id
    product_id = product_id.replace('<', '').replace('>', '').strip()
    print(f"Processed product_id: {product_id}")  # Debug print

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
    return render_template("manager_view_laptop", product_details=product_details)

#M-manage account
@app.route("/manager/account", methods=["GET","POST"])
def manager_account():
    cur = mysql.connection.cursor()
    cur.execute("SELECT stf_id, stf_name, stf_role FROM staff WHERE stf_role='admin'")
    staff= cur.fetchall()
    cur.close()

    staff = [
        {'stf_id': row[0], 'stf_name': row[1], 'stf_role': row[2]}
        for row in staff
    ]

    #add button
    if request.method == "POST":
        action = request.form("action")
        if action == "add":
            return redirect ("/manager/account/new")
        
    #remove button
    if request.method == "POST":
        action = request.form("action")
        if action == "remove":
            return redirect ("/manager/account/remove")

    return render_template("manager_account.html",staff=staff)
    
#M-view account
@app.route("/manager/account/detail/<string:stf_id>", methods=["GET", "POST"])
def manager_view_account(stf_id):
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
        last_num = int(last_id[0][2:])  # Assuming ID format is PC000X
        new_num = last_num + 1
        new_id = f"ST{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with PC0001
        new_id = "ST0001"
    return new_id

from datetime import datetime

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
        
        if stf_dob:
            try:
                datetime.strptime(stf_dob, '%Y-%m-%d')  # Validate date format
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD."
        try: 
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO staff (stf_id, stf_psw, stf_name, stf_email, stf_phone, stf_dob, stf_address, stf_emer_contact, stf_role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (stf_id, stf_psw, stf_name, stf_email, stf_phone, stf_dob, stf_address, stf_emer_contact, stf_role))
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
    if request.method == "POST":
        stf_id = request.form.get("stf_id")
        action = request.form.get("action")
        #cancel button
        if action == "Cancel":
            return redirect ("/manager/account")
        #confirm button
        if action == "Confirm":
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM staff WHERE stf_id = %s", (stf_id,))
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

    return render_template("manager_account_remove.html", staff=staff)

#M-manage reports
def create_report_table():
    cur = mysql.connection.cursor()
    create_table_query = """
            CREATE TABLE IF NOT EXISTS report (
                order_id CHAR(8) PRIMARY KEY,
                date_day DATE,
                date_week DATE,
                date_month DATE,
                date_year DATE,
                sales DECIMAL(10, 2),
                product_sold INT,
                product_id CHAR(6),
                product_name VARCHAR(100),
                total_order INT,
                total_user INT,
                new_user INT
            )
        """
    cur.execute(create_table_query)
    mysql.connection.commit()
    cur.close()

import datetime

def update_report_table():
    cur = mysql.connection.cursor()

    # Create or ensure the existence of the user_tracking table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_tracking (
            id INT PRIMARY KEY,
            previous_total_user INT
        )
    """)

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
        start_of_week = pur_date - datetime.timedelta(days=pur_date.weekday())
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
    
    create_report_table()
    update_report_table()

    return render_template("manager_reports.html")

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
    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    cur = mysql.connection.cursor()

    # Calculate the start of the month for the selected_date
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    date_month = selected_date_obj.replace(day=1).strftime("%Y-%m-%d")

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
        SELECT date_month, 
               SUM(sales) AS total_sales, 
               SUM(product_sold) AS total_product_sold, 
               SUM(new_user) AS total_new_user,
               COUNT(order_id) AS total_orders
        FROM report
        GROUP BY date_month
        ORDER BY date_month
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

    return render_template("manager_reports_monthly.html", 
                           monthly_report=monthly_report, 
                           date_month=date_month,
                           top_product=top_product, 
                           monthly_chart=monthly_chart,
                           sales_growth=sales_growth)

#M-reports/yearly
@app.route("/manager/reports/yearly", methods=["GET","POST"])
def manager_reports_yearly():
    selected_date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
    
    cur = mysql.connection.cursor()

    # Calculate the start and end of the year for the selected_date
    selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
    date_year = selected_date_obj.replace(month=1, day=1).strftime("%Y-%m-%d")

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
        GROUP BY date_year
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

    return render_template("manager_reports_yearly.html", 
                           yearly_report=yearly_report, 
                           date_year=date_year,
                           top_product=top_product, 
                           yearly_chart=yearly_chart,
                           sales_growth=sales_growth,retention_rate=retention_rate)

#M-view feedbacks
@app.route("/manager/feedback", methods=["GET"])
def view_feedback():
    if not session.get('logged_in'):
        return redirect('/login')
    
    # Fetch feedback from the database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT feedback_id, stf_id, feedback, feedback_time
        FROM feedback
    """)
    feedback_list = cur.fetchall()
    cur.close()

    return render_template("manager_view_feedback.html", feedback_list=feedback_list)

#M-reply feedback
def generate_feedback_id():
    cur = mysql.connection.cursor()
    cur.execute("SELECT feedback_id FROM feedback WHERE feedback_id LIKE 'RP%' ORDER BY feedback_id DESC LIMIT 1")
    last_id = cur.fetchone()
    cur.close()
    if last_id:
        # Extract the numeric part of the ID and increment it
        last_num = int(last_id[0][2:])  # Assuming ID format is PC000X
        new_num = last_num + 1
        new_id = f"RP{new_num:04d}"  # Keeps the leading zeros, making the numeric part 4 digits long
    else:
        # If there are no entries, start with PC0001
        new_id = "RP0001"
    return new_id

@app.route("/manager/reply_feedback", methods=["GET", "POST"])
def reply_feedback():
    if not session.get('logged_in'):
        return redirect('/login')
    
    feedback_id = request.args.get('feedback_id')
    if not feedback_id:
        return redirect('/manager/feedback')
    
    if not feedback_id.startswith('FD'):
        flash("Invalid feedback ID. You can only reply to feedback starting with 'FD'.", "error")
        return redirect('/manager/feedback')

    if request.method == 'POST':
        reply = request.form['reply']
        staff_id = session.get('staff_id')
        cur = mysql.connection.cursor()
        cur.execute("SELECT stf_id FROM staff WHERE stf_id=%s", (staff_id,))
        result = cur.fetchone()
        cur.close()        
        if result:
            stf_id = result[0]
        else:
            flash("Staff ID not found. Please log in again.", "error")
            return redirect('/login')
        feedback_time = datetime.now()
        new_feedback_id = generate_feedback_id()

        # Insert the reply into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO feedback (feedback_id, stf_id, feedback, feedback_time)
            VALUES (%s, %s, %s, %s)
        """, (new_feedback_id, stf_id, reply, feedback_time))
        mysql.connection.commit()
        cur.close()

        return redirect('/manager/feedback')  # Redirect to the feedback list after submitting


    # Fetch the specific feedback from the database
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT feedback_id, feedback, stf_id, feedback_time
        FROM feedback
        WHERE feedback_id = %s
    """, (feedback_id,))
    feedback = cur.fetchone()

    return render_template("manager_reply_feedback.html", feedback=feedback)

if __name__=='__main__':
    app.run(debug=True)
