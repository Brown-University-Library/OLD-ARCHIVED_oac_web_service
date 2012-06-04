import unittest
from oac_web_service.models.annotation import Annotation
import oac_web_service.fedora_settings as config
from xml.etree.ElementTree import dump

class FoxmlTest(unittest.TestCase):
    def setUp(self):
        self.annotation = Annotation(source_uri = "demo:26#xpointer('//cow')",
                                     dc_title = "Annotation about my love of the the word 'cow'",
                                     body_content = '<TEI><body>I love the word cow!</body></TEI>',
                                     body_mimetype = 'text/xml')
        self.annotation.create()
    
    def test_submission(self):
        self.annotation.submit()
        assert self.annotation.validate()