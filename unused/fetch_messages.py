""" Sample code to fetch a list of messages from another node
    C.Coghill, Apr 2010

    You can use parts of this code in your projects as long as you 
    attribute it correctly (have a comment beside the included code 
    saying where you got it.)
"""

from mysite.forum.models import message, message

addr = "130.216.24.19"
port = "8008"

import urllib2
from xml.dom.minidom import parseString

n=0 #counter for messages alredy added

def parse_message(message):
    """ Given a DOM object representing a message entry, return a 
        dictionary

           <message ID="">
              <title></title>
              <category></category>
              <creator></creator>
              <created></created>
              <status></status>
              <lastchange></lastchange>
           </message>
    """

    messageID = message.getAttribute("ID")

    # we assume that there is only one element matching the tag. ie. a message doesn't have two titles
    # This may need more error checking for missing or invalid elements.
    titleNode = message.getElementsByTagName("title")[0]
    categoryNode = message.getElementsByTagName("category")[0]
    creatorNode = message.getElementsByTagName("creator")[0]
    createdNode = message.getElementsByTagName("created")[0]
    statusNode = message.getElementsByTagName("status")[0]
    lastchangeNode = message.getElementsByTagName("lastchange")[0]
   
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
  
    return (messageID, {'title': title, 'category':category, 'creator':creator, 'created':created, 'status': status, 'lastchange': lastchange} )
    

def parse_message_xml(data):
    """ Takes a string containing XML message data and returns a dictionary of
        message dictionaries, keyed by messageID
    """

    # An empty dict to start storing out messages in
    messages = {}
    doc = parseString(data)

    # Make sure we have the right kind of data
    assert doc.documentElement.tagName == "messages"

    #go through each "message"
    message_els = doc.getElementsByTagName("message")
    for message in message_els:
        # parse this specific message into a dictionary
        (messageID, messageInfo) = parse_message(message)
        if messageID:
            messages[messageID] = messageInfo
        else:
            #if messageID isn't set, there was an error parsing so we ignore it
            print "Bad message data?"
      
    return messages

def get_messages(addr, port):
    """ Connect to node, port, and fetch a string full of message information
    """
    f = urllib2.urlopen("http://%s:%s/getmessages" % (addr, port)) 
    data = f.read()
    f.close()

    return data


# Fetch message xml from other node
message_data = get_messages(addr, port)

# Convert xml into dictionary
messages = parse_message_xml(message_data)

# Display some of the information to screen so we know it worked
for messageID in messages.keys():
    try:
        b=message(creator=(messages[messageID]['creator']), title=(messages[messageID]['title']), category=(messages[messageID]['category']),status=(messages[messageID]['status']),messageID=(messageID))
        b.save()
        m=m+1
    except:
        n=n+1

print ('%s messages already added' %(n))

