import traceback
from datetime import datetime
from flask import request, jsonify
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError
from xml.etree.ElementTree import tostring
from java.io import ByteArrayInputStream
from java.lang import String
from com.hp.hpl.jena.tdb import TDBFactory
from com.hp.hpl.jena.tdb import TDB
from com.hp.hpl.jena.query import ReadWrite
from oac_web_service.utils import requires_auth

@app.route('/create', methods=['POST'])
@requires_auth
def create():
    """
        A POST method that creates an Annotation (A-1) object
        based on a number of parameters.

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

        oa_selector_type_uri:   Required if an oa_selector is passed in
                                ie. oa:Fragment

        fragment_type:          URI describing the oa_selector type  Optional and only used if
                                an oa_selector is passed in.
                                ie. 'http://www.w3.org/TR/xpath/'

        body_content_model:     A string representing the body's content model
                                ie. 'tei-annotation'


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
                            body_content_model = request.form.get('body_content_model', None),
                            annotator = request.form.get('annotator', None),
                            generator = request.form.get('generator', None),
                            oax_style_uri = request.form.get('oax_style_uri', None),
                            oa_selector = request.form.get('oa_selector', None),
                            oa_selector_type_uri = request.form.get('oa_selector_type_uri', None),
                            fragment_type = request.form.get('fragment_type', None))
        
        annote.create()
        annote.submit()
        if annote.validate():
            # Start dataset transaction
            dataset = TDBFactory.createDataset(app.config['STORE_LOCATION'])
            dataset.begin(ReadWrite.WRITE)
            try:
                model = dataset.getDefaultModel()
                model.begin()
                if annote.annotation_rdf is not None:
                    anno_input_stream = ByteArrayInputStream(String(tostring(annote.annotation_rdf)).getBytes())
                    model.read(anno_input_stream, None)
                    anno_input_stream.close()
                if annote.specific_target_rdf_element is not None:
                    spectaget_input_stream = ByteArrayInputStream(String(tostring(annote.specific_target_rdf_element)).getBytes())
                    model.read(spectaget_input_stream, None)
                    spectaget_input_stream.close()
                if annote.selector_rdf_element is not None:
                    selector_input_stream = ByteArrayInputStream(String(tostring(annote.selector_rdf_element)).getBytes())
                    model.read(selector_input_stream, None)
                    selector_input_stream.close()
                if annote.rels_ext_rdf_element is not None:
                    relsext_input_stream = ByteArrayInputStream(String(tostring(annote.rels_ext_rdf_element)).getBytes())
                    model.read(relsext_input_stream, None)
                    relsext_input_stream.close()
                model.commit()
                model.close()
                dataset.commit() 
            except Exception, exc:
                raise
            finally:
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