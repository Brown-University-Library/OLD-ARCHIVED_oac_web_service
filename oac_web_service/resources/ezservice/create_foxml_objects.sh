java -jar saxon9.jar -xsl:ezdef.xsl -versionmsg:off -s:ez_sdef_serialize.xml > serialize_sdef_foxml.xml

java -jar saxon9.jar -xsl:ezdep.xsl -versionmsg:off -s:ez_sdep_serialize.xml ezdef=ez_sdef_serialize.xml > serialize_sdep_foxml.xml