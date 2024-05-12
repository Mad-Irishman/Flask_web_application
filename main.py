from datetime import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myProject.db'
dp = SQLAlchemy(app)


class Post(dp.Model):
    id = dp.Column(dp.Integer, primary_key=True)
    title = dp.Column(dp.String(300), nullable=False)
    text = dp.Column(dp.Text, nullable=False)
    created_at = dp.Column(dp.DateTime, default=datetime.utcnow)


@app.route("/all posts")
@app.route("/")
def home():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        text = request.form["text"]
        post = Post(title=title, text=text)

        try:
            dp.session.add(post)
            dp.session.commit()
        except:
            return "Error creating"

        return redirect("/")
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
