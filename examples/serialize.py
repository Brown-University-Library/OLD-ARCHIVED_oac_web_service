#! ~/Envs/oac/bin/jython

import urllib
import urllib2
get_url = "http://daxdev.services.brown.edu:8081/oac_web_service/show"
params = { 
  "pid"		: "changeme:9",
  "format"	: "json"
}
args = urllib.urlencode( params )
request = urllib2.Request( get_url + "?" + args)
response = urllib2.urlopen( request )
print response.read()

