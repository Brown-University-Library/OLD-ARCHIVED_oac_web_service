from flask import request, make_response
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError

@app.route('/show', methods=['GET'])
def show():
    """
        A GET method that takes an Annotation (A-1) PID 
        and serializes all of the triples as RDF/XML.
    """
    try:
        pid = request.args.get('pid')
        result = Annotation.serialize(pid)
    except AnnotationError, ex:
        return jsonify({'value' : ex.value, 'trace' : traceback.format_stack()})
    except Exception, ex:
        raise
    else:
        response = make_response(result)
        response.mimetype = 'application/rdf+xml'
        return response