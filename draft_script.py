import sqlite3 as sql
con=sql.connect("draft.db")
con.row_factory=sql.Row
cur=con.cursor()

DrugB="Celexa"
DrugA="Methadose"
DrugC="Advil"
DrugD="Benadryl"
DrugE="Dramamine"
DrugF="Dolprone"

ld=[DrugA, DrugB, DrugC, DrugD, DrugE, DrugF]
ls=[]
for i in ld:
	cur.execute("SELECT SubstName FROM Drug WHERE Name=(?)",[i])
	r=cur.fetchall()
	for row in r:
		ls.append(row[0])

# print(ls)

cur.execute("SELECT * FROM Interaction")
r=cur.fetchall()
for row in r:
	li=list(row[0:])
	if li[0] in ls and li[1] in ls:
		print(li)