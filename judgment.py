from flask import Flask, render_template, redirect, request, flash, session, url_for
import model
from sqlalchemy.orm import joinedload
from datetime import date

app = Flask(__name__)
app.secret_key = '23987ETFSDDF345560DFSASF45DFDF567'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user_list/", defaults={"page":1})
@app.route("/user_list/<int:page>")
def user_list(page):
    perpage = 50
    pages = (model.session.query(model.User).count()) / perpage
    back_one = page - 1
    forward_one = page + 1
    user_list = model.session.query(model.User).limit(perpage).offset((page*perpage) -perpage).all()
    return render_template("user_list.html", users=user_list, pages=pages, back=back_one, forward=forward_one)

@app.route("/view_user/<int:id>")
def show_user_details(id):
    user = model.session.query(model.User).filter_by(id=id).join(model.Rating).join(model.Movie).first()
    print user.id
    print user.age
    ratings = model.session.query(model.Rating).options(joinedload(model.Rating.movie)).filter_by(user_id=id).all()
    return render_template("view_user.html", user=user, ratings=ratings)

@app.route("/view_movie/<int:id>")
def view_movie_details(id):
    # movie_ratings = model.session.query(model.Rating).join(model.Movie).filter_by(id=id).all()
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

    user_id = session['user']
    if user_id:
        r = model.session.query(model.Rating).options(joinedload(model.Rating.movie)).filter_by(user_id=user_id, movie_id=id).first()
        prediction = None
        if r:
            user = r.user
            movie = r.movie
            rating = r.rating
            effective_rating = rating
        else:
            movie = model.get_movie_from_id(id)
            user = model.get_user_from_id(user_id)
            prediction = user.predict_rating(movie)
            rating = None
            effective_rating = prediction
    else:
        rating = None

    the_eye = model.get_the_eye()
    eye_rating = model.get_eye_rating(the_eye, id)

    if not eye_rating:
        eye_rating = the_eye.predict_rating(movie)
    else:
        eye_rating = eye_rating.rating

    difference = abs(eye_rating - effective_rating)

    messages = [ "I suppose you don't have such bad taste after all.",
             "I regret every decision that I've ever made that has brought me to listen to your opinion.",
             "Words fail me, as your taste in movies has clearly failed you.",
             "That movie is great. For a clown to watch. Idiot."]

    beratement = messages[int(difference)]
    return render_template("view_movie.html", title=title, release=release, imdb=imdb, 
           num_ratings=num_ratings, average=average, id=id, rating=rating, prediction=prediction, 
           beratement=beratement)

@app.route("/add_rating", methods=["POST"])
def add_rating():
    rating = request.form.get("rating")
    movie_id = request.form.get("movie")
    if session['user']:
        user_id = session['user']
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
    if session['user']:
        user_id = session['user']
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
        session['user'] = user.id
        # session['loggedIn'] = True
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
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)