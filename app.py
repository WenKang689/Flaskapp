from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL
import yaml
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import boto3
from datetime import datetime
from flask import request, render_template, redirect, flash
from urllib.parse import urlparse
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
#staff login
@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():
    if request.method == "POST":
        if request.form['action'] == 'login':
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
                        return redirect("/admin/laptop")
                else:
                    flash("Invalid staff ID or password.")
            else:
                flash("Invalid staff ID or password.")
            cur.close()
        elif request.form['action'] == 'forgot_password':
            return redirect("/staff/forgot_password")
    return render_template("staff_login.html")

#Staff-forgot password
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

#Staff-reset password
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

        last_id = result[0] if result[0] is not None else 'F0000'
        last_number = int(last_id[1:])  # Get the numeric part and convert to integer
        next_number = last_number + 1
        feedback_id = f'F{next_number:04d}'  # Format as F#### with leading zeros

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

if __name__=='__main__':
    app.run(debug=True)