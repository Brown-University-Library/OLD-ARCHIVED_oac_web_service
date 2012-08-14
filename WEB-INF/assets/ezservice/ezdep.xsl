<?xml version="1.0" encoding="utf-8"?>
<!--
  Fedora EZDep XSLT1.1 Stylesheet, version 1.0
  
  Input:  EZDep XML document
  Param:  sdef - Filename of the corresponding EZDef document
  Output: FOXML Service Deployment for use with Fedora 3.2+
  Modified to output METS as well as FOXML
  Swithun Crowe cs2@st-andrews.ac.uk
-->

<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	
	<!-- Bring in common templates -->
	<xsl:import href="ezcommon.xsl"/>

	<xsl:output method="xml" indent="yes"/>
	
	<xsl:param name="ezdef"/>
	<!-- Get the corresponding EZDef document -->
	<xsl:variable name="sdef" select="document($ezdef)/sdef"/>
	
	<xsl:template match="sdep" mode="foxml">
		<foxml:digitalObject VERSION="{$foxml_version}" PID="{@pid}" xmlns:foxml="info:fedora/fedora-system:def/foxml#">
			
			<!-- Object Properties -->
			<foxml:objectProperties>
				<foxml:property xsl:use-attribute-sets="foxml_object_property_model_state"/>
				<foxml:property xsl:use-attribute-sets="foxml_object_property_model_label" VALUE="{@label}"/>
			</foxml:objectProperties>

			<!-- RELS-EXT Datastream -->
			<foxml:datastream xsl:use-attribute-sets="foxml_rdf_datastream">
				<foxml:datastreamVersion xsl:use-attribute-sets="foxml_rdf_datastream_version">
					
					<foxml:xmlContent>
						<xsl:apply-templates select="." mode="rdf"/>
					</foxml:xmlContent>
					
				</foxml:datastreamVersion>
			</foxml:datastream>
			
			<!-- METHODMAP Datastream -->
			<foxml:datastream xsl:use-attribute-sets="foxml_method_map_datastream">
				<foxml:datastreamVersion xsl:use-attribute-sets="foxml_sdep_method_map_datastream_version">
					
					<foxml:xmlContent>
						<xsl:apply-templates select="." mode="method_map"/>
					</foxml:xmlContent>
					
				</foxml:datastreamVersion>
			</foxml:datastream>
			
			<!-- DSINPUTSPEC Datastream -->
			<foxml:datastream xsl:use-attribute-sets="foxml_ds_input_spec_datastream">
				<foxml:datastreamVersion xsl:use-attribute-sets="foxml_ds_input_spec_datastream_version">

					<foxml:xmlContent>
						<xsl:apply-templates select="." mode="ds_input_spec"/>
					</foxml:xmlContent>
					
				</foxml:datastreamVersion>
			</foxml:datastream>
			
			<!-- WSDL Datastream -->
			<foxml:datastream xsl:use-attribute-sets="foxml_wsdl_datastream">
				<foxml:datastreamVersion xsl:use-attribute-sets="foxml_wsdl_datastream_version">
					
					<foxml:xmlContent>
						<xsl:apply-templates select="." mode="wsdl"/>
					</foxml:xmlContent>
					
				</foxml:datastreamVersion>
			</foxml:datastream>
		</foxml:digitalObject>
		
	</xsl:template>

	<!-- METS Document -->
	<xsl:template match="sdep" mode="mets">
		<mets:mets OBJID="{@pid}" LABEL="{@label}" EXT_VERSION="{$foxml_version}" xmlns:mets="http://www.loc.gov/METS/">

			<mets:metsHdr xsl:use-attribute-sets="mets_hdr"/>
			
			<!-- RELS-EXT Datastream -->
			<mets:amdSec xsl:use-attribute-sets="mets_rels_ext_amdsec">
				<mets:techMD xsl:use-attribute-sets="rels_ext_version_id">
					<mets:mdWrap xsl:use-attribute-sets="mets_rdf_mdwrap">
						
						<mets:xmlData>
							<xsl:apply-templates select="." mode="rdf"/>
						</mets:xmlData>
						
					</mets:mdWrap>
				</mets:techMD>
			</mets:amdSec>
			
			<!-- METHODMAP Datastream -->
			<mets:amdSec xsl:use-attribute-sets="mets_method_map_amdsec">
				<mets:techMD xsl:use-attribute-sets="method_map_version_id">
					<mets:mdWrap xsl:use-attribute-sets="mets_sdep_method_map_mdwrap">
						
						<mets:xmlData>
							<xsl:apply-templates select="." mode="method_map"/>
						</mets:xmlData>
						
					</mets:mdWrap>
				</mets:techMD>
			</mets:amdSec>

			<!-- DS INPUT SPEC Datastream -->
			<mets:amdSec xsl:use-attribute-sets="mets_ds_input_spec_amdsec">
				<mets:techMD xsl:use-attribute-sets="ds_input_spec_version_id">
					<mets:mdWrap xsl:use-attribute-sets="mets_sdep_method_map_mdwrap">
						
						<mets:xmlData>
							<xsl:apply-templates select="." mode="ds_input_spec"/>
						</mets:xmlData>
						
					</mets:mdWrap>
				</mets:techMD>
			</mets:amdSec>

			<!-- WSDL Datastream -->
			<mets:amdSec xsl:use-attribute-sets="mets_wsdl_amdsec">
				<mets:techMD xsl:use-attribute-sets="wsdl_version_id">
					<mets:mdWrap xsl:use-attribute-sets="mets_wsdl_mdwrap">
						
						<mets:xmlData>
							<xsl:apply-templates select="." mode="wsdl"/>
						</mets:xmlData>
						
					</mets:mdWrap>
				</mets:techMD>
			</mets:amdSec>
			
		</mets:mets>
	</xsl:template>

	<!-- RDF Datastream -->
	<xsl:template match="sdep" mode="rdf">
		<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:fedora-model="info:fedora/fedora-system:def/model#">
			<rdf:Description rdf:about="info:fedora/{@pid}">
				
				<fedora-model:hasModel xsl:use-attribute-sets="sdep_pid"/>
				<fedora-model:isDeploymentOf rdf:resource="info:fedora/{$sdef/@pid}"/>
				
				<xsl:apply-templates select="cmodel"/>
				
			</rdf:Description>
		</rdf:RDF>
	</xsl:template>

	<!-- METHODMAP Datastream -->
	<xsl:template match="sdep" mode="method_map">
		<fmm:MethodMap xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap" name="N/A">
			
			<!-- Impl -->
			<xsl:apply-templates select="impl"/>
			
		</fmm:MethodMap>
	</xsl:template>
	
	<!-- DS INPUT SPEC Datastream -->
	<xsl:template match="sdep" mode="ds_input_spec">
		<fbs:DSInputSpec xmlns:fbs="http://fedora.comm.nsdlib.org/service/bindspec" label="N/A">
			
			<!-- For each unique datastream id... -->
			<xsl:apply-templates select="//datastream-input[not(@datastream=preceding::datastream-input/@datastream)]" mode="unique"/>
			
		</fbs:DSInputSpec>
	</xsl:template>
	
	<!-- WSDL Datastream -->
	<xsl:template match="sdep" mode="wsdl">
		<wsdl:definitions name="N/A"
											targetNamespace="urn:thisNamespace"
											xmlns:http="http://schemas.xmlsoap.org/wsdl/http/"
											xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/"
											xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap"
											xmlns:soapenc="http://schemas.xmlsoap.org/wsdl/soap/encoding"
											xmlns:this="urn:thisNamespace"
											xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"
											xmlns:xsd="http://www.w3.org/2001/XMLSchema">
			<wsdl:types>
				<xsd:schema targetNamespace="urn:thisNamespace">
					<xsd:simpleType name="inputType">
						<xsd:restriction base="xsd:string"/>
					</xsd:simpleType>
				</xsd:schema>
			</wsdl:types>
			
			<!-- WSDL Impl -->
			<xsl:apply-templates select="impl" mode="wsdl"/>
			
			<wsdl:portType name="portType">
				<!-- Port Type Impl -->
				<xsl:apply-templates select="impl" mode="portType"/>
			</wsdl:portType>
			
			<wsdl:service name="N/A">
				<wsdl:port binding="this:binding" name="port">
					<http:address location="LOCAL"/>
				</wsdl:port>
			</wsdl:service>
			
			<wsdl:binding name="binding" type="this:portType">
				<http:binding verb="GET"/>
				<!-- Binding Impl -->
				<xsl:apply-templates select="impl" mode="binding"/>
			</wsdl:binding>
			
		</wsdl:definitions>
	</xsl:template>
	
	<!-- CModel -->
	<xsl:template match="cmodel">
		<fedora-model:isContractorOf 
				xmlns:fedora-model="info:fedora/fedora-system:def/model#" 
				xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
				rdf:resource="info:fedora/{.}"/>
	</xsl:template>
	
	<!-- Impl -->
	<xsl:template match="impl">
		<fmm:method operationName="{@method}" wsdlMsgName="{@method}Request" wsdlMsgOutput="response" xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap">

			<!-- User Input - in included stylesheet -->
			<xsl:apply-templates select="$sdef/method[@name=current()/@method]/user-input"/>
			
			<!-- Default Input -->
			<xsl:apply-templates select="/sdep/impl[@method=current()/@method]/default-input"/>
			
			<!-- Datastream Input -->
			<xsl:apply-templates select="/sdep/impl[@method=current()/@method]/datastream-input"/>
			
			<fmm:MethodReturnType wsdlMsgName="response" wsdlMsgTOMIME="N/A"/>
			
		</fmm:method>
	</xsl:template>
	
	<!-- Default Input -->
	<xsl:template match="default-input">
		<fmm:DefaultInputParm 
				parmName="{@name}" 
				defaultValue="{@value}" 
				passBy="VALUE" 
				required="TRUE" 
				xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap"/>
	</xsl:template>
	
	<!-- Datastream Input -->
	<xsl:template match="datastream-input">
		<fmm:DatastreamInputParm 
				parmName="{@datastream}"
				passBy="URL_REF"
				required="TRUE"
				xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap"/>
	</xsl:template>
	
	<!-- Unique Datastream Input -->
	<xsl:template match="datastream-input" mode="unique">
		<fbs:DSInput 
				wsdlMsgPartName="{@datastream}"
				DSMin="1"
				DSMax="1"
				DSOrdinality="false"
				xmlns:fbs="http://fedora.comm.nsdlib.org/service/bindspec">
			
			<!-- optional pid attribute -->
			<xsl:apply-templates select="@object"/>

			<fbs:DSInputLabel>N/A</fbs:DSInputLabel>
			<fbs:DSMIME>N/A</fbs:DSMIME>
			<fbs:DSInputInstruction>N/A</fbs:DSInputInstruction>
			
		</fbs:DSInput>
	</xsl:template>
	
	<!-- optional @object -->
	<xsl:template match="@object">
		<xsl:attribute name="pid">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	
	<!-- WSDL Impl -->
	<xsl:template match="impl" mode="wsdl">
		<wsdl:message name="{@method}Request" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
			<!-- User Input Part -->
			<xsl:apply-templates select="$sdef/method[@name=current()/@method]/user-input" mode="part"/>
			<!-- Default Input Part -->
			<xsl:apply-templates select="default-input" mode="part"/>
			<!-- Datastream Input Part -->
			<xsl:apply-templates  select="datastream-input" mode="part"/>
		</wsdl:message>
		
		<wsdl:message name="response" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
			<wsdl:part name="response" type="xsd:base64Binary"/>
		</wsdl:message>
	</xsl:template>
	
	<!-- User Input Part -->
	<xsl:template match="user-input" mode="part">
		<wsdl:part name="{@name}" type="this:inputType" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>
	</xsl:template>

	<!-- Default Input Part -->
	<xsl:template match="default-input" mode="part">
		<wsdl:part name="{@name}" type="this:inputType" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>
	</xsl:template>

	<!-- Datastream Input Part -->
	<xsl:template match="datastream-input" mode="part">
		<wsdl:part name="{@datastream}" type="this:inputType" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"/>
	</xsl:template>
	
	<!-- Port Type Impl -->
	<xsl:template match="impl" mode="portType">
		<wsdl:operation name="{@method}" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/">
			<wsdl:input message="this:{@method}Request"/>
			<wsdl:output message="this:response"/>
		</wsdl:operation>
	</xsl:template>
	
	<!-- Binding Impl -->
	<xsl:template match="impl" mode="binding">
		<wsdl:operation 
				name="{@method}" 
				xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" 
				xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/"
				xmlns:http="http://schemas.xmlsoap.org/wsdl/http/">
			<http:operation location="{translate(normalize-space(url-pattern), ' ', '')}"/>
			<wsdl:input>
				<http:urlReplacement/>
			</wsdl:input>
			<wsdl:output>
				<mime:content type="N/A"/>
			</wsdl:output>
		</wsdl:operation>
	</xsl:template>
	
</xsl:stylesheet>
