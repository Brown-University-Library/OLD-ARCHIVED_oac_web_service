import sys
import traceback
from flask import render_template
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError

@app.route('/annotate', methods=['POST'])
def annotate():
    """
        POST a new annotation with the following parameters:

        target_url: uri to what is being annotated, 
                    i.e. repo:1234#xpointer('//foo') 

        body_xml: annotation in xml format, 
                  i.e. <TEI><body>Some TEI text goes here.</body></TEI>

        dc_title: Dublin Core title associated with the annotation, 
                  i.e. "dublin core title goes here" 

        target_pid: Fedora PID for the target object,
                    i.e. repo:1234


        Will create 2 Fedora objects.  One will represent the actual annotation (A-1)
        and one will be the body of text that annotates the Fedora object (B-1).
        Therefore, the annotation object (A-1) will connect the Fedora object being 
        annotated (T-1) and the object containing the annotation content (B-1) via RDF. 
        These relationships are stored in the Fedora Commons datastream RELS-EXT.

        A-1 oac:hasBody B-1 
        A-1 oac:hasTarget T-1# 
        B-1 oac:annotates T-1

        Therefore Fedora object repo:1234 (T-1) is annotated by repo:1235 (A-1) and the
        body of the annotation (B-1) contains the annotation text.

    """

    try:
        annote = Annotation( target_pid = request.args['target_pid'],
                             body_xml = request.args['body_xml'],
                             target_uri = request.args['target_uri'],
                             dc_title = request.args['dc_title']
                            )
        annote.build_body()
        annote.build_annotation()
        annote.submit()
        annote.validate()
    except AnnotationError, ex:
        return render_template('error.html', error=ex.value, trace=traceback.format_stack())
    else:
        return make_response("OK", 201)
        
