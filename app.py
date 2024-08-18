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
import MySQLdb
from flask import request, render_template, redirect, flash
from math import ceil
from werkzeug.utils import secure_filename
import uuid

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
            cur.execute(
    "INSERT INTO user (username, password, name, email, phone, dob, address, occupation) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
    (username, password, name, email, phone, dob, address, occupation)
)
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
@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        userdata = request.form
        staff_id = userdata.get("stf_id")
        staff_psw = userdata.get("stf_psw")
        cur = mysql.connection.cursor()
        value = cur.execute("SELECT stf_id, stf_psw, stf_role FROM staff WHERE stf_id=%s", (staff_id,))

        if value > 0:
            data = cur.fetchone()
            passw = data[1]
            role = data[2]
            if staff_psw == passw:
                session["logged_in"] = True
                session["staff_id"] = staff_id
                if role == "manager":
                    flash("Login Successful", "success")
                    return redirect("/manager/homepage")
                elif role == "admin":
                    flash("Login Successful", "success")
                    return redirect("/admin/homepage")
            else:
                flash("Invalid staff ID or password.")
        else:
            flash("Invalid staff ID or password.")
        cur.close()
    return render_template("staff_login.html")


#Admin section (Zhi Xian)
#A-home page
@app.route('/admin/homepage', methods=['GET', 'POST'])
def admin_homepage():
    if not session.get('logged_in'):
        return redirect('/admin/login')
    else:
        # Search bar or admin-specific actions
        if request.method == 'POST':
            if request.form['action'] == 'search':
                search_query = request.form['query']
                session['admin_homepage_search_query'] = search_query
                return redirect("/admin/laptop", search_query=search_query)
            # Add more admin-specific actions here if needed
        return render_template('admin_homepage.html')

#A-laptop
@app.route("/admin/laptop", methods=["GET", "POST"])
def admin_laptop():
    search_query = request.args.get('search', '')

    sql_query = """
    SELECT p.product_id, p.product_name, p.brand, p.price, p.memory, p.graphics, p.storage, p.battery, p.processor, p.os, p.weight, pic.pic_url, p.stock
    FROM product p
    LEFT JOIN (
        SELECT product_id, MIN(pic_url) as pic_url
        FROM product_pic
        GROUP BY product_id
    ) pic ON p.product_id = pic.product_id
    WHERE p.product_name LIKE %s
    OR p.brand LIKE %s
    OR p.processor LIKE %s
    """

    search_term = f'%{search_query}%'
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (search_term, search_term, search_term))
    all_laptops = cur.fetchall()
    cur.close()

    return render_template('admin_laptop_search.html', laptops=all_laptops, search_query=search_query)

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
        cur.close()

        flash(f"Laptop added successfully with ID {product_id}.", "success")
        return redirect("/admin/laptop")

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

                flash("Laptop details and stock updated successfully.", "success")
                return redirect("/admin/laptop")
            else:
                flash("Laptop not found.", "danger")
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

#A-remove laptop
@app.route("/admin/laptop/remove", methods=["GET", "POST"])
def admin_laptop_remove():
    if request.method == "POST":
        product_id = request.form['product_id']

        # Delete laptop from product table
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM product WHERE product_id = %s', (product_id,))
        
        mysql.connection.commit()
        cursor.close()

        flash("Laptop successfully removed.", "success")
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

                object_name = f"New Laptops/{product_id} {laptop_name}/Image-{generate_pic_id()}.jpg"
                pic_url = upload_file_to_s3(image_file, S3_BUCKET, object_name)

                if pic_url:
                    # Save the URL in the database
                    pic_id = generate_pic_id()
                    sql_insert = """
                    INSERT INTO product_pic (pic_id, product_id, pic_url)
                    VALUES (%s, %s, %s)
                    """
                    cur = mysql.connection.cursor()
                    cur.execute(sql_insert, (pic_id, product_id, pic_url))
                    mysql.connection.commit()
                    cur.close()

                    flash("Image uploaded successfully.", "success")
                else:
                    flash("Failed to upload image to S3.", "danger")

            return redirect(url_for('laptop_images', product_id=product_id))

        # Handle image deletion
        if 'delete_pic_id' in request.form:
            delete_pic_id = request.form['delete_pic_id']

            # Delete image from the database
            sql_delete = "DELETE FROM product_pic WHERE pic_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(sql_delete, (delete_pic_id,))
            mysql.connection.commit()
            cur.close()

            flash("Image deleted successfully.", "success")
            return redirect(url_for('laptop_images', product_id=product_id))

    # Display existing images
    sql_query = "SELECT pic_url FROM product_pic WHERE product_id = %s"
    cur = mysql.connection.cursor()
    cur.execute(sql_query, (product_id,))
    images = cur.fetchall()
    cur.close()

    return render_template('admin_laptop_images.html', product_id=product_id, images=images)

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
    
def generate_pic_id():
    return 'PP' + str(uuid.uuid4().int)[:4].zfill(4)


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
        current_time = datetime.now()

        try:
            # Update review with the admin's reply
            cur.execute("""
                UPDATE review 
                SET reply = %s 
                WHERE review_id = %s
            """, (reply_text, review_id))
            mysql.connection.commit()
            flash("Reply sent successfully.", "success")
        except Exception as e:
            print(f"An error occurred: {e}")
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
        ORDER BY review.review_time DESC
        """
        cur.execute(query)
        reviews = cur.fetchall()
        cur.close()

        # Check if any reviews are fetched
        if not reviews:
            flash("All reviews have been replied to.", "info")

        return render_template("admin_reviews.html", reviews=reviews)

    except Exception as e:
        cur.close()
        print(f"An error occurred: {e}")
        flash("An error occurred while retrieving reviews. Please try again later.", "error")
        return redirect("/admin/homepage")

#A-send feedback to manager
@app.route("/admin/feedback/send", methods=["GET", "POST"])
def admin_feedback_send():
    if not session.get('logged_in'):
        return redirect('/login')

    staff_id = session.get('stf_id')  # Assuming staff_id is stored in session after login

    if request.method == "POST":
        feedback_text = request.form.get('feedback')
        feedback_time = datetime.now()

        # Insert feedback into the database
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO feedback (stf_id, feedback, feedback_time) 
            VALUES (%s, %s, %s)
        """, (staff_id, feedback_text, feedback_time))
        mysql.connection.commit()
        cur.close()

        flash("Feedback sent successfully.", "success")
        return redirect("/admin/feedback/send")

    return render_template("admin_feedback_send.html")

#A-orders (Check and cancel orders)
@app.route("/admin/orders", methods=["GET", "POST"])
def admin_orders():
    if not session.get('logged_in'):
        return redirect('/login')

    cur = mysql.connection.cursor()

    # Handle order cancellation
    if request.method == "POST":
        order_id = request.form.get('order_id')
        print(f"Attempting to cancel order: {order_id}")

        try:
            # First, delete related shipping details
            cur.execute("""
                DELETE FROM shipping 
                WHERE order_id = %s
            """, (order_id,))
            
            # Then delete the order from the purchase table
            cur.execute("""
                DELETE FROM purchase 
                WHERE order_id = %s
            """, (order_id,))

            mysql.connection.commit()
            flash(f"Order {order_id} has been canceled.", "success")
        except Exception as e:
            print(f"An error occurred: {e}")
            mysql.connection.rollback()
            flash("An error occurred while canceling the order. Please try again.", "error")
        finally:
            cur.close()
        return redirect("/admin/orders")

    # Pagination parameters
    page = int(request.args.get('page', 1))  # Default to page 1 if no page param
    per_page = 5
    offset = (page - 1) * per_page

    try:
        # Retrieve orders with pagination
        query = """
        SELECT 
            p.order_id, p.username, p.pur_date, p.pur_amount, p.pur_status, 
            s.dest_add, s.receiver_name, s.receiver_phone, s.ship_status, s.ship_time
        FROM purchase p
        LEFT JOIN shipping s ON p.order_id = s.order_id
        ORDER BY p.pur_date DESC
        LIMIT %s OFFSET %s
        """
        cur.execute(query, (per_page, offset))
        orders = cur.fetchall()

        # Count total orders for pagination control
        cur.execute("SELECT COUNT(*) FROM purchase")
        total_orders = cur.fetchone()[0]
        total_pages = ceil(total_orders / per_page)

        cur.close()
        return render_template("admin_orders.html", orders=orders, current_page=page, total_pages=total_pages)
    except Exception as e:
        cur.close()
        print(f"An error occurred: {e}")
        flash("An error occurred while retrieving orders. Please try again later.", "error")
        return redirect("/admin/homepage")


if __name__=='__main__':
    app.run(debug=True)