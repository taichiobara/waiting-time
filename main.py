
import hashlib #暗号化
import datetime#現在時刻ゲットできる

from flask import *

from sqlalchemy import create_engine, Column, String, Integer, DATETIME #StringとIntegerはデータ型、create_engineでDBをつくる、Columnで列を定義、DATETIMEはその瞬間の時間
from sqlalchemy.ext.declarative import declarative_base #データベースのテーブルの親を作る
from sqlalchemy.orm import sessionmaker, scoped_session #sessionをつくる、

app = Flask(__name__) #flaskのお約束
engine = create_engine('sqlite:///app.db') #app.dbというdbをつくる
Base = declarative_base() #データベースのテーブルの親


class User(Base): #箱を作るイメージ # PythonではUserというクラスのインスタンスとしてデータを扱います
    __tablename__ = 'users' #テーブル名
    name = Column(String, primary_key=True, unique=True)#primary_keyはnullがが許容されない、tableにつき1個のみ
    #passw = Column(String) 

    def __repr__(self):
        return "User< {}, {}>".format(self.name)


class Content(Base): #箱を作るイメージ 
    __tablename__ = 'contents'
    id = Column(Integer, primary_key=True) # 整数型のid をprimary_key として、被らないようにします
    name = Column(String)
    content = Column(String)
    timestamp = Column(DATETIME)

    def __repr__(self):#デバッグ用？
        return "Content<{}, {}, {}, {}>".format(self.id, self.name, self.content, self.timestamp)

Base.metadata.create_all(engine) # 実際にデータベースを構築します
SessionMaker = sessionmaker(bind=engine) # Pythonとデータベースの経路です
session = scoped_session(SessionMaker)  # 経路を実際に作成しました


@app.route("/", methods=["GET", "POST"])#url指定
def main_page():
    cont = session.query(Content).all()  #htmlに渡すものを変数にしている。投稿のところ元のDBの情報
    
    if request.method == "GET":#getだとDBには何もしない
        return render_template("mainpage.html", cont=cont)

    user = session.query(User).get(request.form["name"].strip())  #userという変数に、Userという箱のnameの値以外の値を取ってきている。
    
    if user: #userがあった場合
        # if user.passw != str(hashlib.sha256(request.form["pass"].strip().encode("utf-8")).digest()): #合致しなかったら、、、何もしない
        #     return render_template("mainpage.html", cont=cont)

        student = session.query(Content).filter_by(name=request.form["name"]).first()
        student.content = request.form["content"]
        session.add(student)

        # コミット（変更を実行）
        session.commit()

        cont = session.query(Content).all()#contを定義しなおしている。
        return render_template("mainpage.html", cont=cont)

        
    else: #userがなかった場合
        user = User(name=request.form["name"])#userに名前とpassを入れている
        session.add(user)  #DBに追加
        #userがあって、合致した場合
        mess = Content(name=request.form["name"], content=request.form["content"], timestamp=datetime.datetime.now())
        session.add(mess)
        session.commit()
        cont = session.query(Content).all()#contを定義しなおしている。
        return render_template("mainpage.html", cont=cont)

    # #userがあって、合致した場合
    # mess = Content(name=request.form["name"], content=request.form["content"], timestamp=datetime.datetime.now())
    # session.add(mess)
    # session.commit()
    # cont = session.query(Content).all()#contを定義しなおしている。
    # return render_template("mainpage.html", cont=cont)


    # student = session.query(Content).filter_by(name=request.form["name"]).one()
    # student.score = "入れ替えたよ"
    # session.add(student)

    # # コミット（変更を実行）
    # session.commit()



if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True, host='0.0.0.0', port=8888, threaded=True)
