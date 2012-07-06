from flask import request, make_response
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError

@app.route('/show', methods=['GET'])
def show():
    """
        A GET method that takes an Annotation (A-1) PID 
        and an optional format and serializes all of the 
        triples.

        Format options are:
            - rdf/xml or xml (default)
            - rdf/json or json
            - turtle or ttl
            - nt
            - n3
            

    """
    try:
        pid = request.args.get('pid')
        format = request.args.get('format', 'rdf/xml')
        result, mimetype = Annotation.serialize(pid, format)
    except AnnotationError, ex:
        return jsonify({'value' : ex.value, 'trace' : traceback.format_stack()})
    except Exception, ex:
        raise
    else:
        response = make_response(result)
        response.mimetype = mimetype
        return response