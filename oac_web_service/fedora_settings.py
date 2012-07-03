FEDORA_HOST = ""
FEDORA_PORT = ""
FEDORA_USER = ""
FEDORA_PASS = ""

DEFUALT_ANNOTATION_CONTENT_MODEL = "bdr-cmodel:oa-annotation"

pid_path = "/fedora/management/getNextPID?xml=true"
FEDORA_PID_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, pid_path)

ingest_path = "/fedora/objects/new"
FEDORA_INGEST_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ingest_path)

list_path = "/fedora/objects/{pid}/datastreams"
FEDORA_LIST_DATASTREAMS_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, list_path)

get_path = "/fedora/get/{pid}/{dsid}"
FEDORA_GET_DATASTREAM_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, get_path)

ds_path = "%s/{dsid}" % list_path
FEDORA_UPDATE_DATASTREAM_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ds_path)

