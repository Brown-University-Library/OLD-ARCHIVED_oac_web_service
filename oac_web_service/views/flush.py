import traceback
from flask import request, make_response, jsonify
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError
from oac_web_service.utils import requires_auth
from oac_web_service.models.fedora import Fedora

@app.route('/flush', methods=['GET'])
@requires_auth
def flush():
    """
        A GET method that will serialize (dump) all Annotation objects in Fedora.

        An optional 'format' parameter to output the serialization 
        in different formats.

        Format options are:
            - nt (default)
            - rdf/xml or xml
            - rdf/json or json
            - turtle or ttl
            - n3
    """
    try:
        format = request.args.get('format', 'nt')
        query = "prefix fm: <info:fedora/fedora-system:def/model#> select ?s where {?s fm:hasModel <info:fedora/%s> }" \
                 % app.config.get('DEFUALT_ANNOTATION_CONTENT_MODEL')
        all_pids = (p.lstrip('info:fedora/') for p in Fedora.get_sparql_query_resuts(query))
        result, mimetype = Annotation.serialize(all_pids, format=format, check_object=False)
    except AnnotationError, ex:
        return jsonify({'value' : ex.value, 'trace' : traceback.format_stack()})
    except Exception, ex:
        raise
    else:
        response = make_response(result)
        response.mimetype = mimetype
        return response