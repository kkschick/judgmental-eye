from flask import Flask, render_template, redirect, request, flash, session
import model

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'

@app.route("/")
def index():
    return render_template("base.html")



# @app.route("/user_list")
# def show_users():
#     user_list = model.session.query(model.User).limit(50).offset(0).all()
#     # num_users = model.session.query(model.User).count()
#     # record = 0
#     # page = 0
#     # while record < num_users:
#     #     user_list = model.session.query(model.User).limit(50).offset(record).all()
#     #     record += 50
#     #     page += 1
#     #     user_list(page)
#     return render_template("user_list.html", users=user_list)

@app.route("/user_list/", defaults={"page":1})
@app.route("/user_list/<int:page>")
def user_list(page):
    pages = (model.session.query(model.User).count()) / 50
    back_one = page - 1
    forward_one = page + 1
    user_list = model.session.query(model.User).limit(50).offset((page*50) -50).all()
    return render_template("user_list.html", users=user_list, pages=pages, back=back_one, forward=forward_one)
#     # num_users = model.session.query(model.User).count()
#     # record = 0
#     # while record < num_users:
#     #     user_list = model.session.query(model.User).limit(50).offset(record).all()
#     #     record += 50
#     #     page += 1
#     return render_template("user_list.html", users=user_list)


@app.route("/login")
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = model.get_user_from_email(email)

    if user == None:
        flash ("This customer is not registered yet")
        return redirect('signup')
    else:
        session['user'] = user
        session['loggedIn'] = True
        return redirect('/')

@app.route("/signup")
def show_signup():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def make_new_account():
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    gender = request.form.get("gender")
    zipcode = request.form.get("zipcode")    
    model.create_user(email, password, gender, zipcode, age)
    flash ("You're registered! Now please log in")
    return redirect('/login')

@app.route("/logout")
def process_logout():
    session.clear()
    session['loggedIn'] = False
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)