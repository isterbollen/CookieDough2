from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django import forms
from django.contrib.auth.hashers import make_password, check_password

## Functions used in the rest of the views

# This function takes a drug in parameter and checks if this drug exists in the database,
# it returns True or False, if True is returned, it means that the drug exists, if False is
# returned, the drug doesn't exist. 
def CheckExistingDrug(drug):
	cur=connection.cursor()
	cur.execute("SELECT count(*) FROM drug WHERE name=%s",([drug]))
	r=cur.fetchall()
	nb=0
	for row in r:
		nb=row[0]
	if nb==0:
		return False
	else:
		return True

# This function takes a substance in parameter and checks if this substance exists in the database,
# it returns True or False, if True is returned, it means that the substance exists, if False is
# returned, the substance doesn't exist. 
def CheckExistingSubstance(substance):
	cur=connection.cursor()
	cur.execute("SELECT count(*) FROM substance WHERE name=%s",([substance]))
	r=cur.fetchall()
	nb=0
	for row in r:
		nb=row[0]
	if nb==0:
		return False
	else:
		return True

# Same with accession number
def CheckExistingAccNum(acc_nb):
	cur=connection.cursor()
	cur.execute("SELECT count(*) FROM substance WHERE accession_num=%s",([acc_nb]))
	r=cur.fetchall()
	nb=0
	for row in r:
		nb=row[0]
	if nb==0:
		return False
	else:
		return True

# Same with food interaction
def CheckExistingFoodInteraction(substance, food):
	cur=connection.cursor()
	cur.execute("SELECT count(*) FROM food_interactions WHERE subst_name=%s and food=%s",([substance],[food]))
	r=cur.fetchall()
	nb=0
	for row in r:
		nb=row[0]
	if nb==0:
		return False
	else:
		return True

# Checks if the username and password that are in the parameters correspond to an existing administrator
# it returns True if the username exists and the password corresponds, but returns false if the
# username doesn't exist or if the password doesn't correspond
def CheckAdmin(username, password):
	cur=connection.cursor()
	usr=username.split()
	pwd=password.split()
	cur.execute("SELECT * FROM administrator WHERE name=%s",(usr))
	r=cur.fetchall()
	if not r:
		return False
	else:
		if check_password(pwd[0],r[0][1])==True:
			return True
		else:
			return False

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
	# in position 1 or 2 of a row and that another substance of our list is in the corresponding other position, we have
	# an interaction
	# We add only the interactions that came out in the list called listI
	cur.execute("SELECT * FROM interactions ORDER BY level DESC")
	r=cur.fetchall()
	for row in r:
		li=list(row[0:])
		if li[1] in listS and li[2] in listS:
			# Each row of this list contains 'subst_a', 'subst_b', 'description' and 'level'
			listI.append(li)
	context={"nd":ndrugs, 'listI':listI, 'listDbis':listDbis}
	
	#Insert the statistics into the statistics table
	for i in range(len(listDbis)):
		inpage=""
		inpgender=""
		inpcontinent=""
		inpdrug=""
		subst=""
		if request.POST.get("age")!=None and request.POST.get("gender")!=None and request.POST.get("continent")!=None:
			inpdrug=listD[i]
			subst=listS[i]
			inpage=request.POST.get("age")
			inpgender=request.POST.get("gender")
			inpcontinent=request.POST.get("continent")
			cur.execute('INSERT INTO statistics(id, drug, substance, age, gender, continent) VALUES(DEFAULT, %s, %s, %s, %s, %s)', ([inpdrug], [subst], [inpage], [inpgender], [inpcontinent]))
	
	return render(request, 'DrugiComp/home.html', context)

def about(request):
	return render(request, 'DrugiComp/about.html', {'title':'About'})

def statistics(request):
	# Data for chart 1
	cur=connection.cursor()
	cur.execute("SELECT drug, COUNT(*) FROM statistics GROUP BY drug")
	drugs=cur.fetchall()
	drugnames=[]
	drugcount=[]
	for i in drugs:
		drugnames.append(i[0])
		drugcount.append(i[1])

	# Data for chart 2
	cur=connection.cursor()
	cur.execute("SELECT substance, COUNT(*) FROM statistics GROUP BY substance")
	substances=cur.fetchall()
	substnames=[]
	substcount=[]
	for i in substances:
		substnames.append(i[0])
		substcount.append(i[1])

	# Data for chart 3
	cur=connection.cursor()
	cur.execute("SELECT continent, COUNT(*) FROM statistics GROUP BY continent")
	continents=cur.fetchall()
	contnames=[]
	contcount=[]
	for i in continents:
		contnames.append(i[0])
		contcount.append(i[1])

	# Data for chart 4
	cur=connection.cursor()
	cur.execute("SELECT age, COUNT(*) FROM statistics WHERE gender='Male' GROUP BY age")
	meninfo=cur.fetchall()
	menages=[]
	menagecount=[]
	for i in meninfo:
		menages.append(i[0])
		menagecount.append(i[1])

	# Data for chart 5
	cur=connection.cursor()
	cur.execute("SELECT age, COUNT(*) FROM statistics WHERE gender='Female' GROUP BY age")
	womeninfo=cur.fetchall()
	womenages=[]
	womenagecount=[]
	for i in womeninfo:
		womenages.append(i[0])
		womenagecount.append(i[1])

	# Data for chart 6
	cur=connection.cursor()
	cur.execute("SELECT age, COUNT(*) FROM statistics WHERE gender='Other / Do not want to state' GROUP BY age")
	otherinfo=cur.fetchall()
	otherages=[]
	othercount=[]
	for i in otherinfo:
		otherages.append(i[0])
		othercount.append(i[1])

	# Data for chart 7
	cur=connection.cursor()
	cur.execute("SELECT gender, COUNT(*) FROM statistics GROUP BY gender")
	genderinfo=cur.fetchall()
	gendernames=[]
	gendercount=[]
	for i in genderinfo:
		gendernames.append(i[0])
		gendercount.append(i[1])

	return render(request, "DrugiComp/statistics.html", {'title':'Statistics', 'labels1':drugnames, 'data1':drugcount, 'labels2':substnames,
		'data2':substcount, 'labels3':contnames, 'data3':contcount, 'labels4':menages, 'data4':menagecount, 'labels5':womenages, 
		'data5':womenagecount, 'labels6':otherages, 'data6':othercount, 'labels7':gendernames, 'data7':gendercount})

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
		# If the 'subst_a' attribute corresponds to our substance, we select every drug that has this substance in
		# and put it in the ld list
		if row[1]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[2]]))
			res=cur.fetchall()
			for i in res:
				ld.append(i[0])
		# If the 'subst_b' attribute corresponds to our substance, we select every drug that has this substance in
		# and put it in the ld list
		if row[2]==subst:
			cur.execute("SELECT name FROM drug WHERE subst_name=%s", ([row[1]]))
			res=cur.fetchall()
			for i in res:
				ld.append(i[0])
	context={'title':'Test', 'ldrugs':ndrugs, 
	'drug':inpdrug, 'drugsint':drugsint, 'subst':subst, 'acc_nb':acc_nb, 'ld':ld}
	
	#Insert the statistics into the statistics table
	inpage=""
	inpgender=""
	inpcontinent=""
	if request.POST.get("age")!=None and request.POST.get("gender")!=None and request.POST.get("continent")!=None:
		inpage=request.POST.get("age")
		inpgender=request.POST.get("gender")
		inpcontinent=request.POST.get("continent")
		cur.execute('INSERT INTO statistics(id, drug, substance, age, gender, continent) VALUES(DEFAULT, %s, %s, %s, %s, %s)', ([inpdrug], [subst], [inpage], [inpgender], [inpcontinent]))
	
	return render(request, 'DrugiComp/test.html', context)
class FormLogin(forms.Form):
	username=forms.CharField(label=("Admin name"), required=True, widget=forms.TextInput(attrs={'class':'form_text'}))
	password=forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class':'form_text'}), required=True)

def admin_login(request):
	username=None
	form_login=FormLogin()
	if request.method=='GET':
		if 'action' in request.GET:
			action=request.GET.get('action')
			if action=='logout':
				if request.session.has_key('username'):
					request.session.flush()
				return redirect('DrugiComp-admin_login')
		if 'username' in request.session:
			username=request.session['username']
	elif request.method=='POST':
		form_login=FormLogin(request.POST)
		if form_login.is_valid():
			username=form_login.cleaned_data['username']
			password=form_login.cleaned_data['password']
			if CheckAdmin(username, password)==True:
				request.session['username']=username
			else:
				username=None
	context={'title':'Administratior Login', 'username':username, 'form':form_login}
	return render(request, 'DrugiComp/admin_login.html', context)

def admin_page(request):
	session=request.session.get('username')
	if session!=None:
		context={'title':'Administrator Page', 'session':session}
		return render(request, 'DrugiComp/admin_page.html', context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)

def add_ds(request):
	session=request.session.get('username')
	if session!=None:
		drug=request.POST.get("drug_name")
		substance=request.POST.get("substance_name")
		accession_number=request.POST.get("accession_number")
		recommendation=request.POST.get("recommendation")
		subst_int=request.POST.getlist('substances')
		message=""
		ls=[]
		exist_d=CheckExistingDrug(drug)
		exist_s=CheckExistingSubstance(substance)
		exist_an=CheckExistingAccNum(accession_number)
		cur=connection.cursor()
		cur.execute("""SELECT name FROM substance""")
		res=cur.fetchall()
		for r in res:
			ls.append(r)
		if request.POST.get("next_page"):
			cur=connection.cursor()
			if accession_number:
				cur.execute("""INSERT INTO substance VALUES (%s, %s, %s)""", ([accession_number],[substance],[recommendation]))
				cur.execute("""INSERT INTO drug VALUES (%s, %s)""", ([drug],[substance]))
				if subst_int:
					list_interactions=[]
					for row in subst_int:
						description=None
						cur.execute("""SELECT max(int_id) FROM interactions;""")
						if request.POST.get("description"+row)!="":
							description=request.POST.get("description"+row)
						level=request.POST.get("level"+row)
						r=cur.fetchall()
						for i in r:
							max_id=i[0]
						list_interactions.append([substance, row, description, level])
						cur.execute("""INSERT INTO interactions 
							VALUES (%s,%s, %s, %s, %s)""", ([max_id+1],[substance],[row],[description],[level]))
			else:
				cur.execute("INSERT INTO drug VALUES (%s, %s)", ([drug],[substance]))
			context={'drug':drug, 'substance':substance, 'accession_number':accession_number, 
					'recommendation':recommendation, 'list_interactions':list_interactions}
			messages.success(request, f'You added a drug to the database!')
			return render(request, 'DrugiComp/summary_add.html', context)
		context={'drug':drug, 'substance':substance, 'exist_d':exist_d, 'exist_s':exist_s, 
					'exist_an':exist_an, 'ls':ls, 'accession_number':accession_number, 
					'recommendation':recommendation, 'subst_int':subst_int, 'session':session}
		return render(request, 'DrugiComp/add_ds.html', context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)

def remove_dsi(request):
	session=request.session.get('username')
	if session!=None:
		obj=request.POST.get("object")
		cur=connection.cursor()
		cur.execute("SELECT * FROM drug ORDER BY name")
		d_res=cur.fetchall()
		cur.execute("SELECT * FROM substance ORDER BY name")
		s_res=cur.fetchall()
		cur.execute("SELECT * FROM interactions ORDER BY subst_a, subst_b")
		i_res=cur.fetchall()
		cur.execute("SELECT * FROM food_interactions ORDER BY subst_name, food")
		f_res=cur.fetchall()
		listD=request.POST.getlist("drugs")
		listS=request.POST.getlist("substances")
		listI=request.POST.getlist("interactions")
		listI=list(map(int, listI))
		listF=request.POST.getlist("food_interactions")
		listF=list(map(int, listF))
		listIbis=[]
		listFbis=[]
		for i in listI:
			cur.execute("""SELECT subst_a,subst_b FROM interactions WHERE int_id=%s""", ([i]))
			r=cur.fetchall()
			listIbis.append(r)
		for j in listF:
			cur.execute("""SELECT subst_name, food FROM food_interactions WHERE food_int_id=%s""", ([j]))
			r=cur.fetchall()
			listFbis.append(r)
		if request.POST.get("remove_drug"):
			for drug in listD:
				cur.execute("DELETE FROM drug WHERE name=%s;",([drug]))
			messages.success(request, f'You removed one or more drugs!')
			return render(request, 'DrugiComp/admin_page.html')
		if request.POST.get("remove_substance"):
			for subst in listS:
				cur.execute("DELETE FROM substance WHERE name=%s;",([subst]))
			messages.success(request, f'You removed one or more substances and all attributes linked to them!')
			return render(request, 'DrugiComp/admin_page.html')
		if request.POST.get("remove_interaction"):
			for interaction in listI:
				cur.execute("DELETE FROM interactions WHERE int_id=%s",([interaction]))
			messages.success(request, f'You removed one or more interactions!')
			return render(request, 'DrugiComp/admin_page.html')
		if request.POST.get("remove_food_interaction"):
			for fi in listF:
				cur.execute("DELETE FROM food_interactions WHERE food_int_id=%s",([fi]))
			messages.success(request, f'You removed one or more food interactions!')
			return render(request, 'DrugiComp/admin_page.html')
		possibilities=['drug','substance','interactions','food_interactions']
		context={'obj':obj, 'possibilities':possibilities, 'd_res':d_res, 's_res':s_res, 'i_res':i_res, 
				'f_res':f_res, 'listD':listD, 'listS':listS, 'listI':listI, 'listF':listF, 
				'listIbis':listIbis, 'listFbis':listFbis, 'session':session}
		return render(request, 'DrugiComp/remove_dsi.html',context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)

def view_database(request):
	session=request.session.get('username')
	if session!=None:
		cur=connection.cursor()
		cur.execute("SELECT * FROM drug")
		d_res=cur.fetchall()
		cur.execute("SELECT * FROM substance")
		s_res=cur.fetchall()
		cur.execute("SELECT * FROM interactions")
		i_res=cur.fetchall()
		cur.execute("SELECT * FROM food_interactions")
		f_res=cur.fetchall()
		context={'d_res':d_res, 'i_res':i_res, 's_res':s_res, 'f_res':f_res, 'session':session}
		return render(request, 'DrugiComp/view_database.html', context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)

def add_int_foodint(request):
	session=request.session.get('username')
	if session!=None:
		cur=connection.cursor()
		# Drug interaction part
		obj=request.POST.get("object")
		subst_a=request.POST.get("subst_a")
		subst_b=request.POST.getlist("subst_b")
		exist_s=CheckExistingSubstance(subst_a)
		cur.execute("SELECT name FROM substance GROUP BY name")
		list_subst=cur.fetchall()
		subst_b_list=""
		if subst_a:
			cur.execute("""SELECT name FROM substance 
						WHERE name NOT IN (SELECT subst_b 
											FROM interactions WHERE subst_a=%s) 
							AND name!=%s GROUP BY name""", ([subst_a], [subst_a]))
			subst_b_list=cur.fetchall()
		if request.POST.get("new_interaction"):
			for row in subst_b:
				description=None
				cur.execute("""SELECT max(int_id) FROM interactions;""")
				r=cur.fetchall()
				for i in r:
					max_id=i[0]
				if request.POST.get("description"+row)!="":
					description=request.POST.get("description"+row)
				level=request.POST.get("level"+row)
				cur.execute("""INSERT INTO interactions 
					VALUES (%s,%s, %s, %s, %s)""", ([max_id+1],[subst_a],[row],[description],[level]))
			messages.success(request, f'You added an interaction!')
			return render(request, 'DrugiComp/admin_page.html')
		# Food interaction part
		fi_subst=request.POST.get("fi_subst")
		fi_exist_s=CheckExistingSubstance(fi_subst)
		food=request.POST.get("food")
		exist_fi=CheckExistingFoodInteraction(fi_subst, food)
		cur.execute("SELECT DISTINCT food FROM food_interactions;")
		list_food=cur.fetchall()
		indication=request.POST.get("indication")
		if request.POST.get("new_food_interaction"):
			cur.execute("""SELECT max(food_int_id) FROM food_interactions;""")
			r=cur.fetchall()
			for i in r:
				max_id=i[0]
			cur.execute("""INSERT INTO food_interactions VALUES (%s, %s, %s, %s)""", ([max_id+1],[fi_subst],[food],[indication]))
			messages.success(request, f'You added a food interaction!')
			return render(request, 'DrugiComp/admin_page.html')
		possibilities=['interaction','food_interaction', 'Avoid', 'Limit']
		context={'possibilities':possibilities, 'obj':obj, 'exist_s':exist_s, 'list_subst':list_subst, 
				'subst_a':subst_a, 'subst_b_list':subst_b_list, 'subst_b':subst_b, 'food':food, 
				'list_food':list_food, 'fi_subst':fi_subst, 'fi_exist_s':fi_exist_s, 'exist_fi':exist_fi,
				'indication':indication, 'session':session}
		return render(request, 'DrugiComp/add_int_foodint.html', context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)

def modify_dsi(request):
	session=request.session.get('username')
	if session!=None:
		cur=connection.cursor()
		obj=request.POST.get("object")

		# Drug modifying
		cur.execute("SELECT * FROM drug")
		d_res=cur.fetchall()
		drug=request.POST.get("drug_name")
		new_drug=request.POST.get("new_drug")
		exist_d=CheckExistingDrug(drug)
		exist_nd=CheckExistingDrug(new_drug)
		if request.POST.get("modify_drug_name"):
			cur.execute("""UPDATE drug SET name =%s WHERE (name = %s);""", ([new_drug],[drug]))
			messages.success(request, f'You modified the name of a drug!')
			return render(request, 'DrugiComp/admin_page.html')

		# Substance modifying
		cur.execute("SELECT * FROM substance")
		s_res=cur.fetchall()
		subst=request.POST.get("subst_name")
		recommendation=request.POST.get("recommendation")
		exist_s=CheckExistingSubstance(subst)
		subst_objet=request.POST.get("subst_objet")
		new_subst=request.POST.get("new_subst")
		exist_ns=CheckExistingSubstance(new_subst)
		poss_subst=['new_subst_name', 'new_recommendation']
		if request.POST.get("modify_subst_name"):
			cur.execute("""UPDATE substance SET name =%s WHERE (name = %s);""", ([new_subst],[subst]))
			messages.success(request, f'You modified the name of a substance!')
			return render(request, 'DrugiComp/admin_page.html')
		if request.POST.get("modify_recommendation"):
			cur.execute("""UPDATE substance SET recommendation =%s WHERE (name = %s);""", ([recommendation],[subst]))
			messages.success(request, f'You modified the recommendation of a substance!')
			return render(request, 'DrugiComp/admin_page.html')
		cur.execute("""SELECT recommendation FROM substance WHERE name=%s""", ([subst]))
		r=cur.fetchall()
		recom_subst=""
		for row in r:
			recom_subst=row[0]

		# Interaction modifying
		cur.execute("SELECT * FROM interactions")
		i_res=cur.fetchall()
		tick_interaction=request.POST.get("tick_interaction")
		cur.execute("SELECT subst_a, subst_b, description, level FROM interactions WHERE int_id=%s", ([tick_interaction]))
		selected_interaction=cur.fetchall()
		description=request.POST.get("description")
		level=request.POST.get("level")
		if request.POST.get("modify_interaction"):
			cur.execute("""UPDATE interactions SET description = %s WHERE (int_id = %s);""", ([description],[tick_interaction]))
			cur.execute("""UPDATE interactions SET level = %s WHERE (int_id = %s);""", ([level],[tick_interaction]))
			messages.success(request, f'You modified the description and/or level of an interaction!')
			return render(request, 'DrugiComp/admin_page.html')
		
		# Food interaction modifying
		cur.execute("SELECT * FROM food_interactions")
		f_res=cur.fetchall()
		tick_fi=request.POST.get("tick_fi")
		cur.execute("SELECT subst_name,food,indication FROM food_interactions WHERE food_int_id=%s", ([tick_fi]))
		selected_fi=cur.fetchall()
		indication=request.POST.get("indication")
		poss_fi=['Avoid', 'Limit']
		if request.POST.get("modify_food_interaction"):
			cur.execute("""UPDATE food_interactions SET indication = %s WHERE (food_int_id = %s);""", ([indication],[tick_fi]))
			messages.success(request, f'You modified the indication of a food interaction!')
			return render(request, 'DrugiComp/admin_page.html')

		possibilities=['drug','substance','interactions','food_interactions']
		context={'obj':obj, 'possibilities':possibilities, 'drug':drug, 'exist_d':exist_d, 'd_res':d_res,
				'new_drug':new_drug, 'exist_nd':exist_nd, 's_res':s_res, 'subst':subst, 'exist_s':exist_s,
				'recom_subst':recom_subst, 'recommendation':recommendation, 'poss_subst':poss_subst, 'subst_objet':subst_objet,
				'poss_subst':poss_subst, 'new_subst':new_subst, 'exist_ns':exist_ns, 'i_res':i_res, 
				'tick_interaction':tick_interaction, 'selected_interaction':selected_interaction, 
				'description':description, 'f_res':f_res, 'tick_fi':tick_fi, 'selected_fi':selected_fi,
				'indication':indication, 'poss_fi':poss_fi, 'session':session}
		return render(request, 'DrugiComp/modify_dsi.html', context)
	if session==None:
		context={'title':'Error', 'session':session}
		return render(request, 'DrugiComp/error.html', context)
