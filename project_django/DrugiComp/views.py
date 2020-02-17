from django.shortcuts import render
from django.db import connection

def home(request):
	cur=connection.cursor()
	cur.execute("SELECT name FROM drug")
	r=cur.fetchall()
	ndrugs=[row[0] for row in r]
	listD=[]
	listDbis=[]
	listS=[]
	listI=[]
	for i in range(6):
		if request.POST.get(f'drug{i}')!=None:
			listD.append(request.POST.get(f'drug{i}'))
	for i in listD:
		cur.execute("SELECT subst_name FROM drug WHERE name=%s",([i]))
		r=cur.fetchall()
		for row in r:
			listS.append(row[0])
			listDbis.append([i,row[0]])
	cur.execute("SELECT * FROM interactions")
	r=cur.fetchall()
	for row in r:
		li=list(row[0:])
		if li[0] in listS and li[1] in listS:
			listI.append(li)
	context={"nd":ndrugs, 'listI':listI, 'listDbis':listDbis}
	return render(request, 'DrugiComp/home.html', context)

def about(request):
	return render(request, 'DrugiComp/about.html', {'title':'About'})

def statistics(request):
	context={'title':'Statistics'}
	return render(request, 'DrugiComp/statistics.html', context)

def test(request):
	cur=connection.cursor()
	cur.execute("SELECT name FROM drug")
	ndrugs=cur.fetchall()
	inpdrug=""
	subst=""
	acc_nb=""
	ld=[]
	drugsint=[]
	if request.POST.get("drug")!=None:
		inpdrug=request.POST.get("drug")
	cur.execute("""SELECT d.subst_name, s.accession_num 
					FROM drug d JOIN substance s ON d.subst_name=s.name 
					WHERE d.name=%s""",([inpdrug]))
	r=cur.fetchall()
	for row in r:
		subst=row[0]
		acc_nb=row[1]
	cur.execute("""SELECT * FROM interactions 
					WHERE subst_a=%s OR subst_b=%s""",([subst],[subst]))
	r=cur.fetchall()
	for row in r:
		if row[0]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[1]]))
			res=cur.fetchall()
			ld.append(res[0][0])
		if row[1]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[0]]))
			res=cur.fetchall()
			ld.append(res[0][0])
	context={'title':'Test', 'ldrugs':ndrugs, 
	'drug':inpdrug, 'drugsint':drugsint, 'subst':subst, 'acc_nb':acc_nb, 'ld':ld}
	return render(request, 'DrugiComp/test.html', context)
