#! ~/Envs/oac/bin/jython

import urllib
import urllib2
post_url = "http://localhost:5000/annotate"
params = { 
    "source_uri"            : "test:1#xpointer('/foo')",
    "body_content"          : "<TEI><body>text body</body></TEI>",
    "body_mimetype"         : "text/xml",
    "dc_title"              : "Open Annotation Collaboration Annotation object (A-1)",
    "oa_selector"           : "/for/example/an/xpath/statement",
    "oa_selector_type_uri"  : "oa:Fragment"
}
encoded_data = urllib.urlencode( params )
request = urllib2.Request( post_url, encoded_data )
response = urllib2.urlopen( request )
print response.read()


"""
Creates two objects.

BODY:
<foxml:digitalObject VERSION="1.1" PID="changeme:307" xsi:schemaLocation="info:fedora/fedora-system:def/foxml# http://www.fedora.info/definitions/1/0/foxml1-1.xsd">
  <foxml:objectProperties>
    <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="Active"/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="OAC object"/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#ownerId" VALUE=""/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#createdDate" VALUE="2012-05-31T05:32:00.714Z"/>
    <foxml:property NAME="info:fedora/fedora-system:def/view#lastModifiedDate" VALUE="2012-05-31T05:32:00.714Z"/>
  </foxml:objectProperties>
  <foxml:datastream ID="DC" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" CREATED="2012-05-31T05:32:00.736Z" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/" SIZE="412">
      <foxml:xmlContent>
        <oai_dc:dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
          <dc:title>Open Annotation Collaboration body object (B-1)</dc:title>
          <dc:identifier>changeme:307</dc:identifier>
        </oai_dc:dc>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
  <foxml:datastream ID="OAC_BODY" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="OAC_BODY.0" LABEL="OAC Body Content" CREATED="2012-05-31T05:32:00.736Z" MIMETYPE="text/xml" SIZE="35">
      <foxml:xmlContent>
        <TEI>
          <body>text body</body>
        </TEI>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
</foxml:digitalObject>


ANNOTATION:
<foxml:digitalObject VERSION="1.1" PID="changeme:308" xsi:schemaLocation="info:fedora/fedora-system:def/foxml# http://www.fedora.info/definitions/1/0/foxml1-1.xsd">
  <foxml:objectProperties>
    <foxml:property NAME="info:fedora/fedora-system:def/model#state" VALUE="Active"/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#label" VALUE="OAC object"/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#ownerId" VALUE=""/>
    <foxml:property NAME="info:fedora/fedora-system:def/model#createdDate" VALUE="2012-05-31T05:42:40.086Z"/>
    <foxml:property NAME="info:fedora/fedora-system:def/view#lastModifiedDate" VALUE="2012-05-31T05:42:40.086Z"/>
  </foxml:objectProperties>
  <foxml:datastream ID="DC" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="DC1.0" LABEL="Dublin Core Record for this object" CREATED="2012-05-31T05:42:40.106Z" MIMETYPE="text/xml" FORMAT_URI="http://www.openarchives.org/OAI/2.0/oai_dc/" SIZE="418">
      <foxml:xmlContent>
        <oai_dc:dc xsi:schemaLocation="http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd">
          <dc:title>Open Annotation Collaboration Annotation object (A-1)</dc:title>
          <dc:identifier>changeme:308</dc:identifier>
        </oai_dc:dc>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
  <foxml:datastream ID="annotation" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="annotation.0" LABEL="" CREATED="2012-05-31T05:42:40.106Z" MIMETYPE="text/xml" SIZE="811">
      <foxml:xmlContent>
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/changeme:308">
            <rdf:type rdf:resource="oa:Annotation"/>
            <oax:hasBody rdf:resource="info:fedora/changeme:307"/>
            <oax:modelVersion rdf:resource="http://www.openannotation.org/spec/core/20120509.html"/>
            <oax:hasTarget rdf:resource="info:fedora/changeme:308/SpecificTarget"/>
          </rdf:Description>
          <rdf:Description rdf:about="info:fedora/changeme:308">
            <rdf:type rdf:resource="oa:Body"/>
            <dc:format>text/xml</dc:format>
          </rdf:Description>
        </rdf:RDF>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
  <foxml:datastream ID="specifictarget" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="specifictarget.0" LABEL="SpecificTarget data for OAC annotation" CREATED="2012-05-31T05:42:40.106Z" MIMETYPE="application/rdf+xml" SIZE="492">
      <foxml:xmlContent>
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/changeme:308/SpecificTarget">
            <rdf:type rdf:resource="oa:SpecificResource"/>
            <oax:hasSource rdf:resource="test:1#xpointer('/foo')"/>
            <oax:hasSelector rdf:resource="info:fedora/changeme:308/selector"/>
          </rdf:Description>
        </rdf:RDF>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
  <foxml:datastream ID="selector" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="selector.0" LABEL="Selector data for OAC annotation" CREATED="2012-05-31T05:42:40.106Z" MIMETYPE="application/rdf+xml" SIZE="260">
      <foxml:xmlContent>
        <rdf:RDF>
          <rdf:Description rdf:about="info:fedora/changeme:308/selector">
            <rdf:type rdf:resource="oa:Fragment"/>
            <rdf:value>/for/example/an/xpath/statement</rdf:value>
          </rdf:Description>
        </rdf:RDF>
      </foxml:xmlContent>
    </foxml:datastreamVersion>
  </foxml:datastream>
</foxml:digitalObject>
"""