from worddata_Excel import create_word
from flask import Flask, render_template, redirect, url_for,request
#from models.models import db, MemberList #class名
import random
from flask_sqlalchemy import SQLAlchemy ###
from flask.globals import session
import worddata_Excel #自作関数

app = Flask(__name__)
app.secret_key = 'yokoyama' # secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.memberlist' ###
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ###

db = SQLAlchemy(app) ###

class MemberList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    comment = db.Column(db.String(128), nullable=False)

    def __init__(self, username=None, comment=None):
        self.username = username
        self.comment = comment

    def __repr__(self):
        #return '<UserName: %r  ' % (self.username)
        return f"id = {self.id}, username={self.username}"


member_list =[] #global変数
word_data = [] #wordデータ格納用
word_num = 0 #wordを選択番号

global_ulfnum = 0
genre_number = 0

member_vote_list = [] #投票用のリスト

word_Genre = ["一般","旅","食べ物"]


@app.route('/') # メインページ
def main():
    myname = session.get('username')

    if myname  is None:
        checkflg = 0
    else:
        checkflg = 1

    return render_template('main.html',checkflg = checkflg)


@app.route("/index",methods=["post"])
def post():

    if "username" not in session:
        session["username"] = request.form["username"]

    
    myname = session.get('username')
    #myname = request.form["username"]
    member_list.append(request.form["username"]) 

    new_member = MemberList(username=request.form["username"],comment="")
    db.session.add(new_member)
    db.session.commit()

    #class型MemberListへ代入
    #usr = MemberList(request.form["username"], 'はじめまして')
    #print("user--->", usr)
    #db.session.add(usr) # データを追加
    #db.session.commit()

    MemberList_DB = db.session.query(MemberList).all() #デバッグ用
    #print("kokokara MemberList_DB --->",MemberList_DB ,"\n") #デバッグ用
    #print("kokokara MemberList_DB[0] --->",MemberList_DB[0] ,"\n") #デバッグ用
    #print("kokokara MemberList_DB[0].username --->",MemberList_DB[0].username ,"\n") #デバッグ用
    print("word_Genre[0]->",word_Genre[0])
    return render_template('member_list.html', member_list =member_list , val = 0 , myname = myname ,MemberList_DB = MemberList_DB ,word_Genre = word_Genre)

@app.route('/reset2',methods=["post"]) # リセット
def reset2():
   
   global global_ulfnum
   if "username" in session:  # セッション情報があれば削除
        session.pop('username', None)

   session.clear
   member_list =[]
   global_ulfnum = 0
    
   return render_template('main.html')



@app.route('/reset1',methods=["post"]) # リセット
def reset1():
   
   if "username" in session:  # セッション情報があれば削除
        session.pop('username', None)

   session.clear

   #リセット処理のため（継続のため）
   global global_ulfnum
   global_ulfnum = 0
   global word_data #wordデータ格納用リセット
   word_data = []
   global word_num  #wordを選択番号
   word_num = 0
   global_ulfnum = 0
   global genre_number
   genre_number = 0
   global member_vote_list
   member_vote_list = [] #投票用のリスト

   db.session.query(MemberList).delete()
   db.session.commit()

   return render_template('main.html')
    


@app.route("/prepare",methods=["post"]) # 開始準備確認/親だけが実行する処理
def odai_warifuri(): 
    #お題割り振り処理
    global member_vote_list
    global global_ulfnum
    global word_data
    global word_num

    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all()
    
    if myname is None:
        print("ユーザ名がNoneになってしまっています")
        flg_none = '1'
    else:
        flg_none = '0'
    
    listsize  = len(MemberList_DB)
    member_vote_list =[0] * listsize #投票結果をリセット
  
    genre_number = int(request.form.get('genre_num'))
    print("genre_number→",genre_number) 

    global_ulfnum = random.randint(1,listsize) #ここでウルフを決定する.
    
    #print("ウルフNO → ",global_ulfnum,"ウルフ名 → ",MemberList_DB[global_ulfnum-1].username) 
    
    #### エクセルファイルからワードを引っ張ってくる処理（これも親だけの処理）
    [word_data,word_max_row_num] = create_word() #wordデータ生成
    word_num = random.randint(0,len(word_data)-1) #ランダムにワードデータを一つ選択
    #print("word_num,word_max_row_num -->",word_num,len(word_data)-1)
    #print("word_data[word_num][0](市民)-->",word_data[word_num][0])
    #print("word_data[word_num][1]（ウルフ）-->",word_data[word_num][1])

    return render_template('member_list_prepare.html',member_list =member_list, myname = myname , flg_none = flg_none ,MemberList_DB = MemberList_DB )


 ## お題配信する
@app.route("/odaihaishin",methods=["post"])
def odai_haishin():
     global word_data
     global global_ulfnum
     global word_num

     myname = session.get('username')
     MemberList_DB = db.session.query(MemberList).all() #DBからメンバーリストを割り当てる

     print("/odaihaishinnai ウルフNo→→　　",global_ulfnum)
     #print("request.form['action'] →→　　",int(request.form['action']))
     print("/odaihaishinnai word_num →→　　",word_num)

     print("/odaihaishinnai word_data[word_num][0](市民)-->",word_data[word_num][0])
     #print("word_data[word_num][1]（ウルフ）-->",word_data[word_num][1])


     if int(request.form['action']) == global_ulfnum: #ウルフのときの処理
            wordtheme = word_data[word_num][0]
            return render_template('odai.html',wordtheme = wordtheme,myname = myname,MemberList_DB = MemberList_DB)
    
     else:                                       #市民のときの処理
            wordtheme = word_data[word_num][1]
            return render_template('odai.html',wordtheme = wordtheme,myname = myname,MemberList_DB = MemberList_DB)

## 投票結果 
@app.route('/vote', methods=['POST']) 
def vote_result():
    global member_vote_list
    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all() #DBからメンバーリストを割り当てる

    global ulf_of_name
    votenumber = int(request.form.get('sel'))
    print("投票",votenumber)  #デバッグモード
    #print("ウルフNo    →→　　",global_ulfnum)
    print("投票数値リスト→",member_vote_list)  #デバッグモード
    
    member_vote_list[votenumber-1] = member_vote_list[votenumber-1] + 1
    print("投票数値リスト(更新)→",member_vote_list)  #デバッグモード

    ulf_of_name = MemberList_DB[global_ulfnum-1].username #ウルフの人の名前を代入
    
    return render_template('vote_result.html',member_vote_list = member_vote_list,ulf_of_name = ulf_of_name,myname = myname,MemberList_DB = MemberList_DB)


## ゲーム継続　→　メンバー一覧ページ　
@app.route('/repeat')
def game_repeat():

    #リセット処理のため（継続のため）
    global word_data #wordデータ格納用リセット
    word_data = []
    global word_num  #wordを選択番号
    word_num = 0
    global global_ulfnum
    global_ulfnum = 0
    global genre_number
    genre_number = 0
    global member_vote_list
    member_vote_list = [] #投票用のリスト
    
    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all()
    #print("member_list===> " ,member_list)
    return render_template('member_list.html',member_list =member_list,myname = myname,MemberList_DB=MemberList_DB, word_Genre = word_Genre)


## メンバー一覧ページ　
@app.route('/memberlist')
def load_member_list():

    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all()
    #print("member_list===> " ,member_list)
    return render_template('member_list.html',member_list =member_list,myname = myname,MemberList_DB=MemberList_DB, word_Genre = word_Genre)

## お題割り振りページ　（親以外のリンク用）
@app.route('/memberlist_prepare')
def memberlist_prepare():
    global global_ulfnum
    
    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all()
    
    if myname is None:
        print("ユーザ名がNoneになってしまっています")
        flg_none = '1'
    else:
        flg_none = '0'

    if global_ulfnum == 0:
        print("まだ親の人が開始ボタンを教えていません")
        return redirect(url_for('load_member_list'))
    else:
        return render_template('member_list_prepare.html',member_list =member_list,myname = myname,flg_none = flg_none,MemberList_DB = MemberList_DB)
   

## 投票結果　
@app.route('/result')
def result():
    myname = session.get('username')
    MemberList_DB = db.session.query(MemberList).all() #DBからメンバーリストを割り当てる

    return render_template('vote_result.html',member_vote_list = member_vote_list,ulf_of_name = ulf_of_name,myname = myname,MemberList_DB =MemberList_DB)

## 利用規約
@app.route('/terms') 
def terms_of_service():
    return render_template('terms.html')

## ページが間違うとmain
@app.errorhandler(404) 
def redirect_main_page(error):
    return redirect(url_for('main'))

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
