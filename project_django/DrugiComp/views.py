from django.shortcuts import render
from django.db import connection

def home(request):
	cur = connection.cursor()
	drug1=request.POST.get("drug1")
	drug2=request.POST.get("drug2")
	listD=[drug1,drug2]
	listS=[]
	listI=[]
	for i in listD:
		cur.execute("SELECT subst_name FROM drug WHERE name=%s",([i]))
		r=cur.fetchall()
		for row in r:
			listS.append(row[0])
	cur.execute("SELECT * FROM interactions")
	r=cur.fetchall()
	for row in r:
		li=list(row[0:])
		if li[0] in listS and li[1] in listS:
			listI.append(li)
	context = {'interactions':listI}
	return render(request, 'DrugiComp/home.html', context)

def about(request):
	return render(request, 'DrugiComp/about.html', {'title':'About'})

def statistics(request):
	cur=connection.cursor()
	nb=request.POST.get("drug")
	context={'title':'Statistics', 'nbdrug':nb}
	return render(request, 'DrugiComp/statistics.html', context)
