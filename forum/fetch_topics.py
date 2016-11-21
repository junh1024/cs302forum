""" Sample code to fetch a list of topics from another node
    C.Coghill, Apr 2010

    You can use parts of this code in your projects as long as you 
    attribute it correctly (have a comment beside the included code 
    saying where you got it.)
    
    like, i used all of it, save a few lines of modification -jhl
    
    from datetime import datetime
    datetime.fromtimestamp(1172969203.1)
    
"""

#import time
from mysite.forum.models import topic, message

addr = "69.55.232.11" #11 is a invalid, 10 is correct
port = "8080"

#Internal
#addr = "130.216.24.19"port = "8008"


import urllib2
from xml.dom.minidom import parseString

n=0 #counter for topics alredy added

def parse_topic(topic):
    """ Given a DOM object representing a topic entry, return a 
        dictionary

           <topic ID="">
              <title></title>
              <category></category>
              <creator></creator>
              <created></created>
              <status></status>
              <lastchange></lastchange>
           </topic>
    """

    topicID = topic.getAttribute("ID")

    # we assume that there is only one element matching the tag. ie. a topic doesn't have two titles
    # This may need more error checking for missing or invalid elements.
    titleNode = topic.getElementsByTagName("title")[0]
    categoryNode = topic.getElementsByTagName("category")[0]
    creatorNode = topic.getElementsByTagName("creator")[0]
    createdNode = topic.getElementsByTagName("created")[0]
    statusNode = topic.getElementsByTagName("status")[0]
    lastchangeNode = topic.getElementsByTagName("lastchange")[0]
   
    if titleNode:
        title = titleNode.firstChild.nodeValue
    else:
        title = "unknown"
    if categoryNode:
        category = categoryNode.firstChild.nodeValue
    else:
        category = "unknown"
    if creatorNode:
        creator = creatorNode.firstChild.nodeValue
    else:
        creator = "unknown"
    if createdNode:
        created = createdNode.firstChild.nodeValue
    else:
        created = "unknown"
    if statusNode:
        status = statusNode.firstChild.nodeValue
    else:
        status = "unknown"
    if lastchangeNode:
        lastchange = lastchangeNode.firstChild.nodeValue
    else:
        lastchange = "unknown"
  
    return (topicID, {'title': title, 'category':category, 'creator':creator, 'created':created, 'status': status, 'lastchange': lastchange} )
    

def parse_topic_xml(data):
    """ Takes a string containing XML topic data and returns a dictionary of
        topic dictionaries, keyed by topicID
    """

    # An empty dict to start storing out topics in
    topics = {}
    doc = parseString(data)

    # Make sure we have the right kind of data
    assert doc.documentElement.tagName == "topics"

    #go through each "topic"
    topic_els = doc.getElementsByTagName("topic")
    for topic in topic_els:
        # parse this specific topic into a dictionary
        (topicID, topicInfo) = parse_topic(topic)
        if topicID:
            topics[topicID] = topicInfo
        else:
            #if topicID isn't set, there was an error parsing so we ignore it
            print "Bad topic data?"
      
    return topics

def get_topics(addr, port):
    """ Connect to node, port, and fetch a string full of topic information"""
    f = urllib2.urlopen("http://%s:%s/getTopics" % (addr, port), timeout=5) #added a timeout
    data = f.read()
    f.close()

    return data

# Fetch topic xml from other node
topic_data = get_topics(addr, port)

# Convert xml into dictionary
topics = parse_topic_xml(topic_data)

# don't add hidden topics to database
for topicID in topics.keys():
    try:
        if (topics[topicID]['status']) == 3:
            continue
        b=topic(creator=(topics[topicID]['creator']), title=(topics[topicID]['title']), category=(topics[topicID]['category']),status=(topics[topicID]['status']),topicID=(topicID))
        b.save() #created times may be broken because the object is created in the db NOW. also, lastchange time WILL be broken because we last changed it NOW in the db
    except: #most probably an IntegrityError SOMETHING IS NOT UNIQUE
        n=n+1 #increase the error counter

print ('%s topics already added' %(n))

