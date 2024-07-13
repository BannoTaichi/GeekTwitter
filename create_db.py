from app import app, db

with app.app_context():
    db.create_all()

# create_db.pyで作成されるデータベースtest.dbはinstanceフォルダ内に作られるが、それをGeekTwitter直下に置くと上手くいく
