from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.expression import func
from sqlalchemy import Integer, String
from forms import SearchForm, AddForm, DetailsForm
import requests
import os


app = Flask(__name__)
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['READ_TOKEN'] = os.environ.get('API_TOKEN')
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///movie-database.db")
Bootstrap5(app)

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_DETAILS_URL = "https://api.themoviedb.org/3/movie"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w500/"
API_HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {app.config['READ_TOKEN']}"
}

# CREATE DB


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[str] = mapped_column(String(250), nullable=False)
    category: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)

    # Optional: this will allow each movie object to be identified by its title when printed.
    def __repr__(self):
        return f'<Movie {self.title}>'


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/films')
def films():
    list_of_rows = db.session.execute(db.select(Movie).order_by(Movie.category, Movie.title)).scalars().all()
    return render_template('films.html', movies=list_of_rows)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.title.data
        response = requests.get(url=TMDB_SEARCH_URL, params={"query": name}, headers=API_HEADERS)
        data = response.json()["results"]
        return render_template("select.html", movies=data)
    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_url = f'{TMDB_DETAILS_URL}/{movie_api_id}'
        response = requests.get(url=movie_url, headers=API_HEADERS)
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            # The data in release_date includes month and day, we will want to get rid of.
            year=data["release_date"].split("-")[0],
            image_url=f"{TMDB_IMAGE_URL}{data['poster_path']}",
            description=(data["overview"][:245] + '..') if len(data["overview"]) > 245 else data["overview"]
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("edit", id=new_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = DetailsForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if request.method == "POST":
        movie.category = form.category.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        chosen_category = request.form.get('category')
        chosen_movies = db.session.execute(db.select(Movie).where(Movie.category == chosen_category).order_by(func.random()).limit(3)).scalars().all()
        bg_path = '/static/images/christmas-rom-com-background.png' if chosen_category == 'Christmas rom-com' else f'/static/images/{chosen_category}-background.png'
        return render_template('result.html', movies=chosen_movies, bg=bg_path)
    return render_template("search.html", form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('films'))


@app.route("/result", methods=["GET", "POST"])
def result():
    return render_template("result.html")


if __name__ == '__main__':
    app.run(debug=True)