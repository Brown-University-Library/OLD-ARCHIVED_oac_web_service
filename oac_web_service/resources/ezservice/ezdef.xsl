<?xml version="1.0" encoding="utf-8"?>
<!--
  Fedora EZDef XSLT1.1 Stylesheet, version 1.0
  
  Input:  EZDef XML document

  Output: FOXML Service Definition for use with Fedora 3.2+

  Modified to output METS as well as FOXML
  Swithun Crowe, cs2@st-andrews.ac.uk
-->

<xsl:stylesheet 
		version="1.1"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		>

	<!-- Bring in common templates -->
	<xsl:import href="ezcommon.xsl"/>

	<xsl:output method="xml" indent="yes"/>
	
	<!-- FOXML Document -->
	<xsl:template match="sdef" mode="foxml">
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
			
			<!-- SDef METHODMAP Datastream -->
			<foxml:datastream xsl:use-attribute-sets="foxml_method_map_datastream">
				<foxml:datastreamVersion xsl:use-attribute-sets="foxml_sdef_method_map_datastream_version">

					<foxml:xmlContent>
						<xsl:apply-templates select="." mode="method_map"/>
					</foxml:xmlContent>
					
				</foxml:datastreamVersion>
			</foxml:datastream>
		</foxml:digitalObject>
		
	</xsl:template>
	
	<!-- METS Document -->
	<xsl:template match="sdef" mode="mets">
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
					<mets:mdWrap xsl:use-attribute-sets="mets_sdef_method_map_mdwrap">
						
						<mets:xmlData>
							<xsl:apply-templates select="." mode="method_map"/>
						</mets:xmlData>
						
					</mets:mdWrap>
				</mets:techMD>
			</mets:amdSec>
			
		</mets:mets>
	</xsl:template>
	
	<!-- Methods -->
	<xsl:template match="method">
		<fmm:method operationName="{@name}" xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap">
			<xsl:apply-templates/>
		</fmm:method>
	</xsl:template>
	
	<!-- RDF output -->
	<xsl:template match="sdef" mode="rdf">
		<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:fedora-model="info:fedora/fedora-system:def/model#">
			<rdf:Description rdf:about="info:fedora/{@pid}">
				<fedora-model:hasModel xsl:use-attribute-sets="sdef_pid"/>
			</rdf:Description>
		</rdf:RDF>
	</xsl:template>
	
	<!-- method map output -->
	<xsl:template match="sdef" mode="method_map">
		<fmm:MethodMap name="N/A" xmlns:fmm="http://fedora.comm.nsdlib.org/service/methodmap">
			
			<!-- Methods -->
			<xsl:apply-templates/>
			
		</fmm:MethodMap>
	</xsl:template>
	
</xsl:stylesheet>
