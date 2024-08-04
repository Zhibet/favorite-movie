from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuring the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-entries.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.String(2), nullable=False)
    image = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(450), nullable=False)


@app.route('/')
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars().all()
    for movie in movies:
        movie_img = movie.image
        print(movie_img)
    return render_template('index.html', movies=movies)


@app.route('/movie-form', methods=["GET", "POST"])
def form():
    if request.method == 'POST':
        form_data = request.form
        movie_title = form_data.get('name')
        rating = form_data.get('rating')
        image = form_data.get('url')
        description = form_data.get('description')

        new_movie = Movie(
            title=movie_title,
            rating=rating,
            image=image,
            description=description
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('movie_form.html')


@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == "POST":
        movie.title = request.form.get('title', movie.title)
        movie.rating = request.form.get('rating', movie.rating)
        movie.image = request.form.get('image', movie.image)
        movie.description = request.form.get('description', movie.description)

        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit_movie.html', movie=movie)


@app.route("/delete/<int:movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.get_or_404(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


# Create tables if they do not exist
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
