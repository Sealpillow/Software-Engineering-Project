from flask import Flask, redirect, url_for, render_template,request
import ClickProperty,BleuBricks,DirectHome

listings = []
app = Flask(__name__)
# https://fontawesome.com/v4/icons/
# https://grantaguinaldo.com/rendering-variables-python-flask/
# https://stackoverflow.com/questions/67971131/how-to-access-and-display-specific-list-item-in-flask
# https://stackoverflow.com/questions/71224437/how-to-build-an-html-table-using-a-for-loop-in-flask
# https://imagekit.io/blog/how-to-resize-image-in-html/
@app.route("/",methods = ["GET","POST"])
def home():

    # listing.html
    # home.html
    return render_template("home.html")

# https://www.digitalocean.com/community/tutorials/processing-incoming-request-data-in-flask

@app.route("/listings",methods = ["GET","POST"]) # request.form -> dictionary
def listings():
    print(request)
    if request.method == "GET":
        if request.args['request'] == "analysis":
            return redirect(url_for("analysis"))
        if request.args['request'] == "listings":
            extract = {"ClickProperty": ClickProperty.main(),
                       "BleuBricks": BleuBricks.main(),
                       "DirectHome": DirectHome.main()}

            # combine all the listing together so to sort them by increasing price later
            listings = [flat for key in extract.keys() for flat in extract[key]]
            # for flat in listings:
            #     print(flat)
            return render_template("listings.html", listings=listings)
    return render_template(url_for("home"))


@app.route('/analysis',methods = ["GET","POST"])
def analysis():
    return render_template("analysis.html")


@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "GET":
        username = request.args['username']
        password = request.args['password']
        # check database here????????
        return username + password

    return render_template("home.html")


if __name__ == "__main__":
    from waitress import serve
    print("url: http://localhost:8080/")
    # https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
    serve(app, host="0.0.0.0", port=8080)  # http://localhost:8080/

