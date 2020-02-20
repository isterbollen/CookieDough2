from django.shortcuts import render
from django.db import connection

def home(request):
	# Start by creating a list of all the drugs that there are in the database for the dropdown list
	cur=connection.cursor()
	cur.execute("SELECT name FROM drug")
	r=cur.fetchall()
	# We fetch the first item of each row (the name of the drug)
	ndrugs=[row[0] for row in r]
	listD=[]
	listDbis=[]
	listS=[]
	listI=[]
	# For each form input (drug 1 to drug 5) we fetch what is in it and put it in listD
	for i in range(6):
		if request.POST.get(f'drug{i}')!=None:
			listD.append(request.POST.get(f'drug{i}'))
	# For each drug in list D we select the corresponding substance and add it in listS and we also populate the listDbis
	# so that we have the drug (here 'i') and its substance (here row[0)
	for i in listD:
		cur.execute("SELECT subst_name FROM drug WHERE name=%s",([i]))
		r=cur.fetchall()
		for row in r:
			listS.append(row[0])
			listDbis.append([i,row[0]])
	# We start by selecting each interaction in the database and then for each line of the SQL query, we check if the
	# substances we have in our listS are present in the interaction list. In other words if one of our substances is
	# in position 0 or 1 of a row and that another substance of our list is in the corresponding other position, we have
	# an interaction
	# We add only the interactions that came out in the list called listI
	cur.execute("SELECT * FROM interactions")
	r=cur.fetchall()
	for row in r:
		li=list(row[0:])
		if li[0] in listS and li[1] in listS:
			# Each row of this list contains 'subst_a', 'subst_b', 'description' and 'level'
			listI.append(li)
	context={"nd":ndrugs, 'listI':listI, 'listDbis':listDbis}
	return render(request, 'DrugiComp/home.html', context)

def about(request):
	return render(request, 'DrugiComp/about.html', {'title':'About'})

def statistics(request):
	context={'title':'Statistics'}
	return render(request, 'DrugiComp/statistics.html', context)

def test(request):
	# We select every drug in the database for the dropdown list in the input
	cur=connection.cursor()
	cur.execute("SELECT name FROM drug")
	ndrugs=cur.fetchall()
	inpdrug=""
	subst=""
	acc_nb=""
	ld=[]
	drugsint=[]
	# If the input field is filled, i.e. a drug has beed requested, we put it in the inpdrug variable
	if request.POST.get("drug")!=None:
		inpdrug=request.POST.get("drug")
	# For the drug that is in inpdrug, we fetch it's substance's name and the accession number of this substance
	cur.execute("""SELECT d.subst_name, s.accession_num 
					FROM drug d JOIN substance s ON d.subst_name=s.name 
					WHERE d.name=%s""",([inpdrug]))
	r=cur.fetchall()
	# The subst contains the substance name of the drug and acc_nb, the accession number of this drug's substance
	for row in r:
		subst=row[0]
		acc_nb=row[1]
	# Now we look for every interaction where the drug substance we have is in either 'subst_a' or 'subst_b'
	cur.execute("""SELECT * FROM interactions 
					WHERE subst_a=%s OR subst_b=%s""",([subst],[subst]))
	r=cur.fetchall()
	# For each interaction that was selected:
	for row in r:
		if row[0]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[1]]))
			res=cur.fetchall()
			for i in res:
				ld.append(i[0])
		if row[1]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[0]]))
			res=cur.fetchall()
			for i in res:
				ld.append(i[0])
	context={'title':'Test', 'ldrugs':ndrugs, 
	'drug':inpdrug, 'drugsint':drugsint, 'subst':subst, 'acc_nb':acc_nb, 'ld':ld}
	return render(request, 'DrugiComp/test.html', context)
