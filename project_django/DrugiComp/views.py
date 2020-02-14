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
	for i in range(5):
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
	cur = connection.cursor()
	listD=[] # List of the drug to test
	listAll=[] # List of all drugs 
	listSdrug=[] # Substances will be in this list 
	listSalldrugs=[] # Substances from all drugs
	listI=[] # Interactions
	listSnot=[] # Substances not to take
	listDnot=[] # Drugs not to take
	if request.POST.get("drug")!=None:
		listD.append(request.POST.get("drug"))
	# Get all drugs into a list
	cur.execute("SELECT name FROM drug")
	r=cur.fetchall()
	for row in r:
		listAll.append(row[0:])

	# Fetch all substances from the drug to test
	for i in listD:
		cur.execute("SELECT subst_name FROM drug WHERE name=%s",([i]))
		r=cur.fetchall() # Get all substances in the drug
		for row in r:
			listSdrug.append(row[0]) # Save substances in listS

	# Fetch all substances from all drugs
	for i in listAll:
		cur.execute("SELECT subst_name FROM drug WHERE name=%s",([i]))
		r=cur.fetchall() # Get all substances in the drug
		for row in r:
			listSalldrugs.append(row[0]) # Save substances in listS

	# Find interactions
	cur.execute("SELECT * FROM interactions")
	r=cur.fetchall()
	for row in r:
		li=list(row[0:])
		if li[0] in listSdrug and li[1] in listSalldrugs:
			listI.append(li)

	# Trace back the substances in interactions to which drugs has this (these we cannot take)
	for i in listI:
		listSnot.append(i[1])

	# Find out which drugs not to take
	for i in listSnot:
		cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([i]))
		r=cur.fetchall()
		for row in r:
			listDnot.append(row[0:])

	# Autofill function
	cur=connection.cursor()
	cur.execute("SELECT name FROM drug")
	ndrugs=cur.fetchall()
	
	context = {'title':'Test', 'drug':listD, 'drugsNot':listDnot, 'ldrugs':ndrugs}
	return render(request, 'DrugiComp/test.html', context)
