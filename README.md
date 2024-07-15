＜実行環境＞
python=3.8.19

conda install flask==3.0.3, flask-login==0.6.3, pytz

pip3 install flask_sqlalchemy==3.1.1, flask-bootstrap=3.3.7.1

＜DB作成＞
create_db.py で作成されるデータベースtest.db はinstance フォルダ内に作られるが、それをGeekTwitter 直下に置く必要がある
