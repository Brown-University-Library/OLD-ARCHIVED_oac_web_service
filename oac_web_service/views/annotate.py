import sys
import traceback
from flask import render_template
from flask import request
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError

@app.route('/annotate', methods=['POST'])
def annotate():
    """
        POST a new annotation with the following parameters:

        targets:  list of targets (dictionaries) contianing the 'pid' and 'uri' of each target
                  i.e. [{'pid' : 'test:1', 'uri' : "test:1#xpointer('/foo)"},{'pid' : 'test:2', 'uri' : "test:2#xpointer('/bar)"}]

        body_xml: annotation in xml format, 
                  i.e. <TEI><body>Some TEI text goes here.</body></TEI>

        dc_title: Dublin Core title associated with the annotation, 
                  i.e. "dublin core title goes here" 

        Will create 2 Fedora objects.  One will represent the actual annotation (A-1)
        and one will be the body of text that annotates the Fedora object (B-1).
        Therefore, the annotation object (A-1) will connect the Fedora object being 
        annotated (T-1) and the object containing the annotation content (B-1) via RDF. 
        These relationships are stored in the Fedora Commons datastream RELS-EXT.

        A-1 oa:hasBody B-1 
        A-1 oa:hasTarget T-1# 
        B-1 oa:annotates T-1

        Therefore Fedora object repo:1234 (T-1) is annotated by repo:1235 (A-1) and the
        body of the annotation (B-1) contains the annotation text.

        >>> import urllib
        >>> import urllib2
        >>> post_url = "http://127.0.0.1:5000/annotate"
        >>> params = { 
                "targets" : [
                    {'pid' : 'test:1', 'uri' : "test:1#xpointer('/foo)"},
                    {'pid' : 'test:2', 'uri' : "test:2#xpointer('/bar)"}
                ],
                "body_xml" : "<TEI><body>text body</body></TEI>",
                "dc_title" : "Dublin Core Title"
            }
        >>> encoded_data = urllib.urlencode( params )
        >>> request = urllib2.Request( post_url, encoded_data )
        >>> response = urllib2.urlopen( request )

    """

    try:
        annote = Annotation(targets = request.form['targets'],
                            body_xml = request.form['body_xml'],
                            dc_title = request.form['dc_title'])
        annote.build_body()
        annote.build_annotation()
        annote.submit()
        annote.validate()
    except AnnotationError, ex:
        return render_template('error.html', error=ex.value, trace=traceback.format_stack())
    else:
        return make_response("OK", 201)
        
