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
from com.hp.hpl.jena.update import UpdateExecutionFactory
from com.hp.hpl.jena.update import GraphStoreFactory
from com.hp.hpl.jena.update import UpdateFactory
from com.hp.hpl.jena.rdf.model import ResourceFactory

@app.route('/rebuild_all', methods=['GET'])
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


@app.route('/rebuild_one', methods=['POST'])
def rebuild_one():
    """
        A POST method that will rebuild the internal TDB index
        with a specific PID from Fedora
    """

    pid = request.form.get('pid', None)
    if pid is None:
        raise AnnotationError("Please pass a PID parameter to the rebuild POST request")

    print  "calling 'rebuild_one' with PID: %s" % pid

    try:
        # Get PID from Fedora and serialize it
        result, mimetype = Annotation.serialize([pid], format='nt', check_object=True)

        # Don't do anything if this there are no serialization results 
        # ie. was not an Annotation object

        dataset = TDBFactory.createDataset(app.config['STORE_LOCATION'])

        # Remove all triples from TDB involving this PID using SPARQL
        # This was my first attempt, but the SPARQL query does not
        # seem to be working.  Using the Jena API (below) also works.
        """
        query = "DELETE { ?s ?p ?o } WHERE { <info:fedora/%s> ?p ?o }" % pid
        update = UpdateFactory.create(String(query))
        dataset.begin(ReadWrite.WRITE)
        try:
            graph_store = GraphStoreFactory.create(dataset.getDefaultModel())
            update_processor = UpdateExecutionFactory.create(update, graph_store)
            results = update_processor.execute()
        except Exception, exc:
            raise
        finally:
            dataset.end()
            TDB.sync(dataset)
        """

        # Remove all triples from TDB involving this PID using Jena API
        # Start dataset WRITE transaction
        dataset.begin(ReadWrite.WRITE)
        try:
            resource = ResourceFactory.createResource("info:fedora/%s" % pid)
            model = dataset.getDefaultModel()
            model.removeAll(resource, None, None)
            model.commit()
            model.close()
            dataset.commit() 
        except Exception, exc:
            raise
        finally:
            dataset.end()
            TDB.sync(dataset)

        # Add new triples to TDB
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
