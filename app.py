from flask import Flask, render_template, redirect, url_for,request
import random

from flask.globals import session

app = Flask(__name__)
app.secret_key = 'yokoyama' # secret key


member_list2 = []
global_ulfnum = 0
global member_vote_list

@app.route('/') # メインページ
def main():
   
     return render_template('main.html')

@app.route('/reset1',methods=["post"]) # リセット
def reset1():
   global member_list2
   global global_ulfnum
   if "username" in session:  # セッション情報があれば削除
        session.pop('username', None)
    
   member_list2.clear
   member_list2 =[]
   global_ulfnum = 0
    
   return render_template('main.html',member_list2 = member_list2)
    
@app.route("/index",methods=["post"])
def post():

    global member_list2

    if "username" not in session:
        session["username"] = request.form["username"]
        
    myname = session.get('username')
    member_list2.append(myname) 
    #member_list3.append(2,username)

    return render_template('member_list.html', member_list2 =member_list2 , val = 0 , myname = myname)

@app.route("/prepare",methods=["post"]) # 開始準備確認
def odai_warifuri(): 
    #お題割り振り処理
    global member_vote_list
    global global_ulfnum
    global member_list2
    
    myname = session.get('username')
    
    if myname is None:
        print("ユーザ名がNoneになってしまっています")
        flg_none = '1'
    else:
        flg_none = '0'
    

    
    listsize = len(member_list2)
    global_ulfnum = random.randint(1,listsize) #ここでウルフを決定する.
    member_vote_list =[0] * listsize #投票結果をリセット
     #デバッグモード print("投票数値リスト→",member_vote_list) 
     #デバッグモード print([member_list2], listsize ,global_ulfnum,member_list2[global_ulfnum-1]) 
    print("ウルフNO → ",global_ulfnum,"ウルフ名 → ",member_list2[global_ulfnum-1]) 

    return render_template('member_list_prepare.html',member_list2 =member_list2, myname = myname , flg_none = flg_none )


 ## お題配信する
@app.route("/odaihaishin",methods=["post"])
def odai_haishin():
     global member_list2
     myname = session.get('username')
     print("ウルフNo→→　　",global_ulfnum)
     print("request.form['action'] →→　　",int(request.form['action']))
     if int(request.form['action']) == global_ulfnum: #ウルフのときの処理
            wordtheme = "ウルフ"
            return render_template('odai.html',wordtheme = wordtheme,member_list2 =member_list2,myname = myname)
    
     else:                                       #市民のときの処理
            wordtheme = "市民"
            return render_template('odai.html',wordtheme = wordtheme,member_list2 =member_list2,myname = myname)

## 投票結果 
@app.route('/vote', methods=['POST']) 
def vote_result():
    myname = session.get('username')
    global ulf_of_name
    votenumber = int(request.form.get('sel'))
    print("投票",votenumber)  #デバッグモード
    print("ウルフNo    →→　　",global_ulfnum)
    print("投票数値リスト→",member_vote_list)  #デバッグモード
    #member_vote_list[3] = 1
    member_vote_list[votenumber-1] = member_vote_list[votenumber-1] + 1
    print("投票数値リスト(更新)→",member_vote_list)  #デバッグモード

    ulf_of_name = member_list2[global_ulfnum-1] #ウルフの人の名前を代入
    
    return render_template('vote_result.html',member_list2 =member_list2,member_vote_list = member_vote_list,ulf_of_name = ulf_of_name,myname = myname)

## メンバー一覧ページ　
@app.route('/memberlist')
def load_member_list():
    global member_list2
    myname = session.get('username')
    return render_template('member_list.html',member_list2 =member_list2,myname = myname)

## お題割り振りページ　
@app.route('/memberlist_prepare')
def memberlist_prepare():
    myname = session.get('username')
    
    if myname is None:
        print("ユーザ名がNoneになってしまっています")
        flg_none = '1'
    else:
        flg_none = '0'

    return render_template('member_list_prepare.html',member_list2 =member_list2,myname = myname,flg_none = flg_none)

## 投票結果　
@app.route('/result')
def result():
    myname = session.get('username')
    return render_template('vote_result.html',member_list2 =member_list2,member_vote_list = member_vote_list,ulf_of_name = ulf_of_name,myname = myname)

## 利用規約
@app.route('/terms') 
def terms_of_service():
    return render_template('terms.html')

## ページが間違うとmain
@app.errorhandler(404) 
def redirect_main_page(error):
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)
