# python=3.8.19
# conda install flask==3.0.3, flask-login==0.6.3, pytz
# pip3 install flask_sqlalchemy==3.1.1, flask-bootstrap=3.3.7.1

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

from datetime import datetime
import pytz
import os


app = Flask(__name__)

# blog.dbという名前のデータベースを作成
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SECRET_KEY"] = os.urandom(24)
# os.urandomで暗号化のためのランダムな値を作成
# "SECRET_KEY"という環境変数に設定（入れなきゃいけない）
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)  # ログイン機能を持ったメソッドとappの紐づけ


class Post(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary_key : それぞれの投稿を判断する主Key
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo"))
    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        posts = Post.query.all()
        return render_template("index.html", posts=posts)
    else:
        return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form.get("password")

        user = User(
            username=username,
            password=generate_password_hash(password, method="scrypt"),
        )  # インスタンス化
        db.session.add(user)  # データの追加
        db.session.commit()  # データの反映

        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form.get("password")

        # usernameでフィルターをかけて合致したものを持ってくる
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required  # loginしているユーザーしかアクセスできない
def logout():
    logout_user()
    return redirect("/login")


@app.route("/create", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def delete(id):
    post = Post.query.get(id)  # 引数idでインスタンス化
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
