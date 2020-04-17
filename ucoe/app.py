import pyrebase
import json
from flask import *

config = {
    "apiKey": "AIzaSyB2R0KsX4nv0R-22hEy-Nwrs6FjL0BNnzw",
    "authDomain": "test-iaswum.firebaseapp.com",
    "databaseURL": "https://test-iaswum.firebaseio.com",
    "projectId": "test-iaswum",
    "storageBucket": "test-iaswum.appspot.com",
    "messagingSenderId": "1069995406208",
    "appId": "1:1069995406208:web:a8ea3bcd31ab9a13874765",
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
auth = firebase.auth()

admin_email = {"admin1@gmail.com": "password", "admin2@gmail.com": "password"}

# db.child("Names").push({"Name": "Utsav", "Email" : "utsav@gmail.com"})
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").update({"Name": "Utsav", "Email" : "maan@gmail.com"})
# users = db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").get()
# print(users.val())
# db.child("Names/Student Names/-M4w_T2u6lIePYjnq1Ht").remove()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
            # sname = db.child("Student Name").get()
            # to = sname.val()
            #return render_template("index.html", t=to.values())

        if request.form["submit"] == "login":
            email = request.form["email"]
            password = request.form["password"]
            try:
                login = auth.sign_in_with_email_and_password(email, password)
                users = db.child("Student Name").get()
                user = users.val()
                for key, values in user.items():
                    # return values
                    for inkey, invalues in values.items():
                        # return inkey
                        if email in invalues:
                            user_name = values["Name"].upper()
                            try:
                                news_get = db.child("News Updates").get()
                                return render_template(
                                    "index.html",
                                    news=news_get.val(),
                                    user_detail=user_name,
                                )
                            except:
                                return "Error Loading page please try again Later......"
                            #     return "NO NEWS FOUND"
                            # return render_template("index.html", user_detail=user_name)
                # return render_template("index.html", t=user)
            except:
                print("Wrong Pass")
                return "Wrong Email or Password"
            # print(login)

        elif request.form["submit"] == "pass":
            return render_template("forgotpass.html")

        elif request.form["submit"] == "forgotpass":
            email = request.form["email"]
            auth.send_password_reset_email(email)

        elif request.form["submit"] == "get":
            users = db.child("Student Name").get()
            a = users.val()
            # sub = json.loads(users.val())
            print(type(users.val()))
            return a

        elif request.form["submit"] == "add":
            headline = request.form["headline"]
            story = request.form["story"]
            db.child("News Updates").push(
                # {"Headline": headline, "Story": story,}
                {headline: story}
            )
            return render_template("login.html")

        elif request.form["submit"] == "news":
            try:
                news_get = db.child("News Updates").get()
                return render_template("news.html", news=news_get.val())
            except:
                return "NO NEWS FOUND"
            # news = news_get.val()

    return render_template("login.html")

@app.route("/register.html", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":

        if request.form["submit"] == "signup":
            name = request.form["name"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            password = request.form["password"]
            db.child("Student Name").push(
                {
                    "Name": name,
                    "Lastname": lastname,
                    "Email ID": email,
                    "Password": password,
                }
            )
            signup = auth.create_user_with_email_and_password(email, password)
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
