Judgmental Eye: A Movie Rating App
===================================

####The Project

The Judgmental Eye is a movie ratings application where users can log in and rate movies they have seen. 

It uses machine learning to predict how a user will rate a movie they have not yet seen. 

####Table of Contents
- [Technologies Used](#technologies-used)
- [How It Works](#how-it-works)
- [Product Screenshots](#product-screenshots)
- [Try It Yourself!] (#try-it-yourself)

####Technologies Used

The Judgmental Eye was written using Python, Flask, HTML, CSS, Twitter Bootstrap, SQLAlchemy, and Postgres.

It also uses machine learning (a Pearson correlation) and the MovieLens dataset, which contains 100,000 ratings of 1,700 movies from 1,000 users.

![Landing page](/static/screenshots/landingpage.png)

####How It Works

Users can create accounts, log in, and begin rating movies. Movies a user has rated are displayed in My Movie Profile. Users have the ability to rate movies they have not yet seen, and to update their ratings of movies they have seen.

If a user has not yet rated a movie, the Judgmental Eye algorithm uses machine learning to predict how the user will rate it, based on other ratings. The more movies a user rates, the better the Judgmental Eye can predict which movies he/she will or will not enjoy.

####Product Screenshots

View your movie profile to see movies you have rated

![Movie profile](/static/screenshots/movieprofile.png)

The Judgmental Eye will predict how you will rate a movie you have not yet rated

![Rating prediction](/static/screenshots/ratingprediction.png)

The Judgmental Eye will also judge you on your predictions

![Positive judgment](/static/screenshots/eyejudgmentpositive.png)
![Negative judgment](/static/screenshots/eyejudgmentnegative.png)

View other users' movie profiles

![View other users](/static/screenshots/viewotherusers.png)


####Try It Yourself!

#####Environment 

1) Clone the repository:

<pre><code>$ git clone https://github.com/kkschick/JudgmentalEye.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ . env/bin/activate 
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>

#####Database

1) To run the Postgres server, download and run [postgres.app](http://postgresapp.com/), and follow the instructions to set up Postgres on your machine—[instructions for Mac](http://postgresapp.com/documentation/cli-tools.html).  

2) Create the database in PostgreSQL:

<pre><code>$ psql
# CREATE DATABASE movies;
</code></pre>

3) Still in your virtual environment, create the database tables and seed the standards table:

<pre><code>(env)$ python model.py
(env)$ python seed.py
</code></pre>

4) Run the app: 

<pre><code>(env)$ python judgment.py
</code></pre>

5) Point your browser to:

<pre><code>http://localhost:5000/</code></pre>
