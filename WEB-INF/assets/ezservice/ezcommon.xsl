<?xml version="1.0" encoding="utf-8"?>
<!--
  Fedora EZDef XSLT1.1 Stylesheet, version 1.0
  Common templates and attribute sets for ezdef.xsl and ezdep.xsl
  Swithun Crowe cs2@st-andrews.ac.uk
-->

<xsl:stylesheet 
		version="1.1"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		>
	
	<!-- Format - foxml or mets -->
	<xsl:param name="format">foxml</xsl:param>

	<!-- useful variables -->
	<xsl:variable name="foxml_version">1.1</xsl:variable>

	<!-- start processing using format to pick template -->
	<xsl:template match="/">
		<xsl:choose>
			<xsl:when test="$format = 'mets'">
				<xsl:apply-templates mode="mets"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:apply-templates mode="foxml"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	
	<!-- User Input -->
	<xsl:template match="user-input">
		<fmm:UserInputParm 
				xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap" 
				parmName="{@name}" 
				defaultValue="{@default}" 
				passBy="VALUE" 
				required="{boolean(not(@optional='true'))}"
				>
			<xsl:if test="valid">
				<fmm:ValidParmValues>
					<xsl:apply-templates/>
				</fmm:ValidParmValues>
			</xsl:if>
		</fmm:UserInputParm>
	</xsl:template>

	<!-- Valid -->
	<xsl:template match="valid">
		<fmm:ValidParm value="{@value}" xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap"/>
	</xsl:template>
	
	<!-- Attribute Sets -->

	<!-- some common ID values -->
	<xsl:attribute-set name="rels_ext_id">
		<xsl:attribute name="ID">RELS-EXT</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="rels_ext_version_id">
		<xsl:attribute name="ID">RELS-EXT1.0</xsl:attribute>
	</xsl:attribute-set>
	
	<xsl:attribute-set name="method_map_id">
		<xsl:attribute name="ID">METHODMAP</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="method_map_version_id">
		<xsl:attribute name="ID">METHODMAP1.0</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="ds_input_spec_id">
		<xsl:attribute name="ID">DSINPUTSPEC</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="ds_input_spec_version_id">
		<xsl:attribute name="ID">DSINPUTSPEC1.0</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="wsdl_id">
		<xsl:attribute name="ID">WSDL</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="wsdl_version_id">
		<xsl:attribute name="ID">WSDL1.0</xsl:attribute>
	</xsl:attribute-set>
	
	<!-- foxml:property -->
	<xsl:attribute-set name="foxml_object_property_model_state">
		<xsl:attribute name="NAME">info:fedora/fedora-system:def/model#state</xsl:attribute>
		<xsl:attribute name="VALUE">Active</xsl:attribute>
	</xsl:attribute-set>
	
	<!-- foxml:property -->
	<xsl:attribute-set name="foxml_object_property_model_label">
		<xsl:attribute name="NAME">info:fedora/fedora-system:def/model#label</xsl:attribute>
	</xsl:attribute-set>

	<!-- foxml:datastream for RELS-EXT RDF statements -->
	<xsl:attribute-set name="foxml_rdf_datastream" use-attribute-sets="rels_ext_id foxml_datastream"/>
	
	<!-- foxml:datastream for METHODMAP -->
	<xsl:attribute-set name="foxml_method_map_datastream" use-attribute-sets="method_map_id foxml_datastream"/>

	<!-- foxml:datastream for DSINPUTSPEC -->
	<xsl:attribute-set name="foxml_ds_input_spec_datastream" use-attribute-sets="ds_input_spec_id foxml_datastream"/>

	<!-- foxml:datastream for WSDL -->
	<xsl:attribute-set name="foxml_wsdl_datastream" use-attribute-sets="wsdl_id foxml_datastream"/>

	<!-- attributes common to all FOXML datastreams -->
	<xsl:attribute-set name="foxml_datastream">
		<xsl:attribute name="CONTROL_GROUP">X</xsl:attribute>
		<xsl:attribute name="STATE">A</xsl:attribute>
		<xsl:attribute name="VERSIONABLE">true</xsl:attribute>
	</xsl:attribute-set>
	
	<!-- foxml:datastreamVersion for RELS-EXT RDF statements -->
	<xsl:attribute-set name="foxml_rdf_datastream_version" use-attribute-sets="rels_ext_version_id rdf_datastream"/>

	<!-- foxml:datastreamVersion for SDef METHODMAP -->
	<xsl:attribute-set name="foxml_sdef_method_map_datastream_version" use-attribute-sets="method_map_version_id sdef_method_map_datastream"/>
	
	<!-- foxml:datastreamVersion for SDep METHODMAP -->
	<xsl:attribute-set name="foxml_sdep_method_map_datastream_version" use-attribute-sets="method_map_version_id sdep_method_map_datastream"/>

	<!-- foxml:datastreamVersion for DS INPUT SPEC -->
	<xsl:attribute-set name="foxml_ds_input_spec_datastream_version" use-attribute-sets="ds_input_spec_version_id ds_input_spec_datastream"/>

	<!-- foxml:datastreamVersion for WSDL -->
	<xsl:attribute-set name="foxml_wsdl_datastream_version" use-attribute-sets="wsdl_version_id wsdl_datastream"/>

	<!--- attributes common to both FOXML and METS datastreams -->
	<xsl:attribute-set name="rdf_datastream">
		<xsl:attribute name="FORMAT_URI">info:fedora/fedora-system:FedoraRELSExt-1.0</xsl:attribute>
		<xsl:attribute name="LABEL">RDF Statements about this object</xsl:attribute>
		<xsl:attribute name="MIMETYPE">application/rdf+xml</xsl:attribute>
	</xsl:attribute-set>
	
	<xsl:attribute-set name="sdef_method_map_datastream">
		<xsl:attribute name="FORMAT_URI">info:fedora/fedora-system:FedoraSDefMethodMap-1.0</xsl:attribute>
		<xsl:attribute name="LABEL">Abstract Method Map</xsl:attribute>
		<xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="sdep_method_map_datastream">
		<xsl:attribute name="FORMAT_URI">info:fedora/fedora-system:FedoraSDepMethodMap-1.1</xsl:attribute>
		<xsl:attribute name="LABEL">Deployment Method Map</xsl:attribute>
		<xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="ds_input_spec_datastream">
		<xsl:attribute name="FORMAT_URI">info:fedora/fedora-system:FedoraDSInputSpec-1.1</xsl:attribute>
		<xsl:attribute name="LABEL">Datastream Input Specification</xsl:attribute>
		<xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
	</xsl:attribute-set>

	<xsl:attribute-set name="wsdl_datastream">
		<xsl:attribute name="FORMAT_URI">http://schemas.xmlsoap.org/wsdl/</xsl:attribute>
		<xsl:attribute name="LABEL">WSDL Bindings</xsl:attribute>
		<xsl:attribute name="MIMETYPE">text/xml</xsl:attribute>
	</xsl:attribute-set>

	<!-- mets:metsHdr -->
	<xsl:attribute-set name="mets_hdr">
		<xsl:attribute name="RECORDSTATUS">A</xsl:attribute>
	</xsl:attribute-set>

	<!-- mets:amdSec for RELS-EXT -->
	<xsl:attribute-set name="mets_rels_ext_amdsec" use-attribute-sets="rels_ext_id mets_amdsec"/>

	<!-- mets:amdSec for METHODMAP -->
	<xsl:attribute-set name="mets_method_map_amdsec" use-attribute-sets="method_map_id mets_amdsec"/>

	<!-- mets:amdSec for DS INPUT SPEC -->
	<xsl:attribute-set name="mets_ds_input_spec_amdsec" use-attribute-sets="ds_input_spec_id mets_amdsec"/>

	<!-- mets:amdSec for WSDL -->
	<xsl:attribute-set name="mets_wsdl_amdsec" use-attribute-sets="wsdl_id mets_amdsec"/>

	<!-- attributes common to all METS amdSec elements -->
	<xsl:attribute-set name="mets_amdsec">
		<xsl:attribute name="STATUS">A</xsl:attribute>
		<xsl:attribute name="VERSIONABLE">true</xsl:attribute>
	</xsl:attribute-set>
	
	<!-- mets:mdWrap for RELS-EXT -->
	<xsl:attribute-set name="mets_rdf_mdwrap" use-attribute-sets="rdf_datastream mets_mdwrap"/>

	<!-- mets:mdWrap for SDef METHODMAP -->
	<xsl:attribute-set name="mets_sdef_method_map_mdwrap" use-attribute-sets="sdef_method_map_datastream mets_mdwrap"/>

	<!-- mets:mdWrap for SDep METHODMAP -->
	<xsl:attribute-set name="mets_sdep_method_map_mdwrap" use-attribute-sets="sdep_method_map_datastream mets_mdwrap"/>

	<!-- mets:mdWrap for DS INPUT SPEC -->
	<xsl:attribute-set name="mets_ds_input_spec_mdwrap" use-attribute-sets="ds_input_spec_datastream mets_mdwrap"/>

	<!-- mets:mdWrap for WSDL -->
	<xsl:attribute-set name="mets_wsdl_mdwrap" use-attribute-sets="wsdl_datastream mets_mdwrap"/>

	<!-- attributes common to all METS mdWrap elements -->
	<xsl:attribute-set name="mets_mdwrap">
		<xsl:attribute name="MDTYPE">OTHER</xsl:attribute>
		<xsl:attribute name="OTHERMDTYPE">UNSPECIFIED</xsl:attribute>
	</xsl:attribute-set>

	<!-- SDef PID -->
	<xsl:attribute-set name="sdef_pid" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
		<xsl:attribute name="rdf:resource">info:fedora/fedora-system:ServiceDefinition-3.0</xsl:attribute>
	</xsl:attribute-set>
	
	<!-- SDep PID -->
	<xsl:attribute-set name="sdep_pid" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
		<xsl:attribute name="rdf:resource">info:fedora/fedora-system:ServiceDeployment-3.0</xsl:attribute>
	</xsl:attribute-set>
	
</xsl:stylesheet>
