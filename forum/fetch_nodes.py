import csv
#import sys
import urllib2
#from datetime import datetime

from mysite.forum.models import node
node_list = node.objects.all().order_by('-time')

n=0 #counter for nodes alredy added
q=0 #counter for newnode

f = urllib2.urlopen("http://69.55.232.10:8080/checkin", timeout=4)
try:
    reader = csv.reader(f)
    for row in reader:
        try:
            b=node(IP = row[0], port = row[1], name = row[2], time = row[3])
            b.save()
            q=q+1
        except: #name of node alreadyexist so we delete it and readd it
            n=n+1
            c = node_list.get(name__exact=row[2])
            c.delete()
            b=node(IP = row[0], port = row[1], name = row[2], time = row[3])
            b.save()
finally:
    print ("%s new nodes, %s nodes updated" %(q, n))
