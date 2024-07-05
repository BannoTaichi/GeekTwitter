from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)

# blog.dbという名前のデータベースを作成
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary_key : それぞれの投稿を判断する主Key
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = Post.query.all()
        return render_template("index.html", posts=posts)
    else:
        return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "GET":
        return render_template("create.html")

    elif request.method == "POST":
        title = request.form["title"]
        body = request.form.get("body")

        post = Post(title=title, body=body)  # インスタンス化
        db.session.add(post)  # データの追加
        db.session.commit()  # データの反映

        return redirect("/")  # redirect: "GET"メソッドでそのルートにつなぐことができる


@app.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
    post = Post.query.get(id)  # 引数idでインスタンス化
    if request.method == "GET":
        return render_template("update.html", post=post)

    else:
        post.title = request.form["title"]  # 内容の更新（上書き）
        post.body = request.form.get("body")

        db.session.commit()  # データの反映

        return redirect("/")  # redirect: "GET"メソッドでそのルートにつなぐことができる


@app.route("/<int:id>/delete", methods=["GET"])
def delete(id):
    post = Post.query.get(id)  # 引数idでインスタンス化
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
