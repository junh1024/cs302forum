from django.shortcuts import render_to_response, get_object_or_404 #main forum
from time import strftime, localtime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from mysite.forum.models import topic, message
from django.http import HttpResponseRedirect
from django import forms

#request.session['key'] = value
#variable = request.session['key']

@login_required
def init(request):
#move /login to init?
	return render_to_response('forum/init.html')

@login_required(redirect_field_name='/')
def index(request):
	time_string=strftime("Date is %a, %d of %B. | Time is %I:%M:%S %p", localtime())
	uname = str(request.user)
	topic_list = topic.objects.all().order_by('-lastchange')#the negative sign means descending
	error='To create Private Topic, type the recipient in the category field. cASE sENSITIVE'

	if 'title' in request.POST:
		title=request.POST['title']
		if 2 < len(title) < 128 and (title[0] and title[-0]) != ' ' and ('?' or '#' not in title ): #checking for these doesn't work properly
			category=request.POST['category']
			status2=request.POST['status']
			b=topic(creator=uname, title=title, category=category,status=status2)
		try:
			b.save()
			topic_obj = get_object_or_404(topic, title=title) #displays topic
			mesg_list = message.objects.filter(topic=topic_obj).order_by('created')
			return HttpResponseRedirect('/forum/%s' % (title)) #redirects to the topic that was just created
		except: #make more excepts for other errors
			error='Topic with title aready exists'
		else:
			error="Please enter a valid topic title. Topics can't be too long/short, or start/end with a space."
	return render_to_response('forum/index.html',{'uname': uname, 'topic_list': topic_list,'time_string': time_string,'error': error } )

@login_required
def detail(request, title):
	uname = str(request.user)
	ulist=User.objects
	time_string=strftime("Date is %a, %d of %B. | Time is %I:%M:%S %p", localtime())
#print ulist.get(username__exact=uname).date_joined was going to implement a miniprofile for each user, but can't parse remainder happened
	try:
		topic_obj = get_object_or_404(topic, title=title) #displays topic
		mesg_list = message.objects.filter(topic=topic_obj).order_by('created')#doesn't display it in the order that happens to come out of the database :P
		if topic_obj.status == 3 and  ( topic_obj.creator == uname or  topic_obj.category == uname): #authorized to view hidden topic
			print "#authorized to view hidden topic"
			preptopic(request, topic_obj, uname)
			return render_to_response('forum/detail.html', {'uname':uname,'topic':topic_obj,'messages':mesg_list,'time_string': time_string})
		elif topic_obj.status != 3: #normal topic
			print "normal topic"
			preptopic(request, topic_obj, uname)
			return render_to_response('forum/detail.html', {'uname':uname,'topic':topic_obj,'messages':mesg_list,'time_string': time_string})
		else: #not authorized to view topic
			print "not authorized to view topic"
			return HttpResponseRedirect('/forum/' )	
	except:
		return HttpResponseRedirect('/forum/' )

def preptopic(request, topic_obj, uname):
	print "preptopic called"
	if 'body' in request.POST and topic_obj.status != 2:
		body2=request.POST['body'] #extracts the body
		message(creator=uname, topic=topic.objects.get(id=topic_obj.id), body=body2).save() #new message
		topic_obj.save() #updates the date of topic
