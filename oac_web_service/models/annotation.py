from oac_web_service.models.foxml import Foxml
from oac_web_service.models.fedora import Fedora

class Annotation(object):
    def __init__(self, **kwargs):
        self._body = None
        self._annotation = None
        self._errors = []
        self._body_mimetype = None

        # Required fields
        self._source_uri = kwargs.pop('source_uri')
        self._dc_title = kwargs.pop('dc_title')
        self._body_uri = kwargs.pop('body_uri', None)

        if self._body_uri is None:
            #try:
            self._body_content = kwargs.pop('body_content')
            self._body_mimetype = kwargs.pop('body_mimetype')
            self.build_body()
            assert self._body_uri is not None
            #except:
            #    raise AnnotationError("Could not create the (B-1) body object from passed parameters")

        # Optional fields
        self._annotated = kwargs.pop('annotated', None)
        self._annotator = kwargs.pop('annotator', None)
        self._generator = kwargs.pop('generator', None)
        self._oax_style_uri = kwargs.pop('oax_style_uri', None)
        self._oa_selector = kwargs.pop('oa_selector', None)
        self._oa_selector_type_uri = kwargs.pop('oa_selector_type_uri', None)

    def build_body(self):
        self._body_pid = Fedora.get_pid()

        foxml = Foxml(pid=self._body_pid)
        # Object Properties
        foxml.create_object_properties()
        # Dublin Core Datastream
        dublin_core = Foxml.get_dublin_core_element(pid=self._body_pid, title="Open Annotation Collaboration body object (B-1)")
        foxml.create_dublin_core_datastream(dublin_core_element=dublin_core)
        # Attach body
        foxml.create_body_content_datastream(body_mimetype=self._body_mimetype, body_content=self._body_content)

        self._body_uri = "info:fedora/%s" % self._body_pid
        self._body = foxml.get_foxml()

    def build_annotation(self):
        self._annotation_pid = Fedora.get_pid()

        foxml = Foxml(pid=self._annotation_pid)
        self._annotation_uri = "info:fedora/%s" % self._annotation_pid

        # Object Properties
        foxml.create_object_properties()
        # Dublin Core Datastream
        dc_uri = "%s/DC" % self._annotation_uri
        dublin_core = Foxml.get_dublin_core_element(pid=self._annotation_pid, title=self._dc_title)
        foxml.create_dublin_core_datastream(dublin_core_element=dublin_core, fedora_uri=dc_uri)

        # Annotation Datastream
        anno_uri = "%s/annotation" % self._annotation_uri
        annotation_rdf = Foxml.get_annotation_rdf_element(pid=self._annotation_pid,
                                                          body_uri=self._body_uri,
                                                          oa_selector=self._oa_selector,
                                                          body_mimetype=self._body_mimetype,
                                                          annotated=self._annotated,
                                                          generator=self._generator,
                                                          annotator=self._annotator)
    
        foxml.create_annotation_datastream(annotation_rdf_element=annotation_rdf, fedora_uri=anno_uri)
        
        if self._oa_selector is not None:
            # SpecificTarget Datastream
            sptg_uri = "%s/specifictarget" % self._annotation_uri
            specific_target_rdf_element = Foxml.get_specific_target_rdf_element(pid=self._annotation_pid,
                                                                                source_uri=self._source_uri,
                                                                                oax_style_uri=self._oax_style_uri)
            foxml.create_specific_target_datastream(specific_target_rdf_element=specific_target_rdf_element,
                                                    fedora_uri=sptg_uri)

            # Selector Datastream
            sele_uri = "%s/selector" % self._annotation_uri
            selector_rdf_element = Foxml.get_selector_rdf_element(  pid=self._annotation_pid,
                                                                    oa_selector=self._oa_selector,
                                                                    oa_selector_type_uri=self._oa_selector_type_uri)
            foxml.create_selector_datastream(selector_rdf_element=selector_rdf_element, fedora_uri=sele_uri)

        self._annotation = foxml.get_foxml()

    def validate(self):
        """
            Validate that the body and annotation objects
            were created in Fedora correctly
        """
        if not len(self._errors) == 0:
            raise AnnotationError(" ".join(self._errors))
        else:
            return True

    def submit(self):
        """
            Send body and annotate objects to Fedora
        """
        if self._body:
            self._body_response = Fedora.post_foxml(element=self._body)

        if self._annotation:
            self._annotation_response = Fedora.post_foxml(element=self._annotation)

    def get_results(self):
        return  {
                    'errors'            : self._errors,
                    'body_pid'          : self._body_pid,
                    'annotation_pid'    : self._annotation_pid
                }
    results = property(get_results, None)

class AnnotationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)