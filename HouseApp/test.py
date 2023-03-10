import numpy as np
from flask import Flask, redirect, url_for, render_template,request,session,flash
import ClickProperty,DirectHome,sendEmail
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import json
import os
import plot
import random
import string
app = Flask(__name__)
# for sessions
app.secret_key = "dfhfyufnfhhfbf"
# app.permanent_session_lifetime = timedelta(minutes=5)
# https://fontawesome.com/v4/icons/
# https://grantaguinaldo.com/rendering-variables-python-flask/
# https://stackoverflow.com/questions/67971131/how-to-access-and-display-specific-list-item-in-flask
# https://stackoverflow.com/questions/71224437/how-to-build-an-html-table-using-a-for-loop-in-flask
# https://imagekit.io/blog/how-to-resize-image-in-html/

# for sql
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications/33790196#33790196
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)

# relation between the 2 keys
user_wishlist = db.Table("wishlist",
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('listing_link',db.String(100),db.ForeignKey('listing.link'))
)


class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)  # primary to reference to other attribute
    # email = db.Column("name",db.String(sizeofString)),text of column="email"
    # email = db.Column(db.String(sizeofString)),text of column->follow the variable = "email"
    email = db.Column(db.String(100))  # will be assumed as attributes
    password = db.Column(db.String(100))
    question = db.Column(db.String(100))
    answer = db.Column(db.String(100))
    # db.relationship(obj,secondary=relationshipTable,backref = "bookmarked")
    wishlist = db.relationship("listing",secondary=user_wishlist,backref="bookmarked")
    # many-to-many relationship-> user can have multiple listings
    #                             listing can be bookmarked by multiple users

    # takes in variable to create an object
    def __init__(self,email,password,question,answer):  # id will automatically append
        self.email = email
        self.password = password
        self.question = question
        self.answer = answer


class listing(db.Model):
    # _id = db.Column("id",db.Integer,primary_key=True)  # primary to reference to other attribute
    # email = db.Column("name",db.String(sizeofString)),text of column="email"
    # email = db.Column(db.String(sizeofString)),text of column->follow the variable = "email"
    link = db.Column(db.String(100),primary_key=True)  # will be assumed as attributes
    listImg = db.Column(db.String(100))
    area = db.Column(db.String(100))
    room = db.Column(db.String(100))
    bath = db.Column(db.String(100))
    cost = db.Column(db.String(100))
    address = db.Column(db.String(100))
    companyImg = db.Column(db.String(100))
    # takes in variable to create an object
    def __init__(self,link,listImg,area,room,bath,cost,address,companyImg):  # id will automatically appended
        self.link = link
        self.listImg = listImg
        self.area = area
        self.room = room
        self.bath = bath
        self.cost = cost
        self.address = address
        self.companyImg = companyImg

@app.route("/",methods = ["GET","POST"])
def home():
    return render_template("home.html",session=session)

# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

@app.route("/listings",methods = ["GET","POST"]) # request.form -> dictionary
def listings():
    if request.method == "GET":
        dict = request.args.to_dict('listings')
        res = dict['listings'].replace("\'", "\"")  # replace char in string that contain ' to " so that json.load can covert it to json
        res = res.replace("\"s", "'s")  # incase there are strings that contain 's that was replaced to "s
        dictList = json.loads(res)
        listings = [dictList[list] for list in dictList.keys()]

        # display selected option based on input
        location = {"AngMoKio":0, "Bedok":0, "Bishan":0, "BukitBatok":0, "BukitMerah":0,
                    "BukitPanjang":0,"Bukit Timah":0,"CentralArea":0,"ChoaChuKang":0,"Clementi":0,
                    "Geylang":0,"Hougang":0,"JurongEast":0,"JurongWest":0,"KallangWhampoa":0,"MarineParade":0,
                    "PasirRis":0,"Punggol":0,"Queenstown":0,"Sembawang":0,"Sengkang":0,"Serangoon":0,"Tampines":0,
                    "ToaPayoh":0,"Woodlands":0,"Yishun":0}
        flatType = {"Room1":0, "Room2":0, "Room3":0, "Room4":0,"Room5":0}
        bed = {"bed1":0, "bed2":0, "bed3":0}
        bath = {"bath1":0,"bath2":0,"bath3":0,"bath4":0}

        for selectedLoc in session["locOption"]:
            selectedLoc = selectedLoc.replace(" ","")
            selectedLoc = selectedLoc.replace("/","")
            location[selectedLoc] = 1

        for selectedRoom in session["roomOption"]:
            selectedRoom = selectedRoom.replace(" ", "")
            flatType[selectedRoom[1:]+selectedRoom[0]] = 1

        for selectedBed in session["bedOption"]:
            bed["bed"+selectedBed] = 1

        for selectedBath in session["bathOption"]:
            bath["bath"+selectedBath] = 1
        selectedMinPrice = session['minPrice']
        selectedMaxPrice = session['maxPrice']
        selectedMinArea = session['minArea']
        selectedMaxArea = session['maxArea']
    return render_template("listings.html", listings=listings,location=location,flatType=flatType,bed=bed,bath=bath,selectedMinPrice=selectedMinPrice,selectedMaxPrice=selectedMaxPrice,selectedMinArea=selectedMinArea,selectedMaxArea=selectedMaxArea)




@app.route('/analysis',methods = ["GET","POST"])
def analysis():

    path = ".\static"
    png_files = [f for f in os.listdir(path) if f.endswith('.png')]
    png_files = sorted(png_files, key=lambda fname: int(fname.split('.')[0]))
    # display selected option based on input
    location = {"AngMoKio": 0, "Bedok": 0, "Bishan": 0, "BukitBatok": 0, "BukitMerah": 0,
                "BukitPanjang": 0, "Bukit Timah": 0, "CentralArea": 0, "ChoaChuKang": 0, "Clementi": 0,
                "Geylang": 0, "Hougang": 0, "JurongEast": 0, "JurongWest": 0, "KallangWhampoa": 0, "MarineParade": 0,
                "PasirRis": 0, "Punggol": 0, "Queenstown": 0, "Sembawang": 0, "Sengkang": 0, "Serangoon": 0, "Tampines": 0,
                "ToaPayoh": 0, "Woodlands": 0, "Yishun": 0}
    flatType = {"Room1": 0, "Room2": 0, "Room3": 0, "Room4": 0, "Room5": 0}
    bed = {"bed1": 0, "bed2": 0, "bed3": 0}
    bath = {"bath1": 0, "bath2": 0, "bath3": 0, "bath4": 0}

    for selectedLoc in session["locOption"]:
        selectedLoc = selectedLoc.replace(" ", "")
        selectedLoc = selectedLoc.replace("/", "")
        location[selectedLoc] = 1

    for selectedRoom in session["roomOption"]:
        selectedRoom = selectedRoom.replace(" ", "")
        flatType[selectedRoom[1:] + selectedRoom[0]] = 1

    for selectedBed in session["bedOption"]:
        bed["bed" + selectedBed] = 1
    for selectedBath in session["bathOption"]:
        bath["bath" + selectedBath] = 1
    selectedMinPrice = session['minPrice']
    selectedMaxPrice = session['maxPrice']
    selectedMinArea = session['minArea']
    selectedMaxArea = session['maxArea']

    return render_template("analysis.html",png_files=png_files,session=session,location=location,flatType=flatType,bed=bed,bath=bath,selectedMinPrice=selectedMinPrice,selectedMaxPrice=selectedMaxPrice,selectedMinArea=selectedMinArea,selectedMaxArea=selectedMaxArea)


@app.route('/register',methods = ["GET","POST"])
def register():
    if "registered" in session:
        flash("Account Already Registered")
    elif "newlyRegistered" in session:
        flash("Account created")

    return render_template("register.html",session=session)


@app.route('/accountDetail',methods = ["GET","POST"])
def accountDetail():
    if 'email' in session:
        return render_template("accountDetail.html",session=session)
    return redirect(url_for('home'))

@app.route('/wishlist',methods = ["GET","POST"])
def wishlist():
    if request.method == "GET":
        dict = request.args.to_dict('listings')
        res = dict['listings'].replace("\'", "\"")
        dictList = json.loads(res)
        listings = [dictList[list] for list in dictList.keys()]

    return render_template("wishlist.html", listings=listings)

@app.route('/deleteAccount',methods = ["GET","POST"])
def deleteAccount():
    return render_template("deleteAccount.html")


@app.route('/reset',methods = ["GET","POST"])
def reset():
    if "invalidAcc" in session:
        flash("Invalid Account")
    elif "wrongAnswer" in session:
        flash("Wrong Answer")
    elif "resetted" in session:
        flash("Password Resetted")
    return render_template("resetPassword.html",session=session)

@app.route('/controller',methods = ["GET","POST"])
def controller():
    global setup, result
    if request.method == "GET":
        if "registered" in session:  # it removes existing session of "registered", will be set again if requirement met again
            session.pop("registered", None)
        if "validAcc" in session:  # it removes existing session of "validAcc", will be set again if requirement met again
            session.pop("validAcc", None)
        if "invalidAcc" in session:  # it removes existing session of "invalidAcc", will be set again if requirement met again
            session.pop("invalidAcc", None)
        if "resetted" in session:  # it removes existing session of "resetted", will be set again if requirement met again
            session.pop("resetted", None)
        if "newlyRegistered" in session:  # it removes existing session of "newlyRegistered", will be set again if requirement met again
            session.pop("newlyRegistered", None)
        if request.args['request'] == "home":
            session['prevUrl'] = "home"
            return redirect(url_for("home"))

        elif request.args['request'] == "listings":
            listings = {}
            if len(request.args.getlist('locOption')) != 0:  # user new input options
                location = request.args.getlist('locOption')
                flatType = request.args.getlist('roomOption')
                bed = request.args.getlist('bedOption')
                bath = request.args.getlist('bathOption')
                minPrice = request.args['minPrice']
                maxPrice = request.args['maxPrice']
                minArea = request.args['minArea']
                maxArea = request.args['maxArea']

                if not setup:  # if session variables not setup, set the variables as empty
                    session['locOption'] = " "
                    session['roomOption'] = " "
                    session['bedOption'] = " "
                    session['bathOption'] = " "
                    session['minPrice'] = " "
                    session['maxPrice'] = " "
                    session['minArea'] = " "
                    session['maxArea'] = " "
                    session['prevUrl'] = " "
                    setup = True
                # if any of the new input option chosen is not the same as the past, set the session variable
                if not result or session['locOption'] != location or session['roomOption'] != flatType or session['bedOption'] != bed or session['bathOption'] != bath or session['minPrice'] != minPrice or session['maxPrice'] != maxPrice or session['minArea'] != minArea or session['maxArea'] != maxArea:
                    session['locOption'] = location
                    session['roomOption'] = flatType
                    session['bedOption'] = bed
                    session['bathOption'] = bath
                    session['minPrice'] = minPrice
                    session['maxPrice'] = maxPrice
                    session['minArea'] = minArea
                    session['maxArea'] = maxArea
                    # generate new listings, by web scraping
                    extract = {"ClickProperty": ClickProperty.main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea),
                               "DirectHome": DirectHome.main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea)}
                    # combine all the listing together so to sort them by increasing price later
                    exList = [flat for key in extract.keys() for flat in extract[key]]
                    for index, x in enumerate(exList):  # array is converted to dict so that it can be transferred to other app route via request.args.to_dict()
                        listings[str(index)] = x
                    result = listings  # store newly generated listings to result
                else:  # option chosen is the same as the past
                    listings = result  # set listings to the prev listing result
            else:  # go back to original option state
                listings = result  # set listings to the prev listing result
            session['prevUrl'] = "listings"
            return redirect(url_for('listings',listings=listings))

        elif request.args['request'] == "analysis":
            if len(request.args.getlist('locOption')) != 0:  # user new input options
                location = request.args.getlist('locOption')
                flatType = request.args.getlist('roomOption')
                bed = request.args.getlist('bedOption')
                bath = request.args.getlist('bathOption')
                minPrice = request.args['minPrice']
                maxPrice = request.args['maxPrice']
                minArea = request.args['minArea']
                maxArea = request.args['maxArea']

                if not setup:  # if session variables not setup, set the variables as empty
                    session['locOption'] = " "
                    session['roomOption'] = " "
                    session['bedOption'] = " "
                    session['bathOption'] = " "
                    session['minPrice'] = " "
                    session['maxPrice'] = " "
                    session['minArea'] = " "
                    session['maxArea'] = " "
                    session['prevUrl'] = " "
                    setup = True
                # if any of the new input option chosen is not the same as the past, set the session variable
                if session['locOption'] != location or session['roomOption'] != flatType or session['prevUrl'] == "listings":
                    session['locOption'] = location
                    session['roomOption'] = flatType
                    session['bedOption'] = bed
                    session['bathOption'] = bath
                    session['minPrice'] = minPrice
                    session['maxPrice'] = maxPrice
                    session['minArea'] = minArea
                    session['maxArea'] = maxArea
                    # generate new analysis
                    plot.main(location,flatType)
            session['prevUrl'] = "analysis"
            return redirect(url_for("analysis"))
        elif request.args['request'] == 'sortAscend':
            listings = dict(sorted(result.items(), key=lambda x: int(x[1][5].replace(",","").replace("$",""))))  # remove all the '$' and ',' and convert to int for comparison
            session['prevUrl'] = "listings"
            return redirect(url_for('listings', listings=listings))
        elif request.args['request'] == 'sortDescend':
            listings = dict(sorted(result.items(), key=lambda x: -int(x[1][5].replace(",","").replace("$",""))))  # remove all the '$' and ',' and convert to int for comparison
            session['prevUrl'] = "listings"
            return redirect(url_for('listings', listings=listings))
        elif request.args['request'] == "accountDetail":
            return redirect(url_for("accountDetail"))
        elif request.args['request'] == "wishlist":
            if "email" in session:
                found_user = users.query.filter_by(email=session["email"]).first()  # in the user database->find->get filtered by() the first element
                listings= {}
                for index,x in enumerate(found_user.wishlist):  # this current user wishlist
                    listings[str(index)]=[x.link, x.listImg, x.area, x.room, x.bath, x.cost, x.address, x.companyImg]
                print(listings)
                return redirect(url_for("wishlist",listings=listings))
            return redirect(url_for("home"))
        elif request.args['request'] == "deleteAccount":
            return redirect(url_for("deleteAccount"))
        elif request.args['request'] == "delete":
            email = request.args["email"]
            password = request.args["password"]
            found_user = users.query.filter_by(email=email)
            if found_user is None:
                print("user not found")
                return redirect(url_for("accountDelete"))
            else:
                print("account deleted")
                found_user.delete()
                db.session.commit()
                session.pop('email',None)
                return redirect(url_for("home"))
        elif request.args['request'] == "register":
            return redirect(url_for("register"))
        elif request.args["request"] == "registerUser":
            email = request.args["email"]
            password = request.args["password"]
            question = request.args['question']
            answer = request.args['answer']
            found_user = users.query.filter_by(email=email).first()  # in the user database->find->get filtered by() the first element
            if found_user:
                print("exist")
                session["registered"] = " "
                return redirect(url_for('register'))
            else:
                print("added")
                session["newlyRegistered"] = " "
                newUser = users(email,password,question,answer)
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for('register'))
        elif request.args['request'] == "login":
            email = request.args['email']
            password = request.args['password']
            # check database here
            found_user = users.query.filter_by(email=email,password =password).first()  # in the user database->find->get filtered by() the first element
            if found_user:
                print("exist")
                session["email"] = found_user.email
                session["password"] = found_user.password
                session["maskPassword"] = "*"*len(session["password"])
                session.permanent = True
                if 'prevUrl' not in session:
                    return redirect(url_for('home'))
                elif session['prevUrl'] == "listings":
                    return redirect(url_for("controller",request="listings"))
                elif session['prevUrl'] == "analysis":
                    return redirect(url_for("controller",request="analysis"))

            else:
                print("not found")
            return redirect(url_for('home'))
        elif request.args['request'] == "logout":
            session.pop("email",None)
            return redirect(url_for("home"))
        elif request.args['request'] == "changePassword":
            email = session['email']
            newPassword = request.args["newPassword"]
            found_user = users.query.filter_by(email=email).first()  # in the user database->find->get filtered by() the first element
            if found_user:
                session['password'] = newPassword
                session["maskPassword"] = "*" * len(session["password"])
                print("password changed")
                found_user.password = newPassword
                db.session.commit()
            else:
                print("user not found")
            return redirect(url_for("accountDetail"))
        elif "AddToWishList" in request.args['request']:
            if "email" in session:
                info = request.args['request'].split("*")  # split the listing information to be added to database
                link = info[1]
                listImg = info[2]
                area = info[3]
                room = info[4]
                bath = info[5]
                cost = info[6]
                address = info[7]
                companyImg = info[8]
                found_user = users.query.filter_by(email=session["email"]).first()  # in the user database->find->get filtered by() the first element
                found_listing = listing.query.filter_by(link=link).first()  # check if listing selected in database
                if found_listing is None:  # if listing selected is not in database
                    print("listing not found")
                    newListing = listing(link,listImg,area,room,bath,cost,address,companyImg)  # create new listing entry
                    db.session.add(newListing)   # add it to database
                    found_listing = newListing
                found_user.wishlist.append(found_listing)
                db.session.commit()
            return redirect(url_for("controller",request="listings"))
        elif "DeleteFromWishList" in request.args['request']:
            if "email" in session:
                print("listing deleted")
                link = request.args['request'][18:]
                found_user = users.query.filter_by(email=session["email"]).first()  # in the user database->find->get filtered by() the first element
                found_listing = listing.query.filter_by(link=link).first()
                found_user.wishlist.remove(found_listing)
                db.session.commit()
                listings = {}
                for index, x in enumerate(found_user.wishlist):  # this current user wishlist
                    listings[str(index)] = [x.link, x.listImg, x.area, x.room, x.bath, x.cost, x.address, x.companyImg]
                return redirect(url_for("wishlist",listings=listings))
        elif request.args['request'] == "checkAcc":
            email = request.args['email']
            found_user = users.query.filter_by(email=email).first()
            if found_user:
                session["validAcc"] = " "
                session["question"] = found_user.question
                session["answer"] = found_user.answer
                session["temp"] = found_user.email
                print(session["question"])
                print(session["answer"])
            else:
                session["invalidAcc"] = " "
            return redirect(url_for("reset"))
        elif request.args['request'] == "resetPassword":
            answer = request.args["answer"]
            email = session["temp"]
            if answer == session["answer"]:
                found_user = users.query.filter_by(email=email).first()  # in the user database->find->get filtered by() the first element
                print("password resetted")
                session["resetted"] = " "
                session.pop("validAcc",None)
                # define the possible characters for the password
                characters = string.ascii_letters + string.digits + string.punctuation
                # define the length of the password
                length = 12
                # generate the password
                newPassword = ''.join(random.choice(characters) for i in range(length))
                found_user.password = newPassword  # what to set as random password
                db.session.commit()
                sendEmail.main(email,newPassword)
            else:
                session["wrongAnswer"] = " "
            return redirect(url_for("reset"))


if __name__ == "__main__":
    from waitress import serve
    print("url: http://localhost:8080/")
    setup = False  # indication of initial setup is done
    result = {}  # contain current extracted result
    with app.app_context():
        db.create_all()  # create database if it doesn't exist
    # https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
    serve(app, host="0.0.0.0", port=8080)  # http://localhost:8080/

