from django.db import models

#http://stackoverflow.com/questions/1652577/django-ordering-queryset-by-a-calculated-field
#http://www.djangorocks.com/tutorials/how-to-create-a-basic-blog-in-django/writing-the-templates.html 
#http://docs.djangoproject.com/en/1.1/ref/models/fields/#model-field-types

class topic(models.Model):
	title = models.CharField(max_length=40,unique=True)
	category = models.CharField(max_length=40,blank=True,null=True)
	creator = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)
#	moderator = models.CharField(max_length=20,blank=True,null=True) removed, protocol change 1.05
	status = models.PositiveSmallIntegerField(blank=True,null=True)
	lastchange = models.DateTimeField(auto_now=True)
#	topicID = models.CharField(max_length=8,blank=True,null=True)
	def __unicode__(self):
		return self.title

class message(models.Model):
	creator = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)
	topic = models.ForeignKey(topic)
	body = models.TextField(max_length=20)
#	messageID = models.CharField(max_length=8,blank=True,null=True)
#	title = models.CharField(max_length=40) implied in topic title, shouldn't need.
#	image = models.FileField(upload_to='/',blank=True,null=True) Protocol change in 1.05: Images as URL embed/link
	def __unicode__(self):
		return self.body