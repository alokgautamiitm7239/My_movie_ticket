from flask import Flask , render_template,request,url_for,redirect
from .models import *
from flask import current_app as app
from datetime import datetime


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def signin():
    if request.method=="POST": #For validate user credential
        uname=request.form.get("user_name")
        pwd=request.form.get("password")
        usr=User_Info.query.filter_by(email=uname,password=pwd).first()
        if usr and usr.role==0: #Exisiting user and admin
            return redirect(url_for("admin_dashboard",name=uname))
        elif usr and usr.role==1:
            return redirect(url_for("user_dashboard",name=uname))
        else:       #If user doesn't exist
            return render_template("login.html",msg="Invalid User Credential.....")

    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def signup():
    if request.method=="POST": #For register new user
        uname=request.form.get("user_name")
        id=request.form.get("email")
        pwd=request.form.get("password")
        adrs=request.form.get("address")
        pin=request.form.get("pincode")
        usr=User_Info.query.filter_by(email=id).first()
        if usr:
           return render_template("login.html",msg="User is already exist.. try to login")
        new_usr=User_Info(full_name=uname,email=id,password=pwd,address=adrs,pin_code=pin)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="User registration is successfull try to login...")
    return render_template("Signup.html")

@app.route("/admin/<name>")
def admin_dashboard(name):
    theatres=get_theatre()
    shows=get_show()
    return render_template("admin.html",name=name ,theatres=theatres,shows=shows)

@app.route("/user/<name>")
def user_dashboard(name):
    return render_template("user.html",name=name)

#Route for the adding theatre
@app.route("/venue/<name>", methods=["GET","POST"])
def venue(name):
    if request.method=="POST": #For register new theatre
        tname=request.form.get("name")
        lcn=request.form.get("location")
        cpt=request.form.get("capacity")
        pin=request.form.get("pincode")
        new_theatre=Theatre(name=tname,location=lcn,capacity=cpt,pin_code=pin)
        db.session.add(new_theatre)
        db.session.commit()
        return render_template("add_venue.html",msg="Theatre added successfully", uname=name)

    return render_template("add_venue.html" ,uname=name)

#Route for the adding show
@app.route("/show/<tid>/<name>", methods=["GET","POST"])
def show(tid,name):
    if request.method=="POST": #For register new theatre
        sname=request.form.get("name")
        tags=request.form.get("tags")
        price=request.form.get("price")
        DateTime=request.form.get("d&t")  #Date input form is string
        dt_time=datetime.strptime(DateTime,"%Y-%m-%dT%H:%M") #this string pass time (strptime) convert into date format for the database
        id=request.form.get("id")
        new_show=Show(name=sname,tags=tags,tkt_price=price,data_time=dt_time,theatre_id=tid)
        db.session.add(new_show)
        db.session.commit()
        return render_template("add_show.html",msg="Show added successfully", uname=name,tid=tid)

    return render_template("add_show.html" ,uname=name,tid=tid)

#Theatre call function 
def get_theatre():
    theatres=Theatre.query.all()
    return theatres

def get_show():
    shows=Show.query.all()
    return shows
