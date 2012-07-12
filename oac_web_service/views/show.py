import traceback
from flask import request, make_response, jsonify
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError

@app.route('/show', methods=['GET'])
def show():
    """
        A GET method that takes a comma seperated list of Annotation
        (A-1) PIDs to serialize as the 'pid' parameter.
        
        An optional 'format' parameter to output the serialization 
        in different formats.

        Format options are:
            - rdf/xml or xml (default)
            - rdf/json or json
            - turtle or ttl
            - nt
            - n3
    """
    try:
        pid = request.args.get('pid', "")
        pids = filter(None, pid.split(','))
        if len(pids) == 0:
            raise AnnotationError("Must pass in at least one PID using the 'pid' parameter.")
        format = request.args.get('format', 'rdf/xml')
        result, mimetype = Annotation.serialize(pids, format)
    except AnnotationError, ex:
        return jsonify({'value' : ex.value, 'trace' : traceback.format_stack()})
    except Exception, ex:
        raise
    else:
        response = make_response(result)
        response.mimetype = mimetype
        return response