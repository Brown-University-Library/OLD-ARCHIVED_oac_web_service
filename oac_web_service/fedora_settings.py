FEDORA_HOST = ""
FEDORA_PORT = ""
FEDORA_USER = ""
FEDORA_PASS = ""

# The Username and Password to access the OAC services
# that manipulate data.
OAC_USER = ""
OAC_PASS = ""

DEFUALT_ANNOTATION_CONTENT_MODEL = "bdr-cmodel:oa-annotation"

# The folder location where the index store should be created and kept.
# Path needs to be writable by the user running Tomcat
import os
STORE_LOCATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

pid_path = "/fedora/objects/nextPID"
FEDORA_PID_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, pid_path)

ingest_path = "/fedora/objects/new"
FEDORA_INGEST_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ingest_path)

list_path = "/fedora/objects/{pid}/datastreams"
FEDORA_LIST_DATASTREAMS_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, list_path)

ds_path = "%s/{dsid}" % list_path
FEDORA_DATASTREAM_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ds_path)
FEDORA_GET_DATASTREAM_URL = "%s:%s%s/content" % (FEDORA_HOST, FEDORA_PORT, ds_path)

