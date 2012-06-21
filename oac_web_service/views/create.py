import traceback
from datetime import datetime
from flask import request, jsonify
from oac_web_service import app, db_path
from oac_web_service.models.annotation import Annotation, AnnotationError
from xml.etree.ElementTree import tostring
from java.io import ByteArrayInputStream
from java.lang import String
from com.hp.hpl.jena.tdb import TDBFactory
from com.hp.hpl.jena.tdb import TDB
from com.hp.hpl.jena.query import ReadWrite

@app.route('/create', methods=['POST'])
def create():
    """
        POST a new annotation with the following parameters:

        Required Parameters:

        source_uri:             The URI for the whole target object

        dc_title:               Dublin Core title associated with the annotation, 
                                i.e. "dublin core title goes here" 

        body_content:           Contents of the body (XML, text, json, etc.)
            AND
        body_mimetype:          Mimetype of the body_content

            OR

        body_uri:               URI pointing to the body of the annotation


        Optional Parameters:

        annotator:              A string representing a user ID (0 or more)
                                ie. 'Charly'

        generator:              A string representing what generated the annotation
                                ie. 'Web Client'

        oax_style_uri:          A URI for a XSLT stylesheet used to render the whole target object. (0 or 1)

        oa_selector:            A string with the selector value(0 or 1)

        oa_selector_type_uri:   TBD (0 or 1)


        Will create 1 or 2 Fedora objects.  One will represent the actual annotation (A-1)
        and one will be the body of text that annotates the Fedora object (B-1).

        >>> import urllib
        >>> import urllib2
        >>> post_url = "http://localhost:5000/create"
        >>> params = { 
                "source_uri"    : "test:1#xpointer('/foo')",
                "body_content"  : "<TEI><body>text body</body></TEI>",
                "body_mimetype" : "text/xml",
                "dc_title"      : "Open Annotation Collaboration Annotation object (A-1)"
            }
        >>> encoded_data = urllib.urlencode( params )
        >>> request = urllib2.Request( post_url, encoded_data )
        >>> response = urllib2.urlopen( request )
        >>> print response.read()
        {
          "errors": [],
          "body_pid": "changeme:180",
          "annotation_pid": "changeme:181"
        }
    """

    try:
        annote = Annotation(source_uri = request.form.get('source_uri'),
                            dc_title = request.form.get('dc_title'),
                            annotated = datetime.utcnow(),
                            body_content = request.form.get('body_content', None),
                            body_mimetype = request.form.get('body_mimetype', None),
                            body_uri = request.form.get('body_uri', None),
                            annotator = request.form.get('annotator', None),
                            generator = request.form.get('generator', None),
                            oax_style_uri = request.form.get('oax_style_uri', None),
                            oa_selector = request.form.get('oa_selector', None),
                            oa_selector_type_uri = request.form.get('oa_selector_type_uri', None))
        
        annote.create()
        annote.submit()
        if annote.validate():
            rdfxml = String(tostring(annote.annotation_rdf))
            input_stream = ByteArrayInputStream(rdfxml.getBytes())

            # Start dataset transaction
            dataset = TDBFactory.createDataset(db_path)
            dataset.begin(ReadWrite.WRITE)
            try:
                model = dataset.getDefaultModel()
                model.begin()
                model.read(input_stream, None)
                model.commit()
                model.close()
                dataset.commit() 
            except Exception, exc:
                raise
            finally:
                input_stream.close()
                dataset.end()
                TDB.sync(dataset)
            
    except AnnotationError, ex:
        return jsonify({'value' : ex.value, 'trace' : traceback.format_stack()})
    except Exception, ex:
        raise
    else:
        # LOOK: https://github.com/mitsuhiko/flask/issues/478
        # return jsonify(annote.results), 201
        resp = jsonify(annote.results)
        resp.status_code = 201
        return resp