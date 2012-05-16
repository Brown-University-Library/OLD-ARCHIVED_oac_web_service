import unittest
from oac_web_service.models.annotation import Annotation
import oac_web_service.fedora_settings as config
from xml.etree.ElementTree import dump

class FoxmlTest(unittest.TestCase):
    def setUp(self):
        self.annotation = Annotation(targets = [{'pid' : 'demo:26', 'uri' : "demo:26#xpointer('//cow')"},
                        						{'pid' : 'demo:SmileyDinnerware', 'uri' : "demo:SmileyDinnerware#xpointer('//somepixelreference')"}],
                                     body_xml = '<TEI><body>I love the word cow!</body></TEI>',
                                     dc_title = "Annotation about my love of the the word 'cow'"
                                    )

    def test_pid_creation(self):
        pid1 = int(self.annotation.get_pid().split(":")[-1])
        pid2 = int(self.annotation.get_pid().split(":")[-1])
        assert pid2 > pid1

    def test_submission(self):
    	self.annotation.build_body()
        self.annotation.build_annotation()
        self.annotation.submit()
        assert self.annotation.validate()