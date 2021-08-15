# crud.py
from models import db, MemberList #class名

db.create_all() # テーブルの作成


man1 = MemberList('Taro', 'はじめまして')
man2 = MemberList('Jiro','')
man3 = MemberList('Yoko', 'こんばんわ。')


print(man1, man2, man3)
db.session.add_all([man1, man2]) # 複数一緒に追加
db.session.add(man3) # 1つ追加

db.session.commit()
print(man1, man2, man3)

MemberList_1 = MemberList.query.all()
#MemberList_2 = db.session.query(MemberList.username).all()
MemberList_2 = MemberList_1

MemberList_3 = db.session.query(MemberList).all()
for user in MemberList_3:
    print(user.username)

print("kokokara MemberList_1 --->",MemberList_1 ,"\n")
print("kokokara MemberList_3 --->",MemberList_2[1] )


db.session.query(MemberList).delete()
#db.session.delete()
db.session.commit()


