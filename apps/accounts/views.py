from django.shortcuts import render, redirect, HttpResponse
from .models import User
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout as django_logout
from django.forms.forms import NON_FIELD_ERRORS
from django.contrib import messages

def index(request):
	if not 'id' in request.session:
		request.session['id'] = None
	form1 = LoginForm()
	form2 = RegistrationForm()
	if request.method == 'POST':
		# LOGIN
		if 'login' in request.POST:
			form1 = LoginForm(data=request.POST)			
			if form1.is_valid():
				user = authenticate(username=request.POST['email'], password=request.POST['password'])
				form1.full_clean()
				if user:
					login(request, user)
					request.session['id'] = user.alias
					return redirect('/home')
				form1._errors[NON_FIELD_ERRORS] = form1.error_class(['User does not exist or incorrect password.'])
		# REGISTER
		if 'register' in request.POST:
			form2 = RegistrationForm(data=request.POST)
			if form2.is_valid():
				form2.save()
				user = User.objects.get(email=request.POST['email'])
				request.session['id'] = user.alias
				return redirect('/home')
	return render(request, "accounts/index.html", {"form1":form1, "form2":form2})

def home(request):
	if request.session['id'] == None:
		return redirect('/')
	user = User.objects.get(alias=request.session['id'])
	friends = user.friend.all()
	friendslist = []
	for x in friends:
		friendslist.append(x)
	nonfriends = User.objects.all().exclude(alias=user.alias)
	for x in friendslist:
		nonfriends = nonfriends.exclude(alias=x.alias)
	context = {
		'user': request.session['id'],
		'friends': friends,
		'nonfriends': nonfriends,
	}
	return render(request, 'accounts/home.html', context)

def logout(request):
	django_logout(request)
	request.session['id'] = None
	return redirect('/')

def user(request, user_id):
	context = {
		'user': User.objects.get(id=user_id)
	}
	return render(request, 'accounts/user.html', context)

def addfriend(request, user_id):
	newfriend = User.objects.get(id=user_id)
	user = User.objects.get(alias=request.session['id'])
	user.friend.add(newfriend)
	user.save()
	newfriend.friend.add(user)
	return redirect('/home')

def deletefriend(request, user_id):
	oldfriend = User.objects.get(id=user_id)
	user = User.objects.get(alias=request.session['id'])
	user.friend.remove(oldfriend)
	user.save()
	oldfriend.friend.remove(user)
	return redirect('/home')






























