#http://kunxi.org/archives/2007/09/learning-django-by-example1-start-the-engine/
#http://docs.djangoproject.com/en/1.1/intro/tutorial02/

from django.contrib import admin

from mysite.forum.models import topic, message

admin.site.register(topic)
admin.site.register(message)

date_hierarchy = 'topic.created'