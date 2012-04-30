class Annotation(object):
    def __init__(self, **kwargs):
        self._target_pid = kwargs.pop('target_pid')
        self._target_uri = kwargs.pop('target_uri')
        self._body_xml = kwargs.pop('body_xml')
        self._dc_title = kwargs.pop('dc_title')
        # Completed by create_body
        self._body_pid = None
        self._errors = []

    def create_body(self):
        self._body_pid = "1"

    def create_annotation(self):
        self._annotation_pid = "2"

    def validate(self):
        """
            Validate that the body and annotation objects
            were created in Fedora correctly
        """
        return len(self._errors == 0)

    def submit(self):
        """
            Create body and annotate objects in Fedora
        """

class AnnotationError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)