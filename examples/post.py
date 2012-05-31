#! ~/Envs/oac/bin/jython

import urllib
import urllib2
post_url = "http://localhost:8080/oac_web_service/annotate"
params = { 
    "targets" : [
        {'pid' : 'test:1', 'uri' : "test:1#xpointer('/foo')"},
        {'pid' : 'test:2', 'uri' : "test:2#xpointer('/bar')"}
    ],
    "body_xml"       : "<TEI><body>text body</body></TEI>",
    "dc_title"       : "Open Annotation Collaboration Annotation object (A-1)",
    "annotator"      : "Some Person",
    "generator"      : "Web client",
    "model_version"  : "1-Alpha",
    "type"           : "Amazing Annotation"
}
encoded_data = urllib.urlencode( params )
request = urllib2.Request( post_url, encoded_data )
response = urllib2.urlopen( request )