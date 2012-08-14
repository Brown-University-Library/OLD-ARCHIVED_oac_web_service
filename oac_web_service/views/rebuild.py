import traceback
from flask import request, make_response, jsonify
from oac_web_service import app
from oac_web_service.models.annotation import Annotation, AnnotationError
from oac_web_service.utils import requires_auth
from oac_web_service.models.fedora import Fedora
from java.io import ByteArrayInputStream
from java.lang import String
from com.hp.hpl.jena.tdb import TDBFactory
from com.hp.hpl.jena.tdb import TDB
from com.hp.hpl.jena.query import ReadWrite

@app.route('/rebuild', methods=['GET'])
@requires_auth
def rebuild():
    """
        A GET method that will rebuild the internal TDB index
        with all of the Annotation objects in Fedora 
    """
    try:
        query = "prefix fm: <info:fedora/fedora-system:def/model#> select ?s where {?s fm:hasModel <info:fedora/%s> }" \
                 % app.config.get('DEFUALT_ANNOTATION_CONTENT_MODEL')
        all_pids = (p.lstrip('info:fedora/') for p in Fedora.get_sparql_query_resuts(query))
        result, mimetype = Annotation.serialize(all_pids, format='nt', check_object=False)

        dataset = TDBFactory.createDataset(app.config['STORE_LOCATION'])

        # Remove all entries from the default model
        dataset.begin(ReadWrite.WRITE)
        try:
            model = dataset.getDefaultModel()
            model.begin()
            model.removeAll()
            model.commit()
            model.close()
            dataset.commit()
        except Exception, exc:
            raise
        finally:
            dataset.end()
            TDB.sync(dataset)

        # Load the triples
        dataset.begin(ReadWrite.WRITE)
        try:
            model = dataset.getDefaultModel()
            model.begin()
            n3_input_stream = ByteArrayInputStream(String(result).getBytes())            
            model.read(n3_input_stream, None, "N-TRIPLE")
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
        return make_response("success")