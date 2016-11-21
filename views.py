from django.shortcuts import render_to_response
from time import strftime, localtime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django import forms
from django.contrib.auth.forms import UserCreationForm

#from mysite.forum.models import node

def index(request):
	time_string=strftime("Date is %a, %d of %B. | Time is %I:%M:%S %p", localtime())
	return render_to_response('index.html', {'time_string': time_string})

def mylogin(request): #modified from Django Authentication Docs
	time_string=strftime("Date is %a, %d of %B. | Time is %I:%M:%S %p", localtime())
	invalid_login = False
	try:
		username = request.POST['user']
		password = request.POST['pass']
		user = authenticate(username=username, password=password)
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect('/forum/init')
		else:
			account_disabled = True
			return render_to_response('index.html', {'time_string': '!!!', 'account_disabled': account_disabled})
	except:
		return render_to_response('index.html', {'time_string': time_string, 'invalid_login': invalid_login})

def mylogout(request):
	time_string=strftime("Date is %a, %d of %B. | Time is %I:%M:%S %p", localtime())
	logout(request)
	return render_to_response('index.html', {'time_string': time_string})

def register(request): #User Registration form from the Django Book (online)
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect('/')#returnto mainpage
	else:
		form = UserCreationForm()
	return render_to_response('register.html', { 'form': form })

#http://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
