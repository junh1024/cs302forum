from django.conf.urls.defaults import *
from django.http import Http404

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^polls/$', 'mysite.polls.views.index'),
	(r'^polls/(?P<poll_id>\d+)/$', 'mysite.polls.views.detail'),
	(r'^polls/(?P<poll_id>\d+)/results/$', 'mysite.polls.views.results'),
	(r'^polls/(?P<poll_id>\d+)/vote/$', 'mysite.polls.views.vote'),

	(r'^forum/init$', 'mysite.forum.views.init'),#loads the forum
	(r'^forum/$', 'mysite.forum.views.index'),#main forum

	(r'^$', 'mysite.views.index'),#index page
	(r'^login$', 'mysite.views.mylogin'),#login
	(r'^logout$', 'mysite.views.mylogout'),#logout
	(r'^register$', 'mysite.views.register'),#register
#	(r'^checkin$', 'mysite.views.checkin'),#login
	
	(r'^getMessages$', 'mysite.views.index'),#bandwidth saving stubs
	(r'^getTopics$', 'mysite.views.index'),

	(r'^forum/edit/(?P<id>.*)$', 'mysite.forum.views.edit'),#edit a message
	(r'^forum/topic/(?P<id>.*)$', 'mysite.forum.views.detail'),#topic detail

	# (r'^Pictures/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/afs/ec.auckland.ac.nz/users/j/l/jlin200/unixhome/Pictures'}),

	(r'^admin/', include(admin.site.urls)),

)
