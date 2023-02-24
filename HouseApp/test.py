from flask import Flask, redirect, url_for, render_template,request,session
import ClickProperty,BleuBricks,DirectHome
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import json
import os
import plot
app = Flask(__name__)
# for sessions
app.secret_key = "dfhfyufnfhhfbf"
app.permanent_session_lifetime = timedelta(minutes=5)
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
    def __init__(self,email,password,question,answer):  # id will automatically appended
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
        res = dict['listings'].replace("\'", "\"")
        dictList = json.loads(res)
        listings = [dictList[list] for list in dictList.keys()]
    return render_template("listings.html", listings=listings)



@app.route('/analysis',methods = ["GET","POST"])
def analysis():

    path = "..\HouseApp\static"
    png_files = [f for f in os.listdir(path) if f.endswith('.png')]
    png_files = sorted(png_files, key=lambda fname: int(fname.split('.')[0]))

    return render_template("analysis.html",png_files=png_files,session=session)


@app.route('/register',methods = ["GET","POST"])
def register():
    return render_template("register.html")


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


@app.route('/controller',methods = ["GET","POST"])
def controller():
    if request.method == "GET":
        if request.args['request'] == "home":
            return redirect(url_for("home"))
        elif request.args['request'] == "listings":
            if len(request.args.getlist('locOption')) != 0:  # new options
                location = request.args.getlist('locOption')
                flatType = request.args.getlist('roomOption')
                bed = request.args.getlist('bedOption')
                bath = request.args.getlist('bathOption')
                minPrice = request.args['minPrice']
                maxPrice = request.args['maxPrice']
                minArea = request.args['minArea']
                maxArea = request.args['maxArea']
                session['locOption'] = location
                session['roomOption'] = flatType
                session['bedOption'] = bed
                session['bathOption'] = bath
                session['minPrice'] = minPrice
                session['maxPrice'] = maxPrice
                session['minArea'] = minArea
                session['maxArea'] = maxArea
            else:  # go back to original option state
                location = session['locOption']
                flatType = session['roomOption']
                bed = session['bedOption']
                bath = session['bathOption']
                minPrice = session['minPrice']
                maxPrice = session['maxPrice']
                minArea = session['minArea']
                maxArea = session['maxArea']
            extract = {"ClickProperty": ClickProperty.main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea),
                       "DirectHome": DirectHome.main(location, flatType, bed, bath, minPrice, maxPrice, minArea, maxArea)}
            # combine all the listing together so to sort them by increasing price later
            exList = [flat for key in extract.keys() for flat in extract[key]]
            listings = {}
            for index, x in enumerate(exList):  # this current user wishlist
                listings[str(index)] = x
            return redirect(url_for('listings',listings=listings))
        elif request.args['request'] == "analysis":

            if len(request.args.getlist('locOption')) != 0:  # new options
                location = request.args.getlist('locOption')
                flatType = request.args.getlist('roomOption')
                bed = request.args.getlist('bedOption')
                bath = request.args.getlist('bathOption')
                minPrice = request.args['minPrice']
                maxPrice = request.args['maxPrice']
                minArea = request.args['minArea']
                maxArea = request.args['maxArea']
                session['locOption'] = location
                session['roomOption'] = flatType
                session['bedOption'] = bed
                session['bathOption'] = bath
                session['minPrice'] = minPrice
                session['maxPrice'] = maxPrice
                session['minArea'] = minArea
                session['maxArea'] = maxArea
            else:  # go back to original option state
                location = session['locOption']
                flatType = session['roomOption']
                bed = session['bedOption']
                bath = session['bathOption']
                minPrice = session['minPrice']
                maxPrice = session['maxPrice']
                minArea = session['minArea']
                maxArea = session['maxArea']
            plot.main(location,flatType)
            return redirect(url_for("analysis"))
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
            found_user = users.query.filter_by(email=email).first() # in the user database->find->get filtered by() the first element
            if found_user:
                print("exist")
                session["email"] = found_user.email
            else:
                print("added")
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
                return redirect(url_for('home'))
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
                found_listing = listing.query.filter_by(link=link).first()
                if found_listing is None:
                    print("listing not found")
                    newListing = listing(link,listImg,area,room,bath,cost,address,companyImg)
                    db.session.add(newListing)
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


if __name__ == "__main__":
    from waitress import serve
    print("url: http://localhost:8080/")
    db.create_all() # create database if it doesn't exist
    # https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
    serve(app, host="0.0.0.0", port=8080)  # http://localhost:8080/

