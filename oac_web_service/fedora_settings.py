FEDORA_HOST = ""
FEDORA_PORT = ""
FEDORA_USER = ""
FEDORA_PASS = ""

pid_path = "/fedora/management/getNextPID?xml=true"
FEDORA_PID_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, pid_path)

ingest_path = "/fedora/objects/new"
FEDORA_INGEST_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, ingest_path)

update_path = "/fedora/objects/{pid}/datastreams/{dsid}"
FEDORA_UPDATE_URL = "%s:%s%s" % (FEDORA_HOST, FEDORA_PORT, update_path)
