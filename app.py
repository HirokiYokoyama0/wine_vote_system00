
from flask import Flask, render_template, send_file, redirect , request
from flask_sqlalchemy import SQLAlchemy
from flask.globals import session
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

import json

from sqlalchemy.sql.elements import Null
import numpy as np

from charts import get_main_image



app = Flask(__name__)
app.secret_key = 'yokoyama' # secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_memberlist.sqlite' ###
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ###

db = SQLAlchemy(app) ### for userdata
#db = SQLAlchemy(app) ### for WineListdata
#db3 = SQLAlchemy(app) ### for Assecementdata

class Member(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    selfintro = db.Column(db.String(256), nullable=True)
    # One to Many
    #assessment2 = db.relationship('Assecementdata2', backref='members',  uselist=False)
    assessment2 = db.relationship('Assecementdata2', backref='members',lazy=True)

    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        if self.assessment2:
            return f"Member name = {self.name} "
        else:
            return f"Member name = {self.name}"


class WineListdata(db.Model):
    __tablename__ = 'winelist'

    id = db.Column(db.Integer, primary_key=True)
    Brandname = db.Column(db.String(256), nullable=True)
    Grapevarieties = db.Column(db.String(128), nullable=True)
    OtherInfo = db.Column(db.String(256), nullable=True)
    Score_overall = db.Column(db.Integer, nullable=False)
    Selectedflg = db.Column(db.Integer, nullable=True)

    #assessment2 = db.relationship('Assecementdata2', backref='winelist',  lazy='dynamic') #Assecementdataとのリレーション
    #assessment2 = db.relationship('Assecementdata2', backref='winelist', lazy=True) 
    #assessment2 = db.relationship('Assecementdata2', backref='winelist', uselist=False) #Assecementdataとのリレーション
    assessment2 = db.relationship('Assecementdata2', backref='winelist',  lazy='select')

    def __init__(self, Brandname = '' ,Grapevarieties = '',OtherInfo = '',Score_overall = 0):
        self.Brandname = Brandname
        self.Grapevarieties = Grapevarieties
        self.OtherInfo = OtherInfo
        self.Score_overall = Score_overall

    def __str__(self):
        if self.assessment2:
            return f"Brandname name = {self.Brandname} is now {self.assessment2.maincomment}"
        else:
            return f"Brandname name = {self.Brandname}, has no company"

    def toDict(self):
        return {
        'id': self.id,
        'Brandname': self.Brandname,
        'Grapevarieties': self.Grapevarieties
        }

    def toDict2(self):
        model = {}
        for column in self.__table__.columns:
            model[column.name] = str(getattr(self, column.name))
        return model
          
    def __repr__(self):
        return f"id = {self.id},Brandname = {self.Brandname}, Grapevarieties={self.Grapevarieties}, Score_overall = {self.Score_overall}"
            
        
class Assecementdata2(db.Model):

    __tablename__ = 'assessment2'

    id = db.Column(db.Integer, primary_key=True)
    maincomment = db.Column(db.Text)
    score1_spicy = db.Column(db.Integer, nullable=True)
    score2_acidity = db.Column(db.Integer, nullable=True)
    score3_total = db.Column(db.Integer, nullable=True)

    # 外部キー
    members_id = db.Column(db.Integer, db.ForeignKey('members.id'))
    wine_id = db.Column(db.Integer, db.ForeignKey('winelist.id')) #外部キー

    def __init__(self, maincomment, members_id,wine_id):
        self.maincomment = maincomment
        self.members_id = members_id
        self.wine_id =wine_id

@app.route('/') # メインページ
def main():
 
    return render_template('main.html')


@app.route("/debug_resetall") #データリセット
def debug_resetall():

     #リセット処理のため
    db.session.query(Member).delete()
    db.session.query(WineListdata).delete() 
    db.session.query(Assecementdata2).delete()  
    db.session.commit()

    return render_template('main.html')


@app.route("/debug_preset") #データプリセット
def debug_preset():

    # create Member
    tom = Member('Tom')
    nancy = Member('Nancy')
    hiroki = Member('Hiroki')
    # add members
    db.session.add_all([tom,nancy,hiroki])
    db.session.commit()

    new_Wine1 = WineListdata(Brandname = 'カデ・ドック・シャルドネ' ,Grapevarieties = 'シャルドネ',OtherInfo = '',Score_overall = 0)
    new_Wine2 = WineListdata(Brandname = 'エノテカ　シャルドネ' ,Grapevarieties = 'シャルドネ',OtherInfo = '',Score_overall = 0)
    new_Wine3 = WineListdata(Brandname = 'マプ・ソーヴィニヨン・ブラン' ,Grapevarieties = 'ソーヴィニヨン',OtherInfo = '',Score_overall = 0)
    db.session.add_all([new_Wine1,new_Wine2,new_Wine3])
    db.session.commit()

    ###  これは検証用ダミーデータ
    #使い方：Assecementdata2('コメント、なんか最高かもしれない',Employee_id,Wind_id)
    data1=Assecementdata2('mem_id:1 wine_id:1のコメントです',1,1)
    data1.score1_spicy=3
    data1.score2_acidity=3
    data1.score3_total=4.3

    data2=Assecementdata2('mem_id:1 wine_id:2のコメントです',1,2)
    data2.score1_spicy=3.2
    data2.score2_acidity=3.2
    data2.score3_total=3.2
    
    data3=Assecementdata2('mem_id:4 wine_id:1のコメントです',3,1)
    data3.score1_spicy=4.2
    data3.score2_acidity=4.2
    data3.score3_total=4.7
    
    data4=Assecementdata2('mem_id:4 wine_id:3のコメントです',3,3)
    data4.score1_spicy=5
    data4.score2_acidity=5
    data4.score3_total=5

    data5=Assecementdata2('mem_id:4 wine_id:4のコメントです',3,4)
    data5.score1_spicy=1
    data5.score2_acidity=1
    data5.score3_total=1

    db.session.add_all([data1, data2,data3,data4,data5])
    db.session.commit()

    return render_template('main.html')

        

@app.route("/index",methods=["post"])
def index():

    if "username" not in session:
        session["username"] = request.form["username"]

    
    myname = session.get('username')

    # create Member
    myname2 = Member(myname)
 
    # add members
    db.session.add(myname2)
    db.session.commit()

  
    return render_template('wine_register.html')




@app.route("/wine_register") #登録画面表示
def wine_register():
    return render_template('wine_register.html')

@app.route("/wine_register_add",methods=['POST']) #登録（ワイン追加）
def wine_register_add():

    Brandname=request.form["Brandname"]
    #print(request.form['Grapevarieties'])
    #print(request.form.get['Grapevarieties'])
    Grapevarieties=request.form['Grapevarieties']
    Vintage=request.form["Vintage"]
    
    new_Wine = WineListdata(Brandname = Brandname ,Grapevarieties = Grapevarieties ,OtherInfo = Vintage ,Score_overall = 0)
    db.session.add(new_Wine)
    db.session.commit()

    return render_template('wine_register.html')

@app.route("/winelist")
def winelist():


    WineListdata_one = db.session.query(WineListdata).first()
    WineListdata_all = db.session.query(WineListdata).all()
    """
    bbbb=WineListdata_one.toDict2()
    bbbb['id']=int(bbbb['id'])
    print("bbbb->",bbbb)
    print("bbbbt->",type(bbbb))
    print("bbbb2->",bbbb['id'])
    """

    eee = []
    for member in WineListdata_all:
        Wineinfo=member.toDict2()
        Wineinfo['id']=int(Wineinfo['id'])
        eee.append(Wineinfo)
    

    print("1",eee)
    print("2",type(eee))
  
    inputjson_from_python =  [{'id': 1, 'Brandname':'カデ・ドック・シャルドネ', 'Grapevarieties': 'シャルドネ', 'OtherInfo':'test', 'Score_overall':3}]
    print("3",inputjson_from_python)
    print("4",type(inputjson_from_python))
    

    return render_template('winelist_show.html',inputjson_from_python=inputjson_from_python,eee=eee)


@app.route('/register', methods=['POST'])
def set_data():
    text1 = request.form['text1']
    text2 = request.form['text2']

    print("ajax通信で戻ってきたよ→",text1,text2)

    # 一旦セレクトフラグを全リセットする
    WineListdataAll = db.session.query(WineListdata).all()

    for wine in WineListdataAll:
        wine.Selectedflg=0

    db.session.commit()

    # 戻ってきたデータのみをセレクトフラグを立てる
    content1 = db.session.query(WineListdata).filter_by(Brandname = text1).first()
    content2 = db.session.query(WineListdata).filter_by(Brandname = text2).first()

    content1.Selectedflg=1
    content2.Selectedflg=1

    db.session.commit()

    #content1_2 = db.session.query(Assecementdata).filter_by(id = content1.id).first()
    #content1_2.selectedflg=1

    #content2_2 = db.session.query(Assecementdata).filter_by(id = content2.id).first()
    #content2_2.selectedflg=1

    
    return render_template('chart7_bubble.html')

@app.route('/prepare', methods=['POST'])
def prepare():

    return render_template('chart7_bubble.html')


@app.route("/okuru")
def okuru():
    return render_template('test1.html')

@app.route("/hyouka") #評価画面表示
def hyouka():

    myname = session.get('username')

    wine_selected = db.session.query(WineListdata).filter_by(Selectedflg=1).all()

    return render_template('hyouka.html',myname = myname,wine_selected=wine_selected)


@app.route('/hyouka_regi', methods=['POST'])  #評価画面表示-登録
def hyouka_regi():

    myname = session.get('username')

    
    score1_spicy = int(request.form.get('score1_spicy'))
    score2_acidity = int(request.form.get('score2_acidity'))
    score3_total = int(request.form.get('score3_total'))
    comment = request.form.get('comment')

    wind_id = int(request.form.get('action'))
    user_id = db.session.query(Member).filter_by(name = myname).first()

    print("score1_spicy--->",score1_spicy)
    print("wind_id--->",wind_id)
    print("user_id--->",user_id.id)

    
    asse_update = db.session.query(Assecementdata2).filter_by(members_id=user_id.id,wine_id=wind_id).first()

    if asse_update is None: #新規評価追加
        asdata=Assecementdata2(comment,user_id.id,wind_id)
        asdata.score1_spicy=score1_spicy
        asdata.score2_acidity=score2_acidity
        asdata.score3_total=score3_total
     
        db.session.add(asdata)
    else:
        asse_update.maincomment=comment #既存評価更新
        asse_update.score1_spicy=score1_spicy
        asse_update.score2_acidity=score2_acidity
        asse_update.score3_total=score3_total

    db.session.commit()

    

   

    ## セレクトされているWineListdata
    wine_selected = db.session.query(WineListdata).filter_by(Selectedflg=1).all()

     ## WineListdataとAssecementdataを結合
    allwinelist = db.session.query(WineListdata).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).all()
    '''
    #allwinelist2 = db.session.query(WineListdata).filter_by(Selectedflg=1).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).filter_by(members_id=1).all()
    #allwinelist3 = db.session.query(Assecementdata2).filter_by(members_id=4).join(WineListdata, WineListdata.id == Assecementdata2.wine_id).all()
    #allwinelist2 = db.session.query(WineListdata).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).filter_by(members_id=user_id.id).all()
    #allwinelist2 = db.session.query(WineListdata,Assecementdata2).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).filter_by(Selectedflg=1,members_id=4).all()
    
    for wine3 in allwinelist3:
         #if wine2.Selectedflg == 1 : #and wine.members_id == user_id 
            for test2 in wine3.assessment2:
             #for test2 in wine2:
                print("=======")
                #print("コメント→",wine2)
                print("Selectedflag→",wine3.Selectedflg)
                print("wine_id→",test2.wine_id)
                print("members_id",test2.members_id)
                print("id→",test2.id)
                #print("members_id→",wine2.assessment2.members_id)
                #print("end")
    '''

    wine_scorelist =[]

    for wine in allwinelist:
        if wine.Selectedflg == 1 : #and wine.members_id == user_id 

            for test in wine.assessment2:
             
               if int(test.members_id) == user_id.id:
                    print("選択された品種のメインコメントです→",test.maincomment)
                    print("スコアです->",test.score1_spicy)
                    print("ases_id->",test.id)
                    #print("選択された品種のメインコメントです→",wine.assessment2[0].maincomment)
                    wine_scorelist.append(test)

    print("========================>",wine_scorelist)
    print("========================>",wine_scorelist[0].maincomment)


    return render_template('hyouka.html',myname = myname,wine_selected=wine_selected,wine_scorelist=wine_scorelist)


@app.route("/scatter") #結果グラフ表示
def scatter():
    
    return render_template('graph_scatter1.html')


@app.route("/scatter.png") #結果グラフ表示 画像部分
def scatter_png():
    """The view for rendering the scatter chart"""

    score1_spicy_s=[]
    score2_acidity_s=[]
    score3_total_s=[]
    username_s=[]
    i1=0

    ##WineListDataから、セレクトされているWineを抽出
    wine_selectedid = db.session.query(WineListdata).filter_by(Selectedflg=1).first()
    comment_data = db.session.query(Assecementdata2).filter_by(wine_id=wine_selectedid.id).all()
    ##MemberList_DB = db.session.query(Member).all() #DBからメンバーリストを割り当てる

    ## WineListdataとAssecementdataを結合
    wine_selectedid2 = db.session.query(WineListdata).filter_by(Selectedflg=1).all()
    allwinelist = db.session.query(WineListdata).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).all()

    print("======>",wine_selectedid2)


    for wine in allwinelist:
        if wine.Brandname == wine_selectedid2[0].Brandname : 

            for test in wine.assessment2:
                    print("ases_id->",test.id)
                    print("選択されたブランド名→",wine.Brandname)
                    print("選択された品種のメインコメントです→",test.maincomment)
                    print("スコア1です->",test.score1_spicy)
                    print("スコア2です->",test.score2_acidity)
                    print("スコア3です->",test.score3_total)
                   
                    user_name = db.session.query(Member.name).filter_by(id = test.members_id).first()
                    user_name2 = db.session.query(Member).filter_by(id = test.members_id).first()
                    print("menです1->",test.members_id)
                    print("menです2->",user_name)
                    print("menです3->",user_name2.name)
                    print("---------------")


                    if (test.score1_spicy is not None and
                        test.score2_acidity is not None and 
                        test.score3_total is not None):
                         i1=i1+1
                         score1_spicy_s.append(test.score1_spicy)
                         score2_acidity_s.append(test.score2_acidity)
                         score3_total_s.append(test.score3_total*10)
                         username_s.append(user_name2.name)
        
    
    print("aaaaaaaaaaa---->",comment_data)

    img = get_main_image(score1_spicy_s,score2_acidity_s,score3_total_s,username_s)
    return send_file(img, mimetype='image/png', cache_timeout=0)



@app.route("/result_by_wine") #結果グラフ表示（ワイン別） するものを選択
def result_by_wine():
    
    myname = session.get('username')

    wine_selected = db.session.query(WineListdata).filter_by(Selectedflg=1).all()
    
    return render_template('prepare_graph_selected.html',myname=myname,wine_selected=wine_selected)

@app.route("/draw_graph", methods=['POST']) #結果グラフ表示（ワイン別） 
def draw_graph():

    selected_wine = request.form.getlist('checkbox')
    print("===>",selected_wine)    

    ## 今回選択されたWineListdataからIDを抽出
    #wine_selectedtest = db.session.query(WineListdata.id).filter_by(Brandname=selected_wine[0]).all()
    #print("====>",wine_selectedtest) 

    ## WineListdataとAssecementdataを結合
    allwinelist = db.session.query(WineListdata).join(Assecementdata2, WineListdata.id == Assecementdata2.wine_id).all()


    WineLiswine_scorelist =[]
    score1_spicy_s=[]
    score2_acidity_s=[]
    score3_total_s=[]
    comment_name_s=[]
    i1=0

    ##アセスデータかデータを抽出
    wine_selectedid = db.session.query(WineListdata).filter_by(Brandname=selected_wine[0]).first()
    comment_data = db.session.query(Assecementdata2).filter_by(wine_id=wine_selectedid.id).all()
    MemberList_DB = db.session.query(Member).all() #DBからメンバーリストを割り当てる



    for wine in allwinelist:
        if wine.Brandname == selected_wine[0] : 

            for test in wine.assessment2:
                 
                    user_name = db.session.query(Member.name).filter_by(id = test.members_id).first()
               
                    if (test.score1_spicy is not None and
                        test.score2_acidity is not None and 
                        test.score3_total is not None):
                         i1=i1+1
                         score1_spicy_s.append(test.score1_spicy)
                         score2_acidity_s.append(test.score2_acidity)
                         score3_total_s.append(test.score3_total*10)
                         comment_name_s.append([user_name,test.maincomment,score3_total_s])
        
        if wine.Brandname == selected_wine[1] : 

            for test in wine.assessment2:


                    if (test.score1_spicy is not None and
                        test.score2_acidity is not None and 
                        test.score3_total is not None):
                         i1=i1+1
                         score1_spicy_s.append(test.score1_spicy)
                         score2_acidity_s.append(test.score2_acidity)
                         score3_total_s.append(test.score3_total*10)


                    

    return render_template('chart8_bubble.html',xxList=score1_spicy_s,yyList=score2_acidity_s,rrList=score3_total_s,selected_wine=selected_wine,comment_data=comment_data,MemberList_DB=MemberList_DB)




if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)