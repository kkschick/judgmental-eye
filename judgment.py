from flask import Flask, render_template, redirect, request, flash, session, url_for
import model
from datetime import date

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user_list/", defaults={"page":1})
@app.route("/user_list/<int:page>")
def user_list(page):
    pages = (model.session.query(model.User).count()) / 50
    back_one = page - 1
    forward_one = page + 1
    user_list = model.session.query(model.User).limit(50).offset((page*50) -50).all()
    return render_template("user_list.html", users=user_list, pages=pages, back=back_one, forward=forward_one)

@app.route("/view_user/<int:id>")
def show_user_details(id):
    ratings = model.show_user_ratings(id)
    ratings_dict = {}
    for r in ratings:
        title = r.movie.title
        release = r.movie.release_date
        release = release.date()
        rating = r.rating
        movie_id = r.movie_id
        ratings_dict[r] = [title, release, rating, movie_id]
    age = ratings[0].user.age
    gender = ratings[0].user.gender
    zipcode = ratings[0].user.zipcode

    return render_template("view_user.html", ratings=ratings_dict, age=age, gender=gender, zipcode=zipcode)

@app.route("/view_movie/<int:id>")
def view_movie_details(id):
    movie_ratings = model.show_movie_details(id)
    title = movie_ratings[0].movie.title
    release = movie_ratings[0].movie.release_date
    release = release.date()
    imdb = movie_ratings[0].movie.imdb_url
    num_ratings = len(movie_ratings)
    total = 0
    for m in movie_ratings:
        total += m.rating
    average = float(total) / num_ratings

    if session['loggedIn']:
        rating = model.is_rating(session['user'].id, id)
        user = model.get_user_from_id(session['user'].id)
        movie = model.get_movie_from_id(id)
        prediction = None
        if rating:
            rating = rating.rating
        else:
            prediction = user.predict_rating(movie)
    else:
        rating = None
    return render_template("view_movie.html", title=title, release=release, imdb=imdb, 
           num_ratings=num_ratings, average=average, id=id, rating=rating, prediction=prediction)

@app.route("/add_rating", methods=["POST"])
def add_rating():
    rating = request.form.get("rating")
    movie_id = request.form.get("movie")
    if session['loggedIn']:
        user_id = session['user'].id
        model.add_rating(movie_id, user_id, rating)
        flash ("You've rated this movie")
        return redirect(url_for('show_user_details', id=user_id))
    else:
        flash ("You need to log in to rate this movie.")
        return redirect(url_for('view_movie_details', id=movie_id))

@app.route("/update_rating", methods=["POST"])
def update_rating():
    rating = request.form.get("rating")
    movie_id = request.form.get("movie")
    if session['loggedIn']:
        user_id = session['user'].id
        model.update_rating(movie_id, user_id, rating)
        flash ("You've changed your rating for this movie")
        return redirect(url_for('show_user_details', id=user_id))
    else:
        flash ("You need to log in to rate this movie.")
        return redirect(url_for('view_movie_details', id=movie_id))


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
        return redirect('/user_list')

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