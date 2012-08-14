FEDORA_HOST = ""
FEDORA_PORT = ""
FEDORA_USER = ""
FEDORA_PASS = ""

# The Username and Password to access the OAC services
# that manipulate data.
OAC_USER = ""
OAC_PASS = ""

DEFUALT_ANNOTATION_CONTENT_MODEL = "oac:oa-annotation"

# The folder location where the index store should be created and kept.
# Path needs to be writable by the user running Tomcat
# Path needs to be absolute	
STORE_LOCATION = ""

BASE_WEBAPP_FOLDER = "fedora"

object_path = "/%s/objects" % BASE_WEBAPP_FOLDER
FEDORA_OBJECT_PID_URL = "%s:%s%s/{pid}" % (FEDORA_HOST, FEDORA_PORT, object_path)

pid_path = "%s/nextPID" % object_path
FEDORA_PID_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, pid_path)

ingest_path = "%s/new" % object_path
FEDORA_INGEST_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ingest_path)

list_path = "%s/{pid}/datastreams" % object_path
FEDORA_LIST_DATASTREAMS_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, list_path)

ds_path = "%s/{dsid}" % list_path
FEDORA_DATASTREAM_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ds_path)
FEDORA_GET_DATASTREAM_URL = "%s:%s%s/content" % (FEDORA_HOST, FEDORA_PORT, ds_path)

FEDORA_SPARQL_QUERY_URL = "%s:%s/%s/risearch" % (FEDORA_HOST, FEDORA_PORT, BASE_WEBAPP_FOLDER)
