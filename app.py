from flask import Flask, render_template, request , session, redirect, url_for, jsonify, send_file
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import session
from flask_mail import Mail, Message
from sqlalchemy.exc import IntegrityError
import socket
import json
import os
from flask_mysqldb import MySQL
import secrets
                         
socket.getaddrinfo('localhost', 8080)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]


app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)

mail = Mail(app)
local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

class Contacts(db.Model):
    '''
      sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    umail = db.Column(db.String(50), nullable=True)

class Projects(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    pro_link = db.Column(db.String(300), nullable=False)
    date = db.Column(db.String(), nullable=True)
    img_file = db.Column(db.String(50), nullable=True)


class Expes(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.String, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(240), nullable=False)
    com_add = db.Column(db.String(30), nullable=False)
    res_date = db.Column(db.String(), nullable=True)
    post_date = db.Column(db.String(), nullable=True)

class Edcs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    cor_duration = db.Column(db.String(20), nullable=False)
    clg_name = db.Column(db.String(50), nullable=False)
    clg_add = db.Column(db.String(50), nullable=False)
    cor_name = db.Column(db.String(25), nullable=False)
    cor_work = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(120), nullable=True)
    post_date = db.Column(db.String(), nullable=True)

class User(db.Model):
    '''
     name, email, password
    '''
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(150), nullable=True)
    umail = db.Column(db.String(150), nullable=True)
    password = db.Column(db.String(150), nullable=True)
    reset_token = db.Column(db.String(255), unique=True, nullable=True)

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        uname = request.form['uname']
        umail = request.form['umail']
        password = request.form['password']
    
    # Create a new user and add to the database
        new_user = User(uname=uname, umail=umail, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successfully. ","success")
        return redirect('/login')

    return render_template('register.html', params=params)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        umail = request.form['umail']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(umail=umail, password=password).first()
        if user:
            session['umail'] = umail  # Store username in session
            session['password'] = password
            return redirect('/home')
        else:
            flash("check email, password and try again. ","danger")
            return redirect('/login')
    return render_template('login.html')

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        umail = request.form.get('umail')
        password = request.form.get('password')

        # Check if user exists
        user = User.query.filter_by(umail=umail, password=password).first()
        if user:
            session['umail'] = umail  # Store username in session
            session['password'] = password
            return redirect('/home')  # Refresh home page with session
        else:
            flash("check email, password and try again. ","danger")
            return redirect('/login')
    return render_template('login.html', params=params, )

@app.route('/home',methods=['GET','POST'])
def home():
    expe = Expes.query.all()
    edc = Edcs.query.all()
    return render_template('index.html', params=params, expes=expe, edcs=edc)

@app.route('/resume', methods=['GET'])
def resume_route():
    expe = Expes.query.all()
    edc = Edcs.query.all()
    return render_template('resume.html', params=params, expes=expe, edcs=edc)

@app.route('/project', methods=['GET'])
def project_route():
    project = Projects.query.all()
    return render_template('project.html', params=params, projects=project)

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get("name")
        message = request.form.get("message")
        email = request.form.get("email")
        phone = request.form.get("phone")
        umail = session.get("umail")

        entry = Contacts(name=name, msg=message, phone_num=phone, email=email,  umail=umail, date=datetime.now())

        flash("Your form submitted successfully.", "succsess")
        #email html page
        rendered_body= render_template('email.html', params=params)
        mail.send_message(subject="New message from " + name,
                          sender=email,  # Changed to a string
                          recipients=[params['gmail-user']],  # Ensure this is a list
                          body=message +"\n" + phone +"\n"+ "user login mail:-"+umail
                          )
        mail.send_message(subject="JIGNESH SATHAVARA",
                          sender=params['gmail-user'],
                          recipients = [email],
                          html=rendered_body
                          )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html', params=params)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if "admin" in session and session['admin']==params['admin_user']:
        project = Projects.query.all()
        expe = Expes.query.all()
        edc = Edcs.query.all()
        user = User.query.all()
        return render_template("dashboard.html", params=params, projects=project, expes=expe, edcs=edc, user=user)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("upass")
        if username==params['admin_user'] and userpass==params['admin_password']:
            # set the session variable
            session['admin']=username
            project = Projects. query.all()
            expe = Expes.query.all()
            edc = Edcs.query.all()
            user = User.query.all()
            return render_template("dashboard.html", params=params, projects=project, expes=expe, edcs=edc, user=user)
    else:
        flash("check email, password and try again. ","danger")
        return render_template("login1.html", params=params)
    
    return render_template("login1.html", params=params)

@app.route('/edit/<string:sno>', methods=['GET','POST'])
def edit(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        if request.method=='POST':
            box_title = request.form.get('title')
            content = request.form.get('content')
            pro_link = request.form.get('pro_link')
            img_file = request.form.get('img_file')
            date=datetime.now()
            
            if sno == '0':
                project=Projects(title=box_title, content=content, pro_link=pro_link, img_file=img_file, date=date)
                db.session.add(project)
                db.session.commit()
            else:
                project=Projects.query.filter_by(sno=sno).first()
                project.title = box_title
                project.content = content
                project.pro_link = pro_link
                project.img_file = img_file
                project.date = date
                db.session.commit()
                return redirect('/edit/'+sno)
            
        project=Projects.query.filter_by(sno=sno).first()
        return render_template('edit.html', params=params, project=project, sno=sno)


@app.route('/editexp/<string:sno>', methods=['GET','POST'])
def editexp(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        if request.method=='POST':
            join_date = request.form.get('join_date')
            title = request.form.get('title')
            company_name = request.form.get('company_name')
            content = request.form.get('content')
            com_add = request.form.get('com_add')
            res_date = request.form.get('res_date')
            post_date=datetime.now()
            
            if sno == '0':
                expe=Expes(join_date=join_date, title=title, company_name=company_name, content=content, com_add=com_add, res_date=res_date, post_date=post_date)
                db.session.add(expe)
                db.session.commit()
            else:
                expe=Expes.query.filter_by(sno=sno).first()
                expe.join_date = join_date
                expe.title = title
                expe.company_name = company_name
                expe.content = content
                expe.com_add = com_add
                expe.res_date = res_date
                expe.post_date = post_date
                db.session.commit()
                return redirect('/editexp/'+sno)
            
        expe=Expes.query.filter_by(sno=sno).first()
        return render_template('editexp.html', params=params, expe=expe, sno=sno)


@app.route('/edc/<string:sno>', methods=['GET','POST'])
def edc(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        if request.method=='POST':
            cor_duration = request.form.get('cor_duration')
            clg_name = request.form.get('clg_name')
            clg_add = request.form.get('clg_add')
            cor_name = request.form.get('cor_name')
            cor_work = request.form.get('cor_work')
            content = request.form.get('content')
            post_date=datetime.now()
            
            if sno == '0':
                edc=Edcs(cor_duration=cor_duration, clg_name=clg_name, clg_add=clg_add, cor_name=cor_name, cor_work=cor_work, content=content, post_date=post_date)
                db.session.add(edc)
                db.session.commit()
            else:
                edc=Edcs.query.filter_by(sno=sno).first()
                edc.cor_duration = cor_duration
                edc.clg_name = clg_name
                edc.clg_add = clg_add
                edc.cor_name = cor_name
                edc.cor_work = cor_work
                edc.content = content
                post_date = datetime.now()
                db.session.commit()
                return redirect('/edc/'+sno)

        edc=Edcs.query.filter_by(sno=sno).first()
        return render_template('edc.html', params=params, edc=edc, sno=sno)

@app.route("/deletepr/<string:sno>" , methods=['GET', 'POST'])
def deletepr(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        project = Projects.query.filter_by(sno=sno).first()
        db.session.delete(project)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/deleteex/<string:sno>" , methods=['GET', 'POST'])
def deleteex(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        expe = Expes.query.filter_by(sno=sno).first()
        db.session.delete(expe)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/deleteed/<string:sno>" , methods=['GET', 'POST'])
def deleteed(sno):
    if "admin" in session and session['admin']==params['admin_user']:
        edc = Edcs.query.filter_by(sno=sno).first()
        db.session.delete(edc)
        db.session.commit()
    return redirect("/dashboard")

@app.route("/customer")
def customer():
    contact = Contacts.query.all()
    return render_template('customer.html', params=params, contacts=contact)


@app.route('/edituser/<string:id>', methods=['GET','POST'])
def edituser(id):
    if "admin" in session and session['admin']==params['admin_user']:
        if request.method=='POST':
            id = request.form.get('id')
            uname = request.form.get('uname')
            umail = request.form.get('umail')
            password = request.form.get('password')
            
            if id == '0':
                user=User(id=id, uname=uname, umail=umail, password=password)
                db.session.add(user)
                db.session.commit()
            else:
                user=User.query.filter_by(id=id).first()
                user.id = id
                user.uname = uname
                user.umail = umail
                user.password = password
                db.session.commit()
                return redirect('/edutuser/'+id)

        user=User.query.filter_by(id=id).first()
        return render_template('edituser.html', params=params,user=user, id=id)

@app.route("/deleteuser/<string:id>" , methods=['GET', 'POST'])
def deleteuser(id):
    if "admin" in session and session['admin']==params['admin_user']:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
    return redirect("/dashboard")



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('admin')
    return redirect("/dashboard")

@app.route('/logout1')
def logout1():
    session.pop('mail', None)  # Remove the user from the session
    return redirect('/')


@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        umail = request.form['umail']
        user = User.query.filter_by(umail=umail).first()

        if user:
            # Generate a reset token
            reset_token = secrets.token_hex(16)
            user.reset_token = reset_token
            db.session.commit()

            # Send Reset Email
            reset_link = url_for('reset_password', token=reset_token, _external=True)
            msg = Message("Password Reset Request",
                          sender=params['gmail-user'],
                          recipients=[umail]
                          )
            msg.body = f"Click the link below to reset your password:\n{reset_link}"
            mail.send(msg)

            flash("A password reset link has been sent to your email.", "success")
            return redirect('/login')
        else:
            flash("Email not found. Please enter a valid email.", "danger")

    return render_template("forgot_password.html")

# Reset Password Route
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()

    if not user:
        flash("Invalid or expired reset token.", "danger")
        return redirect('/login')

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = new_password  # Hash password in a real app
        user.reset_token = None  # Remove token after reset
        db.session.commit()

        flash("Your password has been successfully reset.", "success")
        return redirect('/login')

    return render_template("reset_password.html", token=token)


if __name__ == '__main__':
    app.run(debug=True)
